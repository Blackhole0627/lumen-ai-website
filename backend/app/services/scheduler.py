"""Picks accounts that are due for contact and starts calls, within capacity.

The pre-call gate still runs inside start_call(), so the scheduler only decides
*who is next*; the guards decide *whether a call is allowed*.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..bootstrap import Container
from ..models import AccountRecord, CallRecord
from ..timeutil import to_db
from .conversation import ConversationService

log = logging.getLogger("scheduler")


def expire_stale_calls(db: Session, now: datetime, minutes: int) -> int:
    stale = db.scalars(
        select(CallRecord).where(CallRecord.status == "in_progress", CallRecord.started_at < to_db(now - timedelta(minutes=minutes)))
    ).all()
    for call in stale:
        call.status, call.outcome, call.ended_at = "abandoned", call.outcome or "timed out", to_db(now)
    db.commit()
    return len(stale)


def run_once(db: Session, container: Container, now: datetime | None = None) -> dict[str, int]:
    now = now or container.clock()
    stats = {"expired": expire_stale_calls(db, now, container.settings.call_timeout_minutes),
             "started": 0, "blocked": 0, "errors": 0}

    in_progress = db.scalar(select(func.count()).select_from(CallRecord).where(CallRecord.status == "in_progress")) or 0
    capacity = container.settings.max_concurrent_calls - in_progress
    if capacity <= 0:
        return stats

    due = db.scalars(
        select(AccountRecord)
        .where(AccountRecord.status == "active",
               or_(AccountRecord.next_contact_after.is_(None), AccountRecord.next_contact_after <= to_db(now)))
        .order_by(AccountRecord.id)
        .limit(capacity)
    ).all()

    service = ConversationService(db, container)
    for acct in due:
        try:
            result = service.start_call(acct.id, now=now)
            stats["blocked" if result.status == "blocked" else "started"] += 1
            log.info("account %s -> %s %s", acct.id, result.status, result.findings)
        except Exception:  # noqa: BLE001 - one bad account must not stop the batch
            db.rollback()
            stats["errors"] += 1
            log.exception("could not start call for %s", acct.id)
    return stats
