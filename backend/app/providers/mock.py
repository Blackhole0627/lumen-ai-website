"""Mock providers: the whole system runs end to end without any vendor accounts.

They log what a real provider would do, so you can follow a call in the console.
The mock LLM is deliberately naive (it ignores affordability) so you can watch
the safety guards correct it.
"""
from __future__ import annotations

import logging
import re
import uuid
from typing import Any

from ..config import Settings
from .base import (
    CRM, CRMS, LLMS, MESSAGING, PAYMENTS, STT, TTS, VOICE,
    LanguageModel, LLMReply, LLMRequest, MessageChannel, MessagingChannel, Payments,
    SpeechToText, TextToSpeech, Transcript, VoiceChannel,
)

log = logging.getLogger("providers.mock")

AGREE = re.compile(r"\b(yes|yeah|yep|ok|okay|sure|works|fine|deal|agreed?)\b", re.I)


@STT.register("mock")
class MockSTT(SpeechToText):
    """Treats the audio bytes as UTF-8 text, so you can 'send audio' from curl."""

    def __init__(self, settings: Settings, **_: Any) -> None:
        pass

    def transcribe(self, audio: bytes, language: str) -> Transcript:
        text = audio.decode("utf-8", errors="ignore").strip()
        return Transcript(text=text, confidence=0.95 if text else 0.0)


@LLMS.register("mock")
class MockLLM(LanguageModel):
    """Scripted 'model'. Replace with a real vendor via LLM_PROVIDER (see _template.py)."""

    def __init__(self, settings: Settings, **_: Any) -> None:
        pass

    def generate(self, request: LLMRequest) -> LLMReply:
        c = request.context
        agent_turns = sum(1 for m in request.messages if m["role"] == "assistant")
        last = next((m["content"] for m in reversed(request.messages) if m["role"] == "user"), "")
        cur = c["currency"]

        if agent_turns == 0:
            return LLMReply(f"Hello, am I speaking with {c['customer_name']}?", intent="greet")
        if not c["verified"]:
            return LLMReply("Thanks. To protect your privacy, could you confirm your date of birth and postcode?", intent="verify")
        if c["plan_booked"]:
            return LLMReply("Your plan is all set. Is there anything else I can help you with today?", intent="wrap_up")
        if c["pending_offer"] and AGREE.search(last):
            return LLMReply("Great, I've set that up. You'll get a text with the details and a link for the first payment.",
                            offer=c["pending_offer"], intent="book_plan")

        # Naive on purpose: always proposes 2 instalments, even when the customer can't afford it.
        balance = c["balance"]
        amount = round(balance / 2, 2)
        return LLMReply(
            f"Thanks, {c['customer_first_name']}. Your balance is {cur}{balance:.2f}. "
            f"I can split that into 2 payments of {cur}{amount:.2f}. Would that work?",
            offer={"instalments": 2, "instalment_amount": amount},
            intent="propose_plan",
        )


@TTS.register("mock")
class MockTTS(TextToSpeech):
    def __init__(self, settings: Settings, **_: Any) -> None:
        pass

    def synthesize(self, text: str, language: str, voice: str) -> bytes:
        return text.encode("utf-8")  # a real provider returns audio (e.g. 8kHz mu-law for phone lines)


@VOICE.register("console")
class ConsoleVoice(VoiceChannel):
    def __init__(self, settings: Settings, **_: Any) -> None:
        pass

    def place_call(self, call_id: str, to_number: str, webhook_url: str) -> str:
        provider_id = f"console-{uuid.uuid4().hex[:10]}"
        log.info("[voice] dialing %s for %s (webhook %s) -> %s", to_number, call_id, webhook_url, provider_id)
        return provider_id

    def say(self, provider_call_id: str, text: str, audio: bytes) -> None:
        log.info("[voice] %s AGENT: %s", provider_call_id, text)

    def transfer(self, provider_call_id: str, reason: str) -> None:
        log.info("[voice] %s transferred to human queue (%s)", provider_call_id, reason)

    def hang_up(self, provider_call_id: str) -> None:
        log.info("[voice] %s hung up", provider_call_id)


@MESSAGING.register("console")
class ConsoleMessaging(MessagingChannel):
    def __init__(self, settings: Settings, **_: Any) -> None:
        pass

    def send(self, to: str, text: str, channel: MessageChannel = "sms") -> str:
        msg_id = f"msg-{uuid.uuid4().hex[:10]}"
        log.info("[%s] to %s: %s", channel, to, text)
        return msg_id


@CRMS.register("mock")
class MockCRM(CRM):
    def __init__(self, settings: Settings, **_: Any) -> None:
        self.outcomes: list[dict[str, Any]] = []

    def get_balance(self, account_id: str) -> float | None:
        return None  # use the imported balance

    def record_outcome(self, account_id: str, outcome: dict[str, Any]) -> None:
        self.outcomes.append({"account_id": account_id, **outcome})
        log.info("[crm] %s <- %s", account_id, outcome)


@PAYMENTS.register("mock")
class MockPayments(Payments):
    def __init__(self, settings: Settings, **_: Any) -> None:
        pass

    def create_payment_link(self, account_id: str, amount: float, currency: str, description: str) -> str:
        link = f"https://pay.example.com/l/{uuid.uuid4().hex[:12]}"
        log.info("[payments] %s %s%.2f '%s' -> %s", account_id, currency, amount, description, link)
        return link
