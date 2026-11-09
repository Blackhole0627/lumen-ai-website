"""Layer 1: decide whether we are allowed to contact this customer at all."""
from __future__ import annotations

from datetime import datetime, timezone

from .models import Account, Action, Decision, Finding, Severity
from .policy import Ruleset

GUARD = "precall"


def check_contact_allowed(account: Account, ruleset: Ruleset, now_utc: datetime | None = None) -> Decision:
    now_utc = now_utc or datetime.now(timezone.utc)
    findings: list[Finding] = []

    # 1. Hard stops from the account record (dispute, bankruptcy, deceased, ...)
    blocking = account.flags & ruleset.blocking_flags
    if blocking:
        findings.append(Finding(GUARD, "ACCOUNT_FLAG", Severity.HIGH, f"blocked by flags: {sorted(blocking)}"))

    # 2. Market must be configured; unknown market = fail closed
    market = ruleset.markets.get(account.market)
    if market is None:
        findings.append(Finding(GUARD, "MARKET_NOT_CONFIGURED", Severity.HIGH, account.market))
        return Decision(Action.BLOCK, findings)

    # 3. Calling hours and rest days in the customer's local time
    local = account.local_now(now_utc)
    start, end = market.calling_hours
    if not (start <= local.hour < end):
        findings.append(Finding(GUARD, "OUTSIDE_CALLING_HOURS", Severity.MEDIUM, f"local time {local:%H:%M}"))
    if local.weekday() in market.no_call_weekdays:
        findings.append(Finding(GUARD, "REST_DAY", Severity.MEDIUM, f"weekday {local.weekday()}"))

    # 4. Contact frequency caps
    if account.contact_attempts_7d >= market.max_attempts_7d:
        findings.append(Finding(GUARD, "FREQUENCY_CAP", Severity.MEDIUM, f"{account.contact_attempts_7d} attempts in 7 days"))
    if account.last_contact_utc:
        hours = (now_utc - account.last_contact_utc).total_seconds() / 3600
        if hours < market.min_hours_between_attempts:
            findings.append(Finding(GUARD, "TOO_SOON", Severity.LOW, f"last contact {hours:.1f}h ago"))

    if findings:
        return Decision(Action.BLOCK, findings)
    return Decision(Action.ALLOW, [Finding(GUARD, "CONTACT_ALLOWED", Severity.INFO, f"local time {local:%H:%M}")])
