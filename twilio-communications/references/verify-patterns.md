# Phone Verification & 2FA Patterns

Complete patterns for phone number verification and two-factor authentication using Twilio Verify. Read this when implementing signup verification, 2FA, or any OTP-based flow.

---

## Why Twilio Verify Over DIY OTP

Building your own OTP system means managing code generation, expiration, rate limiting, and fraud detection. Twilio Verify handles all of this:

- Manages code generation and expiration (10-minute default)
- Built-in fraud prevention (blocked 747M+ fraudulent attempts)
- Automatic rate limiting per phone number
- Multi-channel delivery: SMS, voice call, email, WhatsApp, push
- Google found SMS 2FA blocks "100% of automated bots, 96% of bulk phishing attacks, and 76% of targeted attacks"

The tradeoff: you depend on Twilio's service and pay per verification ($0.05/verification vs ~$0.0079/SMS for DIY). For most applications, the security and reliability are worth it.

---

## Basic Verification Flow

```python
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from enum import Enum

class VerifyChannel(Enum):
    SMS = "sms"
    CALL = "call"
    EMAIL = "email"
    WHATSAPP = "whatsapp"

class TwilioVerify:
    """
    Phone verification with Twilio Verify.
    Never store OTP codes yourself — Twilio handles generation,
    delivery, expiration, and validation.
    """

    def __init__(self, verify_service_sid: str = None):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        # Create a Verify Service in Twilio Console first
        self.service_sid = verify_service_sid or os.environ["TWILIO_VERIFY_SID"]

    def send_verification(
        self,
        to: str,
        channel: VerifyChannel = VerifyChannel.SMS,
        locale: str = "en"
    ) -> dict:
        """
        Send a verification code.

        Args:
            to: Phone number (E.164) or email address
            channel: Delivery method
            locale: Language for the message (e.g., "en", "es", "fr")
        """
        try:
            verification = self.client.verify \
                .v2 \
                .services(self.service_sid) \
                .verifications \
                .create(to=to, channel=channel.value, locale=locale)

            return {
                "success": True,
                "status": verification.status,  # "pending"
                "channel": channel.value,
            }
        except TwilioRestException as e:
            return self._handle_verify_error(e)

    def check_verification(self, to: str, code: str) -> dict:
        """
        Verify the code the user entered.

        Args:
            to: Phone number or email that received the code
            code: The 6-digit code entered by the user
        """
        try:
            check = self.client.verify \
                .v2 \
                .services(self.service_sid) \
                .verification_checks \
                .create(to=to, code=code)

            return {
                "success": check.status == "approved",
                "status": check.status,  # "approved" or "pending"
                "valid": check.valid,
            }
        except TwilioRestException as e:
            return self._handle_verify_error(e)

    def _handle_verify_error(self, error: TwilioRestException) -> dict:
        """
        Handle Verify-specific errors.

        Common codes:
            20404 - Verification not found (expired or wrong number)
            20429 - Too many requests (rate limited)
            60200 - Invalid parameter
            60203 - Max send attempts reached for this number
            60205 - SMS not enabled for this region
        """
        error_map = {
            20404: "Verification expired or not found. Send a new code.",
            20429: "Rate limited. Wait before retrying.",
            60200: "Invalid parameter. Check the phone number format.",
            60203: "Too many attempts for this number. Wait before resending.",
            60205: "SMS not enabled for this region. Check Twilio Geo Permissions.",
        }
        return {
            "success": False,
            "error_code": error.code,
            "error": error_map.get(error.code, str(error.msg)),
        }
```

---

## Integration with a Web Framework

Here's how the verification flow looks in an API:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
verify = TwilioVerify()

@app.route("/auth/send-code", methods=["POST"])
def send_code():
    """Step 1: User requests a verification code."""
    phone = request.json.get("phone")
    if not phone:
        return jsonify({"error": "Phone number required"}), 400

    result = verify.send_verification(phone)
    if result["success"]:
        return jsonify({"message": "Code sent", "channel": result["channel"]})
    else:
        return jsonify({"error": result["error"]}), 400

@app.route("/auth/verify-code", methods=["POST"])
def verify_code():
    """Step 2: User submits the code they received."""
    phone = request.json.get("phone")
    code = request.json.get("code")

    if not phone or not code:
        return jsonify({"error": "Phone and code required"}), 400

    result = verify.check_verification(phone, code)
    if result["success"]:
        # Mark user as verified in your database
        mark_phone_verified(phone)
        return jsonify({"verified": True})
    else:
        return jsonify({"verified": False, "error": result.get("error", "Invalid code")}), 400
```

---

## Channel Fallback

If SMS delivery fails, fall back to a voice call:

```python
def send_with_fallback(self, to: str) -> dict:
    """Try SMS first, fall back to voice call."""
    result = self.send_verification(to, VerifyChannel.SMS)

    if not result["success"] and result.get("error_code") in (60205, 30006):
        # SMS not available for this number — try voice
        result = self.send_verification(to, VerifyChannel.CALL)
        result["fallback"] = True

    return result
```

---

## Security Considerations

- **Never log or store OTP codes.** Twilio manages the lifecycle. Your app only needs to call `check_verification`.
- **Rate limit on your side too.** Twilio rate-limits per number, but also limit how often a single user/IP can request codes to prevent abuse.
- **Set verification expiry.** Default is 10 minutes. Shorter is more secure but risks user frustration.
- **Use the approved channel.** Don't send codes via your own SMS sending — use Verify's built-in delivery for the fraud protection benefits.
