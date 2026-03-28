# Interview Transcript: Local-First Note-Taking App

**Input:** "I'm thinking about building a local-first note-taking app that syncs across devices without a central server"

---

## Phase 1: Intake

### Hypothesis

The stated goal is a local-first notes app with peer-to-peer sync. But the real goal is likely about *ownership and control* — the user is frustrated with note-taking apps that hold data hostage in proprietary clouds, go offline, change pricing, or compromise privacy. The sync-without-a-central-server constraint is the most technically demanding part and will dominate the architecture. There's a tension between "no central server" and "reliable cross-device sync" that needs to be surfaced.

### Gaps Identified

1. What "sync" actually means here — real-time collaboration? Eventually consistent personal sync? Multi-user?
2. The conflict resolution strategy when edits happen on two offline devices
3. Whether "no central server" means truly peer-to-peer or just "no server I don't control" (self-hosted relay is different from pure P2P)
4. What kind of notes — plain text? Rich text? Embedded media? Code blocks?
5. Target platforms — mobile, desktop, web, all of the above?

### Domain Assessment

Greenfield project. Solo developer (assumed). This sits at the intersection of local-first software (CRDTs, Automerge/Yjs), networking (P2P, NAT traversal), and note-taking UX. Technically ambitious.

### Acknowledgment

A local-first notes app with serverless sync. That's a project where the sync layer will make or break the whole thing — the note-taking part is well-understood, but reliable P2P sync across devices without a relay has some real engineering challenges hiding in it. Let me dig into what you're actually after and where the hard edges are.

---

## Phase 2: Investigation

No existing codebase. Greenfield. Skipping this phase.

---

## Phase 3: Interview Loop

### Round 1

**Observation:** The phrase "without a central server" could mean several different things, and each one leads to a very different architecture. Need to pin this down before anything else.

**QUESTION:** When you say "without a central server," which of these best matches what you mean?

1. **Truly peer-to-peer** — devices discover and sync with each other directly, no infrastructure at all
2. **Self-hostable relay** — there's a sync server, but the user runs it themselves (like Syncthing)
3. **Optional relay with E2E encryption** — a relay exists for convenience but can't read the data, and the app works fine without it
4. **No opinion yet** — you just don't want vendor lock-in, and the architecture is open

**ANSWER:** Option 3 is closest. I want it to work fully offline and sync device-to-device when possible, but I'm realistic that NAT traversal is a nightmare. An optional relay that can't read my data sounds right. The core principle is: my notes are mine, always available on my device, and no company can hold them hostage.

**QUESTION:** What's your current workaround? What are you using for notes today, and what specifically is breaking or frustrating you about it?

**ANSWER:** I bounce between Obsidian and Apple Notes. Obsidian is great for Markdown and local files, but sync is either iCloud (unreliable with .md files, merge conflicts) or their paid Obsidian Sync. Apple Notes syncs perfectly but it's locked to Apple's ecosystem and the format is opaque. I want the Obsidian model — plain files I own — with the Apple Notes sync reliability, minus the ecosystem lock-in.

---

### Round 2

**Observation:** The user wants plain Markdown files they own, with sync that just works. That's a strong design constraint — the file format is Markdown on disk, which means the sync layer needs to work with files, not a custom database format. This creates tension with CRDTs, which typically operate on in-memory data structures.

**QUESTION:** When you say "plain files I own," does that mean the on-disk format *must* be standard Markdown files in a normal folder? Or would you accept a local database (like SQLite) as long as you can export to Markdown anytime?

**ANSWER:** Strong preference for plain Markdown files in a folder. That's the escape hatch — if the app dies, I still have my notes. But I could accept a hybrid: Markdown files as the source of truth, with a local database or metadata sidecar for sync state and indexing. As long as I can `ls` my notes directory and see .md files.

**QUESTION:** How many devices, and what platforms? Desktop only, or mobile too?

**ANSWER:** Desktop first — macOS and Linux. Mobile (iOS) would be great eventually but I know that's a different beast. I'd start with desktop and add mobile later. Web is not a priority.

---

### Round 3

**Observation:** Markdown files as source of truth plus desktop-first on macOS and Linux. This narrows the stack significantly. The sync problem becomes: how do you detect changes to .md files across devices and merge them without conflicts. Syncthing does file-level sync but doesn't handle merge conflicts in text content. CRDTs like Automerge handle text merging but don't naturally map to "files in a folder."

**Progress note:** We've got a clear picture of what you want (Markdown files you own, reliable cross-device sync, no vendor lock-in) and who it's for (you, a developer, desktop-first). The big open area is the sync architecture — specifically how you handle the gap between "plain files on disk" and "conflict-free merging."

**QUESTION:** Let's talk about the hard part: conflict resolution. Two scenarios to think through:

1. You edit the same note on your laptop and your desktop while offline, then both come online. What should happen?
2. You create a note on one device and rename it on another. What should happen?

