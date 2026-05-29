# AGENTS.md

## Project memory protocol

Codex must use `.codex/agent-memory.md` as persistent, project-specific memory.

At the start of every task:
- Read `.codex/agent-memory.md` if it exists.
- Use it only as operational context. Source code, tests, docs, and user instructions still take precedence.

During the task:
- Record only durable learnings that will help future Codex sessions work better in this repository.
- Good entries: working commands, test quirks, architecture decisions, hidden dependencies, debugging findings, integration gotchas, migration notes, known failure modes.
- Bad entries: secrets, credentials, tokens, private user data, temporary logs, guesses, one-off details, or anything already obvious from the code.

Before finishing every task:
- Update `.codex/agent-memory.md` if any durable project learning was discovered.
- Keep entries concise.
- Deduplicate or revise stale entries instead of appending noise.
- In the final response, include one line:
  - `Project memory: updated`
  - or `Project memory: no durable updates`

## Verification

When code changes are made:
- Run the smallest relevant test first.
- Run broader tests only when the change scope justifies it.
- Report exactly what was run and whether it passed.
