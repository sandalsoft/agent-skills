---
name: interview
description: >
  Coding-focused Socratic interview that transforms a feature idea into an
  implementation-ready spec. Reads the codebase first, then asks questions
  grounded in actual code, patterns, and constraints. Use when the user has a
  feature request, bug to design a fix for, refactoring idea, or system change
  they want to think through before coding. Triggers on "interview me about",
  "help me think through", "I want to add...", "flesh out this feature",
  "what should I consider for...", or any description of a code change that
  hasn't been fully planned. Also triggers on vague requests like "I'm thinking
  about adding..." or "what if we changed...". The interview surfaces blind
  spots in the design, challenges architectural assumptions, and produces a spec
  that's ready to hand off to a planner or implement directly.
disable-model-invocation: true
---

# Interview

Turn a feature idea into an implementation-ready spec by reading the codebase first and asking questions that only someone who understands the code would think to ask.

The difference between this and a generic interview: every question is grounded in what actually exists. Instead of "what's your auth strategy?" you ask "I see you're using JWT middleware in `src/auth/`. Should this new endpoint go through the same flow, or does it need different permissions?" The codebase is the context. The interview fills in the gaps the code can't answer.

## How It Works

```
Intake → Investigate Codebase → Interview Loop → Challenge → Crystallize
```

### Arguments

`$ARGUMENTS` contains the user's feature idea or description. If empty, ask what they want to build.

Depth flags:
- `--quick` — 3-5 rounds. Good for small features, bug fixes, config changes.
- `--deep` — Up to 15 rounds. Good for new systems, architectural changes, cross-cutting concerns.
- Default is 6-10 rounds. Adapt based on how many files the change touches.

---

## Phase 1: Intake

Read `$ARGUMENTS`. Before touching the codebase:

1. **Form a hypothesis** about what this change actually requires — the user's description often understates the blast radius
2. **Identify what you need to learn from the code** — which directories, patterns, and integration points to check
3. **Gauge the scope** — is this a one-file change, a multi-module feature, or an architectural shift?

Give a brief acknowledgment (2-3 sentences) that shows you understood the idea and hints at the complexity you suspect. Don't parrot. Show insight.

Example: "Adding real-time notifications to the dashboard. That's going to touch the event system, the WebSocket layer, and the frontend state management. Let me look at how those pieces fit together before I start asking questions."

## Phase 2: Investigate Codebase

This phase is mandatory, not optional. Read the code before asking a single question.

### What to investigate

1. **Project structure and conventions** — Read CLAUDE.md if it exists. Scan the directory layout. Understand the module boundaries.
2. **Related code paths** — Find the files most likely to be touched by this change. Read them. Understand the current patterns.
3. **Data model** — Check schemas, types, database migrations. Understand what data exists and how it flows.
4. **Test patterns** — Look at existing tests near the change area. Note the testing style, frameworks, and coverage patterns.
5. **Recent git history** — Check `git log` for the relevant area. Someone may have recently changed these files or tried something similar.
6. **Dependencies and integrations** — What does this area talk to? External APIs, other services, shared libraries?

### What to look for

- Patterns this change should follow (or deliberately break)
- Constraints the user might not know about (e.g., a shared interface that other consumers depend on)
- Existing utilities or abstractions that could be reused
- Landmines — code that looks simple but has hidden complexity (concurrent access, caching, error handling)

**Document what you found.** Before the first question, share a brief summary (4-6 bullet points) of what you learned from the codebase. This builds trust and shows the user you're not asking from ignorance.

Example: "Here's what I found in the codebase:
- Events use a pub/sub pattern in `src/events/bus.ts` — custom EventEmitter subclass, no external library
- The dashboard is SvelteKit with server-sent events for live data (`src/routes/dashboard/+page.server.ts`)
- User preferences are in PostgreSQL, but notification settings don't exist yet — there's no `notification_preferences` table
- Tests in this area use Vitest with a real database (no mocks), fixtures in `tests/fixtures/`
- The last change to the event bus was 3 weeks ago — added a `priority` field to events"

## Phase 3: Interview Loop

Now ask questions — but every question should reflect what you learned from the code. Don't ask things you could have answered by reading files.

### Rules

1. **Use `AskUserQuestion` for every question.** Never dump questions as text. The tool gives structure and lets the user respond precisely.

2. **1-3 questions per round.** Group related questions. Don't overwhelm.

3. **One concept per question.** Split compound questions.

4. **Reference the code.** "I see `OrderService.process()` handles both new orders and modifications. Should this notification fire for both, or just new orders?" is 10x better than "When should notifications fire?"

5. **No questions you could answer from the code.** If the test framework is Vitest, don't ask what test framework to use. If routes follow a pattern, don't ask about the URL structure. Use the code as evidence and ask about the *decisions* the code doesn't capture.

6. **Follow the thread.** Build on previous answers. If the user says something that contradicts what you see in the code, surface it immediately.

7. **Provide options grounded in the codebase.** "I see two patterns for this: the `OrderService` approach (separate handler per event) or the `NotificationService` approach (single dispatcher). Which fits better here?" Always include your recommendation.

