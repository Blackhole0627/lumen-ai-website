"""Versioned ruleset written and approved by the client's compliance team.

The agent never decides policy. It only operates inside the ruleset that is
active for the portfolio, and every decision records the ruleset version.

NOTE: all numbers below are illustrative placeholders, not legal guidance.
Each market's real values must be set and signed off by compliance.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MarketRules:
    calling_hours: tuple[int, int]      # local time, [start, end)
    no_call_weekdays: tuple[int, ...]   # 6 = Sunday
    max_attempts_7d: int
    min_hours_between_attempts: int
    language: str


@dataclass(frozen=True)
class Ruleset:
    version: str
    approved_by: str
    approved_on: str

    # Offer limits
    max_instalments: int = 6
    min_instalment_amount: float = 10.0
    max_discount_pct: float = 0.0          # 0 = no settlement discounts allowed
    max_days_to_first_payment: int = 30
    max_affordability_ratio: float = 0.5   # in hardship, never ask for > 50% of disposable income

    # Conversation rules
    max_verification_attempts: int = 3
    must_disclose_ai: bool = True
    allow_legal_action_mention: bool = False

    # Account flags that stop all collection contact
    blocking_flags: frozenset[str] = frozenset({"dispute", "bankruptcy", "deceased", "cease_contact", "do_not_call"})

    markets: dict[str, MarketRules] = field(default_factory=dict)


DEFAULT_RULESET = Ruleset(
    version="policy-v18",
    approved_by="compliance@client.example",
    approved_on="2026-10-02",
    max_instalments=4,
    min_instalment_amount=20.0,
    markets={
        "GB": MarketRules(calling_hours=(8, 21), no_call_weekdays=(6,), max_attempts_7d=7, min_hours_between_attempts=4, language="en-GB"),
        "ES": MarketRules(calling_hours=(9, 21), no_call_weekdays=(5, 6), max_attempts_7d=3, min_hours_between_attempts=24, language="es-ES"),
        "DE": MarketRules(calling_hours=(8, 20), no_call_weekdays=(6,), max_attempts_7d=5, min_hours_between_attempts=8, language="de-DE"),
    },
)
