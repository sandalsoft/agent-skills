# Skill Auditor — Grading Rubric

Detailed scoring criteria for each audit dimension. Derived from Anthropic's official skills guide, the skill-creator best practices, and the Agent Skills specification.

Read this reference when performing an audit to ensure consistent, thorough grading.

---

## Scoring System

Each dimension is scored on a 4-point scale:

| Grade | Label | Meaning |
|-------|-------|---------|
| A | Excellent | Meets or exceeds all criteria. No action needed. |
| B | Good | Meets most criteria. Minor improvements possible. |
| C | Needs Work | Missing significant criteria. Clear improvement path. |
| F | Failing | Missing most criteria or fundamentally broken. |

Overall skill grade is the weighted average across all dimensions, with the weighting reflecting impact on real-world effectiveness.

---

## Dimension 1: Structure & Progressive Disclosure (Weight: 20%)

Evaluates whether the skill follows the three-level loading system and stays within size constraints.

### Criteria

| Criterion | A | B | C | F |
|-----------|---|---|---|---|
| SKILL.md line count | <200 lines | <500 lines | 500-800 lines | >800 lines |
| Progressive disclosure | 3 clear levels (metadata → body → references) | Body + references but unclear boundaries | Everything in SKILL.md | Single massive file, no references |
| Reference file organization | Clear pointers with "when to read" guidance | References exist but no guidance on when to read | References exist but duplicated in SKILL.md | No references despite >300 lines of content |
| Reference file size | Each <300 lines or has TOC | Some files >300 lines without TOC | Files >500 lines | Monolithic reference files |
| File naming | kebab-case folder, exact SKILL.md | Minor deviations | Incorrect casing | Missing SKILL.md |

### What to check

1. Count lines in SKILL.md (excluding frontmatter)
2. List all files in the skill directory
3. For each reference file: does SKILL.md explain when to read it?
4. Is there content duplication between SKILL.md and references?
5. Does SKILL.md fit within context without overwhelming other skills?

---

## Dimension 2: Description & Triggering (Weight: 25%)

The description is the most important field — it determines whether the skill ever gets used. This dimension gets the highest weight because a skill that doesn't trigger is worthless regardless of content quality.

### Criteria

| Criterion | A | B | C | F |
|-----------|---|---|---|---|
| Trigger coverage | Includes what + when + specific phrases + edge cases | Includes what + when + some phrases | Has what but missing when/triggers | Vague ("helps with projects") |
| Trigger specificity | Clear positive triggers AND negative boundaries | Good positive triggers, no negatives | Generic triggers that could match many skills | No actionable triggers |
| Length | 100-800 characters, dense with trigger info | Under 100 or over 800 but still useful | Too short to trigger or too long to parse | Missing or single sentence |
| Pushiness | Actively suggests when to use ("Use when...even if...") | Suggests use cases | Passive description only | No trigger guidance |
| No XML/security issues | Clean | Clean | Minor issues | Contains < > or reserved names |

### Testing protocol

To actually test triggering, formulate 3 queries that should trigger the skill and 3 that shouldn't:

**Should trigger:**
- Direct request using the skill's domain
- Paraphrased request without naming the skill
- Edge case that's less obvious but should still match

**Should NOT trigger:**
- Adjacent domain that sounds similar
- Query sharing keywords but different intent
- Generic query

Score based on how well the description would discriminate these cases.

### Common failures

- **Invisible skill**: Great content but description says "Helps with X" without trigger phrases
- **Wrong location**: Trigger-relevant info buried in the body instead of the description
- **Over-triggering**: Description so broad it matches unrelated queries
- **Keyword-only**: Relies on keywords without explaining when/why to use

---

## Dimension 3: Content Quality (Weight: 20%)

Evaluates whether the skill's instructions are clear, actionable, and add genuine value beyond what the model already knows.

### Criteria

| Criterion | A | B | C | F |
|-----------|---|---|---|---|
| Actionability | Specific steps, commands, examples | Mostly specific with some vague parts | More guidelines than instructions | Abstract principles only |
| Knowledge delta | Expert knowledge the model wouldn't have | Good domain knowledge | Some useful info mixed with obvious content | Teaches what the model already knows |
| Examples | Before/after or input/output examples | Some examples | Vague examples | No examples |
| Error handling | Troubleshooting section with common issues | Some error guidance | Mentions errors might happen | No error handling |
| Writing style | Explains "why" behind instructions | Mix of why and imperative | Heavy-handed MUSTs without rationale | Unclear or contradictory |

