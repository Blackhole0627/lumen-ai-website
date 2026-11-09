"""Runs a conversation turn by turn, with the safety pipeline around the model.

    start_call()            pre-call gate -> dial -> opening line
    handle_customer_text()  input guard -> identity -> LLM -> offer/output guards -> speak
    hang_up()               close the call

Every turn: load session -> run guards -> save turns + audit -> save session.
"""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from guardrails import Action, AgentDraft, CallState, Decision, PaymentPlan, SafetyPipeline
from guardrails.audit import AuditLog, verify_chain
from guardrails.offer_guard import closest_compliant_plan
from guardrails.pipeline import HANDOFF_TEXT
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import prompts
from ..bootstrap import Container
from ..models import AccountRecord, AuditRecord, CallRecord, PlanRecord, TurnRecord
from ..state import CallSession
from ..timeutil import to_db
from . import accounts, policies

log = logging.getLogger("conversation")

REPEAT_PROMPT = "Sorry, I didn't catch that clearly. Could you say that again?"


class CallNotFound(Exception):
    status_code = 404


class CallClosed(Exception):
    status_code = 409


@dataclass
class TurnResult:
    call_id: str
    status: str
    agent_text: str | None
    action: str
    findings: list[str] = field(default_factory=list)
    plan: dict[str, Any] | None = None


def _codes(decision: Decision) -> list[str]:
    return [f.code for f in decision.findings]


