# Eval 0 — Generic Cleanup (without skill)

## Task
Build a messy movie library at `/tmp/eval-0-movies-baseline/` and reorganize it into a structure that Infuse (Firecore, Apple TV) can scrape cleanly.

## Baseline library that was built
Created 11 items in a flat folder to mimic a typical "dumped from a torrent client" mess:

Loose video files with companion poster/nfo files:
- `Blade.Runner.2049.2017.UHD.BluRay.x265-RARBG.mkv` + matching `.nfo` + matching `.jpg`
- `The.Matrix.1999.1080p.BluRay.x264-SPARKS.mkv` + `...-poster.jpg`
- `Inception.2010.2160p.WEB-DL.x265.mkv` + `inception.nfo` (lowercase mismatch)
- `Dune.Part.Two.2024.1080p.WEBRip.mkv` (no companions)
- `Parasite (2019).mkv` (already half-clean) + `parasite-fanart.jpg`
- `Arrival.2016.720p.BRRip.mp4` (no companions, `.mp4` instead of `.mkv`)

Already-foldered messy release name:
- `Interstellar.2014.IMAX.2160p.UHD.BluRay.REMUX.HDR.HEVC-FraMeSToR/` containing the `.mkv`, `poster.jpg`, and `movie.nfo`

Junk:
- `New Folder/` — empty placeholder
- `leftover.nfo` — orphan NFO with no matching video
- `random-backdrop.jpg` — orphan image with no matching video

## Organization approach
Infuse (like Plex/Jellyfin/Kodi) scrapes best when each movie lives in its own folder named `Title (YYYY)` and the main video file inside shares that exact name. Companion artwork uses fixed names (`poster.jpg`, `fanart.jpg`) and the NFO either matches the video basename or is named `movie.nfo`.

Steps taken:
1. For every video, derived a clean title + year by stripping release-name noise (resolution tags, source tags, codec, group name, separators).
2. Created a per-movie folder `Title (YYYY)/`.
3. Renamed the main video to `Title (YYYY).ext` (kept `.mp4` for Arrival, `.mkv` for the rest).
4. Renamed companion artwork to `poster.jpg` (or `fanart.jpg` for the parasite case, since the filename signaled fanart/backdrop intent).
5. Renamed sidecar NFOs to `Title (YYYY).nfo` so Infuse picks them up.
6. Collapsed the `Interstellar...FraMeSToR/` release folder into a clean `Interstellar (2014)/` folder with the same convention.
7. Removed `New Folder/` (empty placeholder).
8. Removed the orphan `leftover.nfo` and `random-backdrop.jpg` — no matching video to attach them to, and leaving them at the library root would just clutter Infuse's home screen.

## Final top-level
7 movie folders, one per title, no loose files at the root:
- `Arrival (2016)/`
- `Blade Runner 2049 (2017)/`
- `Dune Part Two (2024)/`
- `Inception (2010)/`
- `Interstellar (2014)/`
- `Parasite (2019)/`
- `The Matrix (1999)/`

## What changed (summary)
- All 8 movies moved into per-title `Title (YYYY)` folders with the main video renamed to match the folder.
- Companion files (posters, fanart, NFOs) renamed to Infuse-friendly names (`poster.jpg`, `fanart.jpg`, or matching basename `.nfo`).
- Messy release-name folder for Interstellar was renamed and its contents normalized.
- Empty `New Folder/` removed.
- Orphan `leftover.nfo` and `random-backdrop.jpg` deleted (no parent video to associate them with).

## Caveats / things I'd flag to the user
- I deleted the two orphan files rather than quarantining them. In a real run on a user's library I'd move them to a `_unsorted/` folder first so nothing is destroyed.
- "Dune Part Two" — the canonical TMDB title is `Dune: Part Two`. I dropped the colon because some filesystems (SMB shares to older NAS units) choke on `:`. If the user's NAS supports it, `Dune: Part Two (2024)/` would scrape slightly more reliably.
- All files are empty placeholders (`touch`-created), so the test only validates the naming/layout, not actual media handling.
