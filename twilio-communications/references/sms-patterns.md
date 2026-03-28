# SMS Messaging Patterns

Complete patterns for sending SMS and WhatsApp messages with Twilio. Read this when building notification systems, transactional messaging, or any text-based communication.

---

## Table of Contents

- [Basic SMS Sending](#basic-sms-sending)
- [Bulk SMS with Rate Limiting](#bulk-sms-with-rate-limiting)
- [WhatsApp Messaging](#whatsapp-messaging)
- [Status Callbacks](#status-callbacks)
- [Opt-Out Handling](#opt-out-handling)

---

## Basic SMS Sending

The core pattern: validate the number, send the message, handle errors. Phone numbers must be E.164 format (`+1234567890`). Messages over 160 characters split into segments (each billed separately).

```python
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import re

class TwilioSMS:
    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )
        self.from_number = os.environ["TWILIO_PHONE_NUMBER"]

    def validate_e164(self, phone: str) -> bool:
        """Validate phone number is in E.164 format."""
        return bool(re.match(r'^\+[1-9]\d{1,14}$', phone))

    def send_sms(self, to: str, body: str, status_callback: str = None) -> dict:
        """
        Send an SMS message.

        Args:
            to: Recipient in E.164 format (+1234567890)
            body: Message text (160 chars = 1 segment)
            status_callback: URL for delivery status webhooks
        """
        if not self.validate_e164(to):
            return {"success": False, "error": "Phone number must be in E.164 format"}

        segment_count = (len(body) + 159) // 160

        try:
            message = self.client.messages.create(
                to=to,
                from_=self.from_number,
                body=body,
                status_callback=status_callback
            )
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status,
                "segments": segment_count
            }
        except TwilioRestException as e:
            return self._handle_error(e)

    def _handle_error(self, error: TwilioRestException) -> dict:
        """
        Handle Twilio API errors with actionable messages.

        Common error codes:
            21211 - Invalid phone number
            21408 - Permission not enabled for region
            21610 - Recipient unsubscribed (STOP)
            21614 - Not a valid mobile number
            30004 - Message blocked by carrier
            30005 - Unknown destination handset
            30006 - Landline or unreachable carrier
        """
        error_map = {
            21211: "Invalid phone number. Check the format.",
            21408: "Sending to this region is not enabled. Enable it in Twilio Console > Messaging > Geo Permissions.",
            21610: "Recipient has opted out. Do not retry — honor their STOP request.",
            21614: "Not a valid mobile number. May be a landline.",
            30004: "Message blocked by carrier filtering. Shorten the message or register your A2P 10DLC campaign.",
            30005: "Unknown destination. The number may not exist.",
            30006: "Landline or unreachable carrier. Cannot deliver SMS.",
        }
        return {
            "success": False,
            "error_code": error.code,
            "error": error_map.get(error.code, str(error.msg)),
            "retryable": error.code in (30004, 30005),
        }
```

---

## Bulk SMS with Rate Limiting

Default rate limit is 80 messages per second (MPS) for long codes. Toll-free numbers get ~25 MPS. Short codes get up to 6,000 MPS but require registration.

```python
import asyncio
from typing import List

class BulkSMS(TwilioSMS):
    async def send_bulk(
        self,
        recipients: List[dict],
        rate_limit: int = 50
    ) -> List[dict]:
        """
        Send messages to multiple recipients with rate limiting.

        Args:
            recipients: List of {"to": "+1...", "body": "..."}
            rate_limit: Messages per second (stay under your MPS limit)
        """
        results = []
        delay = 1.0 / rate_limit

        for recipient in recipients:
            result = self.send_sms(
                to=recipient["to"],
                body=recipient["body"]
            )
            results.append({**recipient, **result})

            # Respect rate limit
            if result["success"]:
                await asyncio.sleep(delay)
            else:
                # Back off on errors
                await asyncio.sleep(delay * 5)

        return results
```

For high-volume messaging (10,000+ recipients), use Twilio's Messaging Service instead. It handles sender selection, rate limiting, and compliance automatically:

```python
# Using a Messaging Service (recommended for bulk)
message = client.messages.create(
    to="+1234567890",
    messaging_service_sid=os.environ["TWILIO_MESSAGING_SERVICE_SID"],
    body="Your order has shipped!"
)
```

---

## WhatsApp Messaging

WhatsApp messages use the same Messages API but with a `whatsapp:` prefix on numbers. Key difference: WhatsApp has a 24-hour session window. Outside that window, you must use pre-approved templates.

```python
class TwilioWhatsApp(TwilioSMS):
    def __init__(self):
        super().__init__()
        self.whatsapp_number = f"whatsapp:{os.environ['TWILIO_WHATSAPP_NUMBER']}"

    def send_whatsapp(self, to: str, body: str) -> dict:
        """
        Send a WhatsApp message.

        The recipient must have opted in. Within 24 hours of their last
        message to you, you can send freeform text. Outside that window,
        use a pre-approved template.
        """
        if not self.validate_e164(to):
            return {"success": False, "error": "Phone number must be in E.164 format"}

        try:
            message = self.client.messages.create(
                to=f"whatsapp:{to}",
                from_=self.whatsapp_number,
                body=body
            )
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
        except TwilioRestException as e:
            return self._handle_error(e)

    def send_template(self, to: str, template_sid: str, variables: dict) -> dict:
        """
        Send a pre-approved WhatsApp template message.
        Use this outside the 24-hour session window.
        """
        try:
            message = self.client.messages.create(
                to=f"whatsapp:{to}",
                from_=self.whatsapp_number,
                content_sid=template_sid,
                content_variables=variables
            )
            return {"success": True, "message_sid": message.sid}
        except TwilioRestException as e:
            return self._handle_error(e)
```

---

## Status Callbacks

Track delivery status by providing a webhook URL. Twilio sends POST requests as message status changes.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/sms/status", methods=["POST"])
def sms_status_callback():
    """
    Receive delivery status updates from Twilio.

    Status flow: queued → sending → sent → delivered
    Or: queued → sending → sent → undelivered/failed
    """
    message_sid = request.form["MessageSid"]
    status = request.form["MessageStatus"]
    error_code = request.form.get("ErrorCode")

    # Update your database
    update_message_status(message_sid, status, error_code)

    if status == "failed":
        handle_failed_message(message_sid, error_code)

    return "", 204
```

Pass this URL when sending:

```python
sms.send_sms(
    to="+1234567890",
    body="Your order shipped!",
    status_callback="https://yourdomain.com/sms/status"
)
```

---

## Opt-Out Handling

US regulations require honoring STOP requests. Twilio handles this at the carrier level (replies with a confirmation and blocks future messages), but you should also track it in your database.

```python
@app.route("/sms/incoming", methods=["POST"])
def incoming_sms():
    """Handle incoming SMS including opt-out keywords."""
    from_number = request.form["From"]
    body = request.form["Body"].strip().upper()

    opt_out_keywords = {"STOP", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"}
    opt_in_keywords = {"START", "YES", "UNSTOP"}

    if body in opt_out_keywords:
        mark_opted_out(from_number)
    elif body in opt_in_keywords:
        mark_opted_in(from_number)

    return "", 204
```

Always check opt-out status before sending:

```python
def send_if_allowed(self, to: str, body: str) -> dict:
    if is_opted_out(to):
        return {"success": False, "error": "Recipient has opted out"}
    return self.send_sms(to, body)
```
