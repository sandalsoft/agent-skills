---
name: twilio-communications
version: 1.0.0
description: |
  Build communication features with Twilio: SMS messaging, voice calls,
  WhatsApp Business API, and user verification (2FA/OTP). Covers sending
  notifications, building IVR phone trees, and implementing phone number
  verification. Use when the user wants to send text messages, build a
  phone menu system, add two-factor authentication, verify phone numbers
  at signup, send WhatsApp messages, or integrate any Twilio API. Also use
  when the user mentions "OTP", "phone verification", "IVR", "TwiML",
  "voice response", or asks how to "text users" or "call users"
  programmatically. Do NOT use for email-only communication or push
  notifications unrelated to Twilio.

  Credits: Original patterns from vibeship-spawner-skills (Apache 2.0)
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Twilio Communications

Build SMS, voice, WhatsApp, and verification features with Twilio's APIs. This skill covers the four most common Twilio integration patterns and the compliance/security gotchas that trip people up.

## Which Pattern?

| Need | Pattern | Reference |
|------|---------|-----------|
| Send text messages or notifications | SMS/WhatsApp | `references/sms-patterns.md` |
| Verify phone numbers or add 2FA | Twilio Verify | `references/verify-patterns.md` |
| Build phone menus or call routing | TwiML IVR | `references/twiml-ivr.md` |
| Understand compliance & security | Sharp Edges | `references/sharp-edges.md` |

Read the relevant reference file for complete, working code examples. The sections below cover what you need to know before diving into code.

---

## Core Concepts

**E.164 phone format** — All Twilio APIs require phone numbers as `+[country code][number]` (e.g., `+14155551234`). Validate before every API call.

**Environment variables** — Never hardcode credentials. Every Twilio integration needs at minimum:
```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...
```

**Webhook security** — Twilio sends requests to your server for callbacks and TwiML. Always validate the `X-Twilio-Signature` header using `RequestValidator` to prevent spoofing. See the TwiML reference for a reusable decorator.

**Stateless webhooks** — TwiML voice flows are stateless. Each request from Twilio is independent. Pass state via URL query parameters or a server-side session store, not global variables.

---

## Pattern Summaries

### SMS & WhatsApp Messaging
Send transactional messages (order confirmations, shipping updates, alerts) via SMS or WhatsApp. Key facts:
- Messages >160 chars split into segments (each billed separately)
- Default rate: 80 messages/second for long codes
- US numbers require A2P 10DLC registration or carriers will filter your messages
- WhatsApp has a 24-hour session window — outside it, use pre-approved templates
- Always honor STOP/opt-out requests (legally required)

Read `references/sms-patterns.md` for complete code covering basic sending, bulk messaging, WhatsApp, status callbacks, and opt-out handling.

### Phone Verification (2FA/OTP)
Verify phone numbers at signup or add two-factor authentication. Use Twilio Verify instead of building your own OTP system — it handles code generation, expiration, rate limiting, and fraud prevention.
- Never store OTP codes yourself
- Supports SMS, voice call, email, WhatsApp, and push channels
- Built-in fraud prevention (blocked 747M+ attempts)
- Falls back to voice call if SMS fails

Read `references/verify-patterns.md` for complete code covering the verification flow, web framework integration, channel fallback, and security considerations.

### IVR / Voice (TwiML)
Build phone menus, call routing, voicemail, and voice automation using TwiML. Twilio makes HTTP requests to your webhook, you return TwiML XML, Twilio executes it.
- Core verbs: `<Say>`, `<Gather>`, `<Dial>`, `<Record>`, `<Redirect>`
- Supports both keypad (DTMF) and speech recognition input
- Always validate incoming webhook requests
- Handle no-answer scenarios with voicemail fallback

Read `references/twiml-ivr.md` for complete code covering IVR menus, speech recognition, voicemail with transcription, and local testing setup.

---

## Sharp Edges

These are the issues that cause real problems in production. Read `references/sharp-edges.md` for the full table with solutions.

| Issue | Severity | One-Line Fix |
|-------|----------|------------|
| Webhook spoofing | Critical | Validate `X-Twilio-Signature` on every endpoint |
| Hardcoded credentials | Critical | Environment variables, never in source control |
| Missing opt-out handling | Critical | Track STOP in your database, check before sending |
| A2P 10DLC not registered | High | Register brand + campaign before US messaging |
| WhatsApp session window | High | Track last message time, use templates outside 24h |
| Message segmentation | Medium | Messages >160 chars cost 2x+ |
| Transient failures | Medium | Retry with exponential backoff, max 3 attempts |

---

## Verification Checklist

Before delivering Twilio integration code, verify:

- [ ] Credentials loaded from environment variables (never hardcoded)
- [ ] Phone numbers validated as E.164 before API calls
- [ ] `TwilioRestException` caught with meaningful error messages
- [ ] Webhook endpoints validate `X-Twilio-Signature`
- [ ] Opt-out handling implemented (STOP/UNSUBSCRIBE for SMS)
- [ ] Rate limiting considered (both Twilio's limits and application-level)
- [ ] Status callbacks configured for delivery tracking
- [ ] A2P 10DLC mentioned if targeting US numbers
- [ ] Test credentials documented for development

---

## Self-Improvement

### API Evolution
Twilio's APIs evolve. When updating this skill:
- Check Twilio's changelog for deprecated endpoints or new features
- Update code examples to latest SDK patterns
- Add new channels as Twilio supports them (RCS, etc.)

### Learning from Use
- If generated code hits an error not in the Sharp Edges table, add it
- If a common Twilio pattern is missing (Conversations, Flex, SendGrid), add a reference file
- Track which patterns users request most and expand those first

### Known Gaps
- Twilio Conversations (multi-party chat) not yet covered
- Twilio Flex (contact center) patterns not included
- Voice recording and transcription patterns are minimal
- No Twilio SendGrid (email) coverage — this skill focuses on phone/messaging

---

## References

- **`references/sms-patterns.md`** — SMS and WhatsApp messaging: basic sending, bulk with rate limiting, WhatsApp templates, status callbacks, opt-out handling. Read when building any text messaging feature.
- **`references/verify-patterns.md`** — Phone verification and 2FA: Twilio Verify flow, web framework integration, channel fallback, security. Read when implementing signup verification or two-factor auth.
- **`references/twiml-ivr.md`** — Voice and IVR: phone menus, speech recognition, voicemail with transcription, local testing. Read when building any voice/call feature.
- **`references/sharp-edges.md`** — Compliance, security, and gotchas: webhook validation, opt-out requirements, A2P 10DLC, rate limits, testing safely. Read before shipping to production.
- **`evals/evals.json`** — Test cases for benchmarking skill quality across 4 scenarios.

## Source

Original patterns from vibeship-spawner-skills (Apache 2.0), restructured and expanded.
