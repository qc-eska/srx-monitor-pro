from datetime import datetime

from database.db import get_meta, set_meta
from config import (
    APP_TIMEZONE,
    STATUS_END_HOUR,
    STATUS_INTERVAL_HOURS,
    STATUS_START_HOUR,
)

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None


STATUS_META_KEY = "last_status_slot"


def get_local_now():
    if ZoneInfo is None:
        return datetime.now()
    return datetime.now(ZoneInfo(APP_TIMEZONE))


def get_status_slot(now):
    if STATUS_INTERVAL_HOURS <= 0:
        return None

    if now.hour < STATUS_START_HOUR or now.hour > STATUS_END_HOUR:
        return None

    hour_offset = now.hour - STATUS_START_HOUR
    slot_index = hour_offset // STATUS_INTERVAL_HOURS
    slot_hour = STATUS_START_HOUR + slot_index * STATUS_INTERVAL_HOURS

    if slot_hour > STATUS_END_HOUR:
        return None

    return f"{now.date().isoformat()}:{slot_hour:02d}"


def should_send_status(now=None):
    now = now or get_local_now()
    slot = get_status_slot(now)

    if slot is None:
        return False

    return get_meta(STATUS_META_KEY) != slot


def mark_status_sent(now=None):
    now = now or get_local_now()
    slot = get_status_slot(now)

    if slot is None:
        return

    set_meta(STATUS_META_KEY, slot)


def build_status_message(active_matches, scanned_count, new_alerts_count, now=None):
    now = now or get_local_now()
    return (
        "📊 Status monitora SRX\n"
        f"Aktywnych ofert spełniających kryteria: {active_matches}\n"
        f"Przeskanowanych w ostatnim cyklu: {scanned_count}\n"
        f"Nowych alertów w ostatnim cyklu: {new_alerts_count}\n"
        f"Godzina statusu: {now.strftime('%H:%M')}"
    )
