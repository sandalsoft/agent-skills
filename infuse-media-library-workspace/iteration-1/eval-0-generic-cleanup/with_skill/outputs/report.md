# Firecore/Infuse Library Organization — Report

## Test library built at `/tmp/eval-0-movies/`

Seeded with a mix designed to exercise the skill's edge cases:

- **5 loose movies** with release-name files + companion poster/NFO/backdrop assets
  - `Blade.Runner.2049.2017.UHD.BluRay.x265-RARBG.mkv` (+ poster, backdrop, nfo) — year-in-title trap
  - `The.Matrix.1999.1080p.BluRay.x264-AMIABLE.mkv` (+ poster, nfo)
  - `1917.2019.2160p.WEB-DL.x265-NTb.mkv` (+ poster) — title is all digits
  - `Get.Out.2017.1080p.BluRay.x264-DRONES.mp4` (+ poster)
  - `Inception.2010.1080p.BluRay.x264-SPARKS.mkv` (no companions)
- **2 messy release-name folders** (Cat B)
  - `Arrival.2016.1080p.BluRay.x264-SPARKS/`
  - `Dune.2021.2160p.UHD.BluRay.x265-TERMiNAL/`
- **1 empty placeholder folder** (Cat G): `Empty Placeholder/`
- **3 orphan assets** (Cat E): `leftover.nfo`, `old-movie-poster.jpg`, `random-backdrop.jpg`

Total: 18 entries (15 files + 3 dirs).

## Workflow followed: Inventory -> Plan -> Execute

Used the three scripts shipped with the skill.

### 1. Inventory (`scripts/inventory.py`)

Read-only walk. Classification:

| Cat | Count | Items |
|---|---|---|
| A loose movies | 5 | Blade Runner 2049, The Matrix, 1917, Get Out, Inception |
| B folder renames | 2 | Arrival, Dune |
| E orphans | 3 | leftover.nfo, old-movie-poster.jpg, random-backdrop.jpg |
| G empty dirs | 1 | Empty Placeholder |

Parser correctness: Blade Runner 2049 parsed as `Blade Runner 2049 (2017)` — the "last year wins" rule correctly identified 2017 as the release year and kept 2049 in the title. 1917 parsed as `1917 (2019)` for the same reason.

### 2. Plan (`scripts/plan.py --rename-inside-cat-a`)

Chose to rename inner files to clean `Title (YYYY)` form. Rationale: the user is setting up Infuse fresh and described the state as "looks awful" — clean names display better. With no multi-version groups, no collision risk.

Plan: 19 operations (2 dir renames + 5 mkdirs + 12 moves). Parked 3 orphans + 1 empty dir for user review (not auto-deleted, per skill's destructive-ops policy).

### 3. Execute (`scripts/execute.py`)

Dry-run first surfaced expected "target dir missing" warnings in dry-run mode (mkdir isn't actually performed during dry-run, so downstream moves can't validate). Live run: 19/19 ops, 0 failures.

## What changed

**Created (per-movie folders):** `1917 (2019)/`, `Blade Runner 2049 (2017)/`, `Get Out (2017)/`, `Inception (2010)/`, `The Matrix (1999)/`

**Renamed (Cat B messy folders):**
- `Arrival.2016.1080p.BluRay.x264-SPARKS/` -> `Arrival (2016)/`
- `Dune.2021.2160p.UHD.BluRay.x265-TERMiNAL/` -> `Dune (2021)/`

**Moved + renamed (Cat A):** All 12 loose video + companion files swept into their per-movie folders with clean inner names, e.g.
- `Blade.Runner.2049.2017.UHD.BluRay.x265-RARBG.mkv` -> `Blade Runner 2049 (2017)/Blade Runner 2049 (2017).mkv`
- `Blade.Runner.2049.2017.UHD.BluRay.x265-RARBG-backdrop.jpg` -> `Blade Runner 2049 (2017)/Blade Runner 2049 (2017)-backdrop.jpg`

**Cat B inner files:** Per `plan.py`'s default policy, files inside renamed Cat B folders were left with their release names. This is the documented safe default (`--rename-inside-cat-b` is reserved/disabled — "risky"). Infuse still matches them because the folder name carries `Title (YYYY)`.

## What was parked (untouched, awaiting user decisions)

- `Empty Placeholder/` — empty Cat G folder. User to fill or delete.
- `leftover.nfo`, `old-movie-poster.jpg`, `random-backdrop.jpg` — Cat E orphan assets. Likely leftovers; harmless but cluttering.

## Top-level after organization

```
1917 (2019)/                  <- new, Cat A
Arrival (2016)/               <- renamed from messy, Cat B (inner files keep release name)
Blade Runner 2049 (2017)/     <- new, Cat A (NOT 2049 — release year wins)
Dune (2021)/                  <- renamed from messy, Cat B (inner files keep release name)
Empty Placeholder/            <- parked, Cat G
Get Out (2017)/               <- new, Cat A
Inception (2010)/             <- new, Cat A
The Matrix (1999)/            <- new, Cat A
leftover.nfo                  <- parked orphan, Cat E
old-movie-poster.jpg          <- parked orphan, Cat E
random-backdrop.jpg           <- parked orphan, Cat E
```

8 per-movie folders ready for Infuse, all in `Title (YYYY)` form. 4 items parked for user decisions. Zero data loss.
