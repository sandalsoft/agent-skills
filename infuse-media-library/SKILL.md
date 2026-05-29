---
name: infuse-media-library
description: Organize a movie/media library into Firecore Infuse naming conventions — per-movie `Title (YYYY)/` folders with matching companion assets (NFO, posters, backdrops, logos, trickplay). Handles loose release-named files (e.g. `Blade.Runner.2049.2017.UHD.BluRay.x265-RARBG.mkv`), messy folder names, multi-version movies, "collection" folders that bundle several films, orphan NFO/BIF/poster leftovers, and SMB/NAS ACL gotchas. Use this skill whenever the user wants to clean up, rename, organize, or restructure a movie library — especially when they mention Infuse, Firecore, Plex, Jellyfin, Emby, Kodi, ATV/Apple TV media, release-name patterns (`1080p`, `2160p`, `BluRay`, `WEB-DL`, `x264`, `x265`, `REMUX`), torrent download folders, or want files renamed into `Title (YYYY)` format. Also triggers for media file naming questions, video library structure decisions, .trickplay handling, NFO file management, or "my movies folder is a mess."
---

# Firecore (Infuse) Media Library Organizer

## When to use this skill

You're being asked to take a directory full of movies — typically a mix of loose release-named files, half-organized folders, leftover NFO/poster assets, and multi-movie "collection" folders — and reshape it into the structure Infuse (and most other media players: Plex, Jellyfin, Emby, Kodi) prefer: **one folder per movie, named `Title (YYYY)/`, with all assets inside**.

Even if the user doesn't say "Firecore" or "Infuse" by name, this skill is the right tool whenever the intent is "organize my movies properly." The conventions encoded here also work for Plex/Jellyfin/Emby — they all read the same `Title (YYYY)` folder structure.

## Core workflow: Inventory → Plan → Approve → Execute

The single most important thing this skill does is enforce a **read-first, plan-before-touch** discipline. Media libraries are large, the files are big, and a wrong move can lose data or break a working library. So:

1. **Inventory.** Walk the directory. Group loose files into "movie units" by their shared base name (the .mkv plus its `-backdrop.jpg`, `-landscape.jpg`, `-logo.png`, `-poster.jpg`, `-clearlogo.png`, `-fanart.jpg`, `.nfo`, `.bif`, `.srt`, `-320-10.bif`, and `.trickplay/` companions). Parse a title and year out of each. Identify existing folders. Spot orphan assets, empty placeholder folders, multi-version situations, collection folders, and unparseable items.

2. **Plan.** Sort every item into one of the categories below. Decide what would change. Produce a written plan: what gets moved, what gets renamed, what gets created, what's parked for the user to decide.

3. **Approve.** Show the user the plan — counts per category, the most impactful changes, and a short version of the parked list. **Do not touch the filesystem until they sign off.** Use `AskUserQuestion` (or a clear prompt) to capture decisions about renaming policy, multi-version handling, and any other branch points.

4. **Execute.** Run a dry-run first, verify the operations look right, then go live. Stream progress. Capture errors. After running, present what was done plus an updated parked list.

The categorization framework that makes this tractable:

| Cat | What it is | Default action |
|---|---|---|
| **A** | Loose movie file at top level with its companion files | Move into `Title (YYYY)/`, rename inner files |
| **B** | Existing folder with a messy release-name | Rename folder to `Title (YYYY)` |
| **C** | Same movie has multiple versions at top level (1080p + 2160p, multiple cuts) | Combine into one folder; keep distinct release names to avoid collisions |
| **D** | Multi-movie "collection" folder (Bond, Godfather, etc.) | Park — needs user input on whether to split, dedupe vs. individual folders, or keep |
| **E** | Orphan `.nfo`/`.bif`/poster files with no matching movie | Park — likely leftovers from removed films |
| **F** | Conflicts: two folders that would rename to the same target, multiple rips of same movie, no parseable year | Park — needs user judgment |
| **G** | Empty placeholder folders | Park — fill from elsewhere or delete |
| **H** | Special / unparseable: weird filename, ISO instead of mkv, only extras with no main film | Park — case-by-case |

A → B → C are the safe, mechanical operations. D → H need user input.

**Important**: "Park" is not a soft default. For Category D (collection folders) in particular, do **not** split or delete them without an explicit user "yes" — even when you have a plausible-sounding rationale. A James Bond collection or Godfather Trilogy folder can contain the user's only copy of a film; bulldozing it on autopilot is a data-loss risk. Surface the situation, propose options, then wait. The same goes for orphan files (Cat E) and empty placeholders (Cat G): list them, suggest deletion, but require explicit approval before removing anything irreversible.

## Firecore naming, in one paragraph

Infuse matches a movie if the folder OR file name contains the title and (optionally but strongly preferred) a year. Use **`Title (YYYY)`** with the year in parentheses for unambiguous matching. **Period, space, underscore, and dash are interchangeable** as separators — `28.Days.Later.2002.mkv` works just as well as `28 Days Later (2002).mkv` for matching, though the parenthesized form is cleaner. The recommended structure is one folder per movie holding the video plus `<base>-backdrop.jpg`, `<base>-poster.jpg`, `<base>-logo.png`, `<base>-landscape.jpg`, `<base>.nfo`. Avoid these characters in any path: `" \ / : | < > * ?`. Edition tags use `{edition-Description}` (e.g. `Get Out (2017) {edition-Alternate Ending}.mp4`). TMDB or IMDB IDs can be embedded in curly braces (`{tmdb-27205}`, `{imdb-tt1375666}`). Full rules and edge cases live in `references/firecore-naming.md`.

