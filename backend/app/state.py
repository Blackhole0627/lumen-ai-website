"""Live call state kept between turns.

A call spans many HTTP requests (one per customer utterance), possibly handled
by different processes, so its state is saved after every turn and loaded on the
next. The store is pluggable like any provider:

    memory    - single process only (tests, quick experiments)
    database  - one row per live call; works across API + worker processes
    (redis)   - add one for high call volumes: same interface, register "redis"
"""
from __future__ import annotations

import pickle
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from guardrails import CallState, PaymentPlan, Ruleset
from guardrails.audit import GENESIS
from sqlalchemy.orm import sessionmaker

from .config import Settings
from .models import CallSessionRecord
from .registry import Registry


@dataclass
class CallSession:
    call_id: str
    account_id: str
    ruleset: Ruleset                    # pinned at call start: a call never switches policy mid-way
    state: CallState                    # guardrails state (verified, vulnerability, ...)
    channel: str = "voice"
    language: str = "en-GB"
    provider_call_id: str | None = None
    history: list[tuple[str, str]] = field(default_factory=list)  # ("agent"|"customer", text) as sent to the LLM
    pending_offer: PaymentPlan | None = None
    plan_booked: bool = False
    turn_seq: int = 0
    audit_last_hash: str = GENESIS
    audit_seq: int = 0


class StateStore(ABC):
    @abstractmethod
    def load(self, call_id: str) -> CallSession | None: ...

    @abstractmethod
    def save(self, session: CallSession) -> None: ...

    @abstractmethod
    def delete(self, call_id: str) -> None: ...


STATE_STORES: Registry[StateStore] = Registry("state_store")


@STATE_STORES.register("memory")
class MemoryStateStore(StateStore):
    def __init__(self, settings: Settings, **_: Any) -> None:
        self._data: dict[str, CallSession] = {}
        self._lock = threading.Lock()

    def load(self, call_id: str) -> CallSession | None:
        with self._lock:
            return self._data.get(call_id)

    def save(self, session: CallSession) -> None:
        with self._lock:
            self._data[session.call_id] = session

    def delete(self, call_id: str) -> None:
        with self._lock:
            self._data.pop(call_id, None)


@STATE_STORES.register("database")
class DatabaseStateStore(StateStore):
    """Stores the pickled session. Only ever unpickles rows this service wrote itself."""

    def __init__(self, settings: Settings, session_factory: sessionmaker, **_: Any) -> None:
        self._sf = session_factory

    def load(self, call_id: str) -> CallSession | None:
        with self._sf() as db:
            row = db.get(CallSessionRecord, call_id)
            return pickle.loads(row.data) if row else None

    def save(self, session: CallSession) -> None:
        with self._sf() as db:
            row = db.get(CallSessionRecord, session.call_id)
            blob = pickle.dumps(session)
            if row:
                row.data = blob
            else:
                db.add(CallSessionRecord(call_id=session.call_id, data=blob))
            db.commit()

    def delete(self, call_id: str) -> None:
        with self._sf() as db:
            row = db.get(CallSessionRecord, call_id)
            if row:
                db.delete(row)
                db.commit()
