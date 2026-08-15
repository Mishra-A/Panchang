from datetime import datetime, timezone
from zoneinfo import ZoneInfo



IST = ZoneInfo("Asia/Kolkata")


def ensure_utc(dt: datetime) -> datetime:
    """Convert a timezone-aware datetime to UTC."""
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    return dt.astimezone(timezone.utc)


def utc_to_ist(dt: datetime) -> datetime:
    """Convert UTC datetime to Indian Standard Time."""
    return ensure_utc(dt).astimezone(IST)


def format_ist(dt: datetime) -> str:
    """Return ISO formatted Indian time."""
    return utc_to_ist(dt).isoformat()