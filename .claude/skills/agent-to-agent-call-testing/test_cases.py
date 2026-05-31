"""Feature test-case registry for the agent-to-agent call testing harness.

Each case configures the agent-under-test and the user-sim agent for one
feature, then declares how to verify the feature fired from the transcript or DB.

Placeholders expanded by the harness before use:
    {user_sim_number_spoken}    -> e.g. "(509) 555-1234" (caller number, speech-formatted)
    {under_test_number_spoken}  -> the agent-under-test's own number, spoken form

Voice models (set `voice_provider` + the per-provider model field on either agent
to test a feature on a specific voice):
    xai          -> Grok. voice: ara|eve|rex|sal|leo
    openai       -> openai_voice_model: gpt-realtime-1.5 | gpt-realtime-2
    gemini       -> gemini_voice: <gemini voice>
    elevenlabs   -> elevenlabs_voice_id: <11labs voice id>
Default in cases below is xai; override per case or per run.

Each case dict:
    name                 unique id (used by --only)
    skip                 True = excluded from the default sweep (stub/needs fixture)
    under_test           agent-create overrides for the receiving agent
    user_sim             agent-create overrides for the calling agent
    expect_in_transcript list of substrings that MUST appear (placeholders expanded)
    judge_question       natural-language check the Claude session judges
    needs                fixtures required (e.g. "ghl_calendar"); informational
    verify_db            optional note on which call_logs field proves it

Add your own cases by copying the shape of `caller_phone` below.
"""

from __future__ import annotations

from typing import Any


def expand_placeholders(d: dict[str, Any], ph: dict[str, str]) -> dict[str, Any]:
    """Return a copy of an agent-config dict with {placeholders} expanded in str values."""
    out: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, str):
            for pk, pv in ph.items():
                v = v.replace("{" + pk + "}", pv)
        out[k] = v
    return out


