#!/usr/bin/env python3
"""Generate an execution plan from an inventory JSON file.

The plan is the structured list of filesystem operations needed to move from
the current state to a Firecore-organized layout. Operations are tagged by
category and policy.

Usage:
    python3 plan.py <inventory.json> --out plan.json \
      [--rename-inside-cat-a] [--rename-inside-cat-b] \
      [--combine-multi-version] [--edition-tags]

Read-only — does not modify the filesystem.
"""

import argparse
import json
import os
import re
import sys


ASSET_SUFFIXES = [
    "-backdrop.jpg", "-landscape.jpg", "-logo.png", "-logo.svg",
    "-poster.jpg", "-clearlogo.png", "-fanart.jpg", "-fanart1.jpg",
    "-fanart2.jpg", "-fanart3.jpg", "-thumb.jpg", "-320-10.bif", ".srt",
]


def safe_name(s: str) -> str:
    """Strip illegal filename chars."""
    return re.sub(r'[\"\\/:|<>*?]', "", s).strip()


def derive_new_filename(orig_filename: str, orig_base: str, new_base: str):
    """Compute the renamed-inside-folder name for a file.

    Strips a known asset suffix or .nfo/.bif/.trickplay/video ext from
    orig_filename, then replaces orig_base with new_base.
    Returns the new filename, or None if no rule matched (leave original).
    """
    for suf in ASSET_SUFFIXES:
        if orig_filename == orig_base + suf:
            return new_base + suf
    if orig_filename == orig_base + ".nfo":
        return new_base + ".nfo"
    if orig_filename == orig_base + ".bif":
        return new_base + ".bif"
    if orig_filename == orig_base + ".trickplay":
        return new_base + ".trickplay"
    name, ext = os.path.splitext(orig_filename)
    if name == orig_base:
        return new_base + ext
    return None


def build_plan(inv: dict, opts: dict) -> dict:
    plan = {
        "root": inv["root"],
        "options": opts,
        "operations": [],
        "parked": {
            "category_C": [],
            "category_D": [],
            "category_E": [],
            "category_F": [],
            "category_G": [],
            "category_H": [],
        },
    }

    # Map from Cat B "from" → "to" so Cat A can resolve targets that get renamed
    b_map = {b["from"]: safe_name(b["to"]) for b in inv["category_B_folder_renames"]}

    # Cat B: folder renames go first
    for b in inv["category_B_folder_renames"]:
        plan["operations"].append({
            "op": "rename_dir",
            "src": b["from"],
            "dst": safe_name(b["to"]),
            "category": "B",
            "item_count": b.get("item_count"),
        })

    # Cat A: move loose movies into per-movie folders
    for a in inv["category_A_loose_movies"]:
        ty = safe_name(a["title_year"])
        # Resolve target folder: if existing_target_dir is a Cat B source,
        # use the renamed name; otherwise use the existing or new.
        existing = a["existing_target_dir"]
        if existing and existing in b_map:
            target = b_map[existing]
        elif existing:
            target = existing
        else:
            target = ty
            plan["operations"].append({
                "op": "mkdir_if_absent",
                "path": target,
                "category": "A",
            })

        # Determine inner names
        orig_base = a["video_base"]
        new_base = ty if opts.get("rename_inside_cat_a") else orig_base

        files = [a["video"]] + list(a["companions"])
        if a["nfo"]:
            files.append(a["nfo"])
        if a["bif"]:
            files.append(a["bif"])
        if a["trickplay"]:
            files.append(a["trickplay"])

        for f in files:
            if opts.get("rename_inside_cat_a"):
                new_name = derive_new_filename(f, orig_base, new_base) or f
            else:
                new_name = f
            plan["operations"].append({
                "op": "move",
                "src": f,
                "dst": f"{target}/{new_name}",
                "category": "A",
                "title_year": ty,
            })

    # Cat C: multi-version
    if opts.get("combine_multi_version"):
        for c in inv["category_C_multi_version"]:
            ty = safe_name(c["title_year"])
            plan["operations"].append({
                "op": "mkdir_if_absent",
                "path": ty,
                "category": "C",
            })
            for f in c["all_files"]:
                # Keep release name to avoid collisions
                plan["operations"].append({
                    "op": "move",
                    "src": f,
                    "dst": f"{ty}/{f}",
                    "category": "C",
                    "title_year": ty,
                })
    else:
        plan["parked"]["category_C"] = inv["category_C_multi_version"]

    # Park everything else
    plan["parked"]["category_D"] = inv["category_D_collections"]
    plan["parked"]["category_E"] = inv["category_E_orphan_assets"]
    plan["parked"]["category_F"] = inv["category_F_conflicts"]
    plan["parked"]["category_G"] = inv["category_G_empty_dirs"]
    plan["parked"]["category_H"] = inv["category_H_unparseable_videos"]

    return plan


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("inventory", help="inventory.json path")
    p.add_argument("--out", default="plan.json", help="output plan JSON")
    p.add_argument("--rename-inside-cat-a", action="store_true",
                   help="Inside new Cat A folders, rename files to 'Title (YYYY).ext'")
    p.add_argument("--rename-inside-cat-b", action="store_true",
                   help="(reserved) inside Cat B folders, rename files too. Default off — risky.")
    p.add_argument("--combine-multi-version", action="store_true",
                   help="Combine Cat C multi-version movies into one folder per movie")
    p.add_argument("--edition-tags", action="store_true",
                   help="(reserved) for Cat C, use {edition-...} tags for inner files")
    args = p.parse_args()

    with open(args.inventory, encoding="utf-8") as f:
        inv = json.load(f)

    opts = {
        "rename_inside_cat_a": args.rename_inside_cat_a,
        "rename_inside_cat_b": args.rename_inside_cat_b,
        "combine_multi_version": args.combine_multi_version,
        "edition_tags": args.edition_tags,
    }
    plan = build_plan(inv, opts)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    # Summary
    ops_by_cat = {}
    for op in plan["operations"]:
        cat = op.get("category", "?")
        ops_by_cat[cat] = ops_by_cat.get(cat, 0) + 1
    print(f"Plan written to {args.out}", file=sys.stderr)
    print(f"Total operations: {len(plan['operations'])}", file=sys.stderr)
    for cat, n in sorted(ops_by_cat.items()):
        print(f"  Category {cat}: {n} ops", file=sys.stderr)
    print("Parked:", file=sys.stderr)
    for k, v in plan["parked"].items():
        print(f"  {k}: {len(v)} items", file=sys.stderr)


if __name__ == "__main__":
    main()
