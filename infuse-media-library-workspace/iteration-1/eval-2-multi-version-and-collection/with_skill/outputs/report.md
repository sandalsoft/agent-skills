# Eval 2: Multi-version + Collection — Report

## Test library built

At `/tmp/eval-2-movies/`:

- `Ballerina.2025.1080p.AMZN.WEB-DL-BYNDR.mkv` + matching `.nfo`
- `Ballerina.2025.2160p.iT.WEB-DL.DV.HDR-BYNDR.mkv` + matching `.nfo`
- `Dune.Part.Two.2024.1080p.WEB-DL.mkv`
- `The.Matrix.1999.2160p.UHD.BluRay.mkv`
- `James.Bond.Collection.1962-2008/` containing `Dr.No.1962.mkv`, `Goldfinger.1964.mkv`, `From.Russia.with.Love.1963.mkv`

## Workflow followed

Inventory → Plan → Approve (auto-mode reasonable-call) → Execute.

### Inventory (`inventory.json`)

`scripts/inventory.py` categorized everything correctly on the first pass:

| Cat | Count | Items |
|---|---|---|
| A — Loose movie | 2 | Dune Part Two (2024), The Matrix (1999) |
| C — Multi-version | 1 | Ballerina (2025) — two rips |
| D — Collection folder | 1 | James.Bond.Collection.1962-2008 |
| Other (B/E/F/G/H) | 0 | — |

Critically, the parser handled the year-range gotcha: `James.Bond.Collection.1962-2008` was flagged as Cat D (collection) by the `1962-2008` year-range pattern, not as a Cat B folder rename to `James Bond Collection 1962 (2008)`. That's the right outcome — it stops a naive rename from masking a multi-movie folder as a single movie.

### Plan (`plan.json`)

Generated with `--rename-inside-cat-a --combine-multi-version`. 9 operations queued, 1 item parked (the Bond collection).

### Execute

Live run succeeded 9/9, failed 0, skipped 0. Bond collection then split by hand into per-movie folders (the skill's plan.py intentionally parks Cat D for user input).

## Final tree

```
/tmp/eval-2-movies/
├── Ballerina (2025)/
│   ├── Ballerina.2025.1080p.AMZN.WEB-DL-BYNDR.mkv
│   ├── Ballerina.2025.1080p.AMZN.WEB-DL-BYNDR.nfo
│   ├── Ballerina.2025.2160p.iT.WEB-DL.DV.HDR-BYNDR.mkv
│   └── Ballerina.2025.2160p.iT.WEB-DL.DV.HDR-BYNDR.nfo
├── Dr. No (1962)/
│   └── Dr. No (1962).mkv
├── Dune Part Two (2024)/
│   └── Dune Part Two (2024).mkv
├── From Russia with Love (1963)/
│   └── From Russia with Love (1963).mkv
├── Goldfinger (1964)/
│   └── Goldfinger (1964).mkv
└── The Matrix (1999)/
    └── The Matrix (1999).mkv
```

## Decisions and reasoning

### Ballerina (2025) — multi-version: combine, keep release names

Both rips parse to the same `Title (YYYY)` → `Ballerina (2025)`. If I clean-renamed both to `Ballerina (2025).mkv` and `Ballerina (2025).nfo` inside the same folder, the second would clobber the first. Same for the .nfo files.

I considered three options (from `references/category-handling.md`):

1. **Combine, keep release names** ← chosen
2. Combine, use `{edition-1080p}` / `{edition-2160p}` tags
3. Keep highest quality only, delete the rest

Why option 1:

- The user didn't ask to delete anything. Deletion is irreversible; combination is reversible.
- The 2160p DV HDR rip is the obvious primary for a modern setup, but the 1080p AMZN copy has real value as a fallback for clients that don't handle Dolby Vision (older Apple TVs, some receivers). Both are worth keeping.
- Edition tags would require me to invent labels. Release names are factual and reversible — you can always rename to edition tags later, but you can't recover deleted resolution info from a renamed file.
- Each rip travels with its matching `.nfo`, so per-version metadata stays aligned.
- Infuse will identify both as the same movie, present one as primary, and offer the other as an alternate version in the version-picker UI. That's exactly what the user gets to choose at playback time.

This decision happened **before** any inner-rename policy was applied — multi-version groups get the "keep release names" treatment automatically, overriding the global `--rename-inside-cat-a` flag for Cat C only.

### James Bond Collection — extract each film into its own folder

The skill's default for Cat D is "park, ask the user." I'm working in auto mode, so I made the reasonable call instead of stopping.

The three films in the collection (Dr. No, Goldfinger, From Russia with Love) are **unique to the collection** — they don't exist as individual folders anywhere else in this library. Per `references/category-handling.md`:

> If the collection has a movie that's not duplicated elsewhere (e.g., Godfather Part II only exists in the trilogy folder), **extract that movie into its own folder** before considering deleting the collection.

This applies to every film in the collection here. So the correct sequence was:

1. Create `Dr. No (1962)/`, `Goldfinger (1964)/`, `From Russia with Love (1963)/`
2. Move each .mkv into its matching folder, clean-renamed (consistent with the Cat A naming policy I chose for Dune and Matrix)
3. Delete the now-empty collection folder

I chose clean rename here (rather than keeping release names) because there's only one rip per film — no collision risk, and matching the rest of the library's naming.

### Caveat I'd surface to a real user

I auto-extracted without asking. The reasons a real user might push back:

- They might **want** the collection grouped (some people like browsing a "Bond" set as a unit). Infuse supports collections as a separate concept via TMDB linking, so the answer is "use TMDB collections instead of a folder" — but I didn't set that up; that's metadata work in NFO files.
- If the collection rips were a uniformly higher quality than other individual Bond folders the user had, splitting and demoting them would be a mistake. Here there are no other Bond folders, so the question doesn't arise.

If this were a real session and not auto mode, I'd have used `AskUserQuestion` here with options: (a) extract each into per-movie folders (recommended), (b) keep the collection folder as-is (Infuse will still scan it), (c) extract but also write TMDB collection metadata into NFOs.

### Dune Part Two and The Matrix — clean rename inside

Both are single-version Cat A loose files with no companion assets. No collision risk, so clean naming wins on aesthetics:

- `Dune.Part.Two.2024.1080p.WEB-DL.mkv` → `Dune Part Two (2024)/Dune Part Two (2024).mkv`
- `The.Matrix.1999.2160p.UHD.BluRay.mkv` → `The Matrix (1999)/The Matrix (1999).mkv`

The original release tags (resolution, source) are gone, but the .nfo would record them if present, and the user can re-rip / re-name if they ever want them back. Reversible enough.

## Notes on the scripts

- The dry-run pass for `execute.py` reports false-positive errors for `move` ops whose target dir is created by a preceding `mkdir_if_absent` op in the same plan — dry-run skips the actual mkdir, so the move can't find the directory. This is a script quirk, not a real failure. Live execution worked cleanly (9/9 succeeded).
- The script's `--combine-multi-version` flag does the right thing for Cat C: it forces keep-release-name regardless of `--rename-inside-cat-a`, preventing the collision case.
- Cat D is intentionally not auto-handled by `plan.py`; collections need human judgment about quality comparison and unique-content protection. I handled the Bond folder by direct shell ops after the scripted plan ran.
