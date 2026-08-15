from datetime import datetime
from zoneinfo import ZoneInfo

from backend.app.kaal.choghadiya import (
    calculate_choghadiya,
)


IST = ZoneInfo("Asia/Kolkata")


def test_choghadiya():

    sunrise = datetime(
        2026, 8, 14, 5, 37, 2,
        tzinfo=IST,
    )

    sunset = datetime(
        2026, 8, 14, 18, 44, 31,
        tzinfo=IST,
    )

    next_sunrise = datetime(
        2026, 8, 15, 5, 37, 30,
        tzinfo=IST,
    )

    result = calculate_choghadiya(
        sunrise,
        sunset,
        next_sunrise,
        weekday=4,  # Friday
    )

    assert len(result["day"]) == 8
    assert len(result["night"]) == 8

    assert result["day"][0]["number"] == 1
    assert result["day"][-1]["number"] == 8

    assert result["night"][0]["number"] == 1
    assert result["night"][-1]["number"] == 8

    assert result["day"][0]["type"]
    assert result["night"][0]["type"]