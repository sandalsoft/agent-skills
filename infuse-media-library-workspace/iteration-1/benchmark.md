# Skill Benchmark: firecore-media-library

## Summary

| Metric | with_skill | without_skill | Delta |
|---|---|---|---|
| Pass rate | 100% ± 0% | 93% ± 12% | +0.067 |
| Time | 202.0s ± 54.9s | 93.5s ± 26.1s | +108.467s |
| Tokens | 66176 ± 9962 | 46179 ± 2721 | +19996.666 |

## Per-eval breakdown

| Eval | Config | Pass | Time | Tokens |
|---|---|---|---|---|
| eval-0-generic-cleanup | with_skill | 5/5 | 151.7s | 67371 |
| eval-0-generic-cleanup | without_skill | 4/5 | 105.5s | 47589 |
| eval-1-year-in-title | with_skill | 6/6 | 260.5s | 55670 |
| eval-1-year-in-title | without_skill | 6/6 | 63.6s | 43043 |
| eval-2-multi-version-and-collection | with_skill | 6/6 | 193.7s | 75488 |
| eval-2-multi-version-and-collection | without_skill | 6/6 | 111.4s | 47907 |

## Analyst notes

- Sonnet/Opus baseline is genuinely competent at this task without the skill — the year-parser trap (Blade Runner 2049 → 2017) was handled correctly by both configurations. This narrows the assertion-discrimination signal.
- Three independent with-skill agents flagged the same UX issue: dry-run mode in execute.py reports false-positive 'target dir missing' errors because mkdir ops are simulated. Real iteration target.
- With-skill on eval-2 SPLIT the James Bond collection into individual folders despite the skill's instruction to PARK Cat D collections. Strengthen the 'park-and-ask' language for collections.
- With-skill takes longer (mean ~200s) and uses more tokens (mean ~66k) than baseline (mean ~93s, ~46k) — expected, because with-skill agents run inventory.py and plan.py before executing.
- With-skill produces auditable artifacts (inventory.json, plan.json) that baseline does not — qualitative value beyond pass-rate.