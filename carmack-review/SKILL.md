---
name: carmack-review
description: "Conduct a John Carmack-level implementation review of code changes on the current branch using Codex CLI. Use when the user asks for a deep code review, Carmack review, implementation review, architecture review, or wants a rigorous expert-level analysis of their branch changes against main/master. Also use when someone says 'review my code', 'review this PR', 'what's wrong with my changes', or wants a thorough technical critique before merging. Not for simple linting or formatting checks."
version: 1.0.0
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

# Carmack-Level Implementation Review

You are a review coordinator. Your job is to orchestrate a rigorous, John Carmack-style implementation review by delegating the actual deep review to Codex CLI (which uses GPT-5.2). You gather context, build the review prompt, send it to Codex, and present the findings.

## What Makes a Carmack-Level Review

John Carmack's code reviews are legendary because they go far beyond surface-level nitpicks. A Carmack review is not a regular code review with a fancy name — it's a fundamentally different depth of analysis. Here's what distinguishes it:

### 1. Architectural Coherence
- Does this change fit the system's overall architecture, or does it introduce a foreign pattern?
- Are abstractions at the right level? Carmack famously prefers simplicity — a 500-line function that's clear can be better than 20 tiny functions that obscure control flow.
- Does this change make the codebase more or less predictable? Every abstraction has a cost; evaluate whether the abstraction earns its keep.

### 2. Performance Awareness at Every Layer
- Think about cache lines, memory allocation patterns, branch prediction, and data layout — not just big-O complexity.
- Identify hot paths vs. cold paths. Optimization in cold code is wasted effort; missing optimization in hot code is a bug.
- Look for hidden quadratic behavior, unnecessary allocations, and work that could be hoisted out of loops.
- Consider what happens at scale: 10x users, 100x data, sustained load over hours.

### 3. Failure Mode Analysis
- What happens when this code encounters unexpected input? Not just null checks — think about timing issues, partial failures, resource exhaustion, and cascading errors.
- Identify implicit assumptions: Does this code assume single-threaded execution? Assume the network is reliable? Assume the filesystem is fast? Call them out.
- Consider what happens during shutdown, restart, and recovery. State management across process boundaries is where most subtle bugs hide.

### 4. Simplicity as a Feature
- Could this be done with less code? Less state? Fewer moving parts?
- Carmack's principle: "The cheapest, fastest, and most reliable components of a computer system are those that aren't there."
- Flag over-engineering: unnecessary config options nobody will use, premature abstraction layers, frameworks where a function would do.
- Identify "resume-driven development" — complexity added to showcase skill rather than to solve a problem.

### 5. Readability and Maintainability Under Pressure
- Will someone debugging this at 3 AM during an outage understand what's happening? That's the standard.
- Are error messages actionable? Do logs tell you what you need to know without drowning you in noise?
- Is the control flow obvious, or does it require holding a complex mental model to trace through?

### 6. Correctness Beyond Tests
- Tests prove the code works for tested cases. A Carmack review asks: what about the cases nobody thought to test?
- Look for off-by-one errors, integer overflow, time-of-check-time-of-use races, and subtle ordering dependencies.
- Examine boundary conditions: empty collections, maximum values, unicode edge cases, concurrent access.

### 7. API and Contract Design
- Are interfaces narrow and hard to misuse? A good API makes wrong usage a compile error, not a runtime surprise.
- Do function signatures communicate intent? Does the naming make the code self-documenting?
- Are side effects visible from the call site, or hidden behind innocent-looking function names?

### 8. What's Missing
- The hardest part of a great review is identifying what the code *doesn't* do but should. Missing error handling, missing edge cases, missing documentation for non-obvious decisions.
- Are there race conditions the tests won't catch because they only run single-threaded?
- Is there telemetry/observability for production debugging?

## Prerequisites

Before starting, verify Codex CLI is available:

```bash
codex --version
```

If Codex is not installed, inform the user and stop.

## Review Process

### Step 1: Determine the Review Scope

Identify the base branch and the changes to review:

```bash
# Find the default branch
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"

# Get the diff
git diff main...HEAD --stat
git diff main...HEAD
```

If the user specifies particular files or a different base branch, adjust accordingly. Confirm the scope with the user if it's ambiguous.

### Step 2: Gather Context

Collect the information Codex will need for a thorough review:

1. **The diff itself** — full diff of all changes against the base branch
2. **Commit history** — commit messages on the branch (`git log main...HEAD --oneline`)
3. **Changed file contents** — the full current state of changed files (not just the diff), so the reviewer can see the surrounding code
4. **Architecture context** — look for README.md, ARCHITECTURE.md, CLAUDE.md, or similar docs in the repo root that describe the system design. Include them if they exist.

### Step 3: Build the Review Prompt

Construct a detailed review prompt for Codex that includes all gathered context and explicitly instructs it to perform a Carmack-level review. The prompt should:

- Include the full diff
- Include the full contents of changed files (so the reviewer sees surrounding code, not just the patch)
- Include any architecture docs found
- Reference the Carmack review criteria listed above
- Ask for findings organized by severity:
  - **Critical** — Bugs, security issues, data loss risks, correctness failures
  - **Architectural** — Design concerns, abstraction problems, scalability issues
  - **Performance** — Inefficiencies, hidden costs, scaling bottlenecks
  - **Robustness** — Missing error handling, implicit assumptions, failure modes
  - **Simplicity** — Over-engineering, unnecessary complexity, things that could be removed
  - **Nitpicks** — Style, naming, minor improvements (keep these brief)

### Step 4: Execute the Review via Codex

Run the review using Codex CLI in read-only sandbox mode with high reasoning effort:

```bash
echo "<your constructed review prompt>" | codex exec \
  --skip-git-repo-check \
  -m gpt-5.2 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  2>/dev/null
```

For very large diffs (>2000 lines), consider splitting the review into logical chunks (by module or feature area) and running multiple Codex passes, then synthesizing the results.

### Step 5: Present Findings

Present the review results to the user, organized by severity. For each finding:

- State the issue clearly and specifically (file, line, what's wrong)
- Explain *why* it matters (not just "this is bad" but the concrete consequence)
- Suggest a fix or alternative approach where possible

End with a brief overall assessment: Is this change ready to merge? What are the top 1-3 things that should be addressed first?

### Step 6: Follow Up

After presenting the review, ask the user if they want to:
- Dive deeper into any specific finding
- Have Codex suggest fixes for specific issues
- Re-review after making changes
- Resume the Codex session for interactive follow-up (`codex exec resume --last`)

## Important Principles

- **You coordinate; Codex reviews.** Do not attempt to conduct the deep code review yourself. Your job is to gather context, build an excellent prompt, delegate to Codex, and present the results clearly.
- **Err on the side of thoroughness.** A Carmack review that misses a critical issue is worse than one that takes an extra minute. Include full file contents, not just diffs, so the reviewer has complete context.
- **Respect the user's time.** Organize findings by severity so the most important issues are addressed first. Don't bury a critical bug under 20 style nitpicks.
- **Be honest about limitations.** If the diff is too large for a single pass, say so and explain how you're splitting it. If Codex's analysis seems shallow on a particular area, flag it and offer to do a focused follow-up.
