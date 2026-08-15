from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from backend.app.core.location import Location
from backend.app.astronomy.sunrise import calculate_sunrise_sunset
from backend.app.panchang.vara import calculate_vara
from backend.app.panchang.tithi import get_tithi_with_end_time
from backend.app.panchang.nakshatra import get_nakshatra_with_end_time
from backend.app.panchang.yoga import get_yoga_with_end_time
from backend.app.panchang.karana import get_karana_with_end_time


UTC = ZoneInfo("UTC")


def local_noon_to_utc(target_date: date, timezone_name: str) -> datetime:
    """
    Create local noon for the requested date and convert it to UTC.
    """

    tz = ZoneInfo(timezone_name)

    local_dt = datetime.combine(
        target_date,
        time(12, 0),
        tzinfo=tz,
    )

    return local_dt.astimezone(ZoneInfo("UTC"))


def build_daily_panchang(
    target_date: date,
    location: Location,
) -> dict:
    """
    Build the core daily Panchang for a location.

    Current modules:
    Vara
    Sunrise/Sunset
    Tithi
    Nakshatra
    Yoga
    Karana
    """

    calculation_time_utc = local_noon_to_utc(
        target_date,
        location.timezone,
    )

    vara = calculate_vara(target_date)

    sun_data = calculate_sunrise_sunset(
        target_date=target_date,
        latitude=location.latitude,
        longitude=location.longitude,
    )

    tithi = get_tithi_with_end_time(
        calculation_time_utc
    )

    nakshatra = get_nakshatra_with_end_time(
        calculation_time_utc
    )

    yoga = get_yoga_with_end_time(
        calculation_time_utc
    )

    karana = get_karana_with_end_time(
        calculation_time_utc
    )

    return {
        "date": target_date.isoformat(),

        "location": {
            "city": location.city,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone": location.timezone,
        },

        "vara": vara,

        "sun": sun_data,

        "panchang": {
            "tithi": tithi,
            "nakshatra": nakshatra,
            "yoga": yoga,
            "karana": karana,
        },

        "calculation": {
            "calculated_at_local": calculation_time_utc.astimezone(
                ZoneInfo(location.timezone)
            ).isoformat(),
            "engine_version": "0.1.0",
        },
    }