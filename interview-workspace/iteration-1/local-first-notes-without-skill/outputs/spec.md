# Specification: Local-First Note-Taking App

> Version: 0.1 (v1 scope)
> Date: 2026-03-23

---

## 1. Product Overview

A desktop note-taking application that stores notes as plain markdown files on disk and syncs them between devices over the local network using CRDTs. No central server, no cloud dependency. The user owns their data completely.

**Target user (v1):** Developers and technical users comfortable with markdown who want Obsidian-like functionality without cloud sync dependencies.

**Target user (v2):** Anyone who wants a private, portable note-taking tool -- including non-technical users.

---

## 2. Architecture

### 2.1 High-Level Components

```
+------------------------------------------+
|            Tauri v2 Shell                 |
|  +------------------------------------+  |
|  |     SvelteKit Frontend (WebView)   |  |
|  |  - Editor (CodeMirror 6 / Milkdown)|  |
|  |  - Quick switcher, search UI       |  |
|  |  - Note list, folder tree          |  |
|  +------------------------------------+  |
|  +------------------------------------+  |
|  |     Rust Backend (Tauri Core)      |  |
|  |  - File system watcher + read/write|  |
|  |  - CRDT document state             |  |
|  |  - LAN peer discovery (mDNS)      |  |
|  |  - Sync protocol                   |  |
|  |  - Full-text search index          |  |
|  +------------------------------------+  |
+------------------------------------------+
```

### 2.2 Storage Layer

- **Primary storage:** Plain `.md` files in a user-chosen directory (the "vault").
- **Vault structure:**
  ```
  vault/
    .notera/              # App metadata (hidden)
      crdt-state/         # Per-file CRDT documents
      search-index/       # Full-text search index (tantivy)
      config.toml         # Vault configuration
      trash/              # Soft-deleted notes (30-day retention)
    attachments/          # Images and media
    daily/                # Daily notes (YYYY-MM-DD.md)
    projects/             # User folders
    areas/
    resources/
    archive/
  ```
- **File format:** Standard markdown with YAML frontmatter.
  ```markdown
  ---
  tags: [project-x, meeting]
  created: 2026-03-23T10:30:00Z
  modified: 2026-03-23T14:15:00Z
  ---

  # Meeting Notes

  Content here. Link to [[another-note]].
  ```
- **Frontmatter fields (reserved):** `tags`, `created`, `modified`, `aliases`.
- **Custom frontmatter fields** are preserved but not indexed in v1.

### 2.3 CRDT Layer

- **Library:** Yjs (via `y-crdt` Rust bindings) or Automerge. Final choice after prototyping both with the markdown round-trip test described in section 6.
- **Granularity:** Character-level CRDTs for text content. File-level versioning for metadata and frontmatter.
- **CRDT state storage:** Binary CRDT documents stored in `.notera/crdt-state/`, one per note. These are internal -- users never interact with them directly.
- **Markdown-CRDT reconciliation:**
  - The app watches the vault directory for external file changes (using `notify` crate).
  - When the app modifies a note, it updates both the CRDT document and the markdown file atomically.
  - When an external editor modifies the markdown file, the app diffs the old and new content and applies the diff as a CRDT operation.
  - CRDT state is the authority for sync. Markdown files are the authority for the user. The app keeps them in sync bidirectionally.

### 2.4 Sync Protocol (v1: LAN Only)

- **Peer discovery:** mDNS/DNS-SD on the local network. Each running instance advertises itself as `_notera._tcp.local.`
- **Connection:** Direct TCP connection between peers over LAN.
- **Sync flow:**
  1. Peer A discovers Peer B via mDNS.
  2. Devices exchange a list of document IDs with their CRDT state vectors (lightweight -- just version counters, not full content).
  3. For each document that differs, the peer with newer state sends the CRDT update delta.
  4. The receiving peer merges the delta into its local CRDT state and writes the resolved markdown to disk.
- **New files:** When a file exists on one peer but not the other, the full CRDT document is transferred.
- **Deleted files:** Soft-delete markers sync between peers. If Peer A trashes a note, Peer B moves it to trash as well. Hard delete after 30 days on each device independently.
- **Attachments:** Synced as opaque binary blobs (no CRDT needed). Content-addressed by SHA-256 hash to avoid re-transferring identical files.
- **Pairing (v1):** Simplified for LAN. Devices on the same network with the same vault name auto-discover. User confirms the pairing with a 6-digit code displayed on both devices.
- **No authentication beyond pairing in v1.** E2E encryption deferred to v2 when internet sync is added.

---

## 3. Features (v1)

### 3.1 Editor

- **Hybrid markdown rendering** in a single pane. Headings, bold, italic, code blocks, lists, and links render inline while typing. Raw markdown syntax accessible by placing the cursor on the formatted element.
- **Wikilinks:** `[[note-name]]` syntax. Auto-complete suggestions from the note index as the user types. Clicking a wikilink opens the target note. Broken links visually distinguished.
- **Images:** Pasting an image from clipboard saves it to `attachments/` with a UUID filename and inserts `![](attachments/uuid.png)`. Drag-and-drop supported.
- **Code blocks:** Syntax-highlighted using the editor's built-in language grammars.
- **Keyboard-driven:** All core actions accessible via keyboard shortcuts.

