#!/usr/bin/env python3

import json
import sys


def main() -> None:
    payload = json.load(sys.stdin)

    if payload.get("stop_hook_active"):
        print(json.dumps({"continue": True}))
        return

    last_message = payload.get("last_assistant_message") or ""

    if "Project memory:" in last_message:
        print(json.dumps({"continue": True}))
        return

    reason = """
Before ending this task, follow the project memory protocol.

1. Read `.codex/agent-memory.md` if needed.
2. Update it only if this task produced durable project-specific learnings:
   - working commands
   - test quirks
   - architecture decisions
   - debugging findings
   - integration gotchas
   - known failure modes
3. Do not store secrets, credentials, tokens, private data, temporary logs, or guesses.
4. Then finish with either:
   - `Project memory: updated`
   - `Project memory: no durable updates`
""".strip()

    print(json.dumps({
        "decision": "block",
        "reason": reason,
    }))


if __name__ == "__main__":
    main()
