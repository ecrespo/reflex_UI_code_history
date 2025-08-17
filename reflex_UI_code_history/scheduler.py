from __future__ import annotations

"""
Background scheduler for daily efeméride generation inside Reflex backend.

- Uses APScheduler BackgroundScheduler with a CronTrigger.
- Default schedule: every day at 23:59 local time (configurable via env vars).
- Honors TZ env variable if provided (Python 3.9+ zoneinfo).
- Idempotent start to avoid multiple schedulers in dev reloads.

Env variables:
- TZ: IANA timezone name, e.g. "America/Mexico_City".
- EFEMERIDE_CRON_HOUR: hour in 24h format (default: "23").
- EFEMERIDE_CRON_MINUTE: minute (default: "59").
"""

import os
import threading
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

# Import the job function from the existing script
from generate_tomorrow_efemeride import ensure_tomorrow_efemeride


_scheduler: Optional[BackgroundScheduler] = None
_started = False
_lock = threading.Lock()


def _get_tz() -> Optional[object]:
    tz_env = os.getenv("TZ")
    if tz_env and ZoneInfo is not None:
        try:
            return ZoneInfo(tz_env)
        except Exception:
            return None
    return None


def start_scheduler() -> None:
    """Start the background scheduler if not already started."""
    global _scheduler, _started
    if _started:
        return
    with _lock:
        if _started:
            return

        tz = _get_tz()
        hour = os.getenv("EFEMERIDE_CRON_HOUR", "00")
        minute = os.getenv("EFEMERIDE_CRON_MINUTE", "01")

        _scheduler = BackgroundScheduler(timezone=tz)
        trigger = CronTrigger(hour=hour, minute=minute, timezone=tz)

        # Coalesce to catch up if server was down; max_instances=1 to avoid overlap
        _scheduler.add_job(
            ensure_tomorrow_efemeride,
            trigger,
            id="efemeride_daily",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

        _scheduler.start()
        _started = True


def stop_scheduler() -> None:
    global _scheduler, _started
    with _lock:
        if _scheduler is not None:
            try:
                _scheduler.shutdown(wait=False)
            except Exception:
                pass
            finally:
                _scheduler = None
                _started = False
