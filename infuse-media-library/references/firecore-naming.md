# Firecore Infuse — Full Naming Reference

Source: <https://support.firecore.com/hc/en-us/articles/215090947-Metadata-101>. The conventions below also work for Plex, Jellyfin, Emby, and Kodi — they all read TMDB-style folder structures.

## Filename conventions

Infuse accepts very flexible names. All of these match the same film:

```
Pulp Fiction (1994).mkv
Pulp.Fiction.1994.1080p.BluRay.x264-RELEASE.mkv
Pulp_Fiction_1994.mkv
Pulp-Fiction-1994-1080p-BluRay.mkv
```

**Separators are interchangeable.** Period, space, underscore, and dash all work, and you can mix them. This is why messy torrent release names still match — Infuse is parsing for "title + year" and is forgiving about everything else.

**Year format.** Optional but strongly recommended for matching accuracy. Use `(YYYY)` in parentheses for the most unambiguous form. Bare 4-digit years (`Pulp Fiction 1994.mkv`) also work but can confuse the parser if the title contains a year-like number (`Blade Runner 2049 2017.mkv` — see `parser-patterns.md`).

**Characters to avoid in any filename or folder name:**
```
"  \  /  :  |  <  >  *  ?
```
These are illegal on Windows/SMB and can cause issues on macOS even though HFS+/APFS accept some of them. Strip them before generating new names.

## Recommended directory structure

One folder per movie, holding the video and its assets:

```
/Movies/
  Pulp Fiction (1994)/
    Pulp Fiction (1994).mkv
    Pulp Fiction (1994).nfo
    Pulp Fiction (1994)-poster.jpg
    Pulp Fiction (1994)-backdrop.jpg
    Pulp Fiction (1994)-landscape.jpg
    Pulp Fiction (1994)-logo.png
    Pulp Fiction (1994)-clearlogo.png
    Pulp Fiction (1994).srt
    Pulp Fiction (1994).trickplay/    (Infuse-specific scrubbing previews)
```

Infuse also recognizes these *canonical* names inside a movie folder (no title prefix needed):

```
movie.nfo       — metadata
folder.jpg      — folder icon
backdrop.jpg    — fanart background
poster.jpg      — vertical poster
logo.png        — clear logo
landscape.jpg   — horizontal landscape
clearlogo.png   — transparent logo
```

If a folder contains both `movie.nfo` and `Pulp Fiction (1994).nfo`, Infuse will use whichever it finds first. Mixing is fine.

## Multiple versions / editions

When you have several rips of the same movie, two strategies:

**(a) Multiple files, same folder.** Infuse picks one as primary and offers the others as alternate versions:

```
Mad Max Fury Road (2015)/
  Mad Max Fury Road (2015).mkv
  Mad Max Fury Road (2015) Black and Chrome Edition.mkv
  Mad.Max.Fury.Road.2015.2160p.UHD.BluRay.REMUX.HDR.HEVC.Atmos-EPSiLON.mkv
```

**(b) Explicit edition tags** using `{edition-Description}`:

```
Get Out (2017)/
  Get Out (2017) {edition-Theatrical}.mkv
  Get Out (2017) {edition-Alternate Ending}.mkv
```

Infuse also auto-recognizes a small set of standard edition strings without curly braces:
`Director's Cut`, `Extended Cut`, `Theatrical Cut`, `Unrated Cut`, `Special Edition`, `IMAX`, `Remastered`, `Anniversary Edition`, plus disc/part markers like `disc1`/`disc2` and `part1`/`part2`.

## Embedded TMDB / IMDB IDs

For movies with ambiguous titles (e.g. multiple films named *Crash*), embed an ID directly in the filename:

```
Crash (2004) {tmdb-1639}.mkv
Crash (1996) {imdb-tt0115433}.mkv
```

This forces a specific match and skips Infuse's title-based search entirely.

## Bonus content / extras

Two valid layouts:

**Suffix-based** (file at top level of the movie folder):
```
Pulp Fiction (1994)/
  Pulp Fiction (1994).mkv
  Pulp Fiction (1994)-trailer.mkv
  Pulp Fiction (1994)-deleted.mkv
  Pulp Fiction (1994)-featurette.mkv
  Pulp Fiction (1994)-interview.mkv
  Pulp Fiction (1994)-short.mkv
```

**Folder-based** (subfolders for each extra type — better when you have many):
```
Pulp Fiction (1994)/
  Pulp Fiction (1994).mkv
  Trailers/
  Deleted Scenes/
  Behind The Scenes/
  Featurettes/
  Interviews/
```

Both work in Infuse. Folder-based is cleaner when there are 5+ extras.

## TV shows (different schema)

This skill focuses on movies. TV shows use a different layout:

```
/TV Shows/
  Breaking Bad/
    Season 01/
      Breaking Bad - S01E01 - Pilot.mkv
      Breaking Bad - S01E02 - Cat's in the Bag.mkv
```

If you encounter TV content while organizing a movie library (mini-series, multi-episode releases like `Nuremberg.2000.E01.mkv` + `Nuremberg.2000.E02.mkv`), flag it — the user usually wants TV out of the movies directory.

## What Infuse does NOT need

- A specific .nfo schema. Infuse fetches metadata from TMDB itself; the .nfo is for compatibility with other scrapers (Kodi, Jellyfin).
- Exact case matches. `pulp fiction (1994).mkv` works the same as `Pulp Fiction (1994).mkv`.
- Sample files or release group .nfo files. Those `Sample/` subfolders and `release-group.nfo` files do no harm but add clutter.
