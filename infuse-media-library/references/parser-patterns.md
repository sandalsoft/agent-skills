# Title / Year Parser Patterns

The naive approach — grab the first 4-digit number that looks like a year — fails on a small but important set of titles. This reference documents the patterns that actually work and the test cases that prove it.

## The core rule

When parsing a base filename for `(title, year)`:

1. **If `(YYYY)` appears in parentheses anywhere, use that.** This is unambiguous — only release years get parenthesized.
2. **Otherwise, find every bare year-like token (1900-2030, surrounded by separators), and pick the LAST one.** Release years sit closest to the resolution/codec tags at the end of release names; title-internal year-like numbers come earlier.

The "year-like token" regex (Python):

```python
import re

# Matches a 4-digit year (1900-2030) preceded by start-of-string OR a separator,
# and followed by a separator OR end-of-string. The separators are space, dot,
# underscore, dash, opening/closing bracket.
YEAR_TOKEN = re.compile(r"(?:^|[\s._\-\[])((?:19\d{2}|20\d{2}))(?=[\s._\-\]]|$)")

# Parenthesized year — always wins
PAREN_YEAR = re.compile(r"\((19\d{2}|20\d{2})\)")

def parse_title_year(base: str):
    m = PAREN_YEAR.search(base)
    if m:
        return _normalize(base[:m.start()]), m.group(1)
    matches = list(YEAR_TOKEN.finditer(base))
    if not matches:
        return None, None
    m = matches[-1]
    return _normalize(base[:m.start(1)]), m.group(1)

def _normalize(raw: str) -> str:
    raw = raw.rstrip(" ._-[(")
    s = re.sub(r"[._]+", " ", raw)   # dots/underscores → space
    s = re.sub(r"\s+", " ", s).strip()
    return s
```

Note `_normalize` only collapses `.` and `_` to space, *not* `-`. Hyphens are meaningful in titles like `Mission - Impossible` and `Rambo - First Blood Part II`.

## Test cases — the ones that break naive parsers

| Input filename | Expected title | Expected year |
|---|---|---|
| `Blade.Runner.2049.2017.UHD.BluRay.x265-RARBG.mkv` | Blade Runner 2049 | 2017 |
| `2001.A.Space.Odyssey.1968.2160p.UHD.BluRay.mkv` | 2001 A Space Odyssey | 1968 |
| `1917.2019.1080p.DVDSCR.x264-TOPKEK.nfo` | 1917 | 2019 |
| `Citizen.Kane.1941.2160p.UHD.BluRay.mkv` | Citizen Kane | 1941 |
| `Super.Troopers.2001.720p.BluRay.x264-SiNNERS.mkv` | Super Troopers | 2001 |
| `Indiana.Jones.and.the.Temple.of.Doom.1984.2160p.mkv` | Indiana Jones and the Temple of Doom | 1984 |
| `Top.Secret.1984.1080p.BluRay.mkv` | Top Secret | 1984 |
| `Heat (1995) (2160p BluRay x265 HEVC 10bit HDR DTS 7.1 SAMPA)` | Heat | 1995 |
| `300.2006.1080p.BluRay.x264-hV` | 300 | 2006 |
| `300 - Rise of an Empire (2014)` | 300 - Rise of an Empire | 2014 |

The naive "first year wins" parser fails on rows 1, 2, 3, 5 — every title that contains a year-like number.

## Companion file suffixes

These suffixes identify Infuse/Plex/Jellyfin asset files that belong to a movie. Strip the suffix from a filename to recover the base, then group with the matching video file.

```python
ASSET_SUFFIXES = [
    "-backdrop.jpg",
    "-landscape.jpg",
    "-logo.png",
    "-logo.svg",
    "-poster.jpg",
    "-clearlogo.png",
    "-fanart.jpg",
    "-fanart1.jpg",
    "-fanart2.jpg",
    "-fanart3.jpg",
    "-thumb.jpg",
    "-320-10.bif",   # Infuse trickplay sidecar
    ".srt",
]
NFO_EXT = ".nfo"
BIF_EXT = ".bif"
TRICKPLAY_SUFFIX = ".trickplay"   # this is a DIRECTORY, not a file
```

Trickplay folders contain a single subdirectory (e.g. `320 - 10x10/`) with N.jpg thumbnails inside — Infuse uses these for fast scrubbing previews.

## Things to watch for

**Multi-year collection folders.** Names like `(2001-2011)` or `1962-2008` denote a range. Don't treat the second year as the release year — these are collections, not single films. Detect by looking for `(\d{4}-\d{4})` or `\d{4}-\d{4}` in the folder name and parking it as Category D.

**Folder name doesn't reflect content.** Some folders are named after one release (e.g. `Dune.1984.1080p.BluRay.DTS.x264-CtrlHD/`) but contain a different rip inside. The folder name is what Infuse uses for matching, so renaming the folder is what matters most. Leave inner files alone unless cleanup is explicitly requested.

**Lowercase vs Title Case.** `f1.the.movie.2025.repack.*.mkv` parses to title `f1 the movie` and year `2025`. The case is preserved. If you're generating clean target folders, consider title-casing: `F1 The Movie (2025)`. But also check whether a folder with a different case already exists (`F1 The Movie (2025)/`) — case-insensitive fuzzy match prevents creating duplicates.

**Apostrophes and punctuation in titles.** `Ferris Bueller's Day Off (1986)` is fine — apostrophes are legal. But strip illegal chars (`" \ / : | < > * ?`) before writing. `Mission: Impossible` becomes `Mission Impossible` or `Mission - Impossible`.

**Mismatched folder+file casings.** If the user has folder `John Wick Chapter 4 (2023)/` and also `John.Wick.Chapter.4.2023.UHD.BluRay.2160p...REMUX-FraMeSToR/`, both refer to the same movie. Detect via case-insensitive normalized-title match before treating as separate movies.