### What to check

1. Could a capable model follow these instructions without the skill? (If yes, low knowledge delta)
2. Are instructions specific enough to produce consistent results across runs?
3. Do examples cover the main use cases?
4. Is there guidance for when things go wrong?
5. Does the skill explain reasoning, not just rules?

---

## Dimension 4: Self-Evaluation & Verification (Weight: 15%)

Does the skill include mechanisms for verifying its own output quality? This is critical for skills that produce artifacts (text, code, designs, data) and less critical for pure workflow skills.

### Criteria

| Criterion | A | B | C | F |
|-----------|---|---|---|---|
| Verification process | Explicit checklist or script for output validation | General quality guidance | Mentions checking quality | No verification |
| Success criteria | Measurable, specific criteria | Qualitative but clear criteria | Vague criteria ("make it good") | No criteria |
| Self-check integration | Verification built into the process flow | Verification as a separate optional step | Verification mentioned but not structured | Not mentioned |
| Over-correction awareness | Documents common mistakes from over-applying the skill | Some awareness of failure modes | No failure mode documentation | N/A (not applicable for all skills) |

### What to check

1. After the skill produces output, is there a defined way to verify quality?
2. Are success criteria specific enough to be objectively assessed?
3. Does the skill warn about common ways it can go wrong?
4. Is verification integrated into the workflow or an afterthought?

### Applicability

Not all skills need self-evaluation equally:
- **High need**: Document/content creation, code generation, data transformation
- **Medium need**: Workflow automation, multi-step processes
- **Lower need**: Information retrieval, simple tool orchestration

Grade relative to the skill's category.

---

## Dimension 5: Evals & Testing (Weight: 10%)

Does the skill include test cases for benchmarking its own effectiveness? This is the newest best practice — many existing skills won't have this yet.

### Criteria

| Criterion | A | B | C | F |
|-----------|---|---|---|---|
| Eval set exists | `evals/evals.json` with 3+ diverse test cases | Some test cases documented | Informal examples that could become tests | No test cases |
| Genre coverage | Tests cover distinct scenarios/domains | Tests cover 2+ scenarios | Single scenario | N/A |
| Expected outputs | Clear success criteria per test case | General expected outputs | Vague expectations | N/A |
| Assertions | Quantitative assertions where applicable | Some measurable criteria | All subjective | N/A |
| Baseline comparison | With-skill vs without-skill or vs-old-version comparison | Informal comparison | No comparison | N/A |

### What to check

1. Does an `evals/` directory exist?
2. Are test prompts realistic (not toy examples)?
3. Do expected outputs describe what success actually looks like?
4. Could these tests be run through the skill-creator's eval framework?

---

## Dimension 6: Self-Improvement (Weight: 10%)

Does the skill have mechanisms to get better over time? This includes capturing new patterns, learning from corrections, and updating itself.

### Criteria

| Criterion | A | B | C | F |
|-----------|---|---|---|---|
| Update guidance | Documented process for adding new patterns/knowledge | General guidance on updates | Mentions skill should be updated | No update mechanism |
| Correction capture | Process for learning from user corrections | Acknowledges corrections happen | No correction loop | N/A |
| Failure tracking | Documents known failure modes and tracks new ones | Some failure documentation | No failure tracking | N/A |
| Living document | Clear that skill evolves with use | Versioned but static | No versioning or evolution | N/A |

### What to check

1. Is there guidance on how to add new knowledge to the skill?
2. When the skill makes a mistake, is there a process to prevent recurrence?
3. Does the skill document its known limitations?
4. Is there a version history or changelog approach?

---

## Calculating the Overall Grade

| Dimension | Weight |
|-----------|--------|
| 1. Structure & Progressive Disclosure | 20% |
| 2. Description & Triggering | 25% |
| 3. Content Quality | 20% |
| 4. Self-Evaluation & Verification | 15% |
| 5. Evals & Testing | 10% |
| 6. Self-Improvement | 10% |

Convert letter grades: A=4, B=3, C=2, F=1

**Overall = Σ(weight × grade_value)**

| Range | Overall Grade |
|-------|---------------|
| 3.5–4.0 | A |
| 2.5–3.49 | B |
| 1.5–2.49 | C |
| 1.0–1.49 | F |
