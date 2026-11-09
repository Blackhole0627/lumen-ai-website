"""Layer 6: tamper-evident audit trail.

Every guard decision is appended to a hash chain: each entry stores the hash of
the previous one, so editing or deleting any record breaks verification. This
is what lets the client show a regulator exactly what happened on a call and
which ruleset version was in force.

A chain can continue across processes: pass the last stored hash and sequence
number when creating the log (the backend does this on every turn).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Iterable

from .models import Finding

GENESIS = "0" * 64


def entry_hash(entry: dict[str, Any]) -> str:
    """Hash of an entry, excluding its own 'hash' field."""
    body = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()


def verify_chain(entries: Iterable[dict[str, Any]], genesis: str = GENESIS) -> tuple[bool, int | None]:
    """Return (ok, index_of_first_broken_entry)."""
    prev = genesis
    for i, e in enumerate(entries):
        if e["prev_hash"] != prev or entry_hash(e) != e["hash"]:
            return False, i
        prev = e["hash"]
    return True, None


class AuditLog:
    def __init__(self, last_hash: str = GENESIS, start_seq: int = 0) -> None:
        self.entries: list[dict[str, Any]] = []
        self._genesis = last_hash
        self._start_seq = start_seq

    def record(self, call_id: str, event: str, ruleset_version: str, payload: dict[str, Any], findings: list[Finding]) -> None:
        entry = {
            "seq": self._start_seq + len(self.entries),
            "ts": datetime.now(timezone.utc).isoformat(),
            "call_id": call_id,
            "event": event,
            "ruleset_version": ruleset_version,
            "payload": payload,
            "findings": [{**asdict(f), "severity": f.severity.name} for f in findings],
            "prev_hash": self.entries[-1]["hash"] if self.entries else self._genesis,
        }
        entry["hash"] = entry_hash(entry)
        self.entries.append(entry)

    def verify(self) -> tuple[bool, int | None]:
        return verify_chain(self.entries, self._genesis)

    def for_call(self, call_id: str) -> list[dict[str, Any]]:
        return [e for e in self.entries if e["call_id"] == call_id]

    def export_jsonl(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            for e in self.entries:
                fh.write(json.dumps(e, default=str) + "\n")