TEST_CASES: list[dict[str, Any]] = [
    # ------------------------------------------------------------------ #
    # caller_phone — the agent reads back the caller's real phone number.
    # This is the case that proves the harness exercises the real call path:
    # only a real Twilio call produces a call_log with a real from_number, so
    # {{caller_phone}} resolves and the agent can speak it.
    # ------------------------------------------------------------------ #
    {
        "name": "caller_phone",
        "under_test": {
            "system_prompt": (
                "You are a friendly receptionist. The caller's phone number is "
                "{{caller_phone}}. If they ask what number they're calling from, "
                "say it back clearly and exactly. Keep it short."
            ),
            "greeting": "Hi there! I can see you're calling from {{caller_phone}}. How can I help?",
            "ai_speaks_first": True,
            "tools_enabled": [],
        },
        "user_sim": {
            "system_prompt": (
                "You just dialed a business. The instant they greet you, ask: "
                "'Quick question, what phone number am I calling from?' Listen, "
                "repeat the number back to confirm, then say 'great, thanks, bye' "
                "and end the call. Say nothing else."
            ),
        },
        "expect_in_transcript": ["{user_sim_number_spoken}"],
        "judge_question": "Did the agent correctly tell the caller their own phone number?",
        "verify_db": "call_logs.from_number == user-sim number; transcript contains spoken form",
    },
    # ------------------------------------------------------------------ #
    # Greeting / speech behaviors — no external fixture needed.
    # ------------------------------------------------------------------ #
    {
        "name": "greeting_verbatim",
        "skip": True,
        "under_test": {
            "system_prompt": "You are a receptionist. Keep replies short.",
            "greeting": "Thank you for calling Acme Plumbing, this is Sam speaking.",
            "ai_speaks_first": True,
            "tools_enabled": [],
        },
        "user_sim": {
            "system_prompt": "Wait for their greeting, then say 'just testing, goodbye' and end.",
        },
        "expect_in_transcript": ["Acme Plumbing"],
        "judge_question": "Did the agent open with the configured greeting (Acme Plumbing / Sam)?",
    },
    {
        "name": "recording_disclosure",
        "skip": True,
        "under_test": {
            "system_prompt": "You are a receptionist. Keep replies short.",
            "greeting": "Hello, how can I help you?",
            "ai_speaks_first": True,
            "enable_recording_disclosure": True,
            "tools_enabled": [],
        },
        "user_sim": {
            "system_prompt": "Wait for the greeting, say 'nothing, bye', and end the call.",
        },
        "expect_in_transcript": ["recorded"],
        "judge_question": "Did the agent disclose the call may be recorded?",
    },
    # ------------------------------------------------------------------ #
    # Tools — these fire without external services.
    # ------------------------------------------------------------------ #
    {
        "name": "end_call",
        "skip": True,
        "under_test": {
            "system_prompt": "When the caller says they're done, use end_call to hang up politely.",
            "greeting": "Hello! How can I help?",
            "ai_speaks_first": True,
            "tools_enabled": ["end_call"],
        },
        "user_sim": {
            "system_prompt": "Say 'that's all I needed, you can hang up now', then stop talking.",
        },
        "expect_in_transcript": [],
        "judge_question": "Did the agent end the call cleanly after the caller was done?",
        "verify_db": "call_logs.status == completed shortly after the 'done' cue",
    },
    {
        "name": "dynamic_variable_passthrough",
        "skip": True,
        "under_test": {
            "system_prompt": (
                "Greet the caller by name. Their name is {{first_name}}. Keep it short."
            ),
            "greeting": "Hi {{first_name}}, thanks for calling!",
            "ai_speaks_first": True,
            "variable_definitions": [
                {"name": "first_name", "description": "caller first name", "default_value": "there"}
            ],
            "tools_enabled": [],
        },
        "user_sim": {
            "system_prompt": "Wait for the greeting, say 'yep that's me, bye', and end.",
        },
        # NOTE: requires the harness to pass dynamic_variables on the outbound call
        # (context={"first_name": "Jordan"}); the default outbound path does not, so
        # this stays skipped until the harness wires `context`.
        "expect_in_transcript": ["Jordan"],
        "judge_question": "Did the agent greet the caller by the injected name?",
        "needs": "outbound context.first_name passthrough",
    },
    # ------------------------------------------------------------------ #
    # Agent teams / transfer — use team_harness.py --team instead, which builds
    # a front desk + department agents and verifies the handoff. This stub is
    # here so the feature is documented in the single-call registry too.
    # ------------------------------------------------------------------ #
    {
        "name": "transfer_to_agent",
        "skip": True,
        "needs": "use team_harness.py --team (front desk + departments)",
        "under_test": {
            "system_prompt": (
                "You are the receptionist. If the caller asks for billing, use "
                "transfer_to_agent to hand them to the billing specialist."
            ),
            "greeting": "Thanks for calling! How can I help?",
            "ai_speaks_first": True,
        },
        "user_sim": {
            "system_prompt": "Say 'I have a billing question', then after the handoff say 'thanks, bye'.",
        },
        "expect_in_transcript": [],
        "judge_question": "Did the call hand off from reception to the billing specialist?",
        "verify_db": "call_logs.agent_transitions has 2 entries; agent_id unchanged (originator)",
    },
    # ------------------------------------------------------------------ #
    # Calendar / GHL tools — need a real integration fixture (skip in sweep).
    # ------------------------------------------------------------------ #
    {
        "name": "book_appointment",
        "skip": True,
        "needs": "GHL calendar integration + calendar config on under-test",
        "under_test": {
            "system_prompt": (
                "You book appointments. When the caller wants to book, use "
                "book_appointment. Confirm the day and time back to them."
            ),
            "greeting": "Hi, would you like to book an appointment?",
            "ai_speaks_first": True,
            "tools_enabled": ["check_availability", "book_appointment"],
        },
        "user_sim": {
            "system_prompt": (
                "You want to book for tomorrow afternoon. Give the name Jordan Lee, "
                "agree to the first time offered, confirm, then hang up."
            ),
        },
        "expect_in_transcript": [],
        "judge_question": "Did the agent book an appointment and confirm a specific day/time?",
        "verify_db": "call_logs.appointment_booked / a GHL appointment row",
    },
    {
        "name": "send_sms",
        "skip": True,
        "needs": "GHL or Twilio SMS + sms_phone_number_id; real delivery side-effect",
        "under_test": {
            "system_prompt": "Offer to text the caller details. If they say yes, use send_sms.",
            "greeting": "Hi! Want me to text you our address?",
            "ai_speaks_first": True,
            "tools_enabled": ["send_sms"],
        },
        "user_sim": {
            "system_prompt": "Say 'yes please text me', then 'got it, bye' and end.",
        },
        "expect_in_transcript": [],
        "judge_question": "Did the agent trigger an SMS send?",
        "verify_db": "a messages/SMS row for the user-sim number",
    },
]
