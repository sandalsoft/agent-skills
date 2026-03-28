# Skill Audit Report: twilio-communications

**Audited:** 2026-03-16 (post-refactor)
**Location:** ~/.agents/skills/twilio-communications/
**Version:** 1.0.0
**Overall Grade:** A (3.90/4.0)

---

## Summary

The twilio-communications skill has been completely restructured from a single 300-line file with truncated code and a broken table into a well-organized 6-file package with clean progressive disclosure, complete working code, and proper compliance/security guidance. The only remaining gap is in evals — test cases exist but lack quantitative assertions and baseline comparison.

## Scorecard

| Dimension | Weight | Grade | Score | Key Finding |
|-----------|--------|-------|-------|-------------|
| Structure & Progressive Disclosure | 20% | A | 4 | 155-line SKILL.md, 4 reference files, all under 300 lines |
| Description & Triggering | 25% | A | 4 | Pushy with 7+ trigger phrases, negative boundary, specific keywords |
| Content Quality | 20% | A | 4 | Complete code examples, decision framework, explains why |
| Self-Evaluation & Verification | 15% | A | 4 | 9-item domain-specific checklist covering security and compliance |
| Evals & Testing | 10% | B | 3 | 4 test cases across patterns, but no assertions or baseline |
| Self-Improvement | 10% | A | 4 | API evolution process, known gaps documented, learning from use |
| **Overall** | | **A** | **3.90** | |

### Previous Audit Comparison

| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Structure | C (2) | A (4) | +2 |
| Triggering | C (2) | A (4) | +2 |
| Content | C (2) | A (4) | +2 |
| Self-Evaluation | F (1) | A (4) | +3 |
| Evals | F (1) | B (3) | +2 |
| Self-Improvement | F (1) | A (4) | +3 |
| **Overall** | **C (1.65)** | **A (3.90)** | **+2.25** |

---

## Detailed Findings

### Dimension 1: Structure & Progressive Disclosure — A

**Current state:**
- SKILL.md: 155 lines (131 body + 24 frontmatter)
- references/sms-patterns.md: 280 lines (has TOC)
- references/twiml-ivr.md: 264 lines
- references/verify-patterns.md: 196 lines
- references/sharp-edges.md: 76 lines
- evals/evals.json: 29 lines
- Total: 1,000 lines across 6 files

**Strengths:**
- Clean three-level progressive disclosure: decision framework in SKILL.md → pattern summaries with key facts → complete code in references
- SKILL.md at 155 lines — concise, scannable, focused on decisions not implementation
- Every reference file has explicit "when to read" guidance in both inline pointers and the References section
- All reference files under 300 lines (largest is sms-patterns at 280 with a TOC)
- Zero content duplication — SKILL.md summarizes, references implement

**Issues:**
- None.

---

### Dimension 2: Description & Triggering — A

**Current description:**
> Build communication features with Twilio: SMS messaging, voice calls, WhatsApp Business API, and user verification (2FA/OTP). Covers sending notifications, building IVR phone trees, and implementing phone number verification. Use when the user wants to send text messages, build a phone menu system, add two-factor authentication, verify phone numbers at signup, send WhatsApp messages, or integrate any Twilio API. Also use when the user mentions "OTP", "phone verification", "IVR", "TwiML", "voice response", or asks how to "text users" or "call users" programmatically. Do NOT use for email-only communication or push notifications unrelated to Twilio.

**Trigger analysis:**
- Would trigger on: "send SMS with Twilio", "add 2FA to signup", "build a phone tree", "WhatsApp order updates", "phone verification", "TwiML voice response"
- Would miss: "send a text" (without Twilio context — borderline, but "text users" is covered), "robocall system" (uncommon phrasing)
- Would over-trigger on: Very unlikely — negative boundary excludes email-only and non-Twilio push notifications

**Strengths:**
- Two "Use when..." clauses with specific actions and keywords
- Quoted trigger terms: "OTP", "IVR", "TwiML", "voice response"
- Explicit negative boundary: "Do NOT use for email-only communication or push notifications"
- ~580 characters — optimal range

**Issues:**
- None significant. Could add "Twilio Messaging Service" or "short code" as trigger terms, but these are niche.

---

