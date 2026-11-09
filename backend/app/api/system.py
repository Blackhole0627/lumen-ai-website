from fastapi import APIRouter, Depends
from sqlalchemy import text

from ..bootstrap import Runtime
from ..deps import get_runtime, require_api_key
from ..providers.base import ALL_REGISTRIES
from ..state import STATE_STORES

router = APIRouter(tags=["system"])


@router.get("/health")
def health(runtime: Runtime = Depends(get_runtime)) -> dict:
    with runtime.engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "environment": runtime.settings.environment}


@router.get("/providers", dependencies=[Depends(require_api_key)])
def providers(runtime: Runtime = Depends(get_runtime)) -> dict:
    """Which implementation is active for each dependency, and which are available."""
    s = runtime.settings
    active = {"stt": s.stt_provider, "llm": s.llm_provider, "tts": s.tts_provider, "voice": s.voice_provider,
              "messaging": s.messaging_provider, "crm": s.crm_provider, "payments": s.payments_provider,
              "state_store": s.state_store}
    available = {kind: reg.names() for kind, reg in ALL_REGISTRIES.items()}
    available["state_store"] = STATE_STORES.names()
    return {"active": active, "available": available}
