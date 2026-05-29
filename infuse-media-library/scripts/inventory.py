#!/usr/bin/env python3
"""Inventory a movie library directory.

Walks the top level of <root>, groups files by inferred title+year, classifies
each item into one of categories A-H, and emits a JSON inventory.

Usage:
    python3 inventory.py <root> [--out inventory.json]

Read-only — does not modify the filesystem.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict


VIDEO_EXT = {".mkv", ".mp4", ".avi", ".m4v", ".mov", ".iso", ".wmv",
             ".mpg", ".mpeg", ".flv", ".ts", ".webm"}

ASSET_SUFFIXES = [
    "-backdrop.jpg", "-landscape.jpg", "-logo.png", "-logo.svg",
    "-poster.jpg", "-clearlogo.png", "-fanart.jpg", "-fanart1.jpg",
    "-fanart2.jpg", "-fanart3.jpg", "-thumb.jpg", "-320-10.bif", ".srt",
]
TRICKPLAY_SUFFIX = ".trickplay"

COLLECTION_HINTS = (
    "collection", "trilogy", "duology", "saga", "anniversary",
    "complete blu", "complete bluray",
)

PAREN_YEAR_RE = re.compile(r"\((19\d{2}|20\d{2})\)")
BARE_YEAR_RE = re.compile(r"(?:^|[\s._\-\[])((?:19\d{2}|20\d{2}))(?=[\s._\-\]]|$)")
YEAR_RANGE_RE = re.compile(r"\(?(19\d{2}|20\d{2})-(19\d{2}|20\d{2})\)?")


def _norm(raw: str) -> str:
    raw = raw.rstrip(" ._-[(")
    s = re.sub(r"[._]+", " ", raw)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_title_year(base: str):
    """Return (title, year) or (None, None)."""
    m = PAREN_YEAR_RE.search(base)
    if m:
        return _norm(base[: m.start()]), m.group(1)
    matches = list(BARE_YEAR_RE.finditer(base))
    if not matches:
        return None, None
    m = matches[-1]
    return _norm(base[: m.start(1)]), m.group(1)


def normalize_for_match(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[-._:]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def strip_asset_suffix(name: str):
    for s in ASSET_SUFFIXES:
        if name.endswith(s):
            return name[: -len(s)], s
    return None, None


def is_video(name: str) -> bool:
    return os.path.splitext(name)[1].lower() in VIDEO_EXT


def looks_like_collection(name: str) -> bool:
    low = name.lower()
    if YEAR_RANGE_RE.search(name):
        return True
    return any(hint in low for hint in COLLECTION_HINTS)


def inventory(root: str) -> dict:
    if not os.path.isdir(root):
        raise SystemExit(f"Not a directory: {root}")

    entries = sorted(os.listdir(root))
    files = []
    dirs = []
    for n in entries:
        if n.startswith("."):
            continue
        p = os.path.join(root, n)
        if os.path.isdir(p):
            dirs.append(n)
        else:
            files.append(n)

    trickplay_dirs = [d for d in dirs if d.endswith(TRICKPLAY_SUFFIX)]
    actual_dirs = [d for d in dirs if not d.endswith(TRICKPLAY_SUFFIX)]

    # Step 1: Build video groups (one per loose video file at top level)
    video_groups = {}
    for name in files:
        if is_video(name):
            base = os.path.splitext(name)[0]
            video_groups[base] = {
                "video": name,
                "video_base": base,
                "companions": [],
                "nfo": None,
                "bif": None,
                "trickplay": None,
                "title": None,
                "year": None,
            }

    # Step 2: Attach companions / nfo / bif / trickplay to their video group
    unmatched_files = []
    for name in files:
        if is_video(name):
            continue
        # Asset suffix?
        b, suf = strip_asset_suffix(name)
        if b is not None and b in video_groups:
            video_groups[b]["companions"].append(name)
            continue
        # NFO?
        if name.endswith(".nfo"):
            base = name[:-4]
            if base in video_groups:
                video_groups[base]["nfo"] = name
                continue
        # BIF?
        if name.endswith(".bif"):
            base = name[:-4]
            if base in video_groups:
                video_groups[base]["bif"] = name
                continue
        unmatched_files.append(name)

    unmatched_trickplay = []
    for tp in trickplay_dirs:
        base = tp[: -len(TRICKPLAY_SUFFIX)]
        if base in video_groups:
            video_groups[base]["trickplay"] = tp
        else:
            unmatched_trickplay.append(tp)

    # Step 3: Parse title/year for each video group
    parsed = defaultdict(list)
    unparseable = []
    for base, g in video_groups.items():
        title, year = parse_title_year(base)
        if title and year:
            g["title"] = title
            g["year"] = year
            parsed[f"{title} ({year})"].append(g)
        else:
            unparseable.append(g)

    # Step 4: Analyze existing directories
    dir_info = []
    for d in actual_dirs:
        path = os.path.join(root, d)
        try:
            contents = os.listdir(path)
        except OSError:
            contents = []
        title, year = parse_title_year(d)
        clean = bool(re.search(r"\([12][09]\d{2}\)$", d))
        info = {
            "dir": d,
            "title": title,
            "year": year,
            "title_year": f"{title} ({year})" if title and year else None,
            "is_clean_name": clean,
            "is_collection_hint": looks_like_collection(d),
            "item_count": len(contents),
            "is_empty": len(contents) == 0,
            "contents_sample": contents[:5],
        }
        dir_info.append(info)

    # Step 5: Categorize
    # We'll fill `category` on each item:
    #   A — loose movie that should land in a per-movie folder
    #   B — messy folder, needs rename
    #   C — multi-version loose movies
    #   D — collection folder
    #   E — orphan asset
    #   G — empty folder
    #   H — unparseable loose video

    # Build dir lookup by title_year and by fuzzy-normalized name
    dirs_by_title_year = {}
    dirs_by_fuzzy_name = {}
    for info in dir_info:
        if info["title_year"]:
            dirs_by_title_year.setdefault(info["title_year"], []).append(info["dir"])
        dirs_by_fuzzy_name[normalize_for_match(info["dir"])] = info["dir"]

    # Cat A & C
    cat_A = []
    cat_C = []
    for ty, group in sorted(parsed.items()):
        if len(group) > 1:
            cat_C.append({
                "title_year": ty,
                "versions": [g["video"] for g in group],
                "all_files": _all_files_for_group(group),
            })
            continue
        g = group[0]
        target = dirs_by_title_year.get(ty, [None])[0]
        if not target:
            # fuzzy
            fuzzy = dirs_by_fuzzy_name.get(normalize_for_match(ty))
            target = fuzzy
        cat_A.append({
            "title_year": ty,
            "video": g["video"],
            "video_base": g["video_base"],
            "companions": g["companions"],
            "nfo": g["nfo"],
            "bif": g["bif"],
            "trickplay": g["trickplay"],
            "existing_target_dir": target,
        })

    # Cat B, D, G
    cat_B = []
    cat_D = []
    cat_G = []
    cat_F_no_year_dirs = []
    for info in dir_info:
        if info["is_empty"]:
            cat_G.append(info)
            continue
        if info["is_collection_hint"]:
            cat_D.append(info)
            continue
        if not info["title_year"]:
            cat_F_no_year_dirs.append(info)
            continue
        if info["is_clean_name"]:
            # Already correctly named — no action needed
            continue
        cat_B.append({
            "from": info["dir"],
            "to": info["title_year"],
            "item_count": info["item_count"],
        })

    # Cat E (orphan assets)
    cat_E = unmatched_files

    # Cat H (unparseable videos)
    cat_H = [{
        "video": g["video"],
        "companions": g["companions"],
        "nfo": g["nfo"],
        "trickplay": g["trickplay"],
    } for g in unparseable]

    # Detect Cat B internal conflicts (two folders → same target)
    b_targets = defaultdict(list)
    for b in cat_B:
        b_targets[b["to"]].append(b["from"])
    cat_F_conflicts = []
    for target, sources in b_targets.items():
        if len(sources) > 1:
            cat_F_conflicts.append({
                "target": target,
                "sources": sources,
                "reason": f"{len(sources)} folders would rename to '{target}'",
            })
    cat_B = [b for b in cat_B if b["to"] not in {c["target"] for c in cat_F_conflicts}]

    return {
        "root": root,
        "stats": {
            "total_entries": len(entries),
            "files": len(files),
            "dirs": len(dirs),
            "actual_dirs": len(actual_dirs),
            "trickplay_dirs": len(trickplay_dirs),
            "loose_videos": len([n for n in files if is_video(n)]),
            "parsed_groups": len(parsed),
            "multi_version_groups": len([g for g in parsed.values() if len(g) > 1]),
        },
        "category_A_loose_movies": cat_A,
        "category_B_folder_renames": cat_B,
        "category_C_multi_version": cat_C,
        "category_D_collections": cat_D,
        "category_E_orphan_assets": cat_E,
        "category_F_conflicts": cat_F_conflicts + cat_F_no_year_dirs,
        "category_G_empty_dirs": cat_G,
        "category_H_unparseable_videos": cat_H,
        "unmatched_trickplay_dirs": unmatched_trickplay,
    }


def _all_files_for_group(group):
    out = []
    for g in group:
        out.append(g["video"])
        out.extend(g["companions"])
        if g["nfo"]:
            out.append(g["nfo"])
        if g["bif"]:
            out.append(g["bif"])
        if g["trickplay"]:
            out.append(g["trickplay"])
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", help="Movie library root directory")
    p.add_argument("--out", default=None,
                   help="Output JSON file (default: stdout)")
    args = p.parse_args()

    data = inventory(args.root)

    out_json = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_json)
        print(f"Inventory written to {args.out}", file=sys.stderr)
        print("Summary:", file=sys.stderr)
        for k, v in data["stats"].items():
            print(f"  {k}: {v}", file=sys.stderr)
        print(f"  Cat A loose movies: {len(data['category_A_loose_movies'])}", file=sys.stderr)
        print(f"  Cat B folder renames: {len(data['category_B_folder_renames'])}", file=sys.stderr)
        print(f"  Cat C multi-version: {len(data['category_C_multi_version'])}", file=sys.stderr)
        print(f"  Cat D collections: {len(data['category_D_collections'])}", file=sys.stderr)
        print(f"  Cat E orphans: {len(data['category_E_orphan_assets'])}", file=sys.stderr)
        print(f"  Cat F conflicts: {len(data['category_F_conflicts'])}", file=sys.stderr)
        print(f"  Cat G empty dirs: {len(data['category_G_empty_dirs'])}", file=sys.stderr)
        print(f"  Cat H unparseable: {len(data['category_H_unparseable_videos'])}", file=sys.stderr)
    else:
        print(out_json)


if __name__ == "__main__":
    main()
