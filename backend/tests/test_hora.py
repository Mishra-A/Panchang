from datetime import datetime
from zoneinfo import ZoneInfo

from backend.app.kaal.hora import calculate_hora


IST = ZoneInfo("Asia/Kolkata")


def test_hora():

    sunrise = datetime(
        2026,
        8,
        14,
        5,
        37,
        2,
        tzinfo=IST,
    )

    sunset = datetime(
        2026,
        8,
        14,
        18,
        44,
        31,
        tzinfo=IST,
    )

    next_sunrise = datetime(
        2026,
        8,
        15,
        5,
        37,
        30,
        tzinfo=IST,
    )

    result = calculate_hora(
        sunrise,
        sunset,
        next_sunrise,
        weekday=4,  # Friday
    )

    assert len(result["day"]) == 12
    assert len(result["night"]) == 12

    assert result["day"][0]["number"] == 1
    assert result["day"][-1]["number"] == 12

    assert result["night"][0]["number"] == 13
    assert result["night"][-1]["number"] == 24

    # Friday's first Hora is Venus.
    assert result["day"][0]["planet"] == "Venus"

    for hora in result["day"] + result["night"]:
        assert hora["planet"]

        start = datetime.fromisoformat(
            hora["starts_at"]
        )

        end = datetime.fromisoformat(
            hora["ends_at"]
        )

        assert end > start