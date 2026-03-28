# Skill Audit Report: napkin

**Audited:** 2026-03-16 (post-refactor)
**Location:** ~/.claude/skills/napkin/
**Version:** 5.1.0
**Overall Grade:** A (3.70/4.0)

---

## Summary

The napkin skill is a thoughtfully designed self-improvement loop with strong content quality. After refactoring, it now includes trigger phrases and a negative boundary in the description, a napkin health check for meta-evaluation, 3 evals with assertions, a skill evolution section, domain-specific template examples, and guaranteed activation guidance via CLAUDE.md. README.md and .git/ have been removed. The only remaining gap is that evals lack baseline comparison (with-skill vs without-skill).

## Scorecard

| Dimension | Weight | Grade | Score | Key Finding |
|-----------|--------|-------|-------|-------------|
| Structure & Progressive Disclosure | 20% | A | 4 | ~155 lines, concise, clean directory (README.md and .git/ removed) |
| Description & Triggering | 25% | A | 4 | Trigger phrases, negative boundary, pushy activation language |
| Content Quality | 20% | A | 4 | Excellent philosophy, specific examples, domain-specific template guidance |
| Self-Evaluation & Verification | 15% | B | 3 | Napkin Health Check added with 5-item checklist + guaranteed activation guidance |
| Evals & Testing | 10% | B | 3 | 3 test cases with assertions, but no baseline comparison |
| Self-Improvement | 10% | A | 4 | Skill Evolution section with troubleshooting and update guidance |
| **Overall** | | **A** | **3.70** | |

### Previous Audit Comparison

| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Structure | A (4) | A (4) | — (cleaned up README/.git) |
| Triggering | B (3) | A (4) | +1 |
| Content | A (4) | A (4) | — (added domain examples) |
| Self-Evaluation | C (2) | B (3) | +1 |
| Evals | F (1) | B (3) | +2 |
| Self-Improvement | B (3) | A (4) | +1 |
| **Overall** | **B (3.05)** | **A (3.70)** | **+0.65** |

---

## Priority Action Items

1. **[MEDIUM]** Add quantitative assertions or baseline comparison to evals — addresses D5, expected to raise from B to A
2. **[LOW]** Consider adding a SessionStart hook as an alternative to CLAUDE.md inclusion for guaranteed activation

## Estimated Effort

| Priority | Count | Estimated Work |
|----------|-------|----------------|
| HIGH | 0 | — |
| MEDIUM | 1 | ~10 min: enhance evals with baseline comparison |
| LOW | 1 | ~5 min: optional hook implementation |
