"""Layer 6: tamper-evident audit trail.

Every guard decision is appended to a hash chain: each entry stores the hash of
the previous one, so editing or deleting any record breaks verification. This
is what lets the client show a regulator exactly what happened on a call and
which ruleset version was in force.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from .models import Finding

GENESIS = "0" * 64


def _hash(entry: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(entry, sort_keys=True, default=str).encode()).hexdigest()


class AuditLog:
    def __init__(self) -> None:
        self.entries: list[dict[str, Any]] = []

    def record(self, call_id: str, event: str, ruleset_version: str, payload: dict[str, Any], findings: list[Finding]) -> None:
        entry = {
            "seq": len(self.entries),
            "ts": datetime.now(timezone.utc).isoformat(),
            "call_id": call_id,
            "event": event,
            "ruleset_version": ruleset_version,
            "payload": payload,
            "findings": [{**asdict(f), "severity": f.severity.name} for f in findings],
            "prev_hash": self.entries[-1]["hash"] if self.entries else GENESIS,
        }
        entry["hash"] = _hash(entry)
        self.entries.append(entry)

    def verify(self) -> tuple[bool, int | None]:
        """Return (ok, index_of_first_broken_entry)."""
        prev = GENESIS
        for i, e in enumerate(self.entries):
            body = {k: v for k, v in e.items() if k != "hash"}
            if e["prev_hash"] != prev or _hash(body) != e["hash"]:
                return False, i
            prev = e["hash"]
        return True, None

    def for_call(self, call_id: str) -> list[dict[str, Any]]:
        return [e for e in self.entries if e["call_id"] == call_id]

    def export_jsonl(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            for e in self.entries:
                fh.write(json.dumps(e, default=str) + "\n")