## Critical gotchas — read these before doing anything

These three patterns burn time when they bite, and they're each easy to miss:

**1. Year-in-title throws naive parsers off.** Titles like `Blade Runner 2049`, `2001: A Space Odyssey`, `1917`, and the year-range collection folders `(2001-2011)` all contain digit sequences that look like release years. A regex that grabs the *first* 4-digit year produces nonsense (`Blade Runner (2049)` for a 2017 movie). The fix: find **all** year-like tokens (1900-2030, surrounded by separators), then prefer the **last** one — release years sit closest to the resolution/codec tags at the end of release names. The parenthesized form `(YYYY)` always wins if present. See `references/parser-patterns.md` for the full regex + examples.

**2. SMB/NAS shares lie about permissions.** A folder can show `drwx------ user:group` and still reject writes because of server-side ACLs sitting on top of POSIX bits. The symptoms: `mv` of a file *into* a folder fails with `Permission denied` even though `ls` looks fine. Before every batch of operations, **probe writability with a real write** (touch + remove a tiny test file in each target folder). Also: on SMB, **directory moves across folder boundaries often fail even when file moves succeed** — `cp -R` works as a fallback, but then you need explicit permission to delete the source. If the user owns the NAS, the fix is usually `chown -R nobody:users + chmod -R 777 + setfacl -R -b` on the server, then remount on the client. See `references/smb-acl-troubleshooting.md` — including the Unraid-specific recipe.

**3. Multi-version movies collide if you rename naively.** If the user has both `Ballerina.2025.1080p.*.mkv` and `Ballerina.2025.2160p.*.mkv`, both parse to title `Ballerina (2025)`. Renaming both to `Ballerina (2025).mkv` inside the same folder clobbers one. Two valid strategies: (a) keep their original release names to disambiguate, or (b) use Infuse's `{edition-...}` syntax. Detect multi-version groups *before* deciding on inner renames.

## Scripts

The skill ships with three Python scripts that capture the inventory → plan → execute loop. Use them; don't rewrite the wheel.

- **`scripts/inventory.py <root>`** — Walks the directory. Outputs `inventory.json` with parsed title/year, grouped companions, and the category each item falls into. Read-only, safe to run anytime.
- **`scripts/plan.py <inventory.json>`** — Reads the inventory, generates a structured `plan.json` listing every operation (move, rename, create, park). Read-only.
- **`scripts/execute.py <plan.json> [--dry-run] [--fuzzy-fallback]`** — Executes the plan. Always run with `--dry-run` first. Dry-run simulates `mkdir`/`rename_dir` so subsequent move ops see the would-be folders — what you see in dry-run is what live will do. Logs to a timestamped file.

The scripts are independent — you can also reason about a library by hand and skip them, but for libraries beyond ~30 movies, scripted inventory + planning saves your sanity (and the user's context window).

## How to ask the user good questions

The branch points that matter most, ordered:

1. **Inner file rename?** When moving loose movies into new folders, rename `28.Days.Later.2002.*.mkv` → `28 Days Later (2002).mkv` (clean), or keep the release name? Infuse handles both. Clean is prettier, release-name is reversible.

2. **Multi-version handling.** Combine into one folder (Infuse picks one as primary, others as alternates), or only keep the highest-quality and delete the rest, or use `{edition-...}` tags?

3. **Collection folders.** Some collection folders (e.g., "James Bond 50 Collection") may contain *higher quality* copies than the user's individual folders. Don't assume the collection is always the duplicate to delete. Compare sizes before recommending.

4. **Orphan files.** `.nfo` and `.bif` leftovers from removed films take up almost no space but cause confusion. Default offer: park them in a list for user review, don't auto-delete.

Use `AskUserQuestion` for these — clear options with concrete examples beat free-text. After the user picks, **state back what you understood** before executing.

## Destructive ops require explicit approval, even when given carte blanche

Even when the user says "delete all the duplicates," you should:
- Show the specific list before deleting
- Verify the duplicate is genuinely lower quality (size comparison is a fine first pass)
- For items >1GB, name the file and its size explicitly in the confirmation
- Never bulk-delete inside a directory you haven't listed and shown the user

This is the same discipline that prevents `rm -rf` accidents — slow down for irreversible operations.

## Reference files

For the long-form details that don't belong in the workflow above:

- **`references/firecore-naming.md`** — Full naming spec: filename conventions, folder structure, edition tags, embedded IDs, characters to avoid, bonus content organization (trailers/featurettes/deleted/interviews).
- **`references/parser-patterns.md`** — Year extraction regex with annotated test cases for the tricky titles (`Blade Runner 2049`, `2001 A Space Odyssey`, `1917`, year ranges in collections).
- **`references/smb-acl-troubleshooting.md`** — Why SMB shares reject writes that look like they should work; per-NAS recipes (Synology, QNAP, TrueNAS, Unraid); macOS remount procedure; how to probe writability.
- **`references/workflow.md`** — Step-by-step playbook of inventory → plan → approve → execute, with copy-paste prompts for the user-question moments.
- **`references/category-handling.md`** — Detailed default for each category A–H, including what to do when categories overlap (e.g., a Cat A loose file targeting a Cat B-renamed folder).

Read the references when you hit the specific situation — they're not required reading every time the skill triggers.
