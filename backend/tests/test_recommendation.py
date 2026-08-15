from datetime import date

from backend.app.core.location import LUCKNOW
from backend.app.kaal.daily_kaal import (
    build_daily_kaal,
)
from backend.app.panchang.daily_panchang import (
    build_daily_panchang,
)
from backend.app.muhurat.recommendation import (
    recommend_activity,
)


def test_vehicle_recommendation():

    target_date = date(2026, 8, 14)

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=LUCKNOW,
    )

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=LUCKNOW,
    )

    result = recommend_activity(
        activity="vehicle_purchase",
        daily_kaal=daily_kaal,
        daily_panchang=daily_panchang,
    )

    assert isinstance(result, list)
    assert len(result) > 0

    for window in result:

        assert window["activity"] == (
            "vehicle_purchase"
        )

        assert window["status"] in [
            "recommended",
            "acceptable",
            "avoid",
        ]

        assert 0 <= window["score"] <= 100

        assert "start" in window
        assert "end" in window
        assert "reasons" in window
        assert "warnings" in window

def test_muhurat_windows_do_not_cross_nakshatra_boundary():
    from datetime import date, datetime

    from backend.app.core.location import LUCKNOW
    from backend.app.kaal.daily_kaal import build_daily_kaal
    from backend.app.panchang.daily_panchang import (
        build_daily_panchang,
    )
    from backend.app.panchang.daily_timeline import (
        build_daily_timeline,
    )
    from backend.app.muhurat.recommendation import (
        recommend_activity,
    )

    target_date = date(2026, 8, 20)

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=LUCKNOW,
    )

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=LUCKNOW,
    )

    timeline = build_daily_timeline(
        target_date=target_date,
        location=LUCKNOW,
    )

    nakshatra_periods = (
        timeline["timeline"]["nakshatra"]
    )

    recommendations = recommend_activity(
        activity="vehicle_purchase",
        daily_kaal=daily_kaal,
        daily_panchang=daily_panchang,
    )

    for window in recommendations:

        start = datetime.fromisoformat(
            window["start"]
        )

        end = datetime.fromisoformat(
            window["end"]
        )

        for nakshatra in nakshatra_periods:

            nak_start = datetime.fromisoformat(
                nakshatra["starts_at_ist"]
            )

            nak_end = datetime.fromisoformat(
                nakshatra["ends_at_ist"]
            )

            overlaps_boundary = (
                start < nak_end
                and end > nak_end
            )

            if overlaps_boundary:
                assert (
                    end <= nak_end
                ), (
                    "Muhurat window crosses "
                    f"Nakshatra boundary: "
                    f"{start} -> {end}"
                )       
                
def test_muhurat_windows_do_not_cross_tithi_or_yoga_boundary():
    from datetime import date, datetime

    from backend.app.core.location import LUCKNOW
    from backend.app.kaal.daily_kaal import build_daily_kaal
    from backend.app.panchang.daily_panchang import (
        build_daily_panchang,
    )
    from backend.app.panchang.daily_timeline import (
        build_daily_timeline,
    )
    from backend.app.muhurat.recommendation import (
        recommend_activity,
    )

    target_date = date(2026, 8, 20)

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=LUCKNOW,
    )

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=LUCKNOW,
    )

    timeline = build_daily_timeline(
        target_date=target_date,
        location=LUCKNOW,
    )

    recommendations = recommend_activity(
        activity="vehicle_purchase",
        daily_kaal=daily_kaal,
        daily_panchang=daily_panchang,
    )

    for category in ("tithi", "yoga"):

        periods = timeline["timeline"][category]

        for window in recommendations:

            start = datetime.fromisoformat(
                window["start"]
            )

            end = datetime.fromisoformat(
                window["end"]
            )

            contained = any(
                start >= datetime.fromisoformat(
                    period["starts_at_ist"]
                )
                and end <= datetime.fromisoformat(
                    period["ends_at_ist"]
                )
                for period in periods
            )

            assert contained, (
                f"Muhurat window crosses "
                f"{category} boundary: "
                f"{start} -> {end}"
            )                