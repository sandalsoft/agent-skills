---
name: napkin
description: |
  Maintain a per-repo napkin file at `.claude/napkin.md` that tracks mistakes,
  corrections, and patterns. Activates EVERY session — read the napkin before
  doing anything and update it continuously as you work. Use when the user
  mentions "napkin", "what mistakes", "what did we learn", "track corrections",
  or when starting any new session. Also activates when you make a mistake,
  receive a correction, or discover something worth remembering. Do NOT use
  for formal documentation or changelogs — the napkin is informal working memory.
author: Codex
version: 5.1.0
date: 2026-02-06
---

# Napkin

You maintain a per-repo markdown file that tracks mistakes, corrections, and
patterns that work or don't. You read it before doing anything and update it
continuously as you work — whenever you learn something worth recording.

**This skill is always active. Every session. No trigger required.**

## Session Start: Read Your Notes

First thing, every session — read `.claude/napkin.md` before doing anything
else. Internalize what's there and apply it silently. Don't announce that you
read it. Just apply what you know.

If no napkin exists yet, create one at `.claude/napkin.md`:

```markdown
# Napkin

## Corrections
| Date | Source | What Went Wrong | What To Do Instead |
|------|--------|----------------|-------------------|

## User Preferences
- (accumulate here as you learn them)

## Patterns That Work
- (approaches that succeeded)

## Patterns That Don't Work
- (approaches that failed and why)

## Domain Notes
- (project/domain context that matters)
```

Adapt the sections to fit the repo's domain. A backend API project might add
"API Quirks" and "Migration Pitfalls." A frontend project might add "CSS Gotchas"
and "Component Patterns." Design something you can usefully consume.

## Continuous Updates

Update the napkin as you work, not just at session start and end. Write to
it whenever you learn something worth recording:

- **You hit an error and figure out why.** Log it immediately. Don't wait.
- **The user corrects you.** Log what you did and what they wanted instead.
- **You catch your own mistake.** Log it. Your mistakes count the same as
  user corrections — maybe more, because you're the one who knows what went
  wrong internally.
- **You try something and it fails.** Log the approach and why it didn't work
  so you don't repeat it.
- **You try something and it works well.** Log the pattern.
- **You re-read the napkin mid-task** because you're about to do something
  you've gotten wrong before. Good. Do this.

The napkin is a living document. Treat it like working memory that persists
across sessions, not a journal you write in once.

## What to Log

Log anything that would change your behavior if you read it next session:

- **Your own mistakes**: wrong assumptions, bad approaches, misread code,
  failed commands, incorrect fixes you had to redo.
- **User corrections**: anything the user told you to do differently.
- **Tool/environment surprises**: things about this repo, its tooling, or its
  patterns that you didn't expect.
- **Preferences**: how the user likes things done — style, structure, process.
- **What worked**: approaches that succeeded, especially non-obvious ones.

Be specific. "Made an error" is useless. "Assumed the API returns a list but
it returns a paginated object with `.items`" is actionable.

## Napkin Maintenance

Every 5-10 sessions, or when the file exceeds ~150 lines, consolidate:

- Merge redundant entries into a single rule.
- Promote repeated corrections to User Preferences.
- Remove entries that are now captured as top-level rules.
- Archive resolved or outdated notes.
- Keep total length under 200 lines of high-signal content.

A 50-line napkin of hard-won rules beats a 500-line log of raw entries.

## Example

**Early in a session** — you misread a function signature and pass args in the
wrong order. You catch it yourself. Log it:

```markdown
| 2026-02-06 | self | Passed (name, id) to createUser but signature is (id, name) | Check function signatures before calling, this codebase doesn't follow conventional arg ordering |
```

**Mid-session** — user corrects your import style. Log it:

```markdown
| 2026-02-06 | user | Used relative imports | This repo uses absolute imports from `src/` — always |
```

**Later** — you re-read the napkin before editing another file and use
absolute imports without being told. That's the loop working.

## Napkin Health Check

A healthy napkin:
- [ ] Has been read this session (you applied knowledge from it)
- [ ] Has been updated this session (you logged at least one observation)
- [ ] Is under 200 lines (consolidate if not)
- [ ] Has entries from the last 3+ sessions (not stale)
- [ ] Contains specific, actionable entries (not vague notes)

If the napkin hasn't been updated in 5+ sessions, it's either stale or you're
not logging enough. Re-read it critically and see if anything needs updating.

## Guaranteed Activation

For truly unconditional activation across every session, add this to the
project's `CLAUDE.md`:

```markdown
At the start of every session, read `.claude/napkin.md` if it exists and
apply its contents silently. Update it as you work.
```

This ensures the napkin is loaded even when the session's first prompt is
unrelated to mistake-tracking.

## Skill Evolution

### When the Napkin Approach Isn't Working
- Entries are too vague — re-read "Be specific" guidance and rewrite recent entries
- Napkin isn't being read — add the CLAUDE.md instruction above for guaranteed loading
- Too many entries accumulating — trigger consolidation earlier (every 3 sessions instead of 5-10)
- Wrong sections for this project — adapt the template sections to match the domain

### Updating This Skill
- If a new category of napkin entry emerges across multiple repos, add it to the template
- If the consolidation cadence is wrong, adjust the "every 5-10 sessions" guidance
- If the napkin format doesn't work for a specific domain, document the variant
