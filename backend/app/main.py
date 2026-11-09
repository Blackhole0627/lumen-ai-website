"""FastAPI app factory.

Run:  uvicorn app.main:create_app --factory --reload
Docs: http://localhost:8000/docs
"""
from __future__ import annotations

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from .api import accounts, calls, policies, system, webhooks
from .bootstrap import build_runtime
from .config import Settings, get_settings
from .deps import require_api_key
from .services.accounts import AccountNotFound
from .services.conversation import CallClosed, CallNotFound
from .services.policies import PolicyError


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="Collections Agent Backend", version="0.1.0")
    app.state.runtime = build_runtime(settings)

    # Domain errors carry their own HTTP status code.
    @app.exception_handler(AccountNotFound)
    @app.exception_handler(CallNotFound)
    @app.exception_handler(CallClosed)
    @app.exception_handler(PolicyError)
    async def domain_error(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=getattr(exc, "status_code", 400), content={"detail": str(exc)})

    protected = [Depends(require_api_key)]
    app.include_router(system.router)
    app.include_router(webhooks.router)  # authenticated by vendor signature, not API key
    app.include_router(accounts.router, dependencies=protected)
    app.include_router(policies.router, dependencies=protected)
    app.include_router(calls.router, dependencies=protected)
    return app
