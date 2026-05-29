# Detailed Category Handling

Defaults and edge cases for each category A–H. Read the section for whichever category you're handling.

## Category A: Loose movie + companions

**Detection.** A video file (`.mkv`/`.mp4`/`.avi`/`.iso`/etc) sits at the top level of the library, with optional companion files matching its base name:
- `<base>-backdrop.jpg`, `<base>-landscape.jpg`, `<base>-poster.jpg`, `<base>-logo.png`, `<base>-clearlogo.png`, `<base>-fanart.jpg`
- `<base>.nfo`, `<base>.bif`, `<base>-320-10.bif`, `<base>.srt`
- `<base>.trickplay/` (a directory)

**Default action.** Determine `Title (YYYY)` from the base. If a folder with that name (or a fuzzy-match equivalent) already exists, use it. Otherwise create it. Move all matching files into the folder. If the user opted for "rename inside," rename each file by replacing the old base with `Title (YYYY)`:

```
28.Days.Later.2002.1080p.BluRay.x264-nikt0.mkv → 28 Days Later (2002).mkv
28.Days.Later.2002.1080p.BluRay.x264-nikt0-backdrop.jpg → 28 Days Later (2002)-backdrop.jpg
28.Days.Later.2002.1080p.BluRay.x264-nikt0.trickplay → 28 Days Later (2002).trickplay
```

**Edge cases.**

- **Existing folder is read-only (SMB ACL).** Move fails; park as Cat A blocked. Fix ACL before retry.
- **Existing folder has a different version inside already.** This is a multi-version situation; treat as Cat C. Keep release names to avoid collision.
- **Trickplay directory move fails on SMB.** Use `cp -R` then delete source after user approval.
- **Base name doesn't parse to title+year.** Move to Cat H (unparseable).

## Category B: Messy folder rename

**Detection.** Folder name parses to a title and year, but doesn't look like `Title (YYYY)` (it has resolution tags, codec tags, release group). Examples:
- `Arrival.2016.1080p.BluRay.x264-SPARKS` → `Arrival (2016)`
- `Glengarry Glen Ross 1992 720p HDTV DD5.1 x264-M794` → `Glengarry Glen Ross (1992)`
- `Heat (1995) (2160p BluRay x265 HEVC 10bit HDR DTS 7.1 SAMPA)` → `Heat (1995)`

**Default action.** Rename the folder. **Don't touch contents** unless the user explicitly asks. Many of these folders contain canonical Infuse asset names (`movie.nfo`, `folder.jpg`, `backdrop.jpg`) plus subdirs like `Sample/` and `Featurettes/` — renaming inner files would clobber valid metadata.

**Edge cases.**

- **Two messy folders parse to the same `Title (YYYY)`.** Park both as Cat F. Often these are two rips of the same movie (e.g. `Fight.Club.1999.1080p.*-ESiR` + `Fight.Club.1999.2160p.*-CiNEPHiLES`); user decides which to keep.
- **Target name already exists.** Could be a clean folder. Verify by listing contents; if both exist, treat as multi-version situation.
- **Folder name doesn't reflect inner content.** E.g., folder named `Dune.1984.1080p.BluRay.*` contains a 2160p mkv. The folder name is what Infuse matches on, so rename to clean form. Inner mismatch doesn't matter.
- **Folder is empty.** Move to Cat G — don't rename empty placeholders.

## Category C: Multi-version movies

**Detection.** Multiple videos at top level (or across folders) that parse to the same `Title (YYYY)`. Common cases:
- Same release in 1080p + 2160p (`Ballerina.2025.1080p.*.mkv` + `Ballerina.2025.2160p.*.mkv`)
- Different cuts (`Dune (1984) Alternative Edition Redux.mkv` + `Dune.1984.UHD.BluRay.2160p.*.mkv`)
- Multiple rips/encoders of same release (`Mad.Max.Fury.Road.2015.2160p.*-EPSiLON` + `Mad.Max.Fury.Road.2015.Black.and.Chrome.Edition.1080p.*-FGT`)

**Default action.** Park unless user has given guidance. The user choices are:

1. **Combine in one folder.** Move all versions into a single `Title (YYYY)/` folder, keeping their original release names so they don't collide. Infuse will pick one as primary and offer the others as alternates.
2. **Use edition tags.** Move into one folder; rename each to `Title (YYYY) {edition-1080p}.mkv` and `Title (YYYY) {edition-2160p}.mkv`. Cleaner, but requires the user to choose meaningful edition labels.
3. **Keep highest quality only.** Compare sizes (often a proxy for quality). Keep the largest; delete the rest. Confirm with user before delete.

If combining, **detect multi-version BEFORE deciding the inner-file rename policy.** Multi-version movies get the "keep release names" treatment automatically, regardless of the global "rename inside" choice.

## Category D: Collection folders

