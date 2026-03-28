---
name: humanizer
version: 3.0.0
description: |
  Remove signs of AI-generated writing from text. Use when editing or reviewing
  text to make it sound more natural and human-written. Based on Wikipedia's
  comprehensive "Signs of AI writing" guide. Detects and fixes patterns including:
  inflated symbolism, promotional language, superficial -ing analyses, vague
  attributions, em dash overuse, rule of three, AI vocabulary words, negative
  parallelisms, and excessive conjunctive phrases. Use this skill whenever the
  user wants to "humanize" text, make AI writing sound natural, clean up AI-generated
  content, check text for AI patterns, remove AI-isms, or improve writing that
  "sounds like ChatGPT." Also use when reviewing drafts, blog posts, documentation,
  emails, or any text where the user wants it to sound like a real person wrote it.

  Credits: Original skill by @blader - https://github.com/blader/humanizer
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer

Transform AI-generated text into writing that sounds like a specific, opinionated human wrote it. Removing AI patterns is half the job — the other half is injecting voice.

## Core Philosophy

AI text fails in two ways: obvious patterns (vocabulary, structure, cadence) and absence of personality. Fixing only the patterns produces sterile, voiceless text that's still detectably non-human. The goal is writing that couldn't have come from a model — because it has a point of view.

## Process

1. **Read the input** — understand the genre, audience, and intended tone before touching anything
2. **Identify AI patterns** — scan for the 24 patterns cataloged in the quick reference below
3. **Rewrite** — replace AI-isms with natural alternatives, but also reshape rhythm, inject specificity, and add voice
4. **Verify** — run the self-evaluation checks (see `references/self-evaluation.md`)
5. **Deliver** — provide the humanized text, optionally with a brief changelog

For detailed pattern examples with word lists and before/after pairs, read `references/ai-writing-patterns.md`.

---

## Voice and Personality

Avoiding AI patterns produces clean text. Adding voice produces *human* text. Both are required.

**Signs of soulless writing** (even if technically "clean"):
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

**How to add voice:**

- **Have opinions.** "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.
- **Vary rhythm.** Short punchy sentences. Then longer ones that take their time. Mix it up.
- **Acknowledge complexity.** Real humans have mixed feelings. "Impressive but also kind of unsettling" beats "impressive."
- **Use "I" when it fits.** First person isn't unprofessional — it's honest.
- **Let some mess in.** Perfect structure feels algorithmic. Tangents and asides are human.
- **Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

**Before (clean but soulless):**
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

**After (has a pulse):**
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle — but I keep thinking about those agents working through the night.

---

## Quick Pattern Reference

24 patterns organized by category. For full word lists and examples, read `references/ai-writing-patterns.md`.

### Content Patterns (1–6)

| # | Pattern | Core Issue | Fix |
|---|---------|------------|-----|
| 1 | Inflated significance | "Pivotal moment," "testament to," "evolving landscape" | State the fact. Let readers judge importance. |
| 2 | Notability emphasis | Listing media outlets without context | Pick one source, add what was actually said |
| 3 | Superficial -ing analyses | "highlighting...", "ensuring...", "reflecting..." | Cut the participle phrase entirely |
| 4 | Promotional language | "Nestled," "vibrant," "breathtaking," "renowned" | Replace with specific, verifiable claims |
| 5 | Vague attributions | "Experts believe," "Industry reports suggest" | Name the expert or source, or cut it |
| 6 | Formulaic challenges/prospects | "Despite challenges... continues to thrive" | State the actual challenge and actual outcome |

### Language & Grammar (7–12)

| # | Pattern | Core Issue | Fix |
|---|---------|------------|-----|
| 7 | AI vocabulary | Additionally, crucial, delve, enhance, foster, landscape, pivotal, showcase, tapestry, testament, underscore, vibrant | Use the plain word |
| 8 | Copula avoidance | "Serves as," "stands as," "boasts" | Use "is," "are," "has" |
| 9 | Negative parallelisms | "It's not just X, it's Y" | Just say Y |
| 10 | Rule of three | Three-item lists everywhere | Use 2, 4, or 1 — break the pattern |
| 11 | Synonym cycling | Protagonist → main character → central figure → hero | Repeat the right word |
| 12 | False ranges | "From X to Y" on unrelated scales | List the topics directly |

