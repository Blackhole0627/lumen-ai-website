"""Layer 4: validate any payment offer against the approved ruleset.

The LLM must return offers as structured data (PaymentPlan), never only as free
text. That makes them checkable: if an offer breaks a rule, it's replaced with
the closest compliant plan before the customer hears it.
"""
from __future__ import annotations

import math

from .models import Account, Action, CallState, Decision, Finding, PaymentPlan, Severity
from .policy import Ruleset

GUARD = "offer"


def affordable_monthly_cap(account: Account, ruleset: Ruleset) -> float | None:
    if account.monthly_disposable_income is None:
        return None
    return round(account.monthly_disposable_income * ruleset.max_affordability_ratio, 2)


def validate_offer(plan: PaymentPlan, state: CallState, ruleset: Ruleset) -> list[Finding]:
    acct = state.account
    issues: list[Finding] = []

    def flag(code: str, detail: str, sev: Severity = Severity.HIGH) -> None:
        issues.append(Finding(GUARD, code, sev, detail))

    if plan.instalments < 1 or plan.instalments > ruleset.max_instalments:
        flag("TOO_MANY_INSTALMENTS", f"{plan.instalments} > max {ruleset.max_instalments}")
    if plan.instalment_amount < ruleset.min_instalment_amount:
        flag("INSTALMENT_TOO_SMALL", f"{plan.instalment_amount} < min {ruleset.min_instalment_amount}")
    if plan.discount_pct > ruleset.max_discount_pct:
        flag("DISCOUNT_NOT_ALLOWED", f"{plan.discount_pct}% > max {ruleset.max_discount_pct}%")
    if plan.first_payment_in_days > ruleset.max_days_to_first_payment:
        flag("FIRST_PAYMENT_TOO_LATE", f"{plan.first_payment_in_days} days")

    expected_total = round(acct.balance * (1 - plan.discount_pct / 100), 2)
    if abs(plan.total - expected_total) > 0.05 * plan.instalments:  # allow rounding cents
        flag("TOTAL_MISMATCH", f"plan total {plan.total} vs balance due {expected_total}")

    if state.affordability_mode:
        cap = affordable_monthly_cap(acct, ruleset)
        if cap is None:
            flag("AFFORDABILITY_UNKNOWN", "hardship detected but no income/expenditure on file", Severity.MEDIUM)
        elif plan.instalment_amount > cap:
            flag("UNAFFORDABLE", f"{plan.instalment_amount} > affordable {cap}")

    return issues


def closest_compliant_plan(state: CallState, ruleset: Ruleset) -> PaymentPlan | None:
    """Find the plan with the fewest instalments that satisfies every rule."""
    balance = state.account.balance
    cap = affordable_monthly_cap(state.account, ruleset) if state.affordability_mode else None
    for n in range(1, ruleset.max_instalments + 1):
        amount = math.ceil(balance / n * 100) / 100
        if amount < ruleset.min_instalment_amount and n > 1:
            break
        if cap is None or amount <= cap:
            return PaymentPlan(instalments=n, instalment_amount=amount)
    return None  # nothing compliant: needs a human


def check_offer(plan: PaymentPlan | None, state: CallState, ruleset: Ruleset) -> Decision:
    if plan is None:
        return Decision.allow()
    if not state.verified:
        return Decision(Action.BLOCK, [Finding(GUARD, "OFFER_BEFORE_VERIFICATION", Severity.CRITICAL)])

    issues = validate_offer(plan, state, ruleset)
    if not issues:
        return Decision(Action.ALLOW, [Finding(GUARD, "OFFER_OK", Severity.INFO, f"{plan.instalments} x {plan.instalment_amount}")])

    alt = closest_compliant_plan(state, ruleset)
    if alt is None:
        state.escalated = True
        return Decision(Action.ESCALATE, issues + [Finding(GUARD, "NO_COMPLIANT_PLAN", Severity.HIGH)],
                        "I want to make sure we find something that works for you, so I'm passing you to a specialist who can look at more options.")

    cur = state.account.currency
    text = (f"Based on what you've told me, I can offer {alt.instalments} payment{'s' if alt.instalments > 1 else ''} "
            f"of {cur}{alt.instalment_amount:.2f}. Would that work for you?")
    return Decision(Action.REWRITE, issues, text)