### 3.2 Navigation

- **Quick switcher (Cmd+P):** Fuzzy search across all note titles and aliases. Recently opened notes weighted higher.
- **Folder tree sidebar:** Reflects the vault's directory structure. Drag-and-drop to move notes between folders.
- **Full-text search (Cmd+Shift+F):** Powered by a Tantivy index (Rust full-text search library). Results ranked by relevance with matched terms highlighted. Index updates on file change.

### 3.3 Daily Notes

- **Hotkey (Cmd+D):** Creates or opens today's note at `daily/YYYY-MM-DD.md`.
- **Auto-creation:** Optionally creates today's note on app launch.
- **Template:** Configurable daily note template (plain text with date variables).

### 3.4 Note Management

- **Create:** Cmd+N for new note. Prompted for title, placed in current folder or a default.
- **Rename:** Renames the file on disk. Updates all wikilinks across the vault that reference the old name.
- **Delete:** Moves to `.notera/trash/` with a metadata file recording deletion date. Notes auto-purged after 30 days.
- **Tags:** Parsed from frontmatter `tags` field. Tag browser/filter in the sidebar.

### 3.5 Sync

- LAN peer discovery and sync as described in section 2.4.
- **Sync status indicator** in the UI: connected peers count, last sync timestamp, any unresolved conflicts.
- **Conflict UI:** When auto-merge produces an ambiguous result (heuristic: both peers edited the same line within the same paragraph), surface a diff view. User picks the final version. This should be rare.

---

## 4. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| App launch to usable editor | < 1 second |
| Note open time (average note) | < 100ms |
| Full-text search latency (10k notes) | < 200ms |
| Sync latency (LAN, single note change) | < 2 seconds end-to-end |
| Initial full sync (2,000 notes, ~50MB) | < 60 seconds on LAN |
| Memory usage (2,000 notes open vault) | < 200MB |
| Disk overhead (.notera metadata) | < 2x the raw markdown size |

---

## 5. Tech Stack

| Layer | Technology |
|-------|-----------|
| App shell | Tauri v2 |
| Frontend | SvelteKit + Tailwind CSS v4 |
| Editor | CodeMirror 6 with markdown extensions (primary candidate) or Milkdown |
| Backend | Rust |
| CRDT | y-crdt (Yjs Rust port) or automerge-rs (prototype both) |
| Search | Tantivy |
| Peer discovery | mdns-sd crate (mDNS/DNS-SD) |
| File watching | notify crate |
| Networking | tokio + custom TCP protocol (v1); libp2p (v2) |

---

## 6. Open Questions and Risks

### 6.1 CRDT-to-Markdown Round-Trip (High Risk)

The dual-source-of-truth problem: CRDT state for sync correctness, markdown files for user access. If a user edits a file in VS Code while the app is running, the app must detect the change, diff it against its CRDT state, and apply the diff as CRDT operations without losing concurrent changes from other peers.

**Mitigation:** Build a prototype of just this reconciliation loop before committing to the full app. Test with adversarial scenarios: simultaneous edits from the app and an external editor, large structural changes (reordering sections), frontmatter modifications.

### 6.2 CRDT Metadata Overhead at Scale

CRDT documents carry tombstones and version vectors that grow over time. At 10,000 notes with active editing history, the `.notera/crdt-state/` directory could become large.

**Mitigation:** Implement CRDT compaction/garbage collection. Periodically snapshot the CRDT state and discard old history. Measure actual overhead during development with realistic editing patterns.

### 6.3 Editor Library Selection

CodeMirror 6 and Milkdown offer different tradeoffs. CodeMirror 6 is more mature and extensible but its markdown WYSIWYG mode requires custom extensions. Milkdown is purpose-built for markdown WYSIWYG but has a smaller community.

**Mitigation:** Build a minimal editor prototype with each. Evaluate: wikilink support difficulty, performance with large documents (5,000+ words), quality of the hybrid rendering, extensibility for future features.

### 6.4 Tauri v2 Mobile Maturity

Tauri v2's iOS support is functional but not as battle-tested as desktop. Mobile is v2 scope, but architecture decisions now could make mobile harder later.

**Mitigation:** Keep the frontend/backend contract clean. Don't rely on desktop-only Tauri APIs. Test the Tauri iOS build early even if mobile features come later.

---

## 7. v2 Roadmap (Out of Scope for v1)

Ordered roughly by priority:

1. **Internet sync with NAT traversal** -- libp2p with relay servers, E2E encryption, device pairing via QR code
2. **iOS mobile app** -- Tauri v2 iOS build, read/quick-capture focused UI
3. **Backlinks panel** -- sidebar showing all notes that link to the current note
4. **Templates** -- user-defined note templates with variable substitution
5. **Version history** -- browse and restore previous versions from CRDT history
6. **Graph view** -- visual map of note connections
7. **Plugin system** -- user-extensible with a defined API
8. **Android app**
9. **Linux desktop**
10. **Real-time collaborative editing** -- multiple users editing the same note simultaneously

---

## 8. Project Metadata

- **License:** MIT or Apache 2.0 (decide before first public commit)
- **Repository:** Public from day one
- **Name:** TBD (working name: "Notera")