For scenario 1, here are three common approaches:
- **Last-write-wins** — simpler, but you lose edits. Syncthing does this.
- **CRDT-based text merging** — both edits survive, merged automatically. Automerge/Yjs do this. Requires the app to mediate all edits (no editing .md files in vim directly).
- **Fork-and-flag** — create a conflict copy (like Dropbox) and let the user resolve manually.

**ANSWER:** CRDT-based merging is what I want for the content. I understand that means edits should go through the app to get the CRDT benefits. But I'd also want a file watcher that detects external edits (someone editing in vim) and treats the whole-file replacement as a CRDT operation — basically "this device says the file is now X." It won't be a perfect merge for external edits, but it should still handle it gracefully, maybe with a fork-and-flag fallback for genuine conflicts that can't be auto-merged.

For renames and moves — I think tracking by a stable note ID rather than file path makes sense. The filename is a human-friendly label, not the identity.

---

### Round 4

**Observation:** The user wants CRDT merging through the app with a file-watcher fallback for external edits. This is a sophisticated hybrid approach. The note identity being an ID (not a path) is a good call but introduces a mapping layer — the app needs to maintain a registry of note-id-to-filepath. That's the "metadata sidecar" the user mentioned earlier.

**QUESTION:** Let's talk about the sync transport. For device-to-device sync with an optional relay, there are a few proven approaches:

1. **Syncthing protocol (BEP)** — battle-tested file sync, but operates at file level, no CRDT awareness. You'd layer CRDTs on top.
2. **libp2p** — general-purpose P2P networking library. Handles NAT traversal, peer discovery. You build the sync protocol.
3. **Hypercore/Hyperswarm** — append-only log with built-in P2P replication. Good fit for CRDT operation logs.
4. **Custom over WebRTC/QUIC** — full control but lots of plumbing.

My instinct says Hypercore or libp2p paired with Automerge would be the most natural fit. What's your take?

**ANSWER:** I've been looking at Automerge and it feels right for the CRDT layer. For transport, I'm drawn to Hyperswarm because the append-only log maps well to syncing CRDT operations. I'd want the relay to be something simple I can self-host — a small binary or Docker container, not a whole infrastructure stack. libp2p feels over-engineered for this use case.

**QUESTION:** What's the tech stack you're thinking for the app itself? Given macOS + Linux desktop, are you leaning toward Electron/Tauri, a native app per platform, or something else?

**ANSWER:** Tauri. Electron is too heavy for something that should feel fast and local. I'd use SvelteKit for the frontend and Rust for the backend/sync layer. Tauri v2 supports both macOS and Linux well.

---

### Round 5

**Observation:** Tauri + SvelteKit + Rust + Automerge + Hyperswarm. That's a strong stack, but Hyperswarm is a JavaScript/Node ecosystem tool, and the user wants the backend in Rust. There might be a friction point here — either use the Rust port of Hyperswarm (less mature) or run a Node sidecar for networking. Worth surfacing.

**QUESTION:** Hyperswarm is primarily a Node.js library. Since you want Rust for the backend, you'd either need:

1. **iroh** — a Rust-native networking library from the team behind IPFS. Handles NAT traversal and peer connections natively in Rust. Less mature than Hyperswarm but growing fast.
2. **A Node sidecar** — run Hyperswarm in a Node process alongside Tauri. Works but adds a runtime dependency and complicates packaging.
3. **Automerge-repo** — Automerge's own sync/networking layer, which has both JS and Rust support and handles the transport abstraction for you.

Have you looked at automerge-repo? It might collapse the CRDT + sync transport question into one solution.

**ANSWER:** I haven't looked deeply at automerge-repo. If it handles both the CRDT operations and the sync transport in Rust, that's really appealing — fewer moving parts. I'd want to verify it supports the relay model (optional server that can't read content). Iroh is interesting too as a fallback. Let's assume automerge-repo as the primary approach, with iroh as a backup if the networking layer doesn't fit.

**QUESTION:** What does the note-taking experience itself look like? A few dimensions:

