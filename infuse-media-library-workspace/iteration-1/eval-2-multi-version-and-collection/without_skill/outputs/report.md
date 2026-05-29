# Infuse Library Reorganization Report

## Goal

Reorganize `/tmp/eval-2-movies-baseline/` from a mix of loose release-named files and a misleading "collection" folder into the canonical Infuse layout: one `Title (YYYY)/` folder per movie, with the primary video file named to match.

## Starting State

```
Ballerina.2025.1080p.AMZN.WEB-DL-BYNDR.mkv
Ballerina.2025.1080p.AMZN.WEB-DL-BYNDR.nfo
Ballerina.2025.2160p.iT.WEB-DL.DV.HDR-BYNDR.mkv
Ballerina.2025.2160p.iT.WEB-DL.DV.HDR-BYNDR.nfo
Dune.Part.Two.2024.1080p.WEB-DL.mkv
The.Matrix.1999.2160p.UHD.BluRay.mkv
James.Bond.Collection.1962-2008/
    Dr.No.1962.mkv
    Goldfinger.1964.mkv
    From.Russia.with.Love.1963.mkv
```

## Final State

```
Ballerina (2025)/
    Ballerina (2025) - 1080p.mkv
    Ballerina (2025) - 1080p.nfo
    Ballerina (2025) - 2160p DV HDR.mkv
    Ballerina (2025) - 2160p DV HDR.nfo
Dune Part Two (2024)/
    Dune Part Two (2024).mkv
The Matrix (1999)/
    The Matrix (1999).mkv
Dr. No (1962)/
    Dr. No (1962).mkv
From Russia with Love (1963)/
    From Russia with Love (1963).mkv
Goldfinger (1964)/
    Goldfinger (1964).mkv
```

## Decisions and Reasoning

### Decision 1: Standard loose movies (Dune, Matrix)

Infuse's preferred layout is one folder per movie named `Title (YYYY)`, with the primary video file named the same way inside it. Stripped release tags (1080p.WEB-DL, 2160p.UHD.BluRay) from filenames since Infuse reads quality from the file's actual stream metadata, not its name. Replaced dots with spaces in titles — dots are a torrent-release convention; Infuse prefers human-readable titles.

### Decision 2: Multi-version Ballerina (the interesting one)

Two rips of the same movie — a 1080p AMZN WEB-DL and a 2160p iTunes WEB-DL with Dolby Vision and HDR. Three plausible approaches:

1. **Keep them as two separate movies.** Wrong — they'd duplicate in the library and Infuse would scrape both as the same TMDB entry but show them as twins.
2. **Pick one and discard the other.** User clearly wants both kept, so no.
3. **Single movie folder, multiple version files.** Correct. Infuse natively supports multi-version movies: put both rips in the same `Title (YYYY)/` folder and Infuse will offer a version picker when you select the movie.

I went with option 3. The safest cross-app convention is `Title (YYYY) - {edition}.ext`:

- `Ballerina (2025) - 1080p.mkv`
- `Ballerina (2025) - 2160p DV HDR.mkv`

I kept resolution and HDR format in the edition tag because that's the actual user-facing difference. When someone picks a version in Infuse, "1080p" vs "2160p DV HDR" is what they want to see. I dropped the source tag (AMZN, iT) and the release group (BYNDR) because those don't help the user pick which one to play.

The matching .nfo sidecars were renamed in parallel so they stay paired with their video files. Infuse can read per-file NFO sidecars, so this preserves whatever pre-scraped metadata the user had.

### Decision 3: The "James.Bond.Collection.1962-2008" folder

This is the trap. The folder name suggests it should be preserved as a collection, but **Infuse "collections" are a metadata concept, not a folder structure.** Infuse builds collections automatically from TMDB's belongs-to-collection field — so all three Bond films will appear under a "James Bond Collection" view in the app *without* a wrapping folder, as long as each film is its own scannable movie folder.

If I had left them inside the wrapping folder, Infuse would either treat the folder as a single unknown movie and fail to scrape, or scrape each child file but with a path that confuses some library views.

So I flattened: extracted each film into its own `Title (YYYY)/` folder at the library root and removed the now-empty wrapping folder. Each Bond film now stands on its own:

- `Dr. No (1962)/Dr. No (1962).mkv`
- `From Russia with Love (1963)/From Russia with Love (1963).mkv`
- `Goldfinger (1964)/Goldfinger (1964).mkv`

Infuse will detect all three via TMDB and group them under the James Bond collection in its collections view, exactly as the original folder name was trying (incorrectly) to do.

Title-normalization notes for Bond:
- `Dr.No` -> `Dr. No` (proper punctuation; period after the abbreviation, space before the name).
- `From.Russia.with.Love` -> `From Russia with Love` (lowercase prepositions/articles per standard title case).
- `Goldfinger` already a single word.

## Summary

| Item | Action | Why |
|---|---|---|
| Dune, Matrix loose files | Wrapped in `Title (YYYY)/` folder, renamed | Canonical Infuse layout |
| Ballerina x2 rips | Combined into one folder with edition-suffix filenames | Infuse multi-version support |
| Ballerina .nfo sidecars | Renamed in parallel with their videos | Preserve sidecar pairing |
| Bond collection folder | Flattened; each film extracted to its own folder | Infuse builds collections from metadata, not folders |
| Release tags (BYNDR, AMZN, iT, WEB-DL, etc.) | Dropped from filenames | Infuse reads quality from stream metadata; tags add noise |
