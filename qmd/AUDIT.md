# Skill Audit Report: qmd

**Audited:** 2026-03-16
**Location:** ~/.agents/skills/qmd/
**Version:** unversioned
**Overall Grade:** B (2.85/4.0)

---

## Summary

The qmd skill is a well-written tool wrapper with strong actionability and genuinely useful performance guidance (when to use BM25 vs semantic vs hybrid search). At 129 lines it's concise and doesn't need progressive disclosure. The main gaps are: a thin description that buries trigger phrases in the body instead of the frontmatter, no verification or self-improvement mechanisms, no evals, and a README.md that shouldn't be in the skill directory. The highest-impact fix is enriching the description with the trigger phrases already written on lines 14-17.

## Scorecard

| Dimension | Weight | Grade | Score | Key Finding |
|-----------|--------|-------|-------|-------------|
| Structure & Progressive Disclosure | 20% | A | 4 | 129 lines, concise, no references needed — but has a README.md |
| Description & Triggering | 25% | B | 3 | Has what + when, but generic; good trigger phrases stuck in body |
| Content Quality | 20% | A | 4 | Excellent actionability, clear performance tradeoffs, good examples |
| Self-Evaluation & Verification | 15% | C | 2 | No verification; lower need for a search tool, but basic checks missing |
| Evals & Testing | 10% | F | 1 | No evals directory or test cases |
| Self-Improvement | 10% | F | 1 | No versioning, update guidance, or failure tracking |
| **Overall** | | **B** | **2.85** | |

---

## Detailed Findings

### Dimension 1: Structure & Progressive Disclosure — A

**Current state:**
- SKILL.md: 129 lines (123 body + 6 frontmatter)
- README.md: 9 lines
- No references/ or evals/ directories
- Total: 138 lines across 2 files

**Strengths:**
- At 129 lines, SKILL.md comfortably fits in a single file — no progressive disclosure needed
- Well-organized sections: prerequisites → install → setup → search modes → commands → maintenance
- Information density is high — no filler

**Issues:**
- **README.md present** — Anthropic's skill guide explicitly says "Don't include README.md inside your skill folder. All documentation goes in SKILL.md or references/." The README content (9 lines pointing to the repo) belongs in the repo root, not inside the skill package.
- The `metadata` field in frontmatter contains a dense JSON blob for Clawdbot installation automation (line 5). This works but is unusual — it adds ~200 characters to the always-loaded frontmatter that's only relevant during installation.

**Improvement plan:**
- Delete `README.md` from the skill directory. If distribution needs a README, keep it at the repo level outside the skill folder.
- Consider moving the Clawdbot metadata JSON into a separate `install.json` or reference file if the metadata system supports it (low priority — functional as-is).

---

### Dimension 2: Description & Triggering — B

**Current description:**
> Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.

**Trigger analysis:**
- Would trigger on: "search my notes", "find related documents", "search markdown files"
- Would miss: "what's in my knowledge base about X?", "look through my docs for Y", "find that note I wrote about Z", "search my journal", "qmd search"
- Would over-trigger on: unlikely — fairly specific to local search

**Issues:**
- **Trigger phrases buried in body** — Lines 14-17 contain excellent, specific trigger phrases ("search my notes / docs / knowledge base", "find related notes", "retrieve a markdown document from my collection") that belong in the description, not the body. The body section "When to use (trigger phrases)" is a classic case of the "Wrong Location" failure pattern.
- Description is ~130 characters — functional but leaves room for much more trigger coverage within the 1024-character limit.
- No pushiness ("Also use when...") or negative boundaries.
- The tool name "qmd" doesn't appear in the description — users who know the tool won't trigger the skill by name.

**Improvement plan:**
Replace the description with:

```yaml
description: |
  Local hybrid search for markdown notes and docs using qmd. Index
  collections of markdown files once, then search fast with BM25 keyword
  matching, semantic similarity, or hybrid search. Use when the user wants
  to search notes, docs, journals, or a knowledge base — including "search
  my notes", "find related content", "look through my docs for X", "what's
  in my notes about Y", or "retrieve a markdown document." Also use when
  the user mentions "qmd", "markdown search", or wants to find, retrieve,
  or query local markdown files. Do NOT use for code search (use code
  search tools) or web search.
```

This moves the trigger phrases from the body into the description where they actually influence triggering, adds the tool name, adds pushiness, and adds a negative boundary.

---

### Dimension 3: Content Quality — A

**Strengths:**
- **Excellent actionability**: Every section includes runnable commands. Setup is a 3-line copy-paste. Search modes have clear command examples. Maintenance has cron schedules.
- **High knowledge delta**: The performance characteristics of each search mode are genuinely expert knowledge — knowing that `qmd search` is instant while `vsearch` can take ~1 minute due to local model cold-start saves real debugging time. This isn't in the qmd README.
- **Clear decision framework**: "Prefer `qmd search` (BM25). Use `qmd vsearch` only when keyword search fails. Avoid `qmd query`." — actionable and opinionated.
- **Explains why**: Performance notes explain *why* vsearch is slow (local model loading), not just that it is.
- **Useful operational guidance**: Cron schedules for keeping the index fresh, PATH setup, model cache location.
- **Clean differentiation**: Line 127-129 clearly explains qmd vs memory_search — prevents confusion.

