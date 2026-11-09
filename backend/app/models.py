"""Database tables.

    accounts        customers to contact (imported from the lender)
    policies        versioned rulebooks, approved by a second person
    calls           one row per conversation attempt
    turns           what was said, including the AI's rejected drafts
    audit_events    hash-chained guard decisions (copied from the guardrails AuditLog)
    payment_plans   agreed plans / promises to pay
    call_sessions   live call state between turns (used by the "database" state store)
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base
from .timeutil import now_utc, to_db


def _now() -> datetime:
    return to_db(now_utc())


class AccountRecord(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # lender's account reference
    portfolio: Mapped[str] = mapped_column(String(64), default="default", index=True)
    customer_name: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(32))
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    balance: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(8), default="£")
    market: Mapped[str] = mapped_column(String(2), index=True)
    utc_offset_hours: Mapped[int] = mapped_column(Integer, default=0)
    # Verification data. Encrypt these columns at rest in production.
    dob: Mapped[str] = mapped_column(String(10))
    postcode: Mapped[str] = mapped_column(String(16))
    monthly_disposable_income: Mapped[float | None] = mapped_column(Float, nullable=True)
    flags: Mapped[list] = mapped_column(JSON, default=list)  # dispute, bankruptcy, deceased, ...
    status: Mapped[str] = mapped_column(String(16), default="active", index=True)  # active | paused | closed
    next_contact_after: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class PolicyRecord(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String(32), unique=True)
    rules: Mapped[dict] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(16), default="draft")  # draft | approved | retired
    created_by: Mapped[str] = mapped_column(String(120))
    approved_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class CallRecord(Base):
    __tablename__ = "calls"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), index=True)
    provider_call_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    policy_version: Mapped[str] = mapped_column(String(32))
    channel: Mapped[str] = mapped_column(String(16), default="voice")
    # in_progress | completed | escalated | ended | blocked | abandoned
    status: Mapped[str] = mapped_column(String(16), default="in_progress", index=True)
    outcome: Mapped[str | None] = mapped_column(String(200), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=_now, index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class TurnRecord(Base):
    __tablename__ = "turns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    call_id: Mapped[str] = mapped_column(ForeignKey("calls.id"), index=True)
    seq: Mapped[int] = mapped_column(Integer)
    speaker: Mapped[str] = mapped_column(String(16))           # agent | customer
    draft_text: Mapped[str | None] = mapped_column(Text, nullable=True)  # what the AI wanted to say
    final_text: Mapped[str | None] = mapped_column(Text, nullable=True)  # what was actually said
    action: Mapped[str] = mapped_column(String(16))
    findings: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class AuditRecord(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    call_id: Mapped[str] = mapped_column(String(40), index=True)
    seq: Mapped[int] = mapped_column(Integer)
    ts: Mapped[str] = mapped_column(String(40))  # kept as the exact string that was hashed
    event: Mapped[str] = mapped_column(String(32))
    ruleset_version: Mapped[str] = mapped_column(String(32))
    payload: Mapped[dict] = mapped_column(JSON)
    findings: Mapped[list] = mapped_column(JSON)
    prev_hash: Mapped[str] = mapped_column(String(64))
    hash: Mapped[str] = mapped_column(String(64), unique=True)

    def as_entry(self) -> dict:
        return {
            "seq": self.seq, "ts": self.ts, "call_id": self.call_id, "event": self.event,
            "ruleset_version": self.ruleset_version, "payload": self.payload,
            "findings": self.findings, "prev_hash": self.prev_hash, "hash": self.hash,
        }


class PlanRecord(Base):
    __tablename__ = "payment_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    call_id: Mapped[str] = mapped_column(ForeignKey("calls.id"), index=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), index=True)
    instalments: Mapped[int] = mapped_column(Integer)
    instalment_amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(8))
    policy_version: Mapped[str] = mapped_column(String(32))
    payment_link: Mapped[str | None] = mapped_column(String(300), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="active")  # active | completed | broken
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class CallSessionRecord(Base):
    __tablename__ = "call_sessions"

    call_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    data: Mapped[bytes] = mapped_column(LargeBinary)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)
