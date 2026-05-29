#!/usr/bin/env python3

import json
import pathlib
import subprocess
import sys


MAX_CHARS = 12000


def repo_root(cwd: pathlib.Path) -> pathlib.Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return pathlib.Path(out)
    except Exception:
        return cwd


def main() -> None:
    payload = json.load(sys.stdin)
    cwd = pathlib.Path(payload.get("cwd") or ".").resolve()
    root = repo_root(cwd)

    memory_path = root / ".codex" / "agent-memory.md"
    if not memory_path.exists():
        return

    text = memory_path.read_text(encoding="utf-8").strip()
    if not text:
        return

    if len(text) > MAX_CHARS:
        text = text[-MAX_CHARS:]

    print(
        "# Project memory loaded from .codex/agent-memory.md\n\n"
        + text
    )


if __name__ == "__main__":
    main()