**Issues:**
- **No troubleshooting section.** Common issues like "qmd command not found" (PATH), "no results" (collection not indexed), "vsearch hangs" (model downloading) aren't covered.
- **No error handling guidance.** When using qmd in scripts or agent workflows, what does a failure look like? What exit codes does it return?

**Improvement plan:**
Add a brief troubleshooting section (~10 lines):

```markdown
## Troubleshooting

- **`qmd: command not found`** — Ensure `$HOME/.bun/bin` is in your PATH.
  Run `export PATH="$HOME/.bun/bin:$PATH"` or add to your shell profile.
- **No results from search** — Run `qmd status` to verify the collection
  is indexed. If it shows 0 documents, re-run `qmd collection add`.
- **vsearch hangs on first run** — It's downloading the embedding model
  (~1GB). Check `~/.cache/qmd/models/`. Subsequent runs reuse the cache.
- **Collection path changed** — Remove and re-add the collection:
  `qmd collection remove notes && qmd collection add /new/path --name notes`
```

---

### Dimension 4: Self-Evaluation & Verification — C

**Current state:**
No verification process. No success criteria. No operational health checks.

**Context:** This is an information retrieval / tool orchestration skill — the rubric says "Lower need" for this category. A full output verification framework isn't expected. However, basic operational checks are still valuable: is the collection indexed? Is the tool installed? Are results being returned?

**Improvement plan:**
Add a lightweight operational checklist:

```markdown
## Quick Health Check

Before relying on qmd in a workflow:
- [ ] `qmd status` shows indexed documents (not 0)
- [ ] `qmd search "test"` returns results (not empty)
- [ ] If using vsearch: `qmd embed` has been run at least once
- [ ] Collections point to current file paths (not moved/deleted dirs)
```

This is 6 lines and covers the most common "why isn't this working?" scenarios.

---

### Dimension 5: Evals & Testing — F

**Current state:**
No `evals/` directory. No test cases.

**Improvement plan:**
Create `evals/evals.json`:

```json
{
  "skill_name": "qmd",
  "evals": [
    {
      "id": 1,
      "name": "basic-keyword-search",
      "prompt": "Search my notes for anything about 'authentication'",
      "expected_output": "Uses `qmd search 'authentication'` (BM25, not vsearch). Returns results with file paths and relevant snippets. Does not attempt vsearch or query unless keyword search returns nothing."
    },
    {
      "id": 2,
      "name": "semantic-fallback",
      "prompt": "I'm looking for notes related to login security, but I'm not sure what keywords I used. Can you find related content?",
      "expected_output": "Tries `qmd search` first with likely keywords. If results are poor, falls back to `qmd vsearch` for semantic search. Warns about potential latency."
    },
    {
      "id": 3,
      "name": "collection-setup",
      "prompt": "I have a folder of markdown notes at ~/Documents/notes. How do I set up qmd to search them?",
      "expected_output": "Provides the 3-step setup: collection add, optional context add, embed. Includes the --mask flag for markdown files. Mentions cron for keeping index fresh."
    }
  ]
}
```

---

### Dimension 6: Self-Improvement — F

**Current state:**
No version field. No update guidance. No failure tracking. No known gaps documentation.

**Improvement plan:**
Add a brief section and version:

```yaml
version: 1.0.0
```

```markdown
## Maintenance & Evolution

### Keeping Up with qmd
- qmd is actively developed. Check the [GitHub repo](https://github.com/tobi/qmd) for new features and search modes.
- If new subcommands are added, document them in the Common Commands section.

### Known Limitations
- All examples assume macOS with Homebrew. Linux install paths may differ.
- No Windows support documented.
- Performance notes are based on Apple Silicon; Intel Macs and Linux machines may vary.

### Learning from Use
- If a search mode consistently fails or times out, update the Performance Notes section.
- If users frequently ask for a feature qmd doesn't support (e.g., PDF search, code search), note it here as a gap.
```

---

## Priority Action Items

Ranked by impact (highest first):

1. **[HIGH]** Move trigger phrases from body (lines 14-17) into the description — addresses D2, expected to raise from B to A. This is the single highest-impact change: 30 seconds of editing to significantly improve triggering.
2. **[MEDIUM]** Add troubleshooting section (~10 lines) — addresses D3 minor gap, covers the most common failure scenarios.
3. **[MEDIUM]** Add operational health checklist (~6 lines) — addresses D4, raises from C to B.
4. **[MEDIUM]** Create evals/evals.json with 3 test cases — addresses D5, raises from F to B.
5. **[LOW]** Add version and self-improvement section — addresses D6, raises from F to B.
6. **[LOW]** Delete README.md from skill directory — addresses D1 minor guideline violation.

## Estimated Effort

| Priority | Count | Estimated Work |
|----------|-------|----------------|
| HIGH | 1 | ~2 min: rewrite description with existing trigger phrases |
| MEDIUM | 3 | ~15 min: troubleshooting section, health checklist, evals file |
| LOW | 2 | ~5 min: version/self-improvement section, delete README |
