from backend.app.panchang.tithi import calculate_tithi
from datetime import datetime, timezone

from backend.app.panchang.tithi import get_tithi_with_end_time


def test_tithi_basic():
    result = calculate_tithi(
        sun_longitude=141.72937454572937,
        moon_longitude=165.03730574860634,
    )

    assert result.paksha == "Shukla"
    assert result.number == 2
    assert result.name == "Dvitiya"
    assert 0 <= result.progress_percent < 100
def test_tithi_has_end_time():
    start = datetime(
        2026,
        8,
        14,
        12,
        0,
        0,
        tzinfo=timezone.utc,
    )

    result = get_tithi_with_end_time(start)

    assert result["name"]
    assert result["paksha"] in ["Shukla", "Krishna"]
    assert result["ends_at_utc"]

    end_time = datetime.fromisoformat(
        result["ends_at_utc"]
    )

    assert end_time > start    
