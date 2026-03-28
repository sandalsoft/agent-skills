# Question Bank — Coding Interview

Questions organized by category. Each one is designed to be grounded in codebase context — you should have read relevant files before asking any of these. Adapt the examples to reference actual code you found.

---

## Intent & Behavior

The most important category. Understand what changes for the user before anything else.

- **What should be different when this ships?** — The concrete behavior change. "Users see a notification badge" is better than "we add notifications."
- **Walk me through the interaction.** — Step by step, what does the user do? What do they see at each step? What happens when they click?
- **What's the current workaround?** — If users are already doing this manually (or with a hack), the shape of their workaround tells you what the feature actually needs to do.
- **What triggered this now?** — A customer complaint? A scaling threshold? An upcoming launch? The trigger reveals the real priority.

## Scope & Boundaries

- **What's the v1 vs v2 cut?** — Force the split early. What's the minimum that's useful?
- **Name two things users will expect this to do that it won't.** — Surfaces scope confusion before it becomes scope creep.
- **Can this be done without building anything new?** — Configuration change? Existing library? A shell script? Sometimes the answer is "don't build it."
- **Should this be a feature flag?** — If there's uncertainty, shipping behind a flag reduces risk and lets you iterate.

## Data Model & Schema

Ask these when the change involves new or modified data.

- **What's the source of truth?** — Where does this data originate? Who writes it, who reads it? Is there a race condition between writers?
- **I see `[existing_table]` has these fields. Which of these are relevant?** — Ground the question in what exists. Don't ask users to describe their schema from memory.
- **What happens to existing rows?** — Every schema change needs a migration story. Is it additive (new column with default)? Destructive (dropping a column)? Transformative (backfilling computed data)?
- **What's the query pattern?** — How will this data be read? Single-row lookup? Filtered list? Aggregation? This determines indexing strategy.
- **Does this data have a lifecycle?** — Is it created once and read forever? Updated frequently? Does it need soft-delete? Archiving? TTL?

## API & Interface Design

- **Who calls this?** — Frontend, another service, a cron job, an external webhook? Each consumer has different expectations around latency, error handling, and authentication.
- **I see `[existing_endpoint]` follows this pattern. Should the new endpoint match?** — Consistency matters. If you're breaking the pattern, know why.
- **What's the response when things go wrong?** — Not just "return an error" — what error code, what message, what can the caller actually do about it?
- **Is this idempotent?** — Can the same request be safely retried? If not, what happens on duplicate submissions?

## Integration & Side Effects

- **What gets triggered when this happens?** — Events, webhooks, queue jobs, cache invalidation, audit logs, email notifications. Map the downstream effects.
- **I found [N] callers of `[function]`. Which are affected by this change?** — When modifying shared code, you need to know the blast radius.
- **Does this change affect the admin panel / CLI / API client?** — Other surfaces that consume the same code or data.
- **What happens if the downstream service is down?** — Retry? Queue? Fail silently? Fail loudly? Depends on the business impact.

## Error Handling & Edge Cases

- **What happens when [primary input] is missing, malformed, or enormous?** — The three failure modes every feature faces.
- **What does partial failure look like?** — Step 3 of 5 fails. What happened to steps 1 and 2? Do you roll back? Retry? Continue with a degraded result?
- **What's the concurrent access story?** — Two users editing the same thing. Two requests hitting the same endpoint. Two queue consumers processing the same job.
- **I see `[existing_code]` doesn't handle [case]. Should it?** — Finding gaps in existing error handling during investigation is high-value signal.

## Performance & Scale

Only ask when the change touches a hot path or the answer changes the design.

- **How many times per day will this run?** — One-off admin action and per-request middleware need very different designs.
- **I see this is inside [loop/query/handler]. What's the expected cardinality?** — A nested query on 10 items is fine. On 10,000 items, it's a problem.
- **Does this need to be real-time or can it be eventual?** — Async processing is almost always simpler and more reliable. Push back on "real-time" unless there's a clear user need.
- **What's the caching story?** — Read-heavy data that changes rarely is a caching candidate. But cache invalidation is where bugs live.

## Testing & Verification

- **I see tests in this area use [pattern]. Should the new tests follow the same approach?** — Match existing test conventions unless there's a reason not to.
- **What's the most important thing to test?** — Not "everything." The one scenario where a bug would be worst.
- **What fixture data do we need?** — Existing fixtures may need extension. New test scenarios may need new data.
- **How would you verify this works in production?** — Monitoring, alerts, manual smoke test, canary deployment?

## Migration & Rollout

Only ask when replacing or significantly changing existing behavior.

- **Can old and new run side by side?** — Parallel running is the safest migration strategy.
- **What's the rollback plan?** — If this breaks at 2am, what does oncall do? Revert the deploy? Flip a flag? Run a migration backward?
- **Does the database migration lock any tables?** — Large tables + column additions with defaults = downtime. Know the table sizes.
- **Who needs to know this is changing?** — Other teams consuming your API, users who'll see different behavior, oncall who needs to know what changed.

## Security

Only ask when the change introduces new inputs, permissions, or data exposure.

- **What new inputs does this accept?** — Every new input is an injection vector. What validation exists? What's missing?
- **Who should NOT be able to do this?** — Easier to think about than "who should" and more revealing.
- **Does this expose data that was previously hidden?** — New API endpoints, new fields in responses, new admin capabilities.

---

## Question Selection Heuristics

1. **Ask about what the code didn't tell you.** The codebase answers "how does it work today?" Your questions should answer "what should be different, and why?"
2. **Ask about boundaries and connections.** How this integrates with existing code. What changes ripple outward.
3. **Ask about failure before success.** Understanding how things break reveals requirements that "how does it work?" never surfaces.
4. **Reference specific files and patterns.** "I see X in Y" is always better than "how do you want to handle X?"
5. **Prefer concrete scenarios over abstract categories.** "What happens when a user submits a form while offline?" beats "How do you handle offline scenarios?"
