"""Layer 7: post-call QA scorecard, built from the audit log.

Every call is scored, not a sample. Two separate questions are answered:

  1. Agent quality: how often did the LLM draft something the guards had to fix?
     The customer was protected, but frequent corrections mean the prompt or
     model needs work.
  2. Human review: did anything happen that a person must look at (crisis,
     vulnerability, dispute, complaint, guard failure), or was quality low?

In production this is complemented by an LLM-as-judge review of the full
transcript (tone, empathy, accuracy), calibrated against human graders.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .audit import AuditLog

# Guards that judge the AGENT's behaviour. Input/identity findings describe the customer.
AGENT_SIDE_GUARDS = {"output", "offer", "pipeline"}
PENALTY = {"CRITICAL": 30, "HIGH": 15, "MEDIUM": 5, "LOW": 2, "INFO": 0}
REVIEW_CODES = {"CRISIS", "VULNERABILITY", "DISPUTE", "COMPLAINT", "GUARD_ERROR", "NO_COMPLIANT_PLAN"}
REVIEW_BELOW = 70


@dataclass
class Scorecard:
    call_id: str
    agent_quality: int
    llm_errors_caught: int
    needs_human_review: bool
    review_reasons: list[str]
    outcome: str
    counts: Counter = field(default_factory=Counter)


def score_call(audit: AuditLog, call_id: str) -> Scorecard:
    counts: Counter = Counter()
    quality, caught = 100, 0
    reasons: set[str] = set()
    outcome = "completed"

    for e in audit.for_call(call_id):
        for f in e["findings"]:
            counts[f["code"]] += 1
            if f["guard"] in AGENT_SIDE_GUARDS and f["severity"] != "INFO":
                caught += 1
                quality -= PENALTY[f["severity"]]
            if f["code"] in REVIEW_CODES:
                reasons.add(f["code"])
        action = e["payload"].get("action")
        if e["event"] == "precall" and action == "block":
            outcome = "not called (pre-call block)"
        elif action == "escalate":
            outcome = "escalated to human"
        elif action == "end_call" and outcome == "completed":
            outcome = "ended by guard"

    quality = max(quality, 0)
    if quality < REVIEW_BELOW:
        reasons.add(f"AGENT_QUALITY<{REVIEW_BELOW}")
    return Scorecard(call_id, quality, caught, bool(reasons), sorted(reasons), outcome, counts)
