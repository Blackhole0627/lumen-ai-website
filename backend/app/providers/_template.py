"""TEMPLATE: how to plug in a real vendor. This file is not imported.

Three steps:
  1. Copy this file to e.g. app/providers/myvendor_llm.py and fill in generate().
  2. Import the new module in app/providers/__init__.py so it registers itself.
  3. Set LLM_PROVIDER=myvendor (and LLM_API_KEY / LLM_MODEL) in .env.

The same pattern works for every interface in base.py: STT, TTS, VOICE,
MESSAGING, CRMS, PAYMENTS.
"""
from __future__ import annotations

import json
from typing import Any

from ..config import Settings
from .base import LLMS, LanguageModel, LLMReply, LLMRequest


@LLMS.register("myvendor")
class MyVendorLLM(LanguageModel):
    def __init__(self, settings: Settings, **_: Any) -> None:
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY is required for the myvendor provider")
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.timeout = settings.llm_timeout_seconds
        # self.client = VendorSDK(api_key=self.api_key, timeout=self.timeout)

    def generate(self, request: LLMRequest) -> LLMReply:
        # 1. Send request.system as the system prompt, request.messages as the conversation,
        #    and request.context as a short "current facts" note.
        # 2. Ask for JSON only: {"say": str, "offer": {...} | null, "intent": str}
        #    (use the vendor's structured-output / JSON mode if it has one).
        # 3. Parse strictly. Raise on anything unexpected: the conversation service
        #    then fails closed and hands the call to a human.
        raw = "..."  # = self.client.<vendor call>(...)
        data = json.loads(raw)
        return LLMReply(text=data["say"], offer=data.get("offer"), intent=data.get("intent", "chat"))
