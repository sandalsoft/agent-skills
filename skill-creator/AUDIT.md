# Skill Audit Report: skill-creator

**Audited:** 2026-03-18
**Location:** ~/.claude/skills/skill-creator
**Version:** unversioned
**Overall Grade:** B (2.95/4.0)

---

## Summary

Skill-creator is Anthropic's official skill for building and iterating on skills. The content quality is outstanding — deeply actionable, well-reasoned, and conversational without being sloppy. But the skill doesn't eat its own dog food: no evals directory, no self-improvement mechanisms, no versioning. The cobbler's children have no shoes.

## Scorecard

| Dimension | Weight | Grade | Score | Key Finding |
|-----------|--------|-------|-------|-------------|
| Structure & Progressive Disclosure | 20% | B | 3 | 481 body lines (just under 500 limit); schemas.md at 431 lines lacks a TOC |
| Description & Triggering | 25% | B | 3 | Good trigger coverage but could be pushier per its own advice |
| Content Quality | 20% | A | 4 | Exceptional — explains reasoning, adapts to user skill level, covers edge cases |
| Self-Evaluation & Verification | 15% | A | 4 | The skill IS an eval framework; grading, benchmarking, and blind comparison deeply integrated |
| Evals & Testing | 10% | F | 1 | No evals/ directory despite being the skill that teaches eval creation |
| Self-Improvement | 10% | F | 1 | No update guidance, versioning, correction capture, or failure tracking |
| **Overall** | | **B** | **2.95** | |

## Detailed Findings

### Dimension 1: Structure & Progressive Disclosure — B

**Current state:**
SKILL.md is 485 lines total (481 body lines, 4 frontmatter). The skill has good directory structure with clear separation:
- `agents/` — 3 subagent definitions (grader.md, comparator.md, analyzer.md)
- `scripts/` — 9 Python scripts for eval running, benchmarking, packaging
- `references/` — schemas.md (431 lines)
- `assets/` — eval_review.html template
- `eval-viewer/` — generate_review.py and viewer.html

**Strengths:**
- Three-level progressive disclosure works well: metadata triggers, SKILL.md provides the workflow, agents/scripts/references provide depth
- Reference pointers at lines 459-466 clearly list each agent and reference file with purpose descriptions
- Scripts execute without needing to be loaded into context

**Issues:**
- SKILL.md at 481 lines is right at the boundary — one more section and it's over 500
- `references/schemas.md` is 431 lines with no table of contents, making it hard to navigate to the specific schema you need
- The `eval-viewer/` directory sits outside the standard `scripts/`/`references/`/`assets/` structure — it's a mix of script (generate_review.py) and asset (viewer.html)

**Improvement plan:**
1. Add a TOC to `references/schemas.md` listing the 7 schema sections (evals.json, history.json, grading.json, metrics.json, timing.json, benchmark.json, comparison.json, analysis.json)
2. Move `eval-viewer/generate_review.py` into `scripts/` and `eval-viewer/viewer.html` into `assets/`, then remove the `eval-viewer/` directory
3. Consider extracting the "Claude.ai-specific instructions" and "Cowork-Specific Instructions" sections (lines 420-456) into a `references/environment-adaptations.md` file to bring SKILL.md under 400 lines

### Dimension 2: Description & Triggering — B

**Current description:**
> Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.

**Trigger analysis:**
- Would trigger on: "I want to make a skill", "help me improve this skill", "run evals on my skill", "optimize my skill's description"
- Would miss: "turn this into a skill" (contextual, hard to capture), "how do I test if my skill works" (close but phrased as question), "my skill isn't triggering properly" (debugging framing)
- Would over-trigger on: unlikely — the description is specific enough

**Issues:**
- The skill's own writing guide (line 67) says descriptions should be "a little bit pushy" — this description doesn't follow that advice. It lists capabilities but doesn't push usage in ambiguous cases.
- Missing negative boundaries — what this skill is NOT for (e.g., not for writing CLAUDE.md files, not for hook configuration)
- At 266 characters, it's functional but could use the space budget (up to 800) more aggressively

**Improvement plan:**
Rewrite the description to:
> Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. Also use when someone says "turn this into a skill", asks how to test whether a skill works, wants to package a skill for sharing, or has a skill that isn't triggering correctly. Not for writing CLAUDE.md files or configuring hooks — those are separate concerns.

### Dimension 3: Content Quality — A

**Current state:**
The content quality is the skill's strongest dimension. The writing is conversational, specific, and deeply informed by real usage patterns.

**Strengths:**
- Explains *why* behind every instruction — the "How to think about improvements" section (lines 296-306) is a masterclass in skill-writing philosophy
- Adapts communication to user skill level (lines 33-41) with concrete examples of what terms need explanation
- Covers environment-specific adaptations (Claude.ai, Cowork, headless) with practical workarounds
- The eval workflow is a complete, opinionated system: spawn parallel runs → draft assertions while waiting → capture timing → grade → aggregate → launch viewer → collect feedback → iterate
- JSON schema examples are concrete and annotated with field descriptions
- The "Principle of Lack of Surprise" (line 111) is a thoughtful safety guardrail

