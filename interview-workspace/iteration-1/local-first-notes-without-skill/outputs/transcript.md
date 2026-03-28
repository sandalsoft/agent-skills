# Interview Transcript: Local-First Note-Taking App

## Opening

The user wants to build a local-first note-taking app that syncs across devices without a central server.

---

## Round 1: Core Problem and Motivation

**QUESTION:** What's driving this? Is there a specific pain point with existing note apps, or is this more of a technical interest in the local-first architecture?

**ANSWER:** Both, honestly. I use Obsidian right now and I like the markdown-based approach, but their sync is a paid service and I don't love that my notes go through their servers. I've looked at Logseq too. I want something where I truly own my data and the sync just happens peer-to-peer. But I also think the CRDTs and local-first space is getting mature enough that building something real is feasible now.

**QUESTION:** Who's this for beyond yourself? Are you building a personal tool, something for a small group of technical users, or do you want non-technical people to use it eventually?

**ANSWER:** Initially just me and maybe a few friends who are developers. But I'd like the UX to be good enough that my partner could use it too -- she's not technical. So the sync setup can't require port forwarding or running a server or anything like that.

---

## Round 2: Data Model and Note Structure

**QUESTION:** What does a "note" look like in your head? Plain markdown files on disk like Obsidian? Or something more structured with metadata, tags, rich embeds?

**ANSWER:** Markdown files on disk is the baseline. I want to be able to open the folder in any text editor and have it make sense. But the app itself should support frontmatter for metadata -- tags, created/modified dates, maybe custom fields. Wikilinks between notes are important. I use daily notes a lot. I don't need heavy rich embeds like Notion blocks, but inline images and code blocks should render well.

**QUESTION:** How do you organize notes today? Folders? Tags? A flat list with links?

**ANSWER:** Mix of folders and tags. I have maybe 5 top-level folders (projects, areas, resources, archive, daily) loosely based on PARA. Inside those, I rely on tags and links more than sub-folders. I'd want the app to support both approaches without forcing one.

**QUESTION:** Roughly how many notes are we talking about? Hundreds, thousands, tens of thousands?

**ANSWER:** Around 2,000 right now. I'd expect it to grow to maybe 10,000 over a few years. Individual notes range from a few lines to maybe 5,000 words for long-form writing.

---

## Round 3: Sync Architecture

**QUESTION:** When you say "no central server," what's your tolerance for infrastructure? Are you okay with a relay server that helps devices find each other but never sees the content? Or do you want zero server involvement?

**ANSWER:** A relay for discovery is fine, as long as the content is end-to-end encrypted and the relay can't read anything. I looked at how Syncthing does it -- they have relay servers but the data is encrypted. Something like that would be acceptable. I just don't want a situation where a company can read my notes or where the service disappearing means I lose sync.

**QUESTION:** Which devices do you need to sync between? Laptop to laptop? Phone? Tablet?

**ANSWER:** Desktop (macOS primarily, but Linux would be nice) and mobile (iOS is the priority, Android is a nice-to-have). The desktop app is the primary editing experience. Mobile is mostly for quick capture and reading.

**QUESTION:** How fast does sync need to be? Real-time collaborative editing, or is "syncs within a few seconds when both devices are online" good enough?

**ANSWER:** A few seconds is fine. I'm not trying to build Google Docs. If I edit on my laptop and pick up my phone 30 seconds later, the changes should be there. Real-time collaboration between two people editing the same note simultaneously would be cool eventually but is not a launch requirement.

---

## Round 4: Conflict Resolution

**QUESTION:** Conflict handling is the hard part of this whole thing. What should happen when you edit the same note on two devices while offline, then they reconnect?

**ANSWER:** I've read a bit about CRDTs and I think that's the right approach -- automatic merging at the character level rather than file-level "pick one" conflicts. For the cases where automatic merge produces something weird, I'd want to see a diff view and manually resolve it. But the goal is that 95% of conflicts just merge cleanly without me knowing.

**QUESTION:** Have you looked at specific CRDT implementations? Yjs, Automerge, Diamond Types?

**ANSWER:** I've played with Automerge a bit and liked the API. Yjs seems more battle-tested in production. I'm open to either. The main thing is that the CRDT layer should be underneath the plain-text markdown files -- I don't want a binary blob as the source of truth. The markdown files on disk should always be human-readable.

---

## Round 5: Technical Stack

**QUESTION:** What's your thinking on the tech stack? Native apps per platform, or a cross-platform approach like Electron/Tauri?

**ANSWER:** Tauri. I don't want to ship Chromium. Tauri v2 supports mobile now, so in theory one codebase covers desktop and mobile. The frontend would be a web app -- I'm thinking SvelteKit since that's what I know. The sync layer and file system operations would be in Rust on the backend.

**QUESTION:** For the networking layer -- peer-to-peer connections between devices -- have you thought about the protocol? libp2p, custom WebRTC, something else?

**ANSWER:** I was leaning toward libp2p since it handles NAT traversal, peer discovery, and encrypted channels. There's a Rust implementation (rust-libp2p) that would fit with Tauri. But I'm not married to it. The key requirements are: works through NATs without manual configuration, encrypted, and can work on both desktop and mobile.

