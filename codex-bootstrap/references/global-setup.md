# Global Codex defaults at `~/.codex/AGENTS.md`

Codex reads `AGENTS.md` walking from `~/.codex/AGENTS.md` down through the repo to the current working directory. Files closer to the cwd override earlier ones.

Use `~/.codex/AGENTS.md` for **personal defaults** that apply to every project — preferences about diff size, dependency policy, secret handling, communication style. Anything you'd want Codex to follow regardless of which repo you're in.

## Why this skill doesn't create it

The global file is a personal layer that should reflect your actual cross-project preferences. Scaffolding it from a template would either ship preferences you don't agree with, or ship an empty file you'd have to fill in anyway. Better to write it yourself once and reuse it across every repo.

## Example global file

```bash
mkdir -p ~/.codex
```

Then create `~/.codex/AGENTS.md`:

```md
# ~/.codex/AGENTS.md

## Personal Codex defaults

- Prefer small, reviewable diffs.
- Do not add production dependencies without explicit approval.
- Explain failed commands plainly, including the exit code and the relevant stderr line.
- Never store secrets, credentials, or tokens in memory files.
- When unsure, ask before making destructive changes (rm, git reset --hard, force push, schema migrations).
```

Adjust to your actual preferences. Things to consider:

- **Diff size** — do you want one large PR or many small ones?
- **Dependencies** — can Codex add new packages, or only when you approve?
- **Tests** — should Codex always run tests, even for tiny changes?
- **Communication** — terse status updates, or detailed explanations?
- **Risk** — should Codex stop and ask before destructive operations?

## Precedence order

Codex merges these from least to most specific. Later files override earlier ones where they conflict:

```
~/.codex/AGENTS.md            # personal defaults for every repo
<repo>/AGENTS.md              # shared instructions for this project
<repo>/<subdir>/AGENTS.md     # specialized rules for one service/module
```

This lets each layer focus on what it should:

- Your global file: personal preferences that travel with you.
- The repo's file: the team's shared agreement about the project.
- A subdir file: rules for one specific service when the repo is a monorepo.

Mixing layers (e.g., putting personal preferences in the repo file) causes friction when you switch repos or hand off work to another contributor.
