# Version control for `.codex/agent-memory.md`

You have two reasonable choices for the memory file. Pick based on whether memory should be shared with collaborators.

## Commit it (recommended default)

Use when the memory describes the **project itself** — working commands, test quirks, architecture decisions, known gotchas. These are facts every contributor benefits from on first clone.

```bash
git add AGENTS.md .codex/
git commit -m "chore: bootstrap Codex AGENTS.md and project memory"
```

Watch for: the file growing into one developer's diary. Keep entries focused on durable facts that survive across contributors. If you find yourself adding "I was working on X today and noticed Y," that probably belongs in a personal layer (see split pattern below).

## Gitignore it

Use when memory is **personal** — your debugging notes, your preferred command sequences, scratch findings you don't want broadcast to the team. The repo still shares the hooks and `AGENTS.md`, but each contributor maintains their own memory file.

```bash
echo ".codex/agent-memory.md" >> .gitignore
```

The downside: a fresh clone has no project memory at all. New contributors lose the accumulated learnings until they build their own.

## Split pattern (when memory grows)

If the single file becomes noisy, split into shared + personal:

```
.codex/agent-memory.md          # shared, stable project facts (committed)
.codex/agent-memory.local.md    # personal/session notes (gitignored)
```

`.gitignore`:

```
.codex/agent-memory.local.md
```

Add to `AGENTS.md` so Codex reads both:

> At task start, read `.codex/agent-memory.md`. Also read `.codex/agent-memory.local.md` if it exists. Shared memory takes precedence over local memory.

This is overkill for most projects. Start with one file and only split if a single memory file becomes a problem to maintain.

## Always commit these

Regardless of which option you pick for the memory file, commit:

- `AGENTS.md` — shared project instructions
- `.codex/config.toml` — hook configuration
- `.codex/hooks/session_start_memory.py` — shared infrastructure
- `.codex/hooks/stop_memory_check.py` — shared infrastructure

These define how Codex behaves in the repo. They belong to the team, not to any one developer.
