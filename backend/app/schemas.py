"""Request and response bodies (validated by FastAPI, shown at /docs)."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ----------------------------------------------------------------- accounts

class AccountIn(BaseModel):
    id: str = Field(min_length=1, max_length=64, examples=["ACC-1001"])
    portfolio: str = "default"
    customer_name: str
    phone: str = Field(examples=["+447700900412"])
    email: str | None = None
    balance: float = Field(gt=0)
    currency: str = "£"
    market: str = Field(pattern=r"^[A-Z]{2}$", examples=["GB"])
    utc_offset_hours: int = Field(0, ge=-12, le=14)
    dob: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", examples=["1990-03-14"])
    postcode: str
    monthly_disposable_income: float | None = None
    flags: list[str] = []
    status: Literal["active", "paused", "closed"] = "active"


class AccountOut(BaseModel):
    """No date of birth or postcode in responses."""

    model_config = ConfigDict(from_attributes=True)
    id: str
    portfolio: str
    customer_name: str
    balance: float
    currency: str
    market: str
    flags: list[str]
    status: str
    next_contact_after: datetime | None


class ImportResult(BaseModel):
    created: int
    updated: int


# ----------------------------------------------------------------- policies

class MarketRulesIn(BaseModel):
    calling_hours: tuple[int, int] = Field(examples=[[8, 21]])
    no_call_weekdays: list[int] = Field(default_factory=list, description="0=Mon ... 6=Sun")
    max_attempts_7d: int = Field(ge=0)
    min_hours_between_attempts: int = Field(ge=0)
    language: str = "en-GB"


class PolicyRulesIn(BaseModel):
    max_instalments: int = Field(ge=1)
    min_instalment_amount: float = Field(ge=0)
    max_discount_pct: float = Field(0, ge=0, le=100)
    max_days_to_first_payment: int = Field(30, ge=0)
    max_affordability_ratio: float = Field(0.5, gt=0, le=1)
    max_verification_attempts: int = Field(3, ge=1)
    must_disclose_ai: bool = True
    allow_legal_action_mention: bool = False
    blocking_flags: list[str] = ["dispute", "bankruptcy", "deceased", "cease_contact", "do_not_call"]
    markets: dict[str, MarketRulesIn]


class PolicyCreate(BaseModel):
    version: str = Field(examples=["policy-v19"])
    created_by: str
    rules: PolicyRulesIn


class PolicyApprove(BaseModel):
    approved_by: str


class PolicyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    version: str
    status: str
    created_by: str
    approved_by: str | None
    created_at: datetime
    approved_at: datetime | None
    rules: dict


# ----------------------------------------------------------------- calls

class CallStart(BaseModel):
    account_id: str
    channel: Literal["voice"] = "voice"


class CustomerTurnIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    confidence: float = Field(1.0, ge=0, le=1, description="Speech-recognition confidence")


class PlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    instalments: int
    instalment_amount: float
    currency: str
    payment_link: str | None = None


class TurnOut(BaseModel):
    call_id: str
    status: str
    agent_text: str | None
    action: str
    findings: list[str]
    plan: PlanOut | None = None


class TurnRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    seq: int
    speaker: str
    draft_text: str | None
    final_text: str | None
    action: str
    findings: list[str]


class CallOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    policy_version: str
    status: str
    outcome: str | None
    started_at: datetime
    ended_at: datetime | None


class AuditSummary(BaseModel):
    entries: int
    chain_valid: bool
    first_broken_entry: int | None


class CallDetail(BaseModel):
    call: CallOut
    turns: list[TurnRecordOut]
    plan: PlanOut | None
    audit: AuditSummary


# ----------------------------------------------------------------- webhooks

class VoiceWebhookIn(BaseModel):
    """Generic shape. Each telephony vendor's payload is mapped to this in its adapter."""

    provider_call_id: str
    event: Literal["speech", "hangup"]
    transcript: str | None = None
    confidence: float = 1.0
