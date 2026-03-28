# Skill Audit Report: humanizer

**Audited:** 2026-03-16
**Location:** ~/.agents/skills/humanizer/
**Version:** 3.0.0
**Overall Grade:** A (3.90/4.0)

---

## Summary

The humanizer skill is a well-structured, content-rich skill that closely follows current Anthropic best practices. It has strong progressive disclosure (183-line SKILL.md with two reference files), a pushy description with specific trigger phrases, high knowledge delta from the Wikipedia AI Cleanup catalog, built-in verification, and explicit self-improvement mechanisms. The single area for meaningful improvement is evals — the test cases exist but lack quantitative assertions and baseline comparison setup.

## Scorecard

| Dimension | Weight | Grade | Score | Key Finding |
|-----------|--------|-------|-------|-------------|
| Structure & Progressive Disclosure | 20% | A | 4 | 183-line SKILL.md, clean 3-level disclosure, no duplication |
| Description & Triggering | 25% | A | 4 | Pushy description with 6+ trigger phrases, missing negative boundaries |
| Content Quality | 20% | A | 4 | High knowledge delta (24-pattern catalog), strong examples, explains why |
| Self-Evaluation & Verification | 15% | A | 4 | 5-point checklist + full reference framework, integrated into process |
| Evals & Testing | 10% | B | 3 | 5 test cases across genres, but no assertions or baseline comparison |
| Self-Improvement | 10% | A | 4 | New-pattern capture, correction loop, failure tracking, regression testing |
| **Overall** | | **A** | **3.90** | |

---

## Detailed Findings

### Dimension 1: Structure & Progressive Disclosure — A

**Current state:**
- SKILL.md: 183 lines (159 body + 24 frontmatter)
- references/ai-writing-patterns.md: 348 lines (full 24-pattern catalog with TOC)
- references/self-evaluation.md: 89 lines (verification framework)
- evals/evals.json: 40 lines (5 test cases)
- Total: 660 lines across 4 files

**Strengths:**
- Clean three-level progressive disclosure: metadata (description) → body (process, quick-reference tables, verification, self-improvement) → references (full patterns, eval framework)
- SKILL.md well under 200 lines — among the most concise skills in the portfolio
- Zero content duplication: SKILL.md has compact tables with pattern name + core issue + fix; references have full word lists, explanations, and before/after examples
- Every reference file has explicit "when to read" guidance (lines 42, 76, 134, 177-179)

**Issues:**
- references/ai-writing-patterns.md at 348 lines slightly exceeds the 300-line reference guideline, though it includes a table of contents which mitigates this per the rubric

**Improvement plan:**
No action required. The 348-line reference file is justified by its 24-pattern catalog — splitting it further would hurt usability. The TOC at the top provides quick navigation.

---

### Dimension 2: Description & Triggering — A

**Current description:**
> Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written. Based on Wikipedia's comprehensive "Signs of AI writing" guide. Detects and fixes patterns including: inflated symbolism, promotional language, superficial -ing analyses, vague attributions, em dash overuse, rule of three, AI vocabulary words, negative parallelisms, and excessive conjunctive phrases. Use this skill whenever the user wants to "humanize" text, make AI writing sound natural, clean up AI-generated content, check text for AI patterns, remove AI-isms, or improve writing that "sounds like ChatGPT." Also use when reviewing drafts, blog posts, documentation, emails, or any text where the user wants it to sound like a real person wrote it.

**Trigger analysis:**
- Would trigger on: "humanize this text", "this sounds like AI wrote it", "make this sound more natural", "clean up this AI-generated content", "this reads like ChatGPT"
- Would miss: "this reads weird/robotic" (not explicitly in description), "make this sound less corporate" (adjacent intent), "de-slop this" (emerging slang for AI cleanup)
- Would over-trigger on: General "edit this text" or "improve my writing" requests where the user wants stylistic editing, not AI-pattern removal

**Strengths:**
- ~580 characters — within optimal range
- Two "Use when..." clauses with specific trigger phrases
- Lists specific pattern names for keyword matching
- Covers both explicit ("humanize") and contextual ("reviewing drafts, blog posts") triggers
- Pushy: "Also use when reviewing drafts..."