class ConversationService:
    def __init__(self, db: Session, container: Container) -> None:
        self.db = db
        self.c = container

    # ================================================================ public API

    def start_call(self, account_id: str, channel: str = "voice", now: datetime | None = None) -> TurnResult:
        now = now or self.c.clock()
        acct = accounts.get_account(self.db, account_id)
        ruleset = policies.active_ruleset(self.db)
        live_balance = self.c.crm.get_balance(acct.id)

        call_id = f"call_{uuid.uuid4().hex[:12]}"
        state = CallState(accounts.to_guard_account(self.db, acct, now, live_balance), call_id=call_id)
        market = ruleset.markets.get(acct.market)
        session = CallSession(call_id=call_id, account_id=acct.id, ruleset=ruleset, state=state, channel=channel,
                              language=market.language if market else "en-GB")
        call = CallRecord(id=call_id, account_id=acct.id, policy_version=ruleset.version, channel=channel,
                          status="in_progress", started_at=to_db(now))
        self.db.add(call)

        if acct.status != "active":  # paused / closed by the lender
            call.status, call.outcome, call.ended_at = "blocked", f"ACCOUNT_{acct.status.upper()}", to_db(now)
            self.db.commit()
            return TurnResult(call_id, "blocked", None, "block", [call.outcome])

        pipeline, audit = self._pipeline(session)
        pre = pipeline.start_call(state, now)
        if pre.action is not Action.ALLOW:
            call.status, call.outcome, call.ended_at = "blocked", ",".join(_codes(pre)), to_db(now)
            acct.next_contact_after = to_db(now + timedelta(hours=1))
            self._persist_audit(session, audit)
            self.db.commit()
            return TurnResult(call_id, "blocked", None, pre.action.value, _codes(pre))

        webhook = f"{self.c.settings.public_base_url}/webhooks/voice/{self.c.settings.voice_provider}"
        session.provider_call_id = self.c.voice.place_call(call_id, acct.phone, webhook)
        call.provider_call_id = session.provider_call_id
        acct.next_contact_after = to_db(now + timedelta(hours=market.min_hours_between_attempts))

        # Real telephony: generate the opening line when the provider reports "answered".
        result = self._agent_turn(session, pipeline, call)
        self._finish(session, audit, call)
        return result

    def handle_customer_text(self, call_id: str, text: str, confidence: float = 1.0) -> TurnResult:
        session, call = self._load(call_id)
        pipeline, audit = self._pipeline(session)
        state = session.state

        # Low-confidence speech recognition: ask again instead of guessing at amounts or dates.
        if confidence < self.c.settings.stt_min_confidence:
            self._record_turn(session, call, "customer", None, "[unclear audio]", "rewrite", ["LOW_ASR_CONFIDENCE"])
            self._speak(session, REPEAT_PROMPT)
            self._record_turn(session, call, "agent", None, REPEAT_PROMPT, "allow", [])
            self._finish(session, audit, call)
            return TurnResult(call_id, call.status, REPEAT_PROMPT, "rewrite", ["LOW_ASR_CONFIDENCE"])

        was_verifying = state.awaiting_verification and not state.verified
        result = pipeline.on_customer_turn(state, text)
        stored_text = "[verification details redacted]" if was_verifying else text
        self._record_turn(session, call, "customer", None, stored_text, result.decision.action.value, _codes(result.decision))

        if result.llm_input is None:
            # Guard took over (crisis, opt-out, dispute, failed verification...): speak the scripted reply.
            reply = result.decision.text
            if reply:
                self._speak(session, reply)
                session.history.append(("agent", reply))
            self._record_turn(session, call, "agent", None, reply, result.decision.action.value, [])
            self._apply_status(session, call)
            self._finish(session, audit, call)
            return TurnResult(call_id, call.status, reply, result.decision.action.value, _codes(result.decision))

        session.history.append(("customer", result.llm_input))
        turn = self._agent_turn(session, pipeline, call)
        turn.findings = _codes(result.decision) + turn.findings
        self._finish(session, audit, call)
        return turn

    def hang_up(self, call_id: str, reason: str = "completed") -> TurnResult:
        call = self.db.get(CallRecord, call_id)
        if call is None:
            raise CallNotFound(call_id)
        session = self.c.state_store.load(call_id)
        if call.status == "in_progress":
            call.status = "completed"
            call.outcome = call.outcome or reason
            call.ended_at = to_db(self.c.clock())
            if session and session.provider_call_id:
                self.c.voice.hang_up(session.provider_call_id)
        self.db.commit()
        self.c.state_store.delete(call_id)
        return TurnResult(call_id, call.status, None, "end_call", [])

    def get_call(self, call_id: str) -> dict[str, Any]:
        call = self.db.get(CallRecord, call_id)
        if call is None:
            raise CallNotFound(call_id)
        turns = self.db.scalars(select(TurnRecord).where(TurnRecord.call_id == call_id).order_by(TurnRecord.seq)).all()
        audit = self.db.scalars(select(AuditRecord).where(AuditRecord.call_id == call_id).order_by(AuditRecord.seq)).all()
        plan = self.db.scalar(select(PlanRecord).where(PlanRecord.call_id == call_id))
        ok, broken = verify_chain([a.as_entry() for a in audit])
        return {
            "call": call, "turns": turns, "plan": plan,
            "audit": {"entries": len(audit), "chain_valid": ok, "first_broken_entry": broken},
        }

    # ================================================================ internals

    def _load(self, call_id: str) -> tuple[CallSession, CallRecord]:
        call = self.db.get(CallRecord, call_id)
        if call is None:
            raise CallNotFound(f"Call '{call_id}' not found")
        if call.status != "in_progress":
            raise CallClosed(f"Call '{call_id}' is {call.status}")
        session = self.c.state_store.load(call_id)
        if session is None:
            raise CallNotFound(f"No live state for call '{call_id}'")
        return session, call

    def _pipeline(self, session: CallSession) -> tuple[SafetyPipeline, AuditLog]:
        audit = AuditLog(last_hash=session.audit_last_hash, start_seq=session.audit_seq)
        return SafetyPipeline(session.ruleset, audit), audit

    def _agent_turn(self, session: CallSession, pipeline: SafetyPipeline, call: CallRecord) -> TurnResult:
        state = session.state
        try:
            reply = self.c.llm.generate(prompts.build_request(session, self.c.settings))
            draft = AgentDraft(reply.text, _to_plan(reply.offer))
        except Exception:  # noqa: BLE001 - any model failure fails closed to a human
            log.exception("LLM failed on %s", session.call_id)
            state.escalated = True
            self._speak(session, HANDOFF_TEXT)
            self._record_turn(session, call, "agent", None, HANDOFF_TEXT, "escalate", ["LLM_ERROR"])
            self._apply_status(session, call)
            return TurnResult(session.call_id, call.status, HANDOFF_TEXT, "escalate", ["LLM_ERROR"])

        decision = pipeline.on_agent_turn(state, draft)
        codes = _codes(decision)

        # Remember the plan the customer actually heard (after any guard correction).
        if draft.offer and state.verified:
            offer_issues = [f for f in decision.findings if f.guard == "offer" and f.code != "OFFER_OK"]
            session.pending_offer = closest_compliant_plan(state, session.ruleset) if offer_issues else draft.offer

        plan_out = None
        if reply.intent == "book_plan" and draft.offer and "OFFER_OK" in codes and not session.plan_booked:
            plan_out = self._book_plan(session, call, draft.offer)

        text = decision.text if decision.action is not Action.BLOCK else None
        if text:
            self._speak(session, text)
            session.history.append(("agent", text))
        self._record_turn(session, call, "agent", draft.text, text, decision.action.value, codes)
        self._apply_status(session, call)
        return TurnResult(session.call_id, call.status, text, decision.action.value, codes, plan_out)

    def _book_plan(self, session: CallSession, call: CallRecord, plan: PaymentPlan) -> dict[str, Any]:
        acct = self.db.get(AccountRecord, session.account_id)
        link = self.c.payments.create_payment_link(acct.id, plan.instalment_amount, acct.currency, f"Instalment 1 of {plan.instalments}")
        self.c.crm.record_outcome(acct.id, {
            "type": "promise_to_pay", "call_id": call.id, "instalments": plan.instalments,
            "instalment_amount": plan.instalment_amount, "policy_version": session.ruleset.version,
        })
        self.c.messaging.send(
            acct.phone,
            f"{self.c.settings.lender_name}: your plan is {plan.instalments} x {acct.currency}{plan.instalment_amount:.2f}. "
            f"Pay the first instalment here: {link}",
            channel="sms",
        )
        self.db.add(PlanRecord(call_id=call.id, account_id=acct.id, instalments=plan.instalments,
                               instalment_amount=plan.instalment_amount, currency=acct.currency,
                               policy_version=session.ruleset.version, payment_link=link))
        session.plan_booked = True
        call.outcome = "promise_to_pay"
        return {"instalments": plan.instalments, "instalment_amount": plan.instalment_amount,
                "currency": acct.currency, "payment_link": link}

    def _speak(self, session: CallSession, text: str) -> None:
        if session.provider_call_id:
            audio = self.c.tts.synthesize(text, session.language, self.c.settings.tts_voice)
            self.c.voice.say(session.provider_call_id, text, audio)

    def _apply_status(self, session: CallSession, call: CallRecord) -> None:
        if call.status != "in_progress":
            return
        state = session.state
        if state.escalated:
            call.status, call.ended_at = "escalated", to_db(self.c.clock())
            call.outcome = call.outcome or "handed to human"
            if session.provider_call_id:
                self.c.voice.transfer(session.provider_call_id, "guard escalation")
        elif state.ended:
            call.status, call.ended_at = "ended", to_db(self.c.clock())
            call.outcome = call.outcome or "ended by guard"
            if session.provider_call_id:
                self.c.voice.hang_up(session.provider_call_id)

    def _record_turn(self, session: CallSession, call: CallRecord, speaker: str, draft: str | None,
                     final: str | None, action: str, findings: list[str]) -> None:
        self.db.add(TurnRecord(call_id=call.id, seq=session.turn_seq, speaker=speaker, draft_text=draft,
                               final_text=final, action=action, findings=findings))
        session.turn_seq += 1

    def _persist_audit(self, session: CallSession, audit: AuditLog) -> None:
        for e in audit.entries:
            self.db.add(AuditRecord(call_id=e["call_id"], seq=e["seq"], ts=e["ts"], event=e["event"],
                                    ruleset_version=e["ruleset_version"], payload=e["payload"],
                                    findings=e["findings"], prev_hash=e["prev_hash"], hash=e["hash"]))
        if audit.entries:
            session.audit_last_hash = audit.entries[-1]["hash"]
            session.audit_seq = audit.entries[-1]["seq"] + 1

    def _finish(self, session: CallSession, audit: AuditLog, call: CallRecord) -> None:
        self._persist_audit(session, audit)
        self.db.commit()
        if call.status == "in_progress":
            self.c.state_store.save(session)
        else:
            self.c.state_store.delete(session.call_id)


def _to_plan(offer: dict[str, Any] | None) -> PaymentPlan | None:
    if not offer:
        return None
    return PaymentPlan(
        instalments=int(offer["instalments"]),
        instalment_amount=float(offer["instalment_amount"]),
        discount_pct=float(offer.get("discount_pct", 0.0)),
        first_payment_in_days=int(offer.get("first_payment_in_days", 0)),
    )
