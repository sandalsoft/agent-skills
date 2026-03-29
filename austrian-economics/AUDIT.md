# Skill Audit Report: austrian-economics

**Audited:** 2026-03-27 (re-audit after improvements)
**Location:** /Users/eric/Development/code/Claude/ClaudeSkills/austrian-econ/austrian-economics
**Version:** 1.0.0
**Overall Grade:** A (3.70/4.0)

---

## Summary

A comprehensive Austrian Economics skill with expert-level content, strong progressive disclosure, and a complete set of guardrails. The v1.0.0 update addressed all prior gaps: anti-patterns with specific reasoning, a worked example demonstrating the reasoning method, a 5-point verification checklist, self-improvement guidance with known limitations, and 5 diverse test cases with assertions. Every dimension now meets or exceeds criteria for at least a B, with four dimensions at A.

## Scorecard

| Dimension | Weight | Grade | Score | Key Finding |
|-----------|--------|-------|-------|-------------|
| Structure & Progressive Disclosure | 20% | A | 4 | 381-line body under 500, clean 3-level disclosure with scenario-specific "when to load" guidance |
| Description & Triggering | 25% | A | 4 | Dense description with 20+ trigger keywords, casual phrase examples, and explicit negative boundary |
| Content Quality | 20% | A | 4 | Exceptional knowledge delta, worked example, explains "why" throughout, specific arguments not summaries |
| Self-Evaluation & Verification | 15% | A | 4 | 5-point verification checklist integrated into workflow, 5 battle-tested anti-patterns with reasoning |
| Evals & Testing | 10% | B | 3 | 5 diverse test cases with assertions covering ABCT, multiplier, calculation problem, inflation, methodology; no baseline comparison yet |
| Self-Improvement | 10% | B | 3 | Versioned, update guidance for new topics and corrections, 5 known limitations documented; no changelog yet |
| **Overall** | | **A** | **3.70** | |

## Detailed Findings

### Dimension 1: Structure & Progressive Disclosure — A

**Current state:**
- SKILL.md: 381 lines (367 body lines excluding frontmatter) — under 500 limit
- references/foundations.md: 378 lines with TOC
- references/critiques.md: 286 lines with TOC
- evals/evals.json: 5 test cases with assertions
- kebab-case folder, correct SKILL.md filename

**Strengths:**
- Clean three-level progressive disclosure with scenario-specific loading guidance
- "When to load reference files" section explicitly describes three scenarios: direct rival school engagement → critiques.md, detailed thinker citations → foundations.md, simple definitions → neither
- Both reference files have Tables of Contents and stay under 400 lines
- No content duplication between SKILL.md and references — SKILL.md has principles, references have detailed arguments

**Issues:**
- None. This dimension is well-executed.

### Dimension 2: Description & Triggering — A

**Current description:**
> Expert guide grounded in Austrian School economic theory — praxeology, subjective value, Austrian Business Cycle Theory, the economic calculation problem, and sound money. Applies the rigorous deductive methodology of Mises, Hayek, Menger, and Böhm-Bawerk. Use this skill whenever the user asks about economic theory, monetary policy, inflation, interest rates, business cycles, recessions, central banking, government intervention, socialism, price controls, trade policy, capital theory, entrepreneurship, or any economic question where the Austrian perspective applies. Also use when the user mentions Mises, Hayek, Menger, Rothbard, praxeology, malinvestment, or Austrian economics directly. Trigger even for general economic questions — the Austrian framework has something distinctive to say about nearly every economic topic. Also trigger for casual economic questions like "why is everything so expensive", "is the Fed ruining the economy", "what's wrong with printing money", or "why do we have recessions". Do NOT use for personal financial advice, investment recommendations, or tax planning — those require professional expertise outside the scope of economic theory.

**Trigger analysis:**
- Would trigger on: "explain Austrian business cycle theory", "why is everything so expensive", "what did Mises think about socialism", "is the Fed ruining the economy", "what caused the 2008 recession", "critique of Keynesian economics"
- Would miss: Very few economic questions would miss given the breadth of trigger phrases
- Would over-trigger on: Minimal risk — negative boundary excludes financial advice, investment recs, and tax planning
- Negative boundary present: "Do NOT use for personal financial advice, investment recommendations, or tax planning"

**Strengths:**
- 20+ specific trigger keywords covering formal and casual phrasings
- Explicit casual trigger examples ("why is everything so expensive", "what's wrong with printing money")
- Clear negative boundary preventing over-trigger into financial advice
- Appropriately pushy: "Trigger even for general economic questions"

