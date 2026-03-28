# Sharp Edges & Compliance

Critical gotchas, regulatory requirements, and security concerns when building with Twilio. Read this before shipping any Twilio integration to production.

---

## Critical Issues

These can cause security vulnerabilities, legal problems, or service disruption if ignored.

| Issue | Impact | What to Do |
|-------|--------|------------|
| Webhook spoofing | Attackers can trigger actions by POSTing to your webhook URLs | Always validate `X-Twilio-Signature` using `RequestValidator`. See the TwiML reference for the decorator pattern. |
| Hardcoded credentials | Leaked API keys give full access to your Twilio account (send messages, make calls, read logs) | Use environment variables. Never commit `TWILIO_ACCOUNT_SID` or `TWILIO_AUTH_TOKEN` to source control. |
| Missing opt-out handling | Violates TCPA (US), GDPR (EU), and carrier policies. Fines up to $1,500 per unwanted message. | Track STOP/UNSUBSCRIBE in your database. Twilio blocks at the carrier level, but you must also check before sending. |
| A2P 10DLC not registered (US) | Carriers will filter/block your messages. Delivery rates drop to near zero. | Register your brand and campaign with Twilio for A2P 10DLC before sending to US numbers. Takes 1-2 weeks for approval. |

---

## High-Priority Issues

| Issue | Impact | What to Do |
|-------|--------|------------|
| WhatsApp 24-hour session window | Messages outside the window silently fail unless using approved templates | Track when each user last messaged you. Use `content_sid` (templates) for messages outside the 24-hour window. |
| Rate limit differences by number type | Exceeding limits causes queuing and delays | Long codes: 80 MPS. Toll-free: ~25 MPS. Short codes: up to 6,000 MPS. Size your number type to your volume. |
| Message segment billing | Messages >160 chars split into segments, each billed separately | A 320-char message costs 2x. Include segment count in your send logic. Consider shortening messages. |
| Phone number provisioning | Different countries have different requirements (address verification, local presence) | Check Twilio's regulatory requirements per country before provisioning numbers. Some require proof of local business. |

---

## Medium-Priority Issues

| Issue | Impact | What to Do |
|-------|--------|------------|
| Transient API failures | Network issues cause intermittent send failures | Implement retry with exponential backoff: wait 1s, 2s, 4s. Set a max of 3 retries. Don't retry on 4xx errors (those are permanent). |
| Status callback failures | Your server being down means missed delivery updates | Use a message queue (SQS, Redis) between Twilio's callback and your processing. Log all callbacks for replay. |
| Carrier filtering (US) | Carriers use content filtering that can block legitimate messages | Avoid URL shorteners (bit.ly), ALL CAPS, and spam-like language. Register for A2P 10DLC. Keep messages concise. |
| International formatting | Users enter numbers in local format, not E.164 | Use Twilio's Lookup API to validate and format numbers before sending: `client.lookups.v2.phone_numbers(number).fetch()` |

---

## Testing Safely

**Use Twilio test credentials** to avoid charges during development:

```python
# Test credentials (from Twilio Console > Account > Test Credentials)
TEST_ACCOUNT_SID = "AC..."  # Starts with AC, different from live
TEST_AUTH_TOKEN = "..."

# Magic test numbers
# +15005550006 → always succeeds
# +15005550001 → invalid number error
# +15005550009 → cannot route error
```

**Use ngrok for webhook development:**
```bash
ngrok http 5000
# Then configure Twilio webhook URL to the ngrok address
```

**Use Twilio CLI for quick tests:**
```bash
# Send a test SMS
twilio api:core:messages:create \
  --from "+1234567890" \
  --to "+0987654321" \
  --body "Test message"

# Make a test call
twilio api:core:calls:create \
  --from "+1234567890" \
  --to "+0987654321" \
  --url "http://demo.twilio.com/docs/voice.xml"
```
