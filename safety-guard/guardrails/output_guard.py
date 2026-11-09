"""Layer 5: inspect what the AGENT is about to say, before text-to-speech.

This is the last line of defence against LLM mistakes: leaking account details
to an unverified person, threatening or misleading language, claiming to be
human, or reading out sensitive data.
"""
from __future__ import annotations

import re

from .models import Action, CallState, Decision, Finding, Severity
from .policy import Ruleset

GUARD = "output"

AI_DISCLOSURE = "Just so you know, I'm an automated assistant. "
VERIFY_PROMPT = "Before I can go into any detail, could you confirm your date of birth and postcode?"
SAFE_FALLBACK = "Sorry, let me rephrase that. Is there anything about your account you'd like help with today?"

# Anything that reveals the debt exists counts as disclosure.
DISCLOSURE = re.compile(r"(£|€|\$|R\$)\s?\d|\b(balance|debt|arrears|overdue|owe|outstanding|loan|missed payment|account number)\b", re.I)

PROHIBITED: dict[str, tuple[str, ...]] = {
    "THREAT": (r"\b(arrest|police|jail|prison)\b", r"\bseize (your|the)\b", r"\bbailiff", r"\bgarnish"),
    "LEGAL_THREAT": (r"\b(take you to|see you in) court\b", r"\blegal action\b", r"\bsue you\b"),
    "FALSE_URGENCY": (r"\bfinal (warning|chance)\b", r"\bright now or\b", r"\blast chance\b"),
    "SHAMING": (r"\b(irresponsible|ashamed|embarrass)", r"\btell your (employer|family|neighbours)\b"),
    "HUMAN_IMPERSONATION": (r"\bi'?m (a )?(real|human) (person|being)?\b", r"\bi am not (a )?(robot|bot|ai)\b"),
}

CARD_NUMBER = re.compile(r"\b(?:card\s+)?(?:\d[ -]?){12,18}(\d{4})\b", re.I)
FULL_DOB = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def _redact(text: str) -> tuple[str, list[Finding]]:
    findings = []
    if CARD_NUMBER.search(text):
        text = CARD_NUMBER.sub(r"card ending \1", text)
        findings.append(Finding(GUARD, "REDACTED_CARD", Severity.MEDIUM))
    if FULL_DOB.search(text):
        text = FULL_DOB.sub("[date of birth]", text)
        findings.append(Finding(GUARD, "REDACTED_DOB", Severity.MEDIUM))
    return text, findings


def inspect_agent_turn(state: CallState, text: str, ruleset: Ruleset) -> Decision:
    findings: list[Finding] = []

    # 1. No disclosure to an unverified person or a third party.
    if (not state.verified or state.third_party) and DISCLOSURE.search(text):
        findings.append(Finding(GUARD, "DISCLOSURE_BEFORE_VERIFICATION", Severity.CRITICAL, text[:120]))
        return Decision(Action.REWRITE, findings, VERIFY_PROMPT if not state.third_party else SAFE_FALLBACK)

    # 2. Prohibited language. Legal mentions are only allowed if the ruleset permits them.
    for code, patterns in PROHIBITED.items():
        if code == "LEGAL_THREAT" and ruleset.allow_legal_action_mention:
            continue
        if any(re.search(p, text, re.I) for p in patterns):
            findings.append(Finding(GUARD, code, Severity.HIGH, text[:120]))
    if findings:
        return Decision(Action.REWRITE, findings, SAFE_FALLBACK)

    # 3. Redact sensitive data the LLM tried to read out.
    text, redactions = _redact(text)
    findings += redactions

    # 4. AI disclosure must be in the first agent turn.
    if ruleset.must_disclose_ai and not state.ai_disclosed:
        if not re.search(r"\b(automated|virtual|digital|ai) (assistant|agent)\b", text, re.I):
            text = AI_DISCLOSURE + text
            findings.append(Finding(GUARD, "AI_DISCLOSURE_ADDED", Severity.LOW))
        state.ai_disclosed = True

    action = Action.REWRITE if findings else Action.ALLOW
    return Decision(action, findings, text)
