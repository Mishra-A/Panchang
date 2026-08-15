from backend.app.panchang.nakshatra import calculate_nakshatra
from datetime import datetime, timezone

from backend.app.panchang.nakshatra import (
    get_nakshatra_with_end_time,
)



def test_nakshatra_basic():

    result = calculate_nakshatra(
        moon_sidereal_longitude=20.0
    )

    assert result.number == 2
    assert result.name == "Bharani"
    assert 1 <= result.pada <= 4
    assert 0 <= result.progress_percent < 100

def test_nakshatra_has_end_time():

    start = datetime(
        2026,
        8,
        14,
        12,
        0,
        0,
        tzinfo=timezone.utc,
    )

    result = get_nakshatra_with_end_time(start)

    assert result["name"]
    assert 1 <= result["number"] <= 27
    assert 1 <= result["pada"] <= 4

    assert 0 <= result["progress_percent"] < 100

    assert result["ends_at_utc"]

    end_time = datetime.fromisoformat(
        result["ends_at_utc"]
    )

    assert end_time > start   