- **Editor:** Markdown source editing (like Obsidian's edit mode), WYSIWYG/block editor (like Notion), or both?
- **Organization:** Folders? Tags? Links between notes? All of the above?
- **Search:** Full-text search across all notes? Instant, as-you-type?

**ANSWER:** Dual-mode editor — Markdown source and a live preview, with the ability to toggle. Not a block editor; I find those get in the way. Organization: flat folder structure with tags and bidirectional links (like Obsidian). Full-text search is a must, and it should be fast — indexing locally with something like tantivy (Rust full-text search engine). I don't need a graph view on day one, but the link structure should support it later.

---

### Round 6

**Progress note:** We're in solid shape on the technical architecture — Tauri, SvelteKit, Rust, Automerge, with automerge-repo for sync. The editor, organization, and search model are clear. Remaining gaps: security model for the relay, what the MVP actually includes vs what's deferred, and how you'd know this is working.

**QUESTION:** For the optional relay server — what's the trust model? Two options:

1. **E2E encrypted, relay is a dumb pipe.** The relay stores and forwards encrypted blobs. It can't read note content. You manage your own keys.
2. **E2E encrypted with a key exchange protocol.** Same as above but the relay also helps your devices discover each other and exchange keys on first setup (like Signal's model).

And a follow-up: how do you add a new device? What's the onboarding flow when you install the app on a second machine?

**ANSWER:** Option 2. I don't want to manually manage keys. When I install on a new device, I'd want to scan a QR code or enter a short pairing code from an existing device — similar to how Signal or WhatsApp handle device linking. The relay helps with discovery and key exchange, but after that, devices can sync directly when on the same network. The relay is the fallback for when they're not.

**QUESTION:** What data does the relay actually persist? Does it store encrypted sync data for offline devices to pick up later, or is it purely a live connection broker?

**ANSWER:** It needs to buffer. If my laptop is offline for a day and my desktop made edits, when the laptop comes online it should get those edits even if the desktop is now offline. So the relay stores encrypted CRDT operations temporarily — maybe with a TTL of 30 days. After that, full sync requires both devices online at the same time.

---

### Round 7 (Challenge Phase)

**Observation:** The architecture is ambitious for a solo developer: Tauri, Rust backend with Automerge + automerge-repo, SvelteKit frontend, full-text search with tantivy, E2E encryption with key exchange, a relay server, file watching, CRDT-to-Markdown reconciliation. That's a lot of surface area.

**QUESTION:** Let me push on scope. You're building: a Markdown editor, a CRDT sync engine, a P2P networking layer, an E2E encryption system, a relay server, a full-text search index, and a file watcher that reconciles external edits with CRDTs. Each of those is a meaningful project on its own.

If you had to ship something usable in 4 weeks, what would you cut? What's the smallest version of this that you'd actually use daily instead of Obsidian?

**ANSWER:** Fair challenge. The 4-week version: a Tauri app that edits Markdown files in a local folder, with full-text search. No sync at all. That's the foundation I'd build on. The sync layer is the ambitious part and it can come after the editing experience is solid.

Actually, let me reconsider. The whole *point* is the sync. A Markdown editor without sync is just... another Markdown editor. The 4-week version should be: single-user sync between two of my own devices, using automerge-repo with a self-hosted relay. No external edit detection, no pairing UX (I'll configure it manually). Encryption can be a later layer if automerge-repo doesn't include it by default.

**QUESTION:** What happens when a conflict between the CRDT state and the Markdown file on disk can't be reconciled cleanly — say, an external tool rewrites the file in a way that doesn't map back to the CRDT document? What's the failure mode the user sees?

**ANSWER:** The app should treat the on-disk file as authoritative in that case. Replace the CRDT document state with the file contents, effectively treating it as a new "edit" from that device. This means the CRDT history might lose granularity for that edit, but the file is always the source of truth. If there's a genuine conflict (CRDT has changes not yet written to disk AND the file changed externally), create a `.conflict` copy and notify the user in the app. But honestly, for v1, I might skip the file watcher entirely and have the app own the files. External editing is a power-user feature.

---

### Round 8 (Challenge Phase continued)

**QUESTION:** You mentioned Obsidian's sync is paid and iCloud is unreliable. There's an open-source project called Obsidian Livesync that uses CouchDB for sync and works with the existing Obsidian ecosystem. Have you considered building this as an Obsidian plugin rather than a standalone app? You'd inherit the entire editor, plugin ecosystem, and community.

**ANSWER:** I have, and I rejected it. Three reasons: Obsidian is closed-source (the app itself, not the plugin API), so I'm still dependent on a company. The plugin API is limited for this kind of deep sync integration. And I want to own the full stack — this is partly a learning project for Rust and CRDTs. If it turns out well, having full control of the app means I can take it places an Obsidian plugin never could.

---

## Clarity Tracking (Final)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Intent | 95% | Crystal clear: own your data, sync reliably, no vendor lock-in |
| Outcome | 85% | Solid: Markdown editor with CRDT-based cross-device sync |
| Scope | 80% | Good MVP definition; v1 vs later features are mostly clear |
| Constraints | 75% | Stack is chosen; relay trust model defined; some details on encryption TBD |
| Audience | 90% | The user themselves, developer, power user. Mobile deferred. |
| Criteria | 70% | "Use it instead of Obsidian" is the bar; specific test criteria could be sharper |

**Overall: ~83%** — Above the readiness threshold.

---

## Phase 5: Crystallize

The spec follows in the next section.

---

## Observations & Notes

- The user has a clear mental model and has done prior research (knows Automerge, Hyperswarm, tantivy). This isn't a vague idea — it's a pre-researched project that needed its scope sharpened.
- The biggest risk is scope: the full vision is 6+ months of work for a solo developer. The 4-week MVP (editor + automerge-repo sync between personal devices) is the right starting point.
- The "Markdown files as source of truth" principle creates real architectural tension with CRDTs. The decision to defer external file watching to post-v1 is wise.
- The learning motivation (Rust, CRDTs) means this project doesn't need to "beat" Obsidian to be worthwhile. That removes some pressure from the feature set.
- automerge-repo is the lynchpin dependency. If it doesn't support the relay model or Rust integration is immature, the whole sync architecture needs replanning. This should be the first spike.
