"""Layer 2: right-party verification.

Nothing about the debt may be disclosed until the person on the line has been
verified. Failed or third-party verification ends the call with no disclosure.
"""
from __future__ import annotations

import re

from .models import Action, CallState, Decision, Finding, Severity
from .policy import Ruleset

GUARD = "identity"

SAFE_RETRY = "Sorry, that doesn't match our records. Could you try once more?"
SAFE_GOODBYE = "I'm unable to continue without confirming who I'm speaking with. We'll write to the account holder instead. Goodbye."


def _normalise(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _extract_dob(utterance: str) -> str | None:
    """Very small parser for 'YYYY-MM-DD' or 'DD/MM/YYYY'. Production would use an NLU slot filler."""
    if m := re.search(r"(\d{4})-(\d{2})-(\d{2})", utterance):
        return m.group(0)
    if m := re.search(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})", utterance):
        d, mth, y = m.groups()
        return f"{y}-{int(mth):02d}-{int(d):02d}"
    return None


def verify_identity(state: CallState, utterance: str, ruleset: Ruleset) -> Decision:
    acct = state.account
    state.verification_attempts += 1

    dob_ok = _extract_dob(utterance) == acct.dob
    postcode_ok = _normalise(acct.postcode) in _normalise(utterance)

    # Two independent factors must both match.
    if dob_ok and postcode_ok:
        state.verified = True
        return Decision(Action.ALLOW, [Finding(GUARD, "VERIFIED", Severity.INFO, f"attempt {state.verification_attempts}")])

    finding = Finding(GUARD, "VERIFICATION_FAILED", Severity.MEDIUM,
                      f"attempt {state.verification_attempts}, dob_ok={dob_ok}, postcode_ok={postcode_ok}")

    if state.verification_attempts >= ruleset.max_verification_attempts:
        state.ended = True
        return Decision(Action.END_CALL, [finding], text=SAFE_GOODBYE)
    return Decision(Action.REWRITE, [finding], text=SAFE_RETRY)
