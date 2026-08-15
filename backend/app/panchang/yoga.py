from dataclasses import dataclass


YOGA_NAMES = [
    "Vishkambha",
    "Priti",
    "Ayushman",
    "Saubhagya",
    "Shobhana",
    "Atiganda",
    "Sukarma",
    "Dhriti",
    "Shula",
    "Ganda",
    "Vriddhi",
    "Dhruva",
    "Vyaghata",
    "Harshana",
    "Vajra",
    "Siddhi",
    "Vyatipata",
    "Variyana",
    "Parigha",
    "Shiva",
    "Siddha",
    "Sadhya",
    "Shubha",
    "Shukla",
    "Brahma",
    "Indra",
    "Vaidhriti",
]

YOGA_SPAN = 360.0 / 27.0


@dataclass(frozen=True)
class YogaResult:
    number: int
    name: str
    progress_degrees: float
    progress_percent: float


def calculate_yoga(
    sun_sidereal_longitude: float,
    moon_sidereal_longitude: float,
) -> YogaResult:

    total_longitude = (
        sun_sidereal_longitude
        + moon_sidereal_longitude
    ) % 360.0

    yoga_index = int(
        total_longitude / YOGA_SPAN
    )

    yoga_start = (
        yoga_index * YOGA_SPAN
    )

    progress_degrees = (
        total_longitude - yoga_start
    )

    progress_percent = (
        progress_degrees / YOGA_SPAN
    ) * 100.0

    return YogaResult(
        number=yoga_index + 1,
        name=YOGA_NAMES[yoga_index],
        progress_degrees=progress_degrees,
        progress_percent=progress_percent,
    )
from datetime import datetime, timedelta, timezone

import swisseph as swe

from backend.app.astronomy.ephemeris import get_sidereal_sun_moon


def _julian_day(dt: datetime) -> float:
    """Convert timezone-aware datetime to UT Julian Day."""

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


def _yoga_index_from_datetime(dt: datetime) -> int:
    """Return the current zero-based Yoga index."""

    jd = _julian_day(dt)

    data = get_sidereal_sun_moon(jd)

    sun = data["sun"]["longitude"]
    moon = data["moon"]["longitude"]

    total = (sun + moon) % 360.0

    return int(total / YOGA_SPAN)


def find_yoga_end(
    start_datetime_utc: datetime,
    max_hours: int = 36,
) -> datetime:
    """
    Find the next Yoga transition.

    Returns the transition time in UTC.
    """

    if start_datetime_utc.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    start_datetime_utc = (
        start_datetime_utc.astimezone(timezone.utc)
    )

    previous_time = start_datetime_utc
    previous_index = _yoga_index_from_datetime(
        previous_time
    )

    # Search forward until the Yoga changes.
    for hour in range(1, max_hours + 1):

        current_time = (
            start_datetime_utc
            + timedelta(hours=hour)
        )

        current_index = _yoga_index_from_datetime(
            current_time
        )

        if current_index != previous_index:

            left = previous_time
            right = current_time

            # Binary search to approximately 1 second.
            while (right - left).total_seconds() > 1:

                middle = (
                    left
                    + (right - left) / 2
                )

                middle_index = _yoga_index_from_datetime(
                    middle
                )

                if middle_index == previous_index:
                    left = middle
                else:
                    right = middle

            return right

        previous_time = current_time
        previous_index = current_index

    raise RuntimeError(
        f"Yoga transition not found within {max_hours} hours"
    )
from backend.app.core.time_utils import format_ist

def get_yoga_with_end_time(
    start_datetime_utc: datetime,
) -> dict:
    """Return current Yoga and its next transition time."""

    jd = _julian_day(start_datetime_utc)

    data = get_sidereal_sun_moon(jd)

    sun = data["sun"]["longitude"]
    moon = data["moon"]["longitude"]

    result = calculate_yoga(
        sun_sidereal_longitude=sun,
        moon_sidereal_longitude=moon,
    )

    end_time = find_yoga_end(
        start_datetime_utc
    )

    return {
        "number": result.number,
        "name": result.name,
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