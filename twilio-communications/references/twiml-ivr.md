# TwiML & IVR Patterns

Complete patterns for building Interactive Voice Response (IVR) systems using TwiML. Read this when building phone menus, call routing, voicemail, or any voice-based automation.

---

## How TwiML Works

TwiML (Twilio Markup Language) is XML that tells Twilio what to do with a call. The flow is stateless:

1. Incoming call hits your webhook URL
2. Your server returns TwiML XML
3. Twilio executes the TwiML instructions
4. If TwiML points to another URL (via `action` or `Redirect`), Twilio makes another request
5. Repeat until the call ends

Because each request is independent, pass state via URL query parameters or a server-side session store.

**Core TwiML verbs:**

| Verb | Purpose | Example |
|------|---------|---------|
| `<Say>` | Text-to-speech | Greetings, menu prompts |
| `<Play>` | Play audio file | Hold music, pre-recorded messages |
| `<Gather>` | Collect keypad or speech input | Menu selections, account numbers |
| `<Dial>` | Connect to another number | Transfer to agent, conference |
| `<Record>` | Record caller's voice | Voicemail, call recording |
| `<Redirect>` | Move to another TwiML endpoint | Loop back, route to submenu |
| `<Pause>` | Wait silently | Between prompts |
| `<Hangup>` | End the call | After voicemail, error conditions |

---

## IVR Phone Menu

A complete IVR system with input validation, routing, voicemail, and webhook security.

```python
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.request_validator import RequestValidator
import os
import functools

app = Flask(__name__)


def validate_twilio_request(f):
    """
    Decorator to validate requests actually come from Twilio.
    Without this, anyone can POST to your webhook and trigger actions.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
        url = request.url
        params = request.form.to_dict()
        signature = request.headers.get("X-Twilio-Signature", "")

        if not validator.validate(url, params, signature):
            return "Unauthorized", 403

        return f(*args, **kwargs)
    return wrapper


@app.route("/voice/incoming", methods=["POST"])
@validate_twilio_request
def incoming_call():
    """Handle incoming call with IVR menu."""
    response = VoiceResponse()

    gather = Gather(
        num_digits=1,
        action="/voice/menu-selection",
        method="POST",
        timeout=5,
        action_on_empty_result=True  # Still triggers action if no input
    )
    gather.say(
        "Welcome to Acme Corp. "
        "Press 1 for sales. "
        "Press 2 for support. "
        "Press 3 to leave a message.",
        voice="Polly.Joanna",  # Use Amazon Polly for natural speech
        language="en-US"
    )
    response.append(gather)

    # If gather times out without input, redirect to retry
    response.redirect("/voice/incoming")

    return Response(str(response), mimetype="text/xml")


@app.route("/voice/menu-selection", methods=["POST"])
@validate_twilio_request
def menu_selection():
    """Route based on menu selection."""
    response = VoiceResponse()
    digit = request.form.get("Digits", "")

    if digit == "1":
        response.say("Connecting you to sales.")
        dial = response.dial(
            timeout=30,
            action="/voice/dial-status"  # Handle no-answer
        )
        dial.number(os.environ["SALES_PHONE"])

    elif digit == "2":
        response.say("Connecting you to support.")
        dial = response.dial(
            timeout=30,
            action="/voice/dial-status"
        )
        dial.number(os.environ["SUPPORT_PHONE"])

    elif digit == "3":
        response.say("Please leave a message after the beep. Press pound when finished.")
        response.record(
            max_length=120,           # 2 minutes max
            action="/voice/recording-complete",
            transcribe=True,          # Get text transcription
            transcribe_callback="/voice/transcription",
            play_beep=True,
            finish_on_key="#"
        )

    else:
        response.say("Sorry, that's not a valid option.")
        response.redirect("/voice/incoming")

    return Response(str(response), mimetype="text/xml")


@app.route("/voice/dial-status", methods=["POST"])
@validate_twilio_request
def dial_status():
    """Handle cases where the dialed party doesn't answer."""
    response = VoiceResponse()
    dial_status = request.form.get("DialCallStatus", "")

    if dial_status in ("no-answer", "busy", "failed"):
        response.say("Sorry, no one is available right now. Please leave a message.")
        response.record(
            max_length=120,
            action="/voice/recording-complete",
            play_beep=True,
            finish_on_key="#"
        )
    else:
        response.say("Thank you for calling. Goodbye.")
        response.hangup()

    return Response(str(response), mimetype="text/xml")


@app.route("/voice/recording-complete", methods=["POST"])
@validate_twilio_request
def recording_complete():
    """Handle completed voicemail recording."""
    response = VoiceResponse()
    recording_url = request.form.get("RecordingUrl", "")

    if recording_url:
        # Save recording URL to your database
        save_voicemail(
            caller=request.form.get("From"),
            recording_url=recording_url,
            duration=request.form.get("RecordingDuration")
        )

    response.say("Thank you. Your message has been recorded. Goodbye.")
    response.hangup()

    return Response(str(response), mimetype="text/xml")


@app.route("/voice/transcription", methods=["POST"])
@validate_twilio_request
def transcription_callback():
    """Receive voicemail transcription (async, arrives later)."""
    recording_sid = request.form.get("RecordingSid")
    transcription = request.form.get("TranscriptionText", "")

    # Update your database with the transcription
    update_voicemail_transcription(recording_sid, transcription)

    return "", 204
```

---

## Speech Recognition IVR

Use `input="speech"` on Gather for natural language menus instead of keypad:

```python
@app.route("/voice/speech-menu", methods=["POST"])
@validate_twilio_request
def speech_menu():
    """IVR with speech recognition."""
    response = VoiceResponse()

    gather = Gather(
        input="speech dtmf",        # Accept both speech and keypad
        speech_timeout="auto",       # Auto-detect end of speech
        action="/voice/speech-route",
        method="POST",
        language="en-US",
        hints="sales, support, billing, cancel"  # Improve recognition
    )
    gather.say("How can I help you today? You can say sales, support, or billing.")
    response.append(gather)

    return Response(str(response), mimetype="text/xml")


@app.route("/voice/speech-route", methods=["POST"])
@validate_twilio_request
def speech_route():
    """Route based on speech recognition result."""
    response = VoiceResponse()
    speech = request.form.get("SpeechResult", "").lower()

    if "sales" in speech:
        response.say("Connecting you to sales.")
        response.dial(os.environ["SALES_PHONE"])
    elif "support" in speech or "help" in speech:
        response.say("Connecting you to support.")
        response.dial(os.environ["SUPPORT_PHONE"])
    elif "billing" in speech or "payment" in speech:
        response.say("Connecting you to billing.")
        response.dial(os.environ["BILLING_PHONE"])
    else:
        response.say("I didn't catch that. Let me connect you to an operator.")
        response.dial(os.environ["OPERATOR_PHONE"])

    return Response(str(response), mimetype="text/xml")
```

---

## Testing Locally

Use ngrok to expose your local server to Twilio's webhooks:

```bash
# Terminal 1: Run your Flask app
python app.py

# Terminal 2: Expose via ngrok
ngrok http 5000
```

Then configure your Twilio phone number's webhook URL to the ngrok URL (e.g., `https://abc123.ngrok.io/voice/incoming`).

For automated testing without real calls, use the Twilio CLI:

```bash
twilio phone-numbers:update +1234567890 \
  --voice-url https://abc123.ngrok.io/voice/incoming
```
