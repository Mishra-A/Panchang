from datetime import date, datetime

from backend.app.core.location import LUCKNOW
from backend.app.panchang.daily_timeline import (
    build_daily_timeline,
)


def test_daily_timeline():

    result = build_daily_timeline(
        target_date=date(2026, 8, 14),
        location=LUCKNOW,
    )

    assert result["date"] == "2026-08-14"

    for category in [
        "tithi",
        "nakshatra",
        "yoga",
        "karana",
    ]:

        events = result["timeline"][category]

        assert len(events) >= 1

        for event in events:

            assert event["name"]

            start = datetime.fromisoformat(
                event["starts_at_utc"]
            )

            end = datetime.fromisoformat(
                event["ends_at_utc"]
            )

            assert end > start


def test_nakshatra_transition_2026_08_20():
    from datetime import date

    from backend.app.core.location import LUCKNOW
    from backend.app.panchang.daily_timeline import (
        build_daily_timeline,
    )

    result = build_daily_timeline(
        date(2026, 8, 20),
        LUCKNOW,
    )

    nakshatras = result["timeline"]["nakshatra"]

    assert len(nakshatras) >= 2

    assert nakshatras[0]["name"] == "Vishakha"
    assert nakshatras[1]["name"] == "Anuradha"

    assert (
        nakshatras[0]["ends_at_ist"]
        == nakshatras[1]["starts_at_ist"]
    )            