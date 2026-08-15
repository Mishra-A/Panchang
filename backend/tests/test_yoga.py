from backend.app.panchang.yoga import calculate_yoga


def test_yoga_basic():

    result = calculate_yoga(
        sun_sidereal_longitude=100.0,
        moon_sidereal_longitude=50.0,
    )

    assert result.number == 12
    assert result.name == "Dhruva"
    assert 0 <= result.progress_percent < 100

from datetime import datetime, timezone

from backend.app.panchang.yoga import (
    get_yoga_with_end_time,
)    

def test_yoga_has_end_time():

    start = datetime(
        2026,
        8,
        14,
        12,
        0,
        0,
        tzinfo=timezone.utc,
    )

    result = get_yoga_with_end_time(start)

    assert result["name"]
    assert 1 <= result["number"] <= 27

    assert 0 <= result["progress_percent"] < 100

    assert result["ends_at_utc"]
    assert result["ends_at_ist"]

    end_time = datetime.fromisoformat(
        result["ends_at_utc"]
    )

    assert end_time > start