### Dimension 3: Content Quality — A

**Current state:**
Expert-level content across SKILL.md and two reference files. The update added:
- A worked example (lines 295-339) showing the 5-step reasoning method applied to a Fed rate cut
- 5 specific anti-patterns with non-obvious reasoning (lines 253-293)

**Strengths:**
- Worked example demonstrates the complete reasoning methodology on a realistic scenario
- Anti-patterns explain *why* each mistake is wrong, not just that it's wrong (e.g., "Getting this wrong makes Austrian economics look like fortune-telling rather than rigorous deduction")
- Content explains reasoning throughout — no heavy-handed MUSTs without rationale
- Reference files contain specific logical arguments (transformation problem, regression theorem logic, MV=PQ as tautology)
- The wertfrei section provides concrete examples of the theory/value-judgment boundary

**Issues:**
- None significant at current quality level.

### Dimension 4: Self-Evaluation & Verification — A

**Current state:**
The update added a dedicated Verification section (lines 341-359) with a 5-point checklist, plus 5 battle-tested anti-patterns in the Common Mistakes section (lines 253-293).

**Strengths:**
- 5-point verification checklist with specific, actionable checks:
  1. Individual action (did you trace to individuals?)
  2. Value-free (did you avoid policy prescriptions?)
  3. Qualitative only (did you avoid quantitative predictions?)
  4. Steelmanned opposition (did you engage before dismissing?)
  5. Theory vs. history (did you distinguish them?)
- Each checklist item includes the failure indicator AND the fix ("If you wrote X, rewrite it as Y")
- Anti-patterns document common over-correction modes with specific reasoning
- Verification is integrated as a post-analysis step, not an afterthought

**Issues:**
- None. For a knowledge/analysis skill (medium self-evaluation need per rubric), this exceeds requirements.

### Dimension 5: Evals & Testing — B

**Current state:**
`evals/evals.json` exists with 5 diverse test cases, each with detailed expected outputs and 5-6 assertions.

**Strengths:**
- 5 test cases covering distinct scenarios: ABCT application, multiplier critique, calculation problem, casual inflation question, methodology explanation
- Each test case has realistic prompts (not toy examples)
- Each has detailed expected outputs describing what success looks like
- Assertions are specific and measurable (contains_concept, absence, quality types)
- Test cases include both absence assertions (should NOT predict timing, should NOT dismiss) and presence assertions

**Issues:**
- No baseline comparison (with-skill vs without-skill runs)
- Tests haven't been run through the skill-creator eval framework yet
- Could benefit from 1-2 additional edge case tests (e.g., intra-school debate, topic where Austrian position is weak)

**Improvement plan:**
Run the test cases through the skill-creator eval framework with baseline comparison. Add 1-2 edge case tests for intra-school debates.

### Dimension 6: Self-Improvement — B

**Current state:**
The update added version 1.0.0, an "Updating This Skill" section (lines 361-381) with guidance for new topics and corrections, and 5 known limitations.

**Strengths:**
- Versioned (1.0.0) in frontmatter
- Clear guidance for adding new topics: "add to appropriate reference file, keep SKILL.md focused on principles"
- Correction capture process: "add the specific failure pattern to Common Mistakes with an explanation"
- 5 known limitations documented (Rothbardian ethics, free banking debate, IP, crypto, public choice)

**Issues:**
- No formal changelog or version history
- No guidance on when to bump version numbers
- Could document which corrections have already been captured (linking back to actual incidents)

**Improvement plan:**
Consider adding a brief changelog section or CHANGELOG.md for tracking evolution across versions.

---

## Priority Action Items

Ranked by impact (highest first):

1. **[MEDIUM]** Run eval test cases through skill-creator framework with baseline comparison — addresses Evals (B→A), expected to raise overall from 3.70 to 3.80
2. **[LOW]** Add 1-2 edge case test prompts (intra-school debate, weak-position topic) — addresses Evals (incremental)
3. **[LOW]** Add CHANGELOG.md or version history notes — addresses Self-Improvement (B→A), expected to raise overall from 3.80 to 3.90

## Estimated Effort

| Priority | Count | Estimated Work |
|----------|-------|----------------|
| MEDIUM | 1 | ~30 minutes: run evals with baseline comparison |
| LOW | 2 | ~15 minutes: add edge case tests + changelog |
