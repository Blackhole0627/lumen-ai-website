from dataclasses import asdict

from fastapi import APIRouter, Depends

from ..deps import get_conversation
from ..schemas import CallDetail, CallStart, CustomerTurnIn, TurnOut
from ..services.conversation import ConversationService

router = APIRouter(prefix="/calls", tags=["calls"])


@router.post("", response_model=TurnOut, status_code=201)
def start_call(body: CallStart, service: ConversationService = Depends(get_conversation)):
    """Run the pre-call gate, dial, and return the agent's opening line (or why it was blocked)."""
    return asdict(service.start_call(body.account_id, body.channel))


@router.post("/{call_id}/turns", response_model=TurnOut)
def customer_turn(call_id: str, body: CustomerTurnIn, service: ConversationService = Depends(get_conversation)):
    """Simulate the customer speaking. In production the telephony webhook calls the same code."""
    return asdict(service.handle_customer_text(call_id, body.text, body.confidence))


@router.post("/{call_id}/hangup", response_model=TurnOut)
def hang_up(call_id: str, service: ConversationService = Depends(get_conversation)):
    return asdict(service.hang_up(call_id))


@router.get("/{call_id}", response_model=CallDetail)
def get_call(call_id: str, service: ConversationService = Depends(get_conversation)):
    """Transcript (with the AI's rejected drafts), plan, and audit-chain check."""
    return service.get_call(call_id)
