"""Layer 3: inspect what the CUSTOMER said before the LLM sees it.

Detects situations where the agent must change course regardless of what the
LLM would like to do: crisis, vulnerability, requests for a human, disputes,
cease-contact requests, third parties and prompt-injection attempts.

The keyword rules here are a deterministic baseline. In production, a trained
classifier runs alongside them, and the rules stay as a floor the model can't
lower: if either fires, the guard fires.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Action, CallState, Decision, Finding, Severity

GUARD = "input"


@dataclass(frozen=True)
class Rule:
    code: str
    severity: Severity
    action: Action
    patterns: tuple[str, ...]
    response: str | None = None  # scripted reply that replaces the LLM's turn


RULES: tuple[Rule, ...] = (
    Rule("CRISIS", Severity.CRITICAL, Action.ESCALATE,
         (r"\bkill myself\b", r"\bsuicid", r"\bend it all\b", r"\bdon'?t want to (live|be here)\b", r"\bself[- ]harm"),
         "I'm really sorry you're feeling this way. Your wellbeing matters more than this call. "
         "I'm connecting you to a member of our team now. If you're in immediate danger, please call emergency services."),
    Rule("HUMAN_REQUEST", Severity.MEDIUM, Action.ESCALATE,
         (r"\b(speak|talk) (to|with) (a |an )?(real |actual )?(person|human|someone|agent|advisor)\b", r"\bmanager\b", r"\bnot a (robot|machine)\b"),
         "Of course. I'm transferring you to one of our team now and I'll pass on what we've discussed."),
    Rule("CEASE_CONTACT", Severity.HIGH, Action.END_CALL,
         (r"\bstop (calling|contacting)\b", r"\bdon'?t (call|contact) me\b", r"\bleave me alone\b"),
         "Understood. I've recorded your request and we won't call you again. You'll receive a letter confirming this. Goodbye."),
    Rule("DISPUTE", Severity.HIGH, Action.ESCALATE,
         (r"\bnot my (debt|loan|account)\b", r"\bnever (borrowed|signed|took)\b", r"\bdon'?t owe\b", r"\bfraud\b", r"\bidentity theft\b"),
         "Thank you for telling me. I've paused any collection activity and I'm passing this to our disputes team, who'll contact you in writing."),
    Rule("COMPLAINT", Severity.MEDIUM, Action.ESCALATE,
         (r"\bcomplain", r"\bharass", r"\bombudsman\b", r"\bregulator\b"),
         "I'm sorry about that. I'm logging this as a formal complaint and connecting you to someone who can help."),
    Rule("THIRD_PARTY", Severity.MEDIUM, Action.END_CALL,
         (r"\bwrong number\b", r"\b(he|she|they)'?s not (here|in|available)\b", r"\bthis is (his|her|their) (wife|husband|partner|mother|father|son|daughter)\b", r"\bit'?s not me\b"),
         "Thanks for letting me know. I'll try again another time. Have a good day."),
    Rule("PROMPT_INJECTION", Severity.HIGH, Action.REWRITE,
         (r"\bignore (all |any |your |the )?(previous |prior )?(instructions|rules)\b", r"\bsystem prompt\b", r"\byou are now\b", r"\bdeveloper mode\b", r"\bpretend (to be|you)\b"),
         None),
)

# Soft signals: don't stop the call, but switch the agent into a gentler mode.
VULNERABILITY_SIGNALS: dict[str, tuple[str, ...]] = {
    "financial_hardship": (r"\blost my job\b", r"\bredundan", r"\bunemployed\b", r"\bcan'?t afford\b", r"\bno income\b"),
    "health": (r"\bhospital\b", r"\bcancer\b", r"\bsurgery\b", r"\bseriously ill\b", r"\bdisab"),
    "bereavement": (r"\bpassed away\b", r"\b(died|death)\b", r"\bfuneral\b"),
    "mental_health": (r"\bdepress", r"\banxiety\b", r"\bpanic attack", r"\bcan'?t cope\b"),
}

AI_QUESTION = re.compile(r"\bare you (a )?(robot|bot|machine|ai|computer|real( person)?)\b", re.I)


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(p, text, re.I) for p in patterns)


def sanitize_for_llm(utterance: str) -> str:
    """Customer speech is DATA, never instructions. Wrap it so the LLM prompt can't be hijacked."""
    cleaned = utterance.replace("<", "‹").replace(">", "›")[:1000]
    return f"<customer_utterance>{cleaned}</customer_utterance>"


def inspect_customer_turn(state: CallState, utterance: str) -> Decision:
    decision = Decision.allow()

    for rule in RULES:
        if _matches(utterance, rule.patterns):
            decision = decision.merge(Decision(rule.action, [Finding(GUARD, rule.code, rule.severity, utterance[:120])], rule.response))
            if rule.code == "THIRD_PARTY":
                state.third_party = True

    for category, patterns in VULNERABILITY_SIGNALS.items():
        if _matches(utterance, patterns) and category not in state.vulnerability:
            state.vulnerability.add(category)
            state.affordability_mode = True  # offers are now capped by affordability (see offer_guard)
            decision.findings.append(Finding(GUARD, "VULNERABILITY", Severity.HIGH, category))

    if AI_QUESTION.search(utterance):
        # Must always answer honestly; the output guard checks the reply.
        decision.findings.append(Finding(GUARD, "ASKED_IF_AI", Severity.INFO))

    if decision.action is Action.ESCALATE:
        state.escalated = True
    if decision.action is Action.END_CALL:
        state.ended = True
    return decision
