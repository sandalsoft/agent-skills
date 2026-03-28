# Self-Evaluation Guide

How to verify humanization quality and catch mistakes before delivering the final text. Use this reference after humanizing text to run a structured quality check.

---

## The Read-Aloud Test

The single most reliable test: read the output aloud. AI text has a distinctive cadence — even rhythm, predictable clause lengths, no surprises. Human text stumbles, accelerates, pauses. If you can read it in a monotone without it feeling weird, it's probably still too smooth.

Specific things to listen for:
- Do all sentences start the same way? (Subject-verb, subject-verb, subject-verb)
- Is every sentence roughly the same length?
- Could you swap paragraphs without noticing? (Bad — means no logical flow)
- Does anything surprise you? (Good — means there's a voice)

---

## Quantitative Checks

These can be verified programmatically. Run them as a sanity check, not as the final arbiter — a text can pass all of these and still sound robotic.

### AI Vocabulary Density

Count occurrences of high-frequency AI words (see pattern #7 in the full reference). In natural writing, you might see 1-2 per 500 words. If you're seeing 5+, something slipped through.

**Watch list:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

### Structural Checks

| Check | AI Signal | Target |
|-------|-----------|--------|
| Em dash count per 500 words | 3+ | 0-1 |
| Bold phrases per section | 4+ | 0-2, used for genuine emphasis |
| Rule-of-three lists | 2+ consecutive | Break some into 2 or 4 items |
| Sentences starting with "Additionally" | Any | Rewrite |
| -ing participle phrases per paragraph | 2+ | 0-1 |
| Curly quotes | Any | Replace with straight quotes |
| Emoji in body text | Any | Remove unless the genre demands it |

### Sentence Variance

Measure sentence lengths across the output. AI text clusters around 15-25 words with low variance. Human text ranges from 3-word fragments to 40-word complex sentences. Standard deviation of sentence length should be at least 8-10 words.

---

## Qualitative Checklist

Run through these after the quantitative checks pass:

- [ ] **Voice present** — Can you tell a person wrote this? Is there an opinion, a perspective, a personality?
- [ ] **Specifics over generalities** — Are claims backed by concrete details, not vague gestures at importance?
- [ ] **Natural transitions** — Do paragraphs flow logically, or are they interchangeable blocks?
- [ ] **Rhythm varies** — Short sentences mixed with longer ones? Fragments where they work?
- [ ] **No orphaned AI patterns** — Reread the "words to watch" lists. Did any sneak back in during rewriting?
- [ ] **Meaning preserved** — Did the humanization accidentally remove important information?
- [ ] **Tone matches context** — Formal text should stay formal. Casual text should stay casual. Don't flatten everything to the same register.
- [ ] **No over-correction** — Sometimes "Additionally" is the right word. Sometimes a list of three is natural. The goal is to break the pattern, not ban individual words.

---

## Common Over-Correction Mistakes

Humanization can swing too far in the other direction. Watch for:

**Stripping useful structure.** If the original had a clear outline format and the context calls for it (documentation, instructions, technical specs), don't force it into flowing prose. Structure isn't inherently AI — bad structure is.

**Removing all hedging.** "May" and "might" are real words that humans use. The problem is *excessive* hedging ("could potentially possibly"), not hedging itself.

**Making everything casual.** If the input is a legal document, academic paper, or corporate report, injecting "I" and humor would be wrong. Match the register.

**Losing information.** The before/after examples in the pattern reference often show dramatic cuts. In practice, make sure every fact in the original survives in some form unless it was genuinely fluff.

---

## Testing the Skill Itself

When evaluating whether the humanizer skill is working well across diverse inputs, test with these categories:

| Category | What to test | Success looks like |
|----------|--------------|--------------------|
| Wikipedia-style prose | Encyclopedic articles with AI patterns | Neutral, specific, well-sourced |
| Marketing copy | Promotional text with buzzwords | Clear value props without hype |
| Technical writing | Docs with structural AI patterns | Clean structure, no filler |
| Personal essays | Opinion pieces that sound generic | Distinctive voice, real opinions |
| Business communication | Emails/memos with sycophantic tone | Professional but direct |
| Academic writing | Papers with excessive hedging | Appropriate confidence level |

For each category, compare the output against writing you'd expect from a competent human in that domain. The humanized version shouldn't sound like *one* voice across all categories — it should sound like a different appropriate human for each context.
