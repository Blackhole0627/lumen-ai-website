"""Load an approved policy and sample accounts so you can try a call immediately.

Run:  python -m app.seed
Safe to run more than once.
"""
from __future__ import annotations

from guardrails import DEFAULT_RULESET
from sqlalchemy import select
from sqlalchemy.orm import Session

from .bootstrap import build_runtime
from .config import get_settings
from .models import PolicyRecord
from .services import accounts, policies

SAMPLE_ACCOUNTS = [
    dict(id="ACC-1001", customer_name="Daniel Hughes", phone="+447700900412", balance=240.0, currency="£",
         market="GB", utc_offset_hours=0, dob="1990-03-14", postcode="LS6 1AB", monthly_disposable_income=150.0),
    dict(id="ACC-1002", customer_name="Lucía Romero", phone="+34600000123", balance=460.0, currency="€",
         market="ES", utc_offset_hours=1, dob="1988-03-02", postcode="28004", monthly_disposable_income=300.0),
    dict(id="ACC-1003", customer_name="Priya Shah", phone="+447700900555", balance=120.0, currency="£",
         market="GB", utc_offset_hours=0, dob="1979-11-30", postcode="M1 2AB", flags=["dispute"]),
]


def seed(db: Session) -> dict[str, int]:
    added_policy = 0
    if not db.scalar(select(PolicyRecord).where(PolicyRecord.version == DEFAULT_RULESET.version)):
        policies.create_draft(db, DEFAULT_RULESET.version, policies.rules_from_ruleset(DEFAULT_RULESET), "seed-author")
        policies.approve(db, DEFAULT_RULESET.version, "seed-approver")
        added_policy = 1
    created, updated = accounts.upsert_accounts(db, [dict(a) for a in SAMPLE_ACCOUNTS])
    return {"policies": added_policy, "accounts_created": created, "accounts_updated": updated}


if __name__ == "__main__":
    runtime = build_runtime(get_settings())
    with runtime.session_factory() as session:
        print(seed(session))
