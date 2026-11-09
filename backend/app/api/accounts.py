from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import AccountRecord
from ..schemas import AccountIn, AccountOut, ImportResult
from ..services import accounts

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/import", response_model=ImportResult)
def import_accounts(rows: list[AccountIn], db: Session = Depends(get_db)) -> ImportResult:
    """Create or update accounts (the lender's daily file or API sync lands here)."""
    created, updated = accounts.upsert_accounts(db, [r.model_dump() for r in rows])
    return ImportResult(created=created, updated=updated)


@router.get("", response_model=list[AccountOut])
def list_accounts(portfolio: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    q = select(AccountRecord).order_by(AccountRecord.id).limit(min(limit, 500))
    if portfolio:
        q = q.where(AccountRecord.portfolio == portfolio)
    return db.scalars(q).all()


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: str, db: Session = Depends(get_db)):
    return accounts.get_account(db, account_id)
