from dataclasses import dataclass


MOVABLE_KARANAS = [
    "Bava",
    "Balava",
    "Kaulava",
    "Taitila",
    "Garaja",
    "Vanija",
    "Vishti",
]

FIXED_KARANAS = [
    "Shakuni",
    "Chatushpada",
    "Naga",
    "Kimstughna",
]


@dataclass(frozen=True)
class KaranaResult:
    index: int
    name: str
    type: str


def calculate_karana_from_separation(
    separation: float,
) -> KaranaResult:
    """
    Calculate Karana from Moon-Sun angular separation.

    separation: 0 <= separation < 360 degrees
    """

    separation = separation % 360.0

    # Each Karana spans 6 degrees.
    karana_index = int(separation // 6.0)

    # First half of Shukla Pratipada:
    # Kimstughna
    if karana_index == 0:
        return KaranaResult(
            index=1,
            name="Kimstughna",
            type="fixed",
        )

    # Last four half-Tithis:
    # Krishna Chaturdashi second half onward
    if karana_index == 57:
        return KaranaResult(
            index=58,
            name="Shakuni",
            type="fixed",
        )

    if karana_index == 58:
        return KaranaResult(
            index=59,
            name="Chatushpada",
            type="fixed",
        )

    if karana_index == 59:
        return KaranaResult(
            index=60,
            name="Naga",
            type="fixed",
        )

    # Remaining positions use the 7 movable Karanas cyclically.
    movable_index = (karana_index - 1) % 7

    return KaranaResult(
        index=karana_index + 1,
        name=MOVABLE_KARANAS[movable_index],
        type="movable",
    )


def calculate_karana(
    sun_longitude: float,
    moon_longitude: float,
) -> KaranaResult:
    """
    Calculate current Karana using the Moon-Sun
    angular separation.
    """

    separation = (
        moon_longitude - sun_longitude
    ) % 360.0

    return calculate_karana_from_separation(
        separation
    )
from datetime import datetime, timedelta, timezone

import swisseph as swe

from backend.app.astronomy.ephemeris import get_sun_moon
from backend.app.core.time_utils import format_ist


def _julian_day(dt: datetime) -> float:
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


def _karana_index_from_datetime(dt: datetime) -> int:
    jd = _julian_day(dt)

    data = get_sun_moon(jd)

    separation = (
        data["moon"]["longitude"]
        - data["sun"]["longitude"]
    ) % 360.0

    return int(separation // 6.0)


def find_karana_end(
    start_datetime_utc: datetime,
    max_hours: int = 24,
) -> datetime:

    if start_datetime_utc.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    start_datetime_utc = (
        start_datetime_utc.astimezone(timezone.utc)
    )

    previous_time = start_datetime_utc
    previous_index = _karana_index_from_datetime(
        previous_time
    )

    for hour in range(1, max_hours + 1):

        current_time = (
            start_datetime_utc
            + timedelta(hours=hour)
        )

        current_index = _karana_index_from_datetime(
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

                middle_index = (
                    _karana_index_from_datetime(
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
        f"Karana transition not found within {max_hours} hours"
    )


def get_karana_with_end_time(
    start_datetime_utc: datetime,
) -> dict:

    if start_datetime_utc.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    start_datetime_utc = (
        start_datetime_utc.astimezone(timezone.utc)
    )

    jd = _julian_day(start_datetime_utc)

    data = get_sun_moon(jd)

    result = calculate_karana(
        sun_longitude=data["sun"]["longitude"],
        moon_longitude=data["moon"]["longitude"],
    )

    end_time = find_karana_end(
        start_datetime_utc
    )

    return {
        "index": result.index,
        "name": result.name,
        "type": result.type,
        "ends_at_utc": end_time.isoformat(),
        "ends_at_ist": format_ist(end_time),
    }