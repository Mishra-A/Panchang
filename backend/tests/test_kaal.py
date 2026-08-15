from datetime import date, datetime
from zoneinfo import ZoneInfo

from backend.app.kaal.kaal import (
    calculate_day_kaal,
    calculate_abhijit_muhurat,
    calculate_brahma_muhurta,
)


IST = ZoneInfo("Asia/Kolkata")


def test_day_kaal():

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

    result = calculate_day_kaal(
        sunrise,
        sunset,
        date(2026, 8, 14),
    )

    assert result["rahu_kaal"]
    assert result["yamaganda"]
    assert result["gulika"]

    assert (
        result["rahu_kaal"]["starts_at"]
        < result["rahu_kaal"]["ends_at"]
    )
def test_abhijit_muhurat():

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

    result = calculate_abhijit_muhurat(
        sunrise,
        sunset,
    )

    assert result["name"] == "Abhijit Muhurat"

    start = datetime.fromisoformat(
        result["starts_at"]
    )

    end = datetime.fromisoformat(
        result["ends_at"]
    )

    assert start < end


def test_brahma_muhurta():

    previous_sunrise = datetime(
        2026,
        8,
        13,
        5,
        37,
        0,
        tzinfo=IST,
    )

    current_sunrise = datetime(
        2026,
        8,
        14,
        5,
        37,
        2,
        tzinfo=IST,
    )

    result = calculate_brahma_muhurta(
        previous_sunrise,
        current_sunrise,
    )

    assert result["name"] == "Brahma Muhurta"

    start = datetime.fromisoformat(
        result["starts_at"]
    )

    end = datetime.fromisoformat(
        result["ends_at"]
    )

    assert start < end
    assert end < current_sunrise    