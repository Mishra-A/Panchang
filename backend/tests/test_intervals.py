from datetime import datetime
from zoneinfo import ZoneInfo

from backend.app.muhurat.intervals import (
    split_interval,
    find_period_at,
)


IST = ZoneInfo("Asia/Kolkata")


def test_split_interval():

    start = datetime(
        2026, 8, 14, 10, 0,
        tzinfo=IST,
    )

    end = datetime(
        2026, 8, 14, 12, 0,
        tzinfo=IST,
    )

    choghadiya = [
        {
            "starts_at": "2026-08-14T10:00:00+05:30",
            "ends_at": "2026-08-14T11:38:00+05:30",
        }
    ]

    rahu = [
        {
            "starts_at": "2026-08-14T10:32:00+05:30",
            "ends_at": "2026-08-14T12:10:00+05:30",
        }
    ]

    intervals = split_interval(
        start,
        end,
        choghadiya,
        rahu,
    )

    assert len(intervals) == 3

   
    assert intervals[0][0].minute == 0
    assert intervals[0][1].minute == 32

    assert intervals[1][0].minute == 32
    assert intervals[1][1].minute == 38

    assert intervals[2][0].minute == 38
    assert intervals[2][1].hour == 12
    assert intervals[2][1].minute == 0


def test_find_period_at():

    start = datetime(
        2026, 8, 14, 10, 5,
        tzinfo=IST,
    )

    end = datetime(
        2026, 8, 14, 10, 20,
        tzinfo=IST,
    )

    periods = [
        {
            "name": "Labh",
            "starts_at": "2026-08-14T10:00:00+05:30",
            "ends_at": "2026-08-14T11:00:00+05:30",
        }
    ]

    result = find_period_at(
        start,
        end,
        periods,
    )

    assert result is not None
    assert result["name"] == "Labh"