**Issues:**
- No negative boundaries. Could add: "Do NOT use for general copyediting, grammar correction, or stylistic preference changes that aren't about AI patterns"
- Missing emerging terminology: "de-slop", "sounds robotic", "too AI"

**Improvement plan:**
Minor. Add a negative boundary and 2-3 more trigger phrases to the end of the description:

```
...or any text where the user wants it to sound like a real person wrote it.
Also triggers on "de-slop", "sounds robotic", or "too AI." Do NOT use for
general grammar correction or copyediting unrelated to AI writing patterns.
```

This would close the over-triggering gap and catch emerging terminology.

---

### Dimension 3: Content Quality — A

**Current state:**
- 5-step process is clear and actionable
- Quick-reference tables provide pattern → core issue → fix at a glance for all 24 patterns
- Voice/personality section (lines 46-70) is the skill's most distinctive content — teaches *adding* voice, not just removing patterns
- Full before/after example demonstrates the transformation

**Strengths:**
- High knowledge delta: The 24-pattern catalog sourced from Wikipedia's AI Cleanup project is specialized knowledge most models wouldn't have in structured form. The "words to watch" lists are particularly valuable.
- Explains "why" throughout: "AI text fails in two ways" (line 32), "Fixing only the patterns produces sterile, voiceless text" (line 32), each pattern in the reference explains *why it happens* not just what to fix
- The Voice and Personality section adds genuine editorial insight that goes beyond pattern-matching

**Issues:**
- No troubleshooting section for common failure scenarios (e.g., "what to do when the user says it still sounds like AI after your rewrite")
- The process step 1 ("Read the input — understand the genre, audience, and intended tone") could be more specific about *how* to determine genre/tone

**Improvement plan:**
Add a brief troubleshooting section after Verification (~10 lines):

```markdown
## Troubleshooting

**"It still sounds like AI"** — Check for co-occurring patterns. Fixing one
pattern per sentence while leaving 2-3 others creates a half-cleaned effect
that's actually more noticeable. Rewrite the sentence from scratch.

**"You removed too much"** — You likely cut factual content along with filler.
Re-read the original, list every discrete fact, and verify each appears in
your rewrite.

**"The tone is wrong"** — You probably defaulted to casual voice. Re-read the
input's genre context and match the register (formal stays formal, technical
stays technical).
```

---

### Dimension 4: Self-Evaluation & Verification — A

**Current state:**
- 5-point verification checklist integrated into the process (step 4, lines 126-133)
- Points to `references/self-evaluation.md` for the full framework
- self-evaluation.md includes: read-aloud test, AI vocabulary density metric (target: <2 per 500 words), structural checks table (em dash count, bold count, -ing phrases, etc.), sentence variance measurement, qualitative checklist (7 items), common over-correction mistakes (4 documented), genre-specific testing matrix (6 genres)
- Over-correction awareness documented in both SKILL.md (lines 163-167) and the reference

**Strengths:**
- Verification is built into the workflow, not an afterthought
- Mix of quantitative checks (AI vocab density, em dash count, sentence length variance) and qualitative checks (voice present, tone matches context)
- Excellent over-correction documentation — addresses stripping structure, removing hedging, flattening tone, and losing information
- Genre-specific testing matrix acknowledges different standards for different text types

**Issues:**
- None significant. This is the strongest dimension.

**Improvement plan:**
No action required.

---

### Dimension 5: Evals & Testing — B

**Current state:**
- `evals/evals.json` exists with 5 test cases
- Test names: wikipedia-article-dense-patterns, marketing-copy-with-soul, personal-essay-voice-preservation, technical-docs-structure-preserved, business-email-desycophant
- Each test has a realistic prompt with embedded AI patterns and a detailed expected_output description
- Genre coverage: Wikipedia prose, marketing copy, personal essay, technical docs, business email

**Strengths:**
- 5 diverse test cases covering distinct genres
- Prompts are realistic — they contain multiple overlapping AI patterns that a real user would encounter
- Expected outputs are specific about what should and shouldn't change
- Descriptive test names make it clear what each eval targets

