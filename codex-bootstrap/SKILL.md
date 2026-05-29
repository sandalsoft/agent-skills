---
name: codex-bootstrap
description: Bootstrap a new project for OpenAI Codex by scaffolding AGENTS.md instructions, .codex/agent-memory.md persistent memory, and lifecycle hooks (SessionStart + Stop) that enforce the memory protocol. Use whenever the user wants to set up Codex in a repo, mentions AGENTS.md, asks to add Codex memory or hooks, says "configure Codex for this project", or wants Codex to maintain durable project learnings across sessions. Triggers on phrases like "bootstrap Codex", "set up Codex in this repo", "create AGENTS.md", "add Codex memory", "Codex hooks", "Codex project memory", "configure Codex for X", or any request to make a repository Codex-ready. Run this skill even if the user doesn't explicitly say "AGENTS.md" — any setup intent for Codex should trigger it.
---

# Codex Bootstrap

Scaffold a repo for OpenAI Codex with the durable-memory pattern: stable instructions in `AGENTS.md`, mutable learnings in `.codex/agent-memory.md`, and lifecycle hooks that load memory at session start and enforce the memory-update protocol at session stop.

## Why this pattern

Codex reads `AGENTS.md` at the start of every task, walking from `~/.codex/AGENTS.md` (global) down to the current working directory. Files closer to the cwd override earlier ones. That's the right place for **stable** project instructions.

Memory belongs in a separate file because instructions and learnings have different lifecycles. `AGENTS.md` should rarely change once stable; `.codex/agent-memory.md` should accrue durable findings (working commands, gotchas, test quirks, architecture decisions) as Codex works.

Hooks make the pattern enforceable rather than aspirational. Without them, Codex may skip the memory step under pressure. `SessionStart` loads the memory file as developer context at the start of every session, and `Stop` blocks task completion until Codex either reports an update or confirms there were no durable findings.

## Inputs to gather before scaffolding

Ask the user before writing anything:

1. **Target repo path** — confirm `pwd` is the repo root. If `git rev-parse --show-toplevel` differs, ask which path they want. The hooks rely on `git rev-parse` to locate the root, so a non-git directory is workable but worth flagging.

2. **Version control for `.codex/agent-memory.md`** — commit it (shared with the team, available in fresh clones) or gitignore it (personal, doesn't affect other contributors). Default recommendation: commit it, but keep entries focused on shared project facts. See `references/version-control.md` for the tradeoffs and the shared/local split pattern.

3. **Existing files** — if `AGENTS.md` or `.codex/` already exist, never silently overwrite. Show the user what's there and ask whether to merge, overwrite specific files, or abort.

## Files this skill creates

All paths relative to the repo root:

- `AGENTS.md` — stable instructions with the memory protocol
- `.codex/agent-memory.md` — memory template with empty section headers
- `.codex/config.toml` — enables Codex hooks
- `.codex/hooks/session_start_memory.py` — loads memory at session start
- `.codex/hooks/stop_memory_check.py` — enforces memory update at session stop

## Scaffolding steps

1. **Verify repo state**

   Run `git rev-parse --show-toplevel` to confirm a git repo. If it fails, ask the user whether to proceed. The hooks will still work if `git` is installed and the user is inside any directory — they call `git rev-parse` to find the root — but a non-repo directory is unusual and worth confirming.

2. **Check for conflicts**

   Run `ls AGENTS.md .codex 2>/dev/null` (or equivalent). If anything exists, surface it and ask before proceeding. Don't clobber a hand-written `AGENTS.md`.

3. **Write files from `assets/`**

   Read each template from `assets/` and write to the corresponding destination. Use Read + Write rather than `cp` — that way the contents are visible in the conversation and the user can spot anything they want to tweak before it lands on disk.

   Destinations (in order):
   - `assets/AGENTS.md` → `<repo>/AGENTS.md`
   - `assets/agent-memory.md` → `<repo>/.codex/agent-memory.md`
   - `assets/config.toml` → `<repo>/.codex/config.toml`
   - `assets/session_start_memory.py` → `<repo>/.codex/hooks/session_start_memory.py`
   - `assets/stop_memory_check.py` → `<repo>/.codex/hooks/stop_memory_check.py`

4. **Make hooks executable**

   ```bash
   chmod +x <repo>/.codex/hooks/session_start_memory.py <repo>/.codex/hooks/stop_memory_check.py
   ```

   Without this, Codex will try to run the hooks and they'll fail with a permission error. The `config.toml` invokes them via `python3 <path>`, so technically the executable bit isn't strictly required — but setting it removes one class of confusion if anyone runs the scripts directly.

5. **Apply version control choice**

   - **Committing memory** (default): nothing extra. The file is tracked.
   - **Gitignoring memory**: append `.codex/agent-memory.md` to `.gitignore` (create `.gitignore` if it doesn't exist). The hook scripts and `config.toml` should still be committed — those are shared infrastructure.

6. **Print a summary**

   Tell the user what was created, what to do next, and any caveats. Useful next steps to mention:
   - Codex must trust the project for repo-local hooks to load. The first time Codex runs in this directory, it'll ask.
   - Edit `AGENTS.md` to add repo-specific commands (e.g., `pnpm test`, `cargo check`) — the scaffolded version only contains the memory protocol and a generic verification section.
   - The "Project facts" section of `agent-memory.md` is the only one worth pre-filling manually; the rest should accumulate naturally as Codex works.

## After scaffolding

Don't pre-fill the memory file's body sections. Empty section headers are deliberate prompts for Codex to recognize which kinds of findings belong where. Pre-filling them with examples primes Codex to overwrite or mimic those entries, which defeats the purpose.

If the user asks about layered memory (shared + personal), point them to `references/version-control.md` for the `agent-memory.local.md` split pattern.

If the user asks about global defaults across all their repos, point them to `references/global-setup.md` for the `~/.codex/AGENTS.md` pattern. This skill deliberately doesn't touch the global file — that's a personal layer the user should write themselves so it reflects their actual cross-project preferences.

## Reference files

- `references/version-control.md` — committed vs gitignored memory, and the shared/local split pattern
- `references/global-setup.md` — `~/.codex/AGENTS.md` for personal defaults across every repo
- `assets/` — the literal file templates this skill writes to the target repo
