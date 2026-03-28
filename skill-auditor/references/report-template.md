# Skill Audit Report Template

Use this template when generating audit reports. Fill in all sections. The report should be self-contained — someone reading it should understand both the current state and exactly what to do next.

---

## Report Format

```markdown
# Skill Audit Report: [skill-name]

**Audited:** [date]
**Location:** [path to skill]
**Version:** [version from frontmatter, or "unversioned"]
**Overall Grade:** [A/B/C/F] ([numeric score]/4.0)

---

## Summary

[2-3 sentence executive summary. What is this skill? How does it score? What's the single highest-impact improvement?]

## Scorecard

| Dimension | Weight | Grade | Score | Key Finding |
|-----------|--------|-------|-------|-------------|
| Structure & Progressive Disclosure | 20% | [A-F] | [1-4] | [one-line finding] |
| Description & Triggering | 25% | [A-F] | [1-4] | [one-line finding] |
| Content Quality | 20% | [A-F] | [1-4] | [one-line finding] |
| Self-Evaluation & Verification | 15% | [A-F] | [1-4] | [one-line finding] |
| Evals & Testing | 10% | [A-F] | [1-4] | [one-line finding] |
| Self-Improvement | 10% | [A-F] | [1-4] | [one-line finding] |
| **Overall** | | **[A-F]** | **[X.X]** | |

## Detailed Findings

### Dimension 1: Structure & Progressive Disclosure — [Grade]

**Current state:**
[What exists now. Line counts, file structure, how content is organized.]

**Strengths:**
- [what's working]

**Issues:**
- [specific problem with evidence]

**Improvement plan:**
[Concrete steps to reach the next grade level. Be specific about what to move, create, or restructure.]

### Dimension 2: Description & Triggering — [Grade]

**Current description:**
> [quote the actual description from frontmatter]

**Trigger analysis:**
- Would trigger on: [list queries that would match]
- Would miss: [list queries that should match but wouldn't]
- Would over-trigger on: [list queries that would falsely match]

**Improvement plan:**
[Provide a rewritten description that addresses the issues. Show the exact text.]

### Dimension 3: Content Quality — [Grade]

**Current state:**
[Assessment of actionability, knowledge delta, examples, error handling.]

**Strengths:**
- [what's working]

**Issues:**
- [specific problem with evidence]

**Improvement plan:**
[What to add, remove, or restructure in the content.]

### Dimension 4: Self-Evaluation & Verification — [Grade]

**Current state:**
[Does the skill verify its own output? How?]

**Improvement plan:**
[What verification mechanisms to add. Be specific — provide checklist items or script ideas.]

### Dimension 5: Evals & Testing — [Grade]

**Current state:**
[Does evals/ exist? What test cases exist?]

**Improvement plan:**
[List 3-5 test cases to create, with prompts and expected outputs.]

### Dimension 6: Self-Improvement — [Grade]

**Current state:**
[Does the skill have update/correction/failure-tracking mechanisms?]

**Improvement plan:**
[What self-improvement sections to add.]

---

## Priority Action Items

Ranked by impact (highest first):

1. **[HIGH]** [action item] — addresses [dimension], expected to raise grade from [X] to [Y]
2. **[HIGH]** [action item]
3. **[MEDIUM]** [action item]
4. **[LOW]** [action item]

## Estimated Effort

| Priority | Count | Estimated Work |
|----------|-------|----------------|
| HIGH | [n] | [brief estimate] |
| MEDIUM | [n] | [brief estimate] |
| LOW | [n] | [brief estimate] |
```

---

## Batch Report Format

When auditing multiple skills, use this summary format before the individual reports:

```markdown
# Skills Portfolio Audit

**Audited:** [date]
**Skills reviewed:** [count]

## Portfolio Summary

| Skill | Overall | Structure | Triggering | Content | Self-Eval | Evals | Self-Improve | Top Priority |
|-------|---------|-----------|------------|---------|-----------|-------|--------------|--------------|
| [name] | [A-F] | [A-F] | [A-F] | [A-F] | [A-F] | [A-F] | [A-F] | [one-line] |
| ... | | | | | | | | |

## Portfolio-Wide Patterns

[Observations that apply across multiple skills — common strengths and weaknesses.]

## Recommended Audit Order

[Which skills to improve first, based on usage frequency, grade, and effort required.]

---

[Individual reports follow, one per skill]
```
