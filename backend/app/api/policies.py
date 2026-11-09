from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import PolicyRecord
from ..schemas import PolicyApprove, PolicyCreate, PolicyOut
from ..services import policies

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("", response_model=PolicyOut, status_code=201)
def create_policy(body: PolicyCreate, db: Session = Depends(get_db)):
    """Create a draft rulebook version. It has no effect until someone else approves it."""
    return policies.create_draft(db, body.version, body.rules.model_dump(), body.created_by)


@router.post("/{version}/approve", response_model=PolicyOut)
def approve_policy(version: str, body: PolicyApprove, db: Session = Depends(get_db)):
    return policies.approve(db, version, body.approved_by)


@router.get("", response_model=list[PolicyOut])
def list_policies(db: Session = Depends(get_db)):
    return db.scalars(select(PolicyRecord).order_by(PolicyRecord.id.desc())).all()


@router.get("/active", response_model=PolicyOut)
def active_policy(db: Session = Depends(get_db)):
    return policies.active_record(db)
