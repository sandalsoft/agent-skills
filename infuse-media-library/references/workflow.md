# Detailed Workflow

This is the step-by-step playbook for taking a movie library from "mess" to "Infuse-clean." Read this when you need the long-form version of the loop sketched in `SKILL.md`.

## Phase 1: Inventory

Run `scripts/inventory.py <root>` or do the equivalent manually. The output is a structured analysis: how many entries, how many videos, how the loose files group, which folders are properly named, which are messy, what's orphaned.

You should walk away from Phase 1 able to state:

- How many top-level entries total
- How many loose video files at top level
- How many existing folders, broken down into:
  - `Title (YYYY)` form
  - Messy release-name form
  - Empty
  - `.trickplay` (these belong with their movie)
- How many orphan asset files (NFO/poster/bif with no matching video)
- How many multi-version situations (same parsed title+year, multiple videos)
- How many likely "collection" folders (multi-movie containers)

Phase 1 is read-only. Don't move anything yet.

## Phase 2: Plan

Sort every item into one of the categories below. The default action is in the third column; the parking column says when to ask the user instead.

| Cat | Detection | Default | Park when |
|---|---|---|---|
| **A** | Loose video at top + companion files (nfo, posters, trickplay) | Move all into `Title (YYYY)/` folder, rename inside | — |
| **B** | Existing folder with parseable title/year but messy name | Rename folder to clean `Title (YYYY)` | Two folders would rename to same target |
| **C** | Multiple videos parse to same `Title (YYYY)` | Combine into one folder, keep release names | User wants only highest quality |
| **D** | Folder name suggests collection (`Trilogy`, `Duology`, `Collection`, year-range `(YYYY-YYYY)`) | — | Always park |
| **E** | NFO/BIF/poster file with no matching video anywhere | — | Always park |
| **F** | Two messy folders would rename to same `Title (YYYY)`; folder has no parseable year; no matching video | — | Always park |
| **G** | Empty folder that doesn't match any loose-file group | — | Always park |
| **H** | Unparseable filename; ISO instead of mkv; only extras with no main film | — | Always park |

After categorization, generate a written plan with counts per category and a sample of operations per category.

## Phase 3: Approve

Present the plan to the user with `AskUserQuestion`. The questions that matter most:

**Question 1: Approve A + B safe operations?**

```
OK to proceed with [N] Category A moves (loose movies → per-movie folders) and
[M] Category B folder renames? Files keep their original release-name format
inside folders unless you say otherwise (Infuse handles dots/spaces/dashes
interchangeably).

Options:
- Yes, do both
- Only Category A (moves)
- Only Category B (renames)
- Wait, let me review the full list first
```

**Question 2: Inner file rename policy?**

```
Inside the new folders, should I also rename files to match the folder
(e.g. `28 Days Later (2002).mkv`)?

Options:
- No, keep release names (safest — Infuse matches both)
- Yes, rename to Title (YYYY) (cleaner)
- Only the main video file (compromise — rename .mkv but keep posters/nfo as-is)
```

For Category B specifically, **strongly prefer "no inner renames."** Existing folders often contain canonical Infuse asset names (`movie.nfo`, `folder.jpg`, `backdrop.jpg`) plus subdirectories like `Sample/` and `Featurettes/`. Touching them risks clobbering valid metadata.

**Question 3: Multi-version handling?**

```
[X] movies have multiple versions at top level (e.g. 1080p + 2160p, Director's Cut
+ Theatrical). How to handle?

Options:
- Park them all - I'll decide later
- Combine in one folder per movie (Infuse picks one as primary, others as alternates)
- Combine + add {edition-...} tags (use Firecore's edition syntax)
```

After collecting answers, restate the user's choices and the operations they imply.

## Phase 4: Execute

Always two-step: dry-run, then live.

```bash
python3 scripts/execute.py plan.json --dry-run
# Review output, look for ERROR/SKIP messages
python3 scripts/execute.py plan.json
```

Stream progress. If an operation fails, log it and continue — most failures are SMB ACL issues that don't affect other operations.

After live execution, **verify** the result:

- Loose video count should be ~0 (only unparseable ones remain)
- New folders should contain the expected files
- Source files should be gone (since `mv` removes them)

Then present:

- Stats: before/after counts
- What was done
- What's still parked (categories C-H plus any A/B failures)

## Common operational issues during execute

**Cat A → Cat B target overlap.** A Category A operation might target a folder that's also a Category B rename source. Run Category B first so the folder has its clean name when Category A tries to use it. If Cat A's `target_folder` doesn't exist after Cat B (because B renamed it), fall back to looking up the clean form or doing a fuzzy match.

**Fuzzy folder match.** `Mad Max - Fury Road (2015)` (with dash) and `Mad Max Fury Road (2015)` (without) refer to the same movie. Before creating a new folder, check for case-insensitive, separator-insensitive matches against existing folders. The normalize function from `parser-patterns.md` handles this.

**Trickplay folder moves on SMB.** As noted in `smb-acl-troubleshooting.md`, moving a `.trickplay/` directory across folder boundaries on SMB often fails with `Permission denied`. Use `cp -R` then explicit delete, with user confirmation for the delete step.

**Multi-version + inner rename collision.** If two versions of "Ballerina (2025)" both rename to `Ballerina (2025).mkv`, the second clobbers the first. When moving multi-version groups, *keep the release names* unless the user opted into edition tags.

## After execution

The parked list is what the user does with their fresh-mind judgment. Compile:

1. Cat C items not yet handled (multi-version)
2. Cat D collection folders (need split vs delete decisions)
3. Cat E orphan files (likely deletes, but confirm)
4. Cat F conflicts (require user input)
5. Cat G empty folders (delete or fill)
6. Cat H special cases (ISO files, extras-only folders, unparseable)
7. Any A/B failures from the run

Show this list grouped by category, each entry with enough detail to make a decision. Then `AskUserQuestion` for each category, one question per category.

## Common follow-up tasks after the main pass

These usually surface during the parked-list review:

- **Extract a movie from a collection folder before deleting the collection.** Example: if `The.Godfather.Trilogy/` contains the user's only copy of Part II, mkdir `The Godfather Part II (1974)/` and move the Part II files in before removing the trilogy folder.
- **Quality-based dedupe.** When two folders/files for the same movie exist, compare sizes (`du -sh`). Larger usually = higher quality. Confirm with user before deleting.
- **Convert messy-named folders that contain only extras into their own structured entry.** E.g., `Casino Royale (2006)/becoming.bond-rmxtras.mkv` is the "Becoming Bond" documentary, not the actual Bond film. Move it to a `Becoming Bond (2017)/` folder of its own.
