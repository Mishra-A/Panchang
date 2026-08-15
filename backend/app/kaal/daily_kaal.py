from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from backend.app.core.location import Location
from backend.app.astronomy.sunrise import (
    calculate_sunrise_sunset,
)
from backend.app.kaal.kaal import (
    calculate_day_kaal,
    calculate_abhijit_muhurat,
    calculate_brahma_muhurta,
)
from backend.app.kaal.choghadiya import (
    calculate_choghadiya,
)
from backend.app.kaal.hora import (
    calculate_hora,
)


UTC = ZoneInfo("UTC")


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value).astimezone(UTC)


def _to_ist(value: datetime) -> datetime:
    return value.astimezone(
        ZoneInfo("Asia/Kolkata")
    )


def _get_sun_times(
    target_date: date,
    location: Location,
):
    data = calculate_sunrise_sunset(
        target_date=target_date,
        latitude=location.latitude,
        longitude=location.longitude,
    )

    sunrise = _parse_utc(
        data["sunrise_utc"]
    )

    sunset = _parse_utc(
        data["sunset_utc"]
    )

    return sunrise, sunset


def build_daily_kaal(
    target_date: date,
    location: Location,
) -> dict:

    sunrise_utc, sunset_utc = _get_sun_times(
        target_date,
        location,
    )

    next_sunrise_utc, _ = _get_sun_times(
        target_date + timedelta(days=1),
        location,
    )

    previous_sunrise_utc, _ = _get_sun_times(
        target_date - timedelta(days=1),
        location,
    )

    sunrise = _to_ist(sunrise_utc)
    sunset = _to_ist(sunset_utc)

    next_sunrise = _to_ist(
        next_sunrise_utc
    )

    previous_sunrise = _to_ist(
        previous_sunrise_utc
    )

    weekday = target_date.weekday()

    day_kaal = calculate_day_kaal(
        sunrise,
        sunset,
        target_date,
    )

    abhijit = calculate_abhijit_muhurat(
        sunrise,
        sunset,
    )

    brahma = calculate_brahma_muhurta(
        previous_sunrise,
        sunrise,
    )

    choghadiya = calculate_choghadiya(
        sunrise,
        sunset,
        next_sunrise,
        weekday,
    )

    hora = calculate_hora(
        sunrise,
        sunset,
        next_sunrise,
        weekday,
    )

    return {
        "date": target_date.isoformat(),

        "location": {
            "city": location.city,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone": location.timezone,
        },

        "sun": {
            "sunrise": sunrise.isoformat(),
            "sunset": sunset.isoformat(),
            "previous_sunrise": (
                previous_sunrise.isoformat()
            ),
            "next_sunrise": (
                next_sunrise.isoformat()
            ),
        },

        "kaal": day_kaal,

        "muhurat": {
            "abhijit": abhijit,
            "brahma_muhurta": brahma,
        },

        "choghadiya": choghadiya,

        "hora": hora,
    }