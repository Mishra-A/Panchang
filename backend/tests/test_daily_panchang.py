from datetime import date

from backend.app.core.location import LUCKNOW
from backend.app.panchang.daily_panchang import (
    build_daily_panchang,
)


def test_daily_panchang():

    result = build_daily_panchang(
        target_date=date(2026, 8, 14),
        location=LUCKNOW,
    )

    assert result["date"] == "2026-08-14"

    assert result["location"]["city"] == "Lucknow"

    assert result["vara"]["name"]

    assert result["sun"]["sunrise_utc"]
    assert result["sun"]["sunset_utc"]

    assert result["panchang"]["tithi"]["name"]
    assert result["panchang"]["nakshatra"]["name"]
    assert result["panchang"]["yoga"]["name"]
    assert result["panchang"]["karana"]["name"]