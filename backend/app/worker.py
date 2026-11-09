"""Background worker: starts outbound calls for accounts that are due.

Run:  python -m app.worker          (loops every WORKER_POLL_SECONDS)
      python -m app.worker --once   (one pass, handy for testing or a cron job)
"""
from __future__ import annotations

import argparse
import logging
import time

from .bootstrap import build_runtime
from .config import get_settings
from .services import scheduler

log = logging.getLogger("worker")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Outbound call scheduler")
    parser.add_argument("--once", action="store_true", help="run one pass and exit")
    args = parser.parse_args(argv)

    runtime = build_runtime(get_settings())
    log.info("worker started (poll every %ss, max %s concurrent calls)",
             runtime.settings.worker_poll_seconds, runtime.settings.max_concurrent_calls)
    while True:
        with runtime.session_factory() as db:
            stats = scheduler.run_once(db, runtime.container)
        log.info("pass complete: %s", stats)
        if args.once:
            break
        time.sleep(runtime.settings.worker_poll_seconds)


if __name__ == "__main__":
    main()
