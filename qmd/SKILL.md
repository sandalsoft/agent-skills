---
name: qmd
version: 1.0.0
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
homepage: https://github.com/tobi/qmd
metadata: {"clawdbot":{"emoji":"🔍","os":["darwin","linux"],"requires":{"bins":["qmd"]},"install":[{"id":"bun-qmd","kind":"shell","command":"bun install -g https://github.com/tobi/qmd","bins":["qmd"],"label":"Install qmd via Bun"}]}}
---

# qmd — Quick Markdown Search

Local search engine for Markdown notes, docs, and knowledge bases. Index once, search fast.

## Default Behavior

The search mode you pick matters more than the query you write:

- **`qmd search`** (default): Fast keyword match (BM25). Typically instant. Always try this first.
- **`qmd vsearch`** (fallback): Semantic similarity via local embeddings. Can take ~1 minute on cold start because it loads a local model (e.g., Qwen3-1.7B) into memory. The vector lookup itself is fast — the cost is model loading.
- **`qmd query`** (generally skip): Hybrid search + LLM reranking on top of vsearch. Even slower. Only use if the user explicitly asks for highest-quality results and can wait.

The reason `vsearch` and `query` are slow: each invocation may cold-start a local LLM. If you need repeated semantic searches, consider a warm process (MCP server mode) rather than invoking per-query.

## Prerequisites & Install

```bash
# macOS
brew install oven-sh/bun/bun
brew install sqlite        # SQLite extensions
bun install -g https://github.com/tobi/qmd
```

Ensure PATH includes `$HOME/.bun/bin`.

## Setup

```bash
qmd collection add /path/to/notes --name notes --mask "**/*.md"
qmd context add qmd://notes "Description of this collection"  # optional
qmd embed  # one-time to enable vector + hybrid search
```

Indexes Markdown collections (`**/*.md`). Chunking is content-based (~few hundred tokens per chunk), not heading-based — messy Markdown is fine. Not a replacement for code search; use code search tools for source trees.

## Common Commands

```bash
# Search
qmd search "query"              # BM25 (default, fast)
qmd vsearch "query"             # Semantic (slow cold start)
qmd query "query"               # Hybrid + rerank (slowest)
qmd search "query" -c notes     # Specific collection
qmd search "query" -n 10        # More results
qmd search "query" --json       # Agent-friendly output
qmd search "query" --all --files --min-score 0.3

# Retrieve
qmd get "path/to/file.md"       # Full document by path
qmd get "#docid"                # By ID from search results
qmd multi-get "journals/2025-05*.md"
qmd multi-get "doc1.md, doc2.md, #abc123" --json

# Maintenance
qmd status                      # Index health
qmd update                      # Re-index changed files
qmd embed                       # Update embeddings
```

**Useful flags:** `-n <num>` results, `-c <name>` collection, `--all --min-score <n>` threshold, `--json` / `--files` output format, `--full` full document content.

## Keeping the Index Fresh

```bash
# Hourly incremental updates (keeps BM25 fresh):
0 * * * * export PATH="$HOME/.bun/bin:$PATH" && qmd update

# Optional: nightly embedding refresh (can be slow):
0 5 * * * export PATH="$HOME/.bun/bin:$PATH" && qmd embed
```

For keyword search, `qmd update` is enough (fast). For semantic/hybrid, also run `qmd embed` periodically.

## Models and Cache

Uses local GGUF models; first run auto-downloads (~1GB). Default cache: `~/.cache/qmd/models/` (override with `XDG_CACHE_HOME`).

## qmd vs Memory Search

- **qmd** searches *your local files* (notes/docs) that you explicitly index into collections.
- **memory_search** (claude-mem) searches *agent memory* (saved facts/context from prior conversations).
- Use both: memory_search for "what did we decide before?", qmd for "what's in my notes on disk?"

---

## Troubleshooting

**`qmd: command not found`** — `$HOME/.bun/bin` not in PATH. Run `export PATH="$HOME/.bun/bin:$PATH"` or add to your shell profile.

**No results from search** — Run `qmd status` to check index health. If it shows 0 documents, re-run `qmd collection add` with the correct path and mask.

**vsearch hangs on first run** — It's downloading the embedding model (~1GB) to `~/.cache/qmd/models/`. Check download progress there. Subsequent runs reuse the cache.

**Collection path changed** — Remove and re-add: `qmd collection remove notes && qmd collection add /new/path --name notes --mask "**/*.md"`

**`qmd embed` fails** — Ensure SQLite extensions are installed (`brew install sqlite` on macOS). Check that the collection has documents indexed first (`qmd status`).

---

## Verification

Before relying on qmd in a workflow, quick health check:

- [ ] `qmd status` shows indexed documents (not 0)
- [ ] `qmd search "test"` returns results
- [ ] If using vsearch: `qmd embed` has been run at least once
- [ ] Collections point to current file paths (not moved/deleted directories)
- [ ] PATH includes `$HOME/.bun/bin`

---

## Self-Improvement

### Keeping Up with qmd
qmd is actively developed at [github.com/tobi/qmd](https://github.com/tobi/qmd). When updating this skill:
- Check for new subcommands or search modes and add them to Common Commands
- Update performance notes if model loading behavior changes
- Add new flags or options as they're released

### Learning from Use
- If a search mode consistently fails or times out on specific hardware, update the Performance notes in Default Behavior
- If users frequently ask for features qmd doesn't support (PDF search, code search), document the gap and suggest alternatives
- If `qmd` adds MCP server mode, document warm-process usage to avoid cold-start latency

### Known Limitations
- All examples assume macOS with Homebrew. Linux install paths may differ (use `curl -fsSL https://bun.sh/install | bash` for Bun on Linux)
- Performance notes are based on Apple Silicon; Intel Macs and Linux machines may see different vsearch/query latencies
- No Windows support documented
- Cannot search non-Markdown files (PDFs, Word docs, etc.)

### Testing Changes
After modifying this skill, test against the eval set in `evals/evals.json` to verify the three core scenarios (keyword search, semantic fallback, collection setup) still work correctly.