**Issues:**
- The "Cool? Cool." at line 30 sets a tone that might not land for all users, though it does match the conversational style throughout
- The repeated emphasis on generating the eval viewer (lines 451, 472-483) suggests this was a problem in practice — the fix works but reads as patching a behavior issue rather than solving it structurally

**Improvement plan:**
Minor — this dimension is already at A. The one structural improvement would be to move the repeated "generate the eval viewer" reminders into a single prominent callout rather than scattering them across sections.

### Dimension 4: Self-Evaluation & Verification — A

**Current state:**
The skill is itself an evaluation framework, so self-evaluation is deeply woven into its purpose. The grader agent verifies assertions against outputs. The blind comparator provides unbiased quality comparison. The analyzer surfaces patterns hidden by aggregate metrics.

**Strengths:**
- Verification is integrated into the core workflow loop, not an afterthought
- The grader agent (agents/grader.md) has sophisticated pass/fail criteria including "surface compliance" detection
- The "generalize from feedback" guidance (line 298) explicitly warns against overfitting to test cases
- Success criteria are measurable through pass rates, timing, and token usage
- The grader even critiques the evals themselves (Step 6 in grader.md)

**Issues:**
- No verification mechanism for the skill-creator's *own* output quality (meta-level). When skill-creator produces a skill, there's no checklist for "did the created skill follow all the patterns taught in this skill?"

**Improvement plan:**
Add a "Skill Quality Checklist" section that the creator applies to every skill it produces — a quick 5-point verification before declaring a skill done.

### Dimension 5: Evals & Testing — F

**Current state:**
No `evals/` directory exists. No `evals.json`. No test cases. The skill that teaches eval creation has zero evals for itself.

**Improvement plan:**
Create `evals/evals.json` with at least these test cases:

1. **"Create a skill from scratch"** — prompt: "I want to create a skill that helps me write commit messages following conventional commits format" — expected: produces SKILL.md with frontmatter, description with trigger phrases, structured body under 500 lines
2. **"Improve an existing skill"** — prompt: "Here's my skill at /path/to/skill, the description isn't triggering well" — expected: runs description optimization loop, produces improved description with before/after comparison
3. **"Run evals on a skill"** — prompt: "Run test cases on this skill and show me the results" — expected: spawns parallel subagent runs, generates benchmark.json, launches eval viewer
4. **"Turn conversation into skill"** — prompt: "We just built this great workflow, turn it into a skill" — expected: extracts steps from conversation context, writes SKILL.md, proposes test cases

### Dimension 6: Self-Improvement — F

**Current state:**
No update guidance. No correction capture. No failure mode documentation. No versioning. No changelog. The skill treats itself as a finished artifact rather than a living document.

**Improvement plan:**
1. Add a version field to frontmatter (start at `1.0.0`)
2. Add a "Known Limitations" section documenting failure modes (e.g., "description optimization requires claude CLI", "blind comparison needs subagents", "viewer requires browser or --static flag")
3. Add an "Updating This Skill" section with guidance on when and how to add new patterns — for example, when a new environment (like Claude Desktop) adds new constraints
4. Add a `CHANGELOG.md` tracking what changed and why

---

## Priority Action Items

Ranked by impact (highest first):

1. **[HIGH]** Create `evals/evals.json` with 4 diverse test cases covering the main workflows (create, improve, evaluate, extract-from-conversation) — addresses Evals & Testing (F→B), expected to raise overall from 2.95 to 3.15
2. **[HIGH]** Rewrite the description to be pushier and include negative boundaries, following the skill's own advice — addresses Description & Triggering (B→A), expected to raise overall from 2.95 to 3.20
3. **[MEDIUM]** Add TOC to `references/schemas.md` and consolidate `eval-viewer/` into standard directories — addresses Structure (B→A)
4. **[MEDIUM]** Add versioning, known limitations, and update guidance — addresses Self-Improvement (F→C)
5. **[MEDIUM]** Extract environment-specific sections to a reference file to bring SKILL.md under 400 lines — addresses Structure (B→A)
6. **[LOW]** Add a "Skill Quality Checklist" for verifying created skills — addresses Self-Evaluation (A→A, quality of life improvement)

## Estimated Effort

| Priority | Count | Estimated Work |
|----------|-------|----------------|
| HIGH | 2 | ~30 minutes (write evals, rewrite description) |
| MEDIUM | 3 | ~45 minutes (TOC, restructure, add self-improvement sections) |
| LOW | 1 | ~15 minutes (quality checklist) |