---

## Round 6: Editor Experience

**QUESTION:** For the editor itself, are you thinking a code-mirror-style plain text editor with markdown preview, or a WYSIWYG/hybrid editor like Typora or Notion?

**ANSWER:** Hybrid, like what Obsidian does. You type markdown but headings render as headings, bold renders as bold, links are clickable. Not a split-pane preview. I'd want to use something like Milkdown or TipTap that gives a rich editing experience but stores plain markdown. CodeMirror 6 with markdown extensions could work too -- it's more of a plain-text feel but very extensible.

**QUESTION:** What features does your daily workflow depend on? Quick switcher? Full-text search? Backlinks panel? Graph view?

**ANSWER:** Quick switcher is critical -- Cmd+P to fuzzy-find any note by title. Full-text search across all notes. A backlinks panel showing what links to the current note. Graph view is nice but low priority -- I rarely use it in Obsidian. Daily note creation with a hotkey. And templates -- I have a few templates for meeting notes, project kickoffs, etc.

---

## Round 7: Security and Privacy

**QUESTION:** You mentioned end-to-end encryption for sync. How do you want key management to work? Password-derived keys? Device-based keys with a pairing flow?

**ANSWER:** Device-based keys with a pairing flow. When I add a new device, I want to scan a QR code or enter a short code on the existing device to pair them. After that, sync just works. I don't want to remember another password. The encryption keys should be derived from a shared secret established during pairing.

**QUESTION:** Any notes that need extra protection? Like a "vault within a vault" for sensitive stuff?

**ANSWER:** Not for v1. Everything is encrypted in transit, and the files on disk are just normal files protected by the OS. If someone has physical access to my unlocked laptop they can read the markdown files, and that's fine for now.

---

## Round 8: Scope and Priorities

**QUESTION:** Let's talk about what's in v1 versus what comes later. If you had to ship something in 8 weeks that you'd actually use daily, what makes the cut?

**ANSWER:** v1 must have:
- Markdown editor with hybrid rendering (type markdown, see formatted output inline)
- File-based storage (plain .md files in a folder)
- Frontmatter support for tags and metadata
- Wikilinks between notes
- Quick switcher (Cmd+P)
- Full-text search
- Daily notes
- Sync between two desktop devices over the local network (LAN)
- Basic conflict resolution with CRDTs

v1 can skip:
- Mobile app (v2)
- Internet sync / NAT traversal (v2 -- LAN-only sync is fine for v1)
- Graph view
- Templates
- Plugins/extensions
- Backlinks panel (nice to have but not blocking)
- End-to-end encryption (v1 is LAN-only so less critical, but v2 needs it)

**QUESTION:** That's a reasonable cut. One more thing: are you thinking of this as open source?

**ANSWER:** Yes, open source from the start. MIT or Apache 2.0 license. I want other people to be able to build on it and I think that's the right move for a local-first tool -- if the project dies, anyone can fork it.

---

## Round 9: Edge Cases and Concerns

**QUESTION:** What happens if you accidentally delete a note? Is there a trash/recycle bin, or do you rely on git history or filesystem snapshots?

**ANSWER:** A soft-delete trash folder that keeps deleted notes for 30 days. Also, the CRDT history could serve as a lightweight version history -- I'd like to be able to see previous versions of a note and restore them. Full git integration would be cool but is a v2 feature.

**QUESTION:** How should the app handle large files? Images, PDFs, attachments?

**ANSWER:** Images referenced in notes should be stored in an `attachments` subfolder. The app should handle copying/pasting images into a note -- save the image file, insert a markdown image link. PDFs and other attachments are out of scope for v1. For sync, images need to sync too, but since they're immutable (you don't edit an image), they can just be copied without CRDT overhead.

**QUESTION:** Any concerns about the approach you've been mulling over? Things that keep you up at night about this project?

**ANSWER:** Two things. First, I'm worried about the CRDT-to-markdown round-trip. If the CRDT is the source of truth for sync, but markdown files on disk are the source of truth for the user, keeping those two representations in sync without data loss seems hard. What happens if the user edits the markdown file directly in VS Code while the app is running? Second, I'm worried about sync performance at scale. CRDTs can have large metadata overhead. With 10,000 notes, will the initial sync between a new device and an existing one take forever?

---

## Summary of Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Storage format | Plain markdown files on disk | User ownership, editor-agnostic |
| Sync approach | CRDT-based, peer-to-peer | No central server dependency |
| v1 sync scope | LAN only | Simpler, avoids NAT traversal complexity |
| CRDT library | Yjs or Automerge (TBD) | Mature, good merge semantics |
| App framework | Tauri v2 + SvelteKit frontend | No Chromium, cross-platform potential |
| Backend language | Rust (via Tauri) | Performance, file system access, libp2p ecosystem |
| Editor | CodeMirror 6 or Milkdown (TBD) | Hybrid markdown rendering |
| Conflict strategy | Auto-merge with manual diff fallback | Minimize user friction |
| License | MIT or Apache 2.0 | Open source from day one |
| Target platforms (v1) | macOS desktop | Developer's primary platform |

---

# Final Specification

See [spec.md](spec.md) for the complete specification document.
