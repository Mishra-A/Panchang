from datetime import date

from fastapi import APIRouter, HTTPException, Query

from backend.app.core.location import LUCKNOW

from backend.app.panchang.daily_panchang import (
    build_daily_panchang,
)

from backend.app.panchang.daily_timeline import (
    build_daily_timeline,
)

from backend.app.kaal.daily_kaal import (
    build_daily_kaal,
)

from backend.app.muhurat.recommendation import (
    recommend_activity,
)

from backend.app.muhurat.ranking import (
    get_best_recommendations,
)


router = APIRouter(
    prefix="/api/v1/panchang",
    tags=["Panchang"],
)


LOCATIONS = {
    "lucknow": LUCKNOW,
}


@router.get("/daily")
def get_daily_panchang(
    target_date: date = Query(
        ...,
        alias="date",
    ),
    city: str = Query(
        "Lucknow"
    ),
    activity: str | None = Query(
        None
    ),
):
    """
    Return daily Panchang, Kaal,
    complete Panchang timeline and
    optional Muhurat recommendations.
    """

    # --------------------------------------------------
    # LOCATION
    # --------------------------------------------------

    location = LOCATIONS.get(
        city.lower()
    )

    if location is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Location not supported: {city}"
            ),
        )

    # --------------------------------------------------
    # DAILY PANCHANG
    # --------------------------------------------------

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=location,
    )

    # --------------------------------------------------
    # DAILY KAAL
    # --------------------------------------------------

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=location,
    )

    # --------------------------------------------------
    # COMPLETE PANCHANG TIMELINE
    #
    # This contains exact transitions for:
    # Tithi
    # Nakshatra
    # Yoga
    # Karana
    #
    # Example:
    #
    # Vishakha
    # 00:00 → 09:08
    #
    # Anuradha
    # 09:08 → 24:00
    # --------------------------------------------------

    daily_timeline = build_daily_timeline(
        target_date=target_date,
        location=location,
    )

    # --------------------------------------------------
    # BASE RESPONSE
    # --------------------------------------------------

    response = {
        "date": target_date.isoformat(),

        "location": {
            "city": location.city,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone": location.timezone,
        },

        "panchang": daily_panchang,

        "kaal": daily_kaal,

        "timeline": daily_timeline[
            "timeline"
        ],
    }

    # --------------------------------------------------
    # OPTIONAL MUHURAT
    # --------------------------------------------------

    if activity is not None:

        recommendations = recommend_activity(
            activity=activity,
            daily_kaal=daily_kaal,
            daily_panchang=daily_panchang,
        )

        best_windows = get_best_recommendations(
            recommendations,
            limit=3,
        )

        response["muhurat"] = {
            "activity": activity,
            "best_windows": best_windows,
        }

    return response