"""FastAPI dependencies: runtime, DB session, auth, services."""
from __future__ import annotations

import hmac
from typing import Iterator

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from .bootstrap import Runtime
from .services.conversation import ConversationService


def get_runtime(request: Request) -> Runtime:
    return request.app.state.runtime


def get_db(runtime: Runtime = Depends(get_runtime)) -> Iterator[Session]:
    with runtime.session_factory() as db:
        yield db


def get_conversation(db: Session = Depends(get_db), runtime: Runtime = Depends(get_runtime)) -> ConversationService:
    return ConversationService(db, runtime.container)


def require_api_key(x_api_key: str | None = Header(default=None), runtime: Runtime = Depends(get_runtime)) -> None:
    expected = runtime.settings.api_key
    if not x_api_key or not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid X-API-Key header")


def verify_webhook_signature(provider: str, request: Request) -> None:
    """Every telephony vendor signs its webhooks differently. Implement per vendor before going live:
    read the signature header, recompute it with the shared secret, compare with hmac.compare_digest."""
    return None
