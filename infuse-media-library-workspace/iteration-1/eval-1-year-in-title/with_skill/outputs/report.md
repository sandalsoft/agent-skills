# Eval 1 — Year-in-Title — Report

## Task
Build a 6-file test movie library at `/tmp/eval-1-movies/` containing release-named loose files (including titles with year-like numbers in the title), then reorganize into Infuse `Title (YYYY)/` per-movie folders. The critical check: **`Blade Runner 2049` (released 2017) must land under `Blade Runner 2049 (2017)/`, not `Blade Runner (2049)/`**.

## What I did

1. **Built test library** with `touch` — 6 empty placeholder files for 4 movies (Blade Runner 2049 has 3 companion files: mkv + nfo + poster).
2. **Inventory** — ran `scripts/inventory.py /tmp/eval-1-movies/`. All 4 movies categorized as Cat A (loose movies). Year parsing correctly handled the tricky titles.
3. **Plan** — ran `scripts/plan.py --rename-inside-cat-a` so inner files get clean `Title (YYYY).ext` names. 10 operations queued, all Cat A. No parked items.
4. **Dry run** — sanity-checked the plan. (Dry run reports false "target dir missing" errors because `mkdir` is simulated, not actually done — known artifact, not a real failure.)
5. **Execute (live)** — 10/10 ops succeeded, 0 failed. Companion files (poster, nfo) correctly followed the main video into the Blade Runner 2049 folder.

## Year-parsing verification (the load-bearing part)

| Title (with year-like digits in title) | Parser output | Correct? |
|---|---|---|
| `Blade.Runner.2049.2017.UHD.BluRay.x265-RARBG.mkv` | `Blade Runner 2049 (2017)` | yes — picked the *last* year token (2017), kept `2049` in title |
| `2001.A.Space.Odyssey.1968.2160p.UHD.BluRay.mkv` | `2001 A Space Odyssey (1968)` | yes — `2001` kept in title, `1968` picked as release year |
| `1917.2019.1080p.DVDSCR.x264-TOPKEK.mkv` | `1917 (2019)` | yes — `1917` kept as title, `2019` picked as release year |
| `Citizen.Kane.1941.2160p.UHD.BluRay.mkv` | `Citizen Kane (1941)` | yes — straightforward case |

## Final layout

```
/tmp/eval-1-movies/
  1917 (2019)/
    1917 (2019).mkv
  2001 A Space Odyssey (1968)/
    2001 A Space Odyssey (1968).mkv
  Blade Runner 2049 (2017)/
    Blade Runner 2049 (2017).mkv
    Blade Runner 2049 (2017).nfo
    Blade Runner 2049 (2017)-poster.jpg
  Citizen Kane (1941)/
    Citizen Kane (1941).mkv
```

## Decisions made under Auto Mode

- **Rename inside folders** — picked the clean `Title (YYYY).ext` form (`--rename-inside-cat-a`) over keeping release names. Justified because this is a fresh test library, no multi-version collisions exist, and the clean form is what Infuse documentation recommends.
- **Skipped the user-approval gate** — Auto Mode + tiny well-defined library + no parked items meant no genuine branch points to surface.

## Notes / observations

- `scripts/plan.py` writes to `--out` flag, not stdout. First invocation without `--out` wrote `plan.json` to cwd; cleaned up and re-ran with `--out` pointing into the outputs dir.
- The execute dry-run prints `ERR target dir missing` for moves into dirs the same plan creates earlier — false alarms (mkdir is also dry-run); live run confirmed all 10 ops worked. Worth knowing when interpreting dry-run output.
