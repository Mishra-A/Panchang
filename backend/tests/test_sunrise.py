from datetime import date, datetime

from backend.app.astronomy.sunrise import (
    calculate_sunrise_sunset,
)


def test_sunrise_sunset():

    result = calculate_sunrise_sunset(
        target_date=date(2026, 8, 14),
        latitude=26.8467,
        longitude=80.9462,
    )

    assert result["sunrise_utc"]
    assert result["sunset_utc"]

    sunrise = datetime.fromisoformat(
        result["sunrise_utc"]
    )

    sunset = datetime.fromisoformat(
        result["sunset_utc"]
    )

    assert sunrise < sunset