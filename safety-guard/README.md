# Safety guardrails for the AI collections agent

This is a reference implementation of the safety layer around our voice and messaging agent.
The code shows the logic and structure, not a finished production system: detectors are
rule-based baselines and the ruleset values are placeholders.

## The core idea

The LLM writes the conversation, but it never has the final say.
Deterministic guards sit on both sides of it, and every decision is written to a
tamper-evident log.

```
                      ┌──────────────────────── AUDIT LOG (hash-chained, every decision) ───────────────────────┐
                      │                                                                                          │
 account ─► PRE-CALL ─┤  customer ─► INPUT GUARD ─► IDENTITY ─► LLM ─► OFFER GUARD ─► OUTPUT GUARD ─► voice/text │
            GATE      │  speech      (crisis,       (verify     (draft   (policy &     (disclosure,               │
         (hours,      │              human request,  before      text +   affordability) threats, PII,            │
          flags,      │              dispute,        any         struct.                 AI disclosure)          │
          caps)       │              injection)      detail)     offer)                                          │
                      └──────────────────────────────────────────────► POST-CALL QA (every call scored) ─────────┘
```

## Layers

| # | Layer | File | Protects against |
|---|-------|------|------------------|
| 1 | Pre-call gate | `guardrails/precall.py` | Calling outside legal hours or on rest days, over-contacting, calling disputed/bankrupt/deceased/cease-contact accounts, unconfigured markets |
| 2 | Identity | `guardrails/identity.py` | Disclosing a debt to the wrong person. Two factors must match; after the attempt limit, the call ends with nothing disclosed |
| 3 | Input guard | `guardrails/input_guard.py` | Missing a crisis, ignoring a request for a human, continuing collection on a disputed debt, prompt injection. Also detects vulnerability, which switches on affordability mode |
| 4 | Offer guard | `guardrails/offer_guard.py` | Offers outside the approved policy (instalments, minimums, discounts, dates) or above what a vulnerable customer can afford. It rewrites to the nearest compliant plan, or escalates if none exists |
| 5 | Output guard | `guardrails/output_guard.py` | Disclosure before verification, threats, legal threats, false urgency, shaming, claiming to be human, reading out card numbers or dates of birth. Ensures the agent says it is an AI |
| 6 | Audit log | `guardrails/audit.py` | Disputes about what happened on a call. Each entry records the ruleset version and the hash of the previous entry, so any edit is detectable |
| 7 | QA scorecard | `guardrails/qa.py` | Silent quality drift. Every call gets an agent-quality score (LLM errors the guards caught) and a human-review flag |

`guardrails/pipeline.py` runs the layers in order. `guardrails/policy.py` holds the versioned ruleset.

## Design principles

1. **Policy is data, owned by compliance.** Offer limits, calling hours and contact caps live in a
   versioned `Ruleset` approved by the client's compliance team. The LLM can't change them, and
   every logged decision names the version in force.
2. **Structured offers.** The LLM must output any payment plan as structured data next to its text,
   so it can be checked by code instead of parsed out of free text.
3. **Strictest action wins.** If guards disagree: `ESCALATE > END_CALL > BLOCK > REWRITE > ALLOW`.
4. **Fail closed.** If any guard throws an error, the call goes to a human. It never continues unguarded.
5. **Customer speech is data, not instructions.** Utterances are wrapped and escaped before reaching
   the LLM, and verification answers (DOB, postcode) are never sent to the LLM at all.
6. **Scripted responses for high-risk moments.** Crisis, cease-contact, disputes and third parties
   get pre-approved wording, not generated text.
7. **Everything is logged.** That includes the LLM's rejected drafts, which measure model quality.

## Run the demo

Python 3.10+ with no dependencies:

```bash
python demo.py
```

It plays scripted calls in which the "LLM" makes deliberate mistakes, and shows which guard catches
each one: pre-call blocks, disclosure before verification, threats, an unaffordable offer, a prompt
injection asking for a 90% discount, a card number read aloud, a crisis disclosure, and a third
party answering. It then checks the audit chain (and shows that tampering is detected) and prints
QA scorecards. Sample output is in `demo_output.txt`.

## Path to production

| Area | Now (this code) | Production |
|------|-----------------|------------|
| Detection | Regex baselines | Fine-tuned classifiers per language, with the regex rules kept as a floor that can't be lowered |
| Speech | Final transcripts | Streaming ASR with partial-transcript checks, so crisis and opt-out are caught mid-sentence |
| Output | Check before TTS | Same, plus an LLM-as-judge second opinion on high-risk turns within a latency budget |
| Ruleset | Python constants | Admin UI with maker/checker approval, effective dates and per-portfolio overrides |
| Time zones | Fixed UTC offset | Real tz database, public holidays per market |
| Audit | In-memory hash chain | Append-only store (WORM storage), periodic anchoring of the chain hash, retention policy |
| QA | Finding-based score | Plus LLM-as-judge transcript review calibrated against human graders; weekly sampling |
| Testing | Demo script | Red-team evaluation set (injections, vulnerable customers, edge cases) run on every prompt or model change, with pass thresholds that block release |
| Monitoring | n/a | Dashboards for escalation rate, guard-trigger rate per rule, LLM error rate, complaint rate |
