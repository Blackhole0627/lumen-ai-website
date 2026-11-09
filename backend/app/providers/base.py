"""Interfaces for every external service, plus one registry per interface.

Services only depend on these interfaces. Each concrete vendor (or mock) lives in
its own module and registers itself under a name; config picks the name.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal

from ..registry import Registry


# ----------------------------------------------------------------- speech-to-text

@dataclass
class Transcript:
    text: str
    confidence: float = 1.0  # 0..1; low values trigger "could you repeat that?"


class SpeechToText(ABC):
    @abstractmethod
    def transcribe(self, audio: bytes, language: str) -> Transcript: ...


# ----------------------------------------------------------------- language model

@dataclass
class LLMRequest:
    system: str                         # rules and persona
    messages: list[dict[str, str]]      # [{"role": "user"|"assistant", "content": "..."}]
    context: dict[str, Any] = field(default_factory=dict)  # current facts (verified, balance, ...)


@dataclass
class LLMReply:
    text: str                                   # what the agent wants to say
    offer: dict[str, Any] | None = None         # {"instalments": int, "instalment_amount": float, ...}
    intent: str = "chat"                        # greet | verify | propose_plan | book_plan | wrap_up | chat


class LanguageModel(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMReply:
        """Return the next agent turn. Raise on any failure: the caller fails closed to a human."""


# ----------------------------------------------------------------- text-to-speech

class TextToSpeech(ABC):
    @abstractmethod
    def synthesize(self, text: str, language: str, voice: str) -> bytes: ...


# ----------------------------------------------------------------- channels

class VoiceChannel(ABC):
    """Telephony provider: places calls and plays audio. Customer speech comes back via webhook."""

    @abstractmethod
    def place_call(self, call_id: str, to_number: str, webhook_url: str) -> str:
        """Start an outbound call. Returns the provider's own call id."""

    @abstractmethod
    def say(self, provider_call_id: str, text: str, audio: bytes) -> None: ...

    @abstractmethod
    def transfer(self, provider_call_id: str, reason: str) -> None:
        """Hand the live call to a human agent queue."""

    @abstractmethod
    def hang_up(self, provider_call_id: str) -> None: ...


MessageChannel = Literal["sms", "whatsapp", "email"]


class MessagingChannel(ABC):
    @abstractmethod
    def send(self, to: str, text: str, channel: MessageChannel = "sms") -> str:
        """Send a message. Returns the provider's message id."""


# ----------------------------------------------------------------- lender systems

class CRM(ABC):
    @abstractmethod
    def get_balance(self, account_id: str) -> float | None:
        """Live balance from the lender's system, or None to use the imported balance."""

    @abstractmethod
    def record_outcome(self, account_id: str, outcome: dict[str, Any]) -> None: ...


class Payments(ABC):
    @abstractmethod
    def create_payment_link(self, account_id: str, amount: float, currency: str, description: str) -> str: ...


# ----------------------------------------------------------------- registries

STT: Registry[SpeechToText] = Registry("stt")
LLMS: Registry[LanguageModel] = Registry("llm")
TTS: Registry[TextToSpeech] = Registry("tts")
VOICE: Registry[VoiceChannel] = Registry("voice")
MESSAGING: Registry[MessagingChannel] = Registry("messaging")
CRMS: Registry[CRM] = Registry("crm")
PAYMENTS: Registry[Payments] = Registry("payments")

ALL_REGISTRIES = {r.kind: r for r in (STT, LLMS, TTS, VOICE, MESSAGING, CRMS, PAYMENTS)}
