"""Builds everything the app needs from Settings, in one place.

Both the API (main.py) and the worker (worker.py) start from build_runtime(), so
they always use the same providers, database and state store.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from . import providers  # noqa: F401  (import registers all providers)
from .config import Settings
from .db import Base, make_engine, make_session_factory
from .providers.base import CRM, CRMS, LLMS, MESSAGING, PAYMENTS, STT, TTS, VOICE
from .providers.base import LanguageModel, MessagingChannel, Payments, SpeechToText, TextToSpeech, VoiceChannel
from .state import STATE_STORES, StateStore
from .timeutil import now_utc


@dataclass
class Container:
    """The selected implementation of every external dependency."""

    settings: Settings
    stt: SpeechToText
    llm: LanguageModel
    tts: TextToSpeech
    voice: VoiceChannel
    messaging: MessagingChannel
    crm: CRM
    payments: Payments
    state_store: StateStore
    clock: Callable[[], datetime] = field(default=now_utc)  # override in tests


@dataclass
class Runtime:
    settings: Settings
    engine: Engine
    session_factory: sessionmaker
    container: Container


def _clock(settings: Settings) -> Callable[[], datetime]:
    if not settings.clock_override:
        return now_utc
    if settings.environment == "production":
        raise RuntimeError("CLOCK_OVERRIDE is for local testing and is not allowed in production")
    fixed = datetime.fromisoformat(settings.clock_override.replace("Z", "+00:00"))
    if fixed.tzinfo is None:
        fixed = fixed.replace(tzinfo=timezone.utc)
    logging.getLogger("bootstrap").warning("CLOCK_OVERRIDE active: the app thinks it is %s", fixed.isoformat())
    return lambda: fixed


def build_container(settings: Settings, session_factory: sessionmaker) -> Container:
    s = settings
    return Container(
        clock=_clock(s),
        settings=s,
        stt=STT.create(s.stt_provider, settings=s),
        llm=LLMS.create(s.llm_provider, settings=s),
        tts=TTS.create(s.tts_provider, settings=s),
        voice=VOICE.create(s.voice_provider, settings=s),
        messaging=MESSAGING.create(s.messaging_provider, settings=s),
        crm=CRMS.create(s.crm_provider, settings=s),
        payments=PAYMENTS.create(s.payments_provider, settings=s),
        state_store=STATE_STORES.create(s.state_store, settings=s, session_factory=session_factory),
    )


def build_runtime(settings: Settings) -> Runtime:
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    if settings.environment == "production" and settings.api_key == "change-me":
        raise RuntimeError("Set API_KEY before running in production")

    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)  # swap for Alembic migrations once the schema settles
    session_factory = make_session_factory(engine)
    return Runtime(settings, engine, session_factory, build_container(settings, session_factory))