### Dimension 3: Content Quality — A

**Strengths:**
- Decision framework table (line 32-37) immediately answers "which pattern should I use?"
- Core Concepts section distills the four things every Twilio integration needs (E.164, env vars, webhook security, stateless webhooks) — high knowledge delta
- Pattern summaries give enough context to choose a path without reading all references
- Sharp Edges table in SKILL.md provides critical safety info at a glance
- All reference code is complete — error handling methods, status callbacks, opt-out handling, voicemail with transcription all fully implemented
- Explains reasoning: why Verify over DIY OTP (fraud prevention stats), why webhook validation (spoofing), why A2P 10DLC (carrier filtering)

**Issues:**
- Code examples are Python/Flask only. A note acknowledging framework-agnostic principles (the key is returning TwiML XML from any HTTP handler) would help non-Flask users. This is minor — the concepts transfer.

---

### Dimension 4: Self-Evaluation & Verification — A

**Current state:**
9-item verification checklist (lines 112-120) covering:
- Security: credentials from env vars, webhook signature validation
- Compliance: opt-out handling, A2P 10DLC
- Quality: E.164 validation, error handling, rate limiting, status callbacks
- Development: test credentials

**Strengths:**
- Domain-specific and actionable — each item maps to a real production issue
- Covers the full spectrum from security to compliance to developer experience
- Sharp Edges table provides a secondary verification layer

**Issues:**
- None. For an API integration skill, this checklist covers the critical failure modes.

---

### Dimension 5: Evals & Testing — B

**Current state:**
- `evals/evals.json` with 4 test cases
- Covers: SMS notifications (FastAPI), phone verification (signup flow), IVR phone tree (Flask), WhatsApp order updates
- Each has realistic prompts and specific expected outputs

**Strengths:**
- One test per major pattern ensures baseline coverage
- Prompts include framework context (FastAPI, Flask) making them realistic
- Expected outputs are specific about what should be present (error handling, A2P mention, session window awareness)

**Issues:**
- No `assertions` field for programmatic verification (e.g., "output validates X-Twilio-Signature", "credentials loaded from environment variables", "TwilioRestException handled")
- No baseline comparison (with-skill vs without-skill)
- Missing edge cases: non-US international messaging, high-volume bulk scenarios, error recovery patterns

**Improvement plan:**
Add assertions to existing evals:
```json
"assertions": [
  {"text": "Credentials loaded from environment variables, not hardcoded", "type": "programmatic"},
  {"text": "TwilioRestException caught with error code mapping", "type": "programmatic"},
  {"text": "Phone number validated as E.164 before API call", "type": "programmatic"}
]
```

Add 1-2 edge case evals:
```json
{
  "id": 5,
  "name": "international-sms-compliance",
  "prompt": "I need to send SMS to users in the UK, Germany, and India. What do I need to know about international messaging with Twilio?",
  "expected_output": "Country-specific requirements, geo permissions, international number formatting, cost differences, local number provisioning requirements."
}
```

---

### Dimension 6: Self-Improvement — A

**Current state:**
- API Evolution section with concrete update guidance
- Learning from Use section (add errors to Sharp Edges, add missing patterns)
- Known Gaps section documenting 4 specific gaps: Conversations, Flex, recording/transcription, SendGrid
- Version 1.0.0 in frontmatter

**Strengths:**
- Known Gaps are specific and honest about what's not covered
- Learning from Use guidance is actionable (where to add new errors, when to create new reference files)
- Versioned, indicating active maintenance

**Issues:**
- None for a v1 skill. A changelog will become relevant at v2.

---

## Priority Action Items

1. **[MEDIUM]** Add quantitative assertions to `evals/evals.json` — addresses D5, expected to raise from B to A
2. **[LOW]** Add 1-2 edge case evals (international messaging, error recovery) — addresses D5 coverage
3. **[LOW]** Add brief note about framework-agnostic principles for non-Flask users — addresses D3 minor gap

## Estimated Effort

| Priority | Count | Estimated Work |
|----------|-------|----------------|
| HIGH | 0 | — |
| MEDIUM | 1 | ~10 min: add assertions to 4 existing evals |
| LOW | 2 | ~10 min: 1 new eval + framework note |
