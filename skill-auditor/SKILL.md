---
name: skill-auditor
version: 1.0.0
description: |
  Audit skills against Anthropic's official best practices and produce graded
  reports with detailed improvement plans. Use when the user wants to review,
  audit, evaluate, grade, or assess the quality of their skills — whether a
  single skill, a batch of skills, or their entire skill portfolio. Also use
  when the user asks "are my skills any good?", "which skills need updating?",
  "audit my skills", "review this skill", "grade my skills", or wants to
  prioritize which skills to improve first. Covers structure, triggering,
  content quality, self-evaluation, evals, and self-improvement mechanisms.
  Produces actionable reports, not just scores.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
---

# Skill Auditor

Evaluate skills against Anthropic's published best practices and produce graded reports with concrete improvement plans. The goal isn't just to score — it's to tell you exactly what to fix and in what order.

## When to Use This vs. skill-judge

**skill-judge** evaluates design quality theory — knowledge delta, freedom calibration, pattern recognition. It answers: "Is this a well-designed skill?"

**skill-auditor** evaluates against Anthropic's practical standards — structure, triggering, evals, self-improvement. It answers: "Does this skill follow current best practices, and what specifically needs to change?"

Use both for a complete picture. Use this one when you want actionable improvement plans.

---

## Audit Process

### Step 1: Discover Skills

Find all skills to audit. The user may specify a single skill, a list, or ask for a full portfolio audit.

**Single skill:**
```
Read the SKILL.md and all files in the skill directory.
```

**Portfolio audit:**
```
Search these locations for skills:
- ~/.claude/skills/
- ~/.agents/skills/
- ~/.claude/repo-template/skills/
- Project-local .claude/skills/ directories
- Any symlinked skill directories
```

For each skill found, record: name, path, file count, SKILL.md line count.

### Step 2: Read the Grading Rubric

Read `references/grading-rubric.md` for the full scoring criteria. It defines six dimensions:

| # | Dimension | Weight | What It Measures |
|---|-----------|--------|------------------|
| 1 | Structure & Progressive Disclosure | 20% | File organization, line counts, reference separation |
| 2 | Description & Triggering | 25% | Whether the skill actually gets invoked when needed |
| 3 | Content Quality | 20% | Actionability, knowledge delta, examples, error handling |
| 4 | Self-Evaluation & Verification | 15% | Can the skill verify its own output quality? |
| 5 | Evals & Testing | 10% | Does the skill have test cases for benchmarking? |
| 6 | Self-Improvement | 10% | Can the skill get better over time? |

Triggering gets the highest weight because a skill that doesn't trigger is worthless regardless of content quality.

### Step 3: Audit Each Skill

For each skill, evaluate all six dimensions. Be specific with evidence — quote line counts, cite missing files, reference exact text from descriptions. The rubric has detailed criteria for each grade level (A/B/C/F).

**What to examine:**

1. **Structure**: Count SKILL.md lines. List all files. Check for references/ directory. Look for content duplication between SKILL.md and references. Check if reference pointers include "when to read" guidance.

2. **Triggering**: Read the description field carefully. Mentally test it against 3 should-trigger and 3 should-not-trigger queries. Check for: specific trigger phrases, "Use when..." language, negative boundaries, pushy phrasing. A description that just says what the skill does without saying when to use it is a C at best.

3. **Content**: Assess whether instructions are specific enough to produce consistent results. Look for before/after examples, error handling, troubleshooting. Check if the skill explains *why* behind rules rather than heavy-handed MUSTs.

4. **Self-Evaluation**: Look for verification checklists, quality checks, success criteria. Does the skill tell you how to know if the output is good? This matters most for content-producing skills.

5. **Evals**: Check for `evals/` directory with `evals.json`. Look for test prompts with expected outputs. Check if tests cover diverse scenarios.

6. **Self-Improvement**: Look for update guidance, correction capture process, failure mode documentation, versioning. Does the skill explain how to add new knowledge or learn from mistakes?

### Step 4: Generate the Report

Read `references/report-template.md` for the exact report format. Every report must include:

- **Scorecard** — grade per dimension with one-line findings
- **Detailed findings** — current state, strengths, issues, and improvement plan per dimension
- **Priority action items** — ranked by impact, with expected grade improvement
- **Estimated effort** — rough sizing by priority level

For portfolio audits, also generate:
- **Portfolio summary table** — all skills at a glance
- **Portfolio-wide patterns** — common strengths and weaknesses
- **Recommended audit order** — which skills to improve first

### Step 5: Write the Report

Save the report to a location the user can easily find:

- Single skill: `[skill-dir]/AUDIT.md`
- Portfolio: `~/.claude/skill-audit-[date].md` with individual reports as sections

Tell the user where the report is and summarize the key findings.

---

## Grading Philosophy

**Be honest, not harsh.** Many existing skills were written before current best practices existed. A low grade isn't a failure — it's a roadmap. The improvement plan is more valuable than the score.

**Grade relative to category.** A workflow automation skill doesn't need the same self-evaluation depth as a content creation skill. The rubric accounts for this — apply it with judgment.

**Evidence over opinion.** Every grade should be backed by something concrete: a line count, a missing file, a quoted description, a specific gap. "The content could be better" is not a finding. "Lines 45-120 duplicate content already in references/patterns.md" is.

**Improvement plans must be actionable.** "Improve the description" is not a plan. "Rewrite the description to: [exact proposed text]" is. For triggering improvements, provide the actual rewritten description. For structural improvements, specify exactly which content to move where.

---

## Verification

After generating a report, verify:

1. Every dimension has a grade with evidence
2. Every grade below A has a specific improvement plan
3. Priority action items are ranked and sized
4. The report could be handed to someone unfamiliar with the skill and they'd know exactly what to do

---

## References

- **`references/grading-rubric.md`** — Complete scoring criteria for all six dimensions. Read this before every audit to ensure consistent grading. Contains the A/B/C/F criteria tables, testing protocols, and weighted scoring formula.
- **`references/report-template.md`** — Exact report format for single-skill and portfolio audits. Use this template to generate reports — don't improvise the structure.
