"""Policy (rulebook) versions with maker-checker approval.

One person drafts a version, a different person approves it. The newest approved
version is the one new calls use; each call pins the version it started with.
"""
from __future__ import annotations

from dataclasses import asdict

from guardrails import Ruleset
from guardrails.policy import MarketRules
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import PolicyRecord
from ..timeutil import from_db, now_utc, to_db


class PolicyError(Exception):
    status_code = 400


class PolicyNotFound(PolicyError):
    status_code = 404


class ApprovalNotAllowed(PolicyError):
    status_code = 403


class NoActivePolicy(PolicyError):
    status_code = 503


def rules_from_ruleset(rs: Ruleset) -> dict:
    """Ruleset dataclass -> JSON-friendly dict (used for seeding)."""
    data = asdict(rs)
    for key in ("version", "approved_by", "approved_on"):
        data.pop(key)
    data["blocking_flags"] = sorted(rs.blocking_flags)
    data["markets"] = {code: asdict(m) for code, m in rs.markets.items()}
    return data


def ruleset_from_record(rec: PolicyRecord) -> Ruleset:
    r = dict(rec.rules)
    markets = {
        code: MarketRules(
            calling_hours=tuple(m["calling_hours"]),
            no_call_weekdays=tuple(m["no_call_weekdays"]),
            max_attempts_7d=m["max_attempts_7d"],
            min_hours_between_attempts=m["min_hours_between_attempts"],
            language=m["language"],
        )
        for code, m in r.pop("markets").items()
    }
    blocking = frozenset(r.pop("blocking_flags"))
    approved_on = from_db(rec.approved_at).date().isoformat() if rec.approved_at else ""
    return Ruleset(version=rec.version, approved_by=rec.approved_by or "", approved_on=approved_on,
                   blocking_flags=blocking, markets=markets, **r)


def create_draft(db: Session, version: str, rules: dict, created_by: str) -> PolicyRecord:
    if db.scalar(select(PolicyRecord).where(PolicyRecord.version == version)):
        raise PolicyError(f"Policy version '{version}' already exists")
    rec = PolicyRecord(version=version, rules=rules, created_by=created_by, status="draft")
    db.add(rec)
    db.commit()
    return rec


def approve(db: Session, version: str, approved_by: str) -> PolicyRecord:
    rec = db.scalar(select(PolicyRecord).where(PolicyRecord.version == version))
    if rec is None:
        raise PolicyNotFound(f"Policy version '{version}' not found")
    if rec.status != "draft":
        raise PolicyError(f"Policy '{version}' is {rec.status}, only drafts can be approved")
    if approved_by.strip().lower() == rec.created_by.strip().lower():
        raise ApprovalNotAllowed("The approver must be a different person from the author")
    rec.status, rec.approved_by, rec.approved_at = "approved", approved_by, to_db(now_utc())
    db.commit()
    return rec


def active_record(db: Session) -> PolicyRecord:
    rec = db.scalar(
        select(PolicyRecord).where(PolicyRecord.status == "approved")
        .order_by(PolicyRecord.approved_at.desc(), PolicyRecord.id.desc()).limit(1)
    )
    if rec is None:
        raise NoActivePolicy("No approved policy. Create one and have a second person approve it.")
    return rec


def active_ruleset(db: Session) -> Ruleset:
    return ruleset_from_record(active_record(db))