### Style (13–18)

| # | Pattern | Core Issue | Fix |
|---|---------|------------|-----|
| 13 | Em dash overuse | Multiple em dashes per paragraph | Replace most with commas or periods |
| 14 | Boldface overuse | Mechanical emphasis on terms | Remove unless genuine emphasis |
| 15 | Inline-header lists | "**Topic:** Description" format | Convert to prose or simpler lists |
| 16 | Title Case headings | Every Word Capitalized | Sentence case |
| 17 | Emoji decoration | 🚀 💡 ✅ on headings/bullets | Remove |
| 18 | Curly quotes | \u201c\u201d instead of "" | Straight quotes |

### Communication (19–21) and Filler (22–24)

| # | Pattern | Core Issue | Fix |
|---|---------|------------|-----|
| 19 | Chat artifacts | "I hope this helps!", "Would you like..." | Delete — these aren't content |
| 20 | Knowledge-cutoff disclaimers | "As of [date]," "based on available information" | State the fact or omit |
| 21 | Sycophantic tone | "Great question!", "You're absolutely right!" | Get to the point |
| 22 | Filler phrases | "In order to," "it is important to note that" | Use the short version |
| 23 | Excessive hedging | "Could potentially possibly" | One hedge word max |
| 24 | Generic conclusions | "The future looks bright" | End with a concrete fact or next step |

---

## Verification

After humanizing, run these quick checks before delivering:

1. **Read-aloud test** — Does it sound natural spoken aloud? Monotone-compatible text is still too smooth.
2. **AI vocabulary scan** — Count words from pattern #7. Target: fewer than 2 per 500 words.
3. **Sentence variance** — Are sentence lengths varied? All-similar-length is an AI fingerprint.
4. **Voice check** — Is there a person behind this text? Could you tell who wrote it?
5. **Information preservation** — Did any important facts get lost in the rewrite?

For the full evaluation framework including quantitative checks, structural metrics, and genre-specific testing guidance, read `references/self-evaluation.md`.

---

## Self-Improvement

This skill should get better over time. AI writing patterns evolve as models change — new patterns emerge, old ones get fixed upstream. Here's how to keep the skill current:

### Capture New Patterns

When you encounter an AI writing pattern that isn't in the 24-pattern catalog:

1. Note the pattern with a concrete example
2. Identify why it happens (what statistical tendency drives it)
3. Write a clear fix
4. Add it to `references/ai-writing-patterns.md` in the appropriate category
5. Update the quick-reference table in this file

### Learn from Corrections

When the user corrects your humanization ("no, that still sounds like AI" or "you removed too much"):

1. Identify which pattern you missed or which fix went too far
2. Check if the pattern reference covers this case
3. If not, add it — either as a new pattern or as a note under "Common Over-Correction Mistakes" in `references/self-evaluation.md`

### Track Failure Modes

Common ways the skill underperforms. Check these first when something isn't working:

- **Over-correction**: Stripping useful structure from technical docs, removing all hedging from academic text, flattening formal tone to casual
- **Under-correction**: Missing patterns that co-occur (e.g., AI vocabulary + rule of three + promotional language in one sentence — fixing only one leaves the others)
- **Voice mismatch**: Injecting casual voice into text that should be formal, or vice versa
- **Information loss**: Cutting "fluff" that was actually important context

### Testing Changes

After modifying the skill or its references, test against the eval set in `evals/evals.json`. The evals cover five genres (Wikipedia prose, marketing copy, personal essay, technical docs, business email) and each has specific success criteria. Run them to catch regressions.

---

## References

- **`references/ai-writing-patterns.md`** — Complete catalog of all 24 AI writing patterns with word lists, explanations, and before/after examples. Read this when you need the full detail during humanization.
- **`references/self-evaluation.md`** — Verification framework: read-aloud test, quantitative checks (AI vocabulary density, structural metrics, sentence variance), qualitative checklist, common over-correction mistakes, and genre-specific testing guidance. Read this after humanizing to verify quality.
- **`evals/evals.json`** — Test cases covering five genres for benchmarking skill performance.

## Source

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.
