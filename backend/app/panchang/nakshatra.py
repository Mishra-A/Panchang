from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import swisseph as swe
from backend.app.core.time_utils import format_ist

from backend.app.astronomy.ephemeris import get_planet_position



NAKSHATRA_NAMES = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishtha",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

NAKSHATRA_SPAN = 360.0 / 27.0
PADA_SPAN = NAKSHATRA_SPAN / 4.0


@dataclass(frozen=True)
class NakshatraResult:
    number: int
    name: str
    pada: int
    progress_degrees: float
    progress_percent: float


def calculate_nakshatra(
    moon_sidereal_longitude: float,
) -> NakshatraResult:

    longitude = moon_sidereal_longitude % 360.0

    nakshatra_index = int(
        longitude / NAKSHATRA_SPAN
    )

    nakshatra_start = (
        nakshatra_index * NAKSHATRA_SPAN
    )

    position_in_nakshatra = (
        longitude - nakshatra_start
    )

    pada = int(
        position_in_nakshatra / PADA_SPAN
    ) + 1

    progress_percent = (
        position_in_nakshatra / NAKSHATRA_SPAN
    ) * 100.0

    return NakshatraResult(
        number=nakshatra_index + 1,
        name=NAKSHATRA_NAMES[nakshatra_index],
        pada=pada,
        progress_degrees=position_in_nakshatra,
        progress_percent=progress_percent,
    )
def _julian_day(dt: datetime) -> float:
    """Convert timezone-aware datetime to Swiss Ephemeris UT Julian Day."""
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    dt = dt.astimezone(timezone.utc)

    hour = (
        dt.hour
        + dt.minute / 60.0
        + dt.second / 3600.0
        + dt.microsecond / 3_600_000_000.0
    )

    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        hour,
    )


def _moon_sidereal_longitude(julian_day: float) -> float:
    """Get Moon's Lahiri sidereal longitude."""
    result = get_planet_position(
        julian_day,
        swe.MOON,
        sidereal=True,
    )

    return result["longitude"]


def _nakshatra_index_from_datetime(dt: datetime) -> int:
    """Return zero-based Nakshatra index."""
    jd = _julian_day(dt)
    longitude = _moon_sidereal_longitude(jd)

    return int(longitude / NAKSHATRA_SPAN)


def find_nakshatra_end(
    start_datetime_utc: datetime,
    max_hours: int = 36,
) -> datetime:
    """
    Find the next Nakshatra transition.

    Returns the transition time in UTC.
    """

    if start_datetime_utc.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    start_datetime_utc = start_datetime_utc.astimezone(timezone.utc)

    current_index = _nakshatra_index_from_datetime(
        start_datetime_utc
    )

    previous_time = start_datetime_utc
    previous_index = current_index

    # Nakshatra normally lasts around 24 hours,
    # but we allow a larger search window.
    for hour in range(1, max_hours + 1):

        current_time = (
            start_datetime_utc
            + timedelta(hours=hour)
        )

        current_index = _nakshatra_index_from_datetime(
            current_time
        )

        if current_index != previous_index:

            # Boundary is between previous_time and current_time.
            left = previous_time
            right = current_time

            # Binary search to approximately 1 second.
            while (right - left).total_seconds() > 1:

                middle = (
                    left
                    + (right - left) / 2
                )

                middle_index = (
                    _nakshatra_index_from_datetime(
                        middle
                    )
                )

                if middle_index == previous_index:
                    left = middle
                else:
                    right = middle

            return right

        previous_time = current_time
        previous_index = current_index

    raise RuntimeError(
        f"Nakshatra transition not found within "
        f"{max_hours} hours"
    )
def get_nakshatra_with_end_time(
    start_datetime_utc: datetime,
) -> dict:
    """Return Nakshatra, Pada and next transition time."""

    jd = _julian_day(start_datetime_utc)

    moon = get_planet_position(
        jd,
        swe.MOON,
        sidereal=True,
    )

    result = calculate_nakshatra(
        moon["longitude"]
    )

    end_time = find_nakshatra_end(
        start_datetime_utc
    )

    return {
        "number": result.number,
        "name": result.name,
        "pada": result.pada,
        "progress_degrees": round(
            result.progress_degrees,
            6,
        ),
        "progress_percent": round(
            result.progress_percent,
            4,
        ),
        "ends_at_utc": end_time.isoformat(),
        "ends_at_ist": format_ist(end_time),
    }