**Detection.** Folder name contains "Collection", "Trilogy", "Duology", "Saga", or a year range like `(2001-2011)`. Inside: multiple videos with different titles. Examples:
- `Harry.Potter.Collection.(2001-2011).*/` — 8 films
- `James.Bond.50.Collection.1962-2008.*/` — 24 films
- `The.Godfather.Trilogy.(1972-1990).*/` — 3 films
- `Mission - Impossible/` — 6 films (looser naming, but same structure)

**Default action.** Park. Always ask the user. **Do not split, dedupe, or delete a collection folder on autopilot — even if you have a plausible rationale.** Collection folders are exactly the situation where the user has irreplaceable content (e.g., the only copy of Godfather Part II lives inside a Trilogy folder; the user's highest-quality Bond rips may live in a James Bond Collection folder while individual Bond folders contain lower-quality versions). Splitting without confirmation can delete the only good copy of a film. The questions to ask:

1. **Are individual folders for these movies already in the library?** If yes, the collection may be entirely or mostly duplicate.
2. **Quality comparison.** Sometimes the collection has *higher* quality than the individual folders (e.g., the James Bond 50 Collection has uniform 1080p BluRay DTS rips while individual Bond folders may be smaller compressed copies). Check `du -sh` per movie before recommending which to keep.
3. **Unique content protection.** If the collection has a movie that's not duplicated elsewhere (e.g., Godfather Part II only exists in the trilogy folder), **extract that movie into its own folder** before considering deleting the collection.

The order of operations when a collection has both duplicates and unique items:

```
1. Identify unique movies (not duplicated elsewhere)
2. Extract each unique movie into its own Title (YYYY)/ folder
3. Verify all duplicates are confirmed lower-or-equal quality
4. Delete the collection folder
```

## Category E: Orphan asset files

**Detection.** `.nfo`, `.bif`, `-poster.jpg`, etc., at top level with no matching video file anywhere in the library. Almost always leftovers from movies the user removed.

**Default action.** Park. Default offer to delete is fine if the user wants to clean up, but get explicit approval — they're small (KB range) so the urgency to delete is low, but they clutter the directory.

Don't delete these silently. Even though they're small and clearly orphaned, the user may want to review the list (sometimes they reveal "oh I forgot I had X").

## Category F: Conflicts / special

**Detection.** A bag of situations that don't have a clean default:
- Two folders/files would produce the same `Title (YYYY)` target on rename
- Folder name has no parseable year
- Inner content doesn't match folder name (e.g., folder named for one movie, file for another)
- The folder contains only sample/extras/featurettes, not the main movie

**Default action.** Always park. For each, summarize the conflict and propose 2-3 resolution options.

Examples:

- Two `Fight Club (1999)` candidates (1080p ESiR vs 2160p CiNEPHiLES). Propose: keep highest quality (2160p), delete the lower.
- `Talladega.Nights.The.Ballad.Of.Ricky.Bobby.1080p.BluRay.x264-Grond/` — no year in folder. Inner mkv says 2006. Propose: rename folder to `Talladega Nights The Ballad of Ricky Bobby (2006)/`.
- `Casino Royale (2006)/becoming.bond-rmxtras.mkv` only — inner file is *Becoming Bond* (2017), not the actual Casino Royale film. Propose: move file to its own `Becoming Bond (2017)/` folder; main Casino Royale film is missing.

## Category G: Empty folders

**Detection.** Top-level folder with zero entries inside.

**Default action.** Park. Often these are:
- Placeholders the user created in advance (e.g., `Paddington in Peru (2024)/` empty because they planned to download)
- Old folders whose content was moved/deleted elsewhere
- Created by Sonarr/Radarr as part of monitoring

Offer to delete after confirming. Don't assume "empty = trash" — placeholders are intentional.

## Category H: Special / unparseable

**Detection.** Video files that don't parse to a title+year:
- No year visible (`The Goonies 35mm 1080p.mkv`, `daftpunk1080p.mkv`)
- Custom names (`Simon Schama's Power of Art - Rothko - Black on Maroon-.mp4`)
- Concert films and documentaries with non-standard naming

Also includes:
- ISO files where the rest of the library uses MKV (works in Infuse but unusual)
- Folders containing only extras (`Mission - Impossible (1996)/Mission.Impossible.1996.COMPLETE.UHD.BLURAY-*.iso` — the actual movie is the ISO)

**Default action.** Park. For each, check the companion .nfo file (if any) — it often has the actual title and year. Then either:

1. **Web-search to disambiguate.** "Daft Punk 1080p" could be "Daft Punk Alive 2007", "Daft Punk Unchained" (2015), or "Daft Punk's Electroma" (2006). The .nfo file's `<year>` tag often resolves the ambiguity.
2. **Best-guess + create folder.** If the title is unambiguous despite no year (e.g., `Life of Brian` is clearly Monty Python's 1979 film), create the right folder and move the files in.
3. **Park as truly unknown.** Some files are user-specific and only they can identify them.

When creating a folder for a best-guess case, **state the guess explicitly** to the user: "I'm putting this in `Life of Brian (1979)/` because that's the Monty Python film and the only one matching the filename. Let me know if it should be somewhere else."
