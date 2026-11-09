from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..bootstrap import Runtime
from ..deps import get_db, get_runtime, verify_webhook_signature
from ..models import CallRecord
from ..schemas import VoiceWebhookIn
from ..services.conversation import ConversationService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/voice/{provider}")
def voice_webhook(provider: str, body: VoiceWebhookIn, request: Request,
                  db: Session = Depends(get_db), runtime: Runtime = Depends(get_runtime)) -> dict:
    """Telephony provider -> us: the customer said something, or hung up.

    Uses the provider's signature instead of X-API-Key, because the vendor calls it.
    """
    verify_webhook_signature(provider, request)
    call = db.scalar(select(CallRecord).where(CallRecord.provider_call_id == body.provider_call_id))
    if call is None:
        raise HTTPException(404, "Unknown provider_call_id")

    service = ConversationService(db, runtime.container)
    if body.event == "hangup":
        service.hang_up(call.id, reason="customer hung up")
        return {"ok": True}

    result = service.handle_customer_text(call.id, body.transcript or "", body.confidence)
    return {"say": result.agent_text, "action": result.action, "status": result.status}
