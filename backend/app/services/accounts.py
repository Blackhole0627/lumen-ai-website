"""Account import and conversion to the guardrails Account type."""
from __future__ import annotations

from datetime import datetime, timedelta

from guardrails import Account
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import AccountRecord, CallRecord
from ..timeutil import from_db, to_db


class AccountNotFound(Exception):
    status_code = 404


def upsert_accounts(db: Session, rows: list[dict]) -> tuple[int, int]:
    created = updated = 0
    for row in rows:
        rec = db.get(AccountRecord, row["id"])
        if rec is None:
            db.add(AccountRecord(**row))
            created += 1
        else:
            for key, value in row.items():
                setattr(rec, key, value)
            updated += 1
    db.commit()
    return created, updated


def get_account(db: Session, account_id: str) -> AccountRecord:
    rec = db.get(AccountRecord, account_id)
    if rec is None:
        raise AccountNotFound(f"Account '{account_id}' not found")
    return rec


def to_guard_account(db: Session, rec: AccountRecord, now: datetime, live_balance: float | None = None) -> Account:
    """Contact history is derived from the calls table, so it can't drift out of sync."""
    real_calls = (CallRecord.account_id == rec.id) & (CallRecord.status != "blocked")
    attempts_7d = db.scalar(
        select(func.count()).select_from(CallRecord).where(real_calls, CallRecord.started_at >= to_db(now - timedelta(days=7)))
    ) or 0
    last_contact = db.scalar(select(func.max(CallRecord.started_at)).where(real_calls))

    return Account(
        account_id=rec.id,
        customer_name=rec.customer_name,
        balance=live_balance if live_balance is not None else rec.balance,
        currency=rec.currency,
        market=rec.market,
        utc_offset_hours=rec.utc_offset_hours,
        dob=rec.dob,
        postcode=rec.postcode,
        monthly_disposable_income=rec.monthly_disposable_income,
        flags=set(rec.flags or []),
        contact_attempts_7d=attempts_7d,
        last_contact_utc=from_db(last_contact),
    )
