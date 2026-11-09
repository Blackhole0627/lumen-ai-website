"""Core data types shared by every guard in the pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum, IntEnum


class Action(str, Enum):
    """What the pipeline should do with a call or a message."""

    ALLOW = "allow"        # pass through unchanged
    REWRITE = "rewrite"    # replace with a safe, compliant alternative
    BLOCK = "block"        # do not call / do not send
    ESCALATE = "escalate"  # hand over to a human agent
    END_CALL = "end_call"  # close the conversation politely

    @property
    def priority(self) -> int:
        # When several guards disagree, the most protective action wins.
        return {"allow": 0, "rewrite": 1, "block": 2, "end_call": 3, "escalate": 4}[self.value]


class Severity(IntEnum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Finding:
    """One thing a guard noticed. Findings are always written to the audit log."""

    guard: str
    code: str
    severity: Severity
    detail: str = ""


@dataclass
class Decision:
    action: Action
    findings: list[Finding] = field(default_factory=list)
    text: str | None = None  # final text to speak/send when ALLOW or REWRITE

    @staticmethod
    def allow(text: str | None = None) -> "Decision":
        return Decision(Action.ALLOW, text=text)

    def merge(self, other: "Decision") -> "Decision":
        """Combine two decisions; the stricter action and its text win."""
        stricter = other if other.action.priority > self.action.priority else self
        return Decision(stricter.action, self.findings + other.findings, stricter.text or self.text)


# ---------------------------------------------------------------- domain objects

@dataclass
class Account:
    account_id: str
    customer_name: str
    balance: float
    currency: str
    market: str                      # e.g. "GB", "ES"
    utc_offset_hours: int            # customer's local offset (use real tz data in production)
    dob: str                         # "YYYY-MM-DD"
    postcode: str
    monthly_disposable_income: float | None = None
    flags: set[str] = field(default_factory=set)  # dispute, bankruptcy, deceased, cease_contact, do_not_call
    contact_attempts_7d: int = 0
    last_contact_utc: datetime | None = None

    def local_now(self, now_utc: datetime | None = None) -> datetime:
        now_utc = now_utc or datetime.now(timezone.utc)
        return now_utc + timedelta(hours=self.utc_offset_hours)


@dataclass
class PaymentPlan:
    """Structured offer the LLM must emit separately from its spoken text."""

    instalments: int
    instalment_amount: float
    discount_pct: float = 0.0
    first_payment_in_days: int = 0

    @property
    def total(self) -> float:
        return round(self.instalments * self.instalment_amount, 2)


@dataclass
class AgentDraft:
    """What the LLM proposes to say next, before any guard has seen it."""

    text: str
    offer: PaymentPlan | None = None


@dataclass
class CallState:
    """Everything the guards need to know about the conversation so far."""

    account: Account
    call_id: str
    verified: bool = False
    awaiting_verification: bool = False  # the agent has just asked for DOB/postcode
    verification_attempts: int = 0
    third_party: bool = False
    ai_disclosed: bool = False
    vulnerability: set[str] = field(default_factory=set)
    affordability_mode: bool = False
    escalated: bool = False
    ended: bool = False
    turn: int = 0
