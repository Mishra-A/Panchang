from datetime import datetime, timezone

from backend.app.core.time_utils import utc_to_ist


def test_utc_to_ist():
    dt = datetime(
        2026,
        8,
        14,
        13,
        17,
        22,
        tzinfo=timezone.utc,
    )

    result = utc_to_ist(dt)

    assert result.hour == 18
    assert result.minute == 47