**Issues:**
- No `assertions` field in any test case. The skill-creator framework supports quantitative assertions (e.g., "output contains zero instances of words from the AI vocabulary list", "em dash count < 2", "all factual claims from input preserved"). These could be checked programmatically.
- No baseline comparison setup. There's no `without_skill` configuration to measure whether the skill actually improves over unguided humanization.
- Missing edge case tests: very short input (1 sentence), input that's already human-sounding (should change little), input mixing languages, input with code blocks that shouldn't be modified

**Improvement plan:**

1. **Add assertions to existing evals.** For each test case, add 3-4 programmatically verifiable assertions:
   ```json
   "assertions": [
     {"text": "No AI vocabulary words from pattern #7 list", "type": "programmatic"},
     {"text": "Em dash count <= 1", "type": "programmatic"},
     {"text": "All factual claims from input preserved", "type": "human"},
     {"text": "Sentence length std dev >= 8 words", "type": "programmatic"}
   ]
   ```

2. **Add edge case evals:**
   ```json
   {
     "id": 6,
     "name": "already-human-minimal-changes",
     "prompt": "Humanize this: 'I spent three hours debugging a memory leak yesterday. Turned out the cache wasn't expiring. Pretty annoying.'",
     "expected_output": "Minimal or no changes. The input is already human-sounding. The skill should recognize this and not over-process."
   },
   {
     "id": 7,
     "name": "mixed-code-and-prose",
     "prompt": "Humanize this README section but don't touch the code blocks: [technical README with AI patterns in prose but valid code in fenced blocks]",
     "expected_output": "Code blocks preserved exactly. Surrounding prose humanized. Heading case fixed."
   }
   ```

3. **Set up baseline comparison** by adding a note in evals.json about running with-skill vs without-skill configurations through the skill-creator framework.

---

### Dimension 6: Self-Improvement — A

**Current state:**
- "Capture New Patterns" section with 5-step process for adding new patterns (lines 142-150)
- "Learn from Corrections" section with 3-step process for feedback integration (lines 152-158)
- "Track Failure Modes" section documenting 4 known failure categories (lines 160-167)
- "Testing Changes" section pointing to evals for regression testing (lines 169-171)
- Version 3.0.0 indicates active evolution

**Strengths:**
- The new-pattern capture process is specific: note → identify why → write fix → add to reference → update quick-reference
- Correction capture distinguishes between missed patterns and over-corrections, directing fixes to the appropriate file
- Failure modes are concrete and actionable (over-correction, under-correction, voice mismatch, information loss)
- Regression testing is built in via the eval set

**Issues:**
- No changelog or version history documenting what changed between versions
- The self-improvement guidance is instructions for the *model using the skill* to update files, but in practice models don't persist changes between sessions. This is more useful as guidance for the *skill maintainer* (the user).

**Improvement plan:**
Minor. Consider adding a CHANGELOG.md or a brief version history section at the bottom of SKILL.md:

```markdown
## Changelog
- **3.0.0** — Restructured from single 439-line file to progressive disclosure
  (183-line SKILL.md + references). Added verification, self-improvement, and evals.
- **2.1.1** — Original version by @blader. Single-file with all 24 patterns inline.
```

---

## Priority Action Items

Ranked by impact (highest first):

1. **[MEDIUM]** Add quantitative assertions to `evals/evals.json` — addresses Evals & Testing (D5), expected to raise from B to A. Enables programmatic grading through the skill-creator framework.
2. **[MEDIUM]** Add 2-3 edge case test cases (already-human input, mixed code/prose) — addresses D5, improves coverage for realistic scenarios.
3. **[LOW]** Add negative trigger boundaries to description — addresses Triggering (D2), prevents false activation on general editing requests.
4. **[LOW]** Add troubleshooting section (~10 lines) — addresses Content Quality (D3), handles "it still sounds like AI" scenarios.
5. **[LOW]** Add CHANGELOG.md or version history — addresses Self-Improvement (D6), provides context for future maintainers.

## Estimated Effort

| Priority | Count | Estimated Work |
|----------|-------|----------------|
| HIGH | 0 | — |
| MEDIUM | 2 | ~15 min: add assertions to 5 existing evals + 2-3 new test cases |
| LOW | 3 | ~10 min: one-line description addition, short troubleshooting section, brief changelog |