8. **Show observations between rounds.** Brief insight that contextualizes the next question. "The event bus doesn't have backpressure. If this notification triggers on every order update, that could be thousands per minute during peak."

### What to Ask About

Pull from `references/question-bank.md` for the full catalog, but prioritize based on what the code reveals:

**Always explore (early rounds):**
- Intent behind the change — what behavior should be different when this ships?
- Scope boundaries — which of the things this *could* do should it actually do in v1?
- User-facing behavior — what does the user see, click, or experience differently?

**Explore based on what the code reveals (middle rounds):**
- Data model changes — new tables, columns, migrations, backwards compatibility
- API contract changes — new endpoints, modified responses, versioning
- State management — where does new state live, who owns it, how does it get invalidated
- Error handling — what happens when the new code path fails? How does the user know?
- Side effects — what else gets triggered? Queue jobs, webhooks, cache invalidation, audit logs?

**Explore when the change warrants it (later rounds):**
- Migration strategy — can this deploy without downtime? What about existing data?
- Performance implications — does this change a hot path? Add a query to a loop?
- Security surface — new inputs, new permissions, new data exposure?
- Testing strategy — what tests are needed, what fixtures, what edge cases?
- Rollback plan — if this goes wrong, how do you undo it?

### Tracking Clarity

Internally track clarity across these dimensions (0-100%):

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Behavior | 25% | What changes for the user, concretely |
| Scope | 20% | What's in, out, and deferred |
| Data Model | 20% | Schema changes, migrations, data flow |
| Integration | 15% | How this connects to existing code |
| Edge Cases | 10% | Failure modes, error states, concurrent access |
| Verification | 10% | How you'd test and validate this works |

Show progress every 2-3 rounds: "We've nailed the user-facing behavior and scope. The gaps are around error handling and how to migrate existing data."

**Ready to wrap** when clarity hits ~80% or the user says they've heard enough.

## Phase 4: Challenge

Stress-test the design with code-aware challenges. Pick 1-2:

**Simpler Alternative** — "Could this be a configuration change instead of a feature? I see `config/features.ts` already has toggle support." or "What if you just added a column to the existing `orders` table instead of creating a `notifications` model?"

**Blast Radius Check** — "This changes `EventBus.emit()`, which is called from 14 places. Have you considered which of those callers will be affected?" or "The `UserService` that consumes this event is also used by the admin panel. Will this notification fire for admin actions too?"

**Scaling Question** — "Right now there are ~500 orders/day. What happens at 50,000? This pattern creates a row per notification per user."

**Migration Risk** — "There are 2M rows in the `orders` table. Adding this column with a default value will lock the table. What's the zero-downtime approach?"

Don't label these. Just ask naturally.

## Phase 5: Crystallize

Produce an implementation-ready spec. Ask the user where to save it (default: `SPEC.md` in the project root).

### Spec Format

```markdown
# [Feature Title]

## Problem
What's broken or missing today, and why it matters now.

## Goal
One sentence: what's different when this ships.

## Behavior
What the user sees and does differently. Be specific about interactions,
states, and feedback. Include before/after if helpful.

## Scope

### In Scope
- Concrete changes to ship in this iteration

### Out of Scope
- Deferred items with reasoning

## Technical Design

### Architecture
How this fits into the existing codebase. Reference actual files and
patterns. Include a diagram if helpful (Mermaid syntax).

### Files to Change
List specific files that need modification and what changes in each.
Group by module/concern.

### Data Model Changes
New tables, columns, migrations. Include SQL or schema snippets.

### API Changes
New or modified endpoints, request/response shapes.

### Key Decisions
Decisions made during the interview with rationale.
Format: **Decision**: Rationale. Reference the codebase pattern that
informed the choice.

### Open Questions
Unresolved items with current best thinking.

## Edge Cases
Specific scenarios to handle, with expected behavior for each.

## Testing Plan
What tests to write, what fixtures are needed, what to assert.
Reference existing test patterns in the codebase.

## Migration & Rollout
How to deploy safely. Data migrations, feature flags, rollback plan.

## Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
```

After writing the spec, suggest the next step: planning task breakdown, prototyping the riskiest piece, or starting implementation.

---

## Anti-Patterns

- **The generic interview.** Asking "what's your tech stack?" when you could read `package.json`. Every question should demonstrate you read the code.
- **The checklist march.** Going category by category instead of following the conversation. If the user reveals a tricky migration problem, dig into it — don't save it for "the migration section."
- **The echo chamber.** Accepting "it should be simple" when the code says otherwise. If you see complexity, name it.
- **The premature solution.** Proposing code during the interview. Understand the problem first. The spec phase is for design, not implementation.
- **The scope creep enabler.** Letting every "oh, and also..." into v1. Push back. "That sounds like a v2 concern — let's keep the scope tight."
- **The clean-room interviewer.** Asking theoretical questions when concrete codebase evidence exists. "How do you want to handle errors?" is worse than "I see `OrderService` uses `Result<T, AppError>`. Should this follow the same pattern, or does it need different error types?"
