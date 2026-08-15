from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import swisseph as swe

from backend.app.core.time_utils import format_ist


TITHI_NAMES = [
    "Pratipada",
    "Dvitiya",
    "Tritiya",
    "Chaturthi",
    "Panchami",
    "Shashthi",
    "Saptami",
    "Ashtami",
    "Navami",
    "Dashami",
    "Ekadashi",
    "Dvadashi",
    "Trayodashi",
    "Chaturdashi",
    "Purnima",
]


@dataclass(frozen=True)
class TithiResult:
    number: int
    name: str
    paksha: str
    progress_degrees: float
    progress_percent: float


def normalize_degrees(value: float) -> float:
    """Normalize an angle to the range [0, 360)."""
    return value % 360.0


def calculate_tithi(
    sun_longitude: float,
    moon_longitude: float,
) -> TithiResult:
    """
    Calculate Tithi from Sun and Moon longitudes.

    Tithi is based on the angular separation
    between Moon and Sun.

    Each Tithi covers 12 degrees.
    """

    separation = normalize_degrees(
        moon_longitude - sun_longitude
    )

    tithi_index = int(separation // 12.0)

    # --------------------------------------------------
    # Shukla Paksha
    # --------------------------------------------------
    if tithi_index < 15:
        paksha = "Shukla"

        number = tithi_index + 1

        name = TITHI_NAMES[tithi_index]

    # --------------------------------------------------
    # Krishna Paksha
    # --------------------------------------------------
    else:
        paksha = "Krishna"

        number = tithi_index - 14

        if number == 15:
            name = "Amavasya"
        else:
            name = TITHI_NAMES[number - 1]

    # Progress inside current Tithi
    progress_degrees = separation % 12.0

    progress_percent = (
        progress_degrees / 12.0
    ) * 100.0

    return TithiResult(
        number=number,
        name=name,
        paksha=paksha,
        progress_degrees=progress_degrees,
        progress_percent=progress_percent,
    )


def _angular_separation(
    julian_day: float,
) -> float:
    """
    Return Moon-Sun angular separation
    in degrees [0, 360).
    """

    sun_position, _, _ = swe.calc_ut(
        julian_day,
        swe.SUN,
    )

    moon_position, _, _ = swe.calc_ut(
        julian_day,
        swe.MOON,
    )

    return normalize_degrees(
        moon_position[0] - sun_position[0]
    )


def _tithi_index_from_jd(
    julian_day: float,
) -> int:
    """
    Return zero-based Tithi index.

    0-14  -> Shukla
    15-29 -> Krishna
    """

    separation = _angular_separation(
        julian_day
    )

    return int(separation // 12.0)


def _datetime_to_jd(
    dt: datetime,
) -> float:
    """
    Convert timezone-aware datetime
    to Swiss Ephemeris Julian Day.

    Swiss Ephemeris calculations use UT.
    """

    if dt.tzinfo is None:
        raise ValueError(
            "Datetime must be timezone-aware"
        )

    dt = dt.astimezone(timezone.utc)

    decimal_hour = (
        dt.hour
        + dt.minute / 60.0
        + dt.second / 3600.0
        + dt.microsecond / 3_600_000_000.0
    )

    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        decimal_hour,
    )


def find_tithi_end(
    start_datetime_utc: datetime,
    max_hours: int = 48,
) -> datetime:
    """
    Find the next Tithi boundary.

    The calculation is performed in UTC.

    First we search forward hour-by-hour
    to find the hour containing the boundary.

    Then binary search is used to find the
    transition to approximately one second.
    """

    if start_datetime_utc.tzinfo is None:
        raise ValueError(
            "start_datetime_utc must be timezone-aware"
        )

    start_datetime_utc = (
        start_datetime_utc.astimezone(
            timezone.utc
        )
    )

    # Current Tithi
    start_jd = _datetime_to_jd(
        start_datetime_utc
    )

    previous_index = _tithi_index_from_jd(
        start_jd
    )

    previous_time = start_datetime_utc

    # --------------------------------------------------
    # Find the hour containing the Tithi boundary
    # --------------------------------------------------

    for hour in range(
        1,
        max_hours + 1,
    ):

        current_time = (
            start_datetime_utc
            + timedelta(hours=hour)
        )

        current_jd = _datetime_to_jd(
            current_time
        )

        current_index = (
            _tithi_index_from_jd(
                current_jd
            )
        )

        # Tithi changed
        if current_index != previous_index:

            left = previous_time
            right = current_time

            # --------------------------------------------------
            # Binary search
            # --------------------------------------------------

            while (
                right - left
            ).total_seconds() > 1:

                middle = (
                    left
                    + (right - left) / 2
                )

                middle_jd = _datetime_to_jd(
                    middle
                )

                middle_index = (
                    _tithi_index_from_jd(
                        middle_jd
                    )
                )

                if (
                    middle_index
                    == previous_index
                ):
                    left = middle
                else:
                    right = middle

            return right

        previous_time = current_time
        previous_index = current_index

    raise RuntimeError(
        "Tithi transition not found "
        f"within {max_hours} hours"
    )


def get_tithi_with_end_time(
    start_datetime_utc: datetime,
) -> dict:
    """
    Return the current Tithi and its
    next transition time.

    Input:
        timezone-aware datetime.

    Output:
        Dictionary containing:

        number
        name
        paksha
        progress_degrees
        progress_percent
        ends_at_utc
        ends_at_ist
    """

    if start_datetime_utc.tzinfo is None:
        raise ValueError(
            "Datetime must be timezone-aware"
        )

    # Always calculate astronomical values in UTC
    start_datetime_utc = (
        start_datetime_utc.astimezone(
            timezone.utc
        )
    )

    # --------------------------------------------------
    # Julian Day
    # --------------------------------------------------

    jd = _datetime_to_jd(
        start_datetime_utc
    )

    # --------------------------------------------------
    # Sun position
    # --------------------------------------------------

    sun_position, _, _ = swe.calc_ut(
        jd,
        swe.SUN,
        swe.FLG_SWIEPH | swe.FLG_SPEED,
    )

    # --------------------------------------------------
    # Moon position
    # --------------------------------------------------

    moon_position, _, _ = swe.calc_ut(
        jd,
        swe.MOON,
        swe.FLG_SWIEPH | swe.FLG_SPEED,
    )

    # --------------------------------------------------
    # Calculate Tithi
    # --------------------------------------------------

    result = calculate_tithi(
        sun_longitude=sun_position[0],
        moon_longitude=moon_position[0],
    )

    # --------------------------------------------------
    # Find next Tithi boundary
    # --------------------------------------------------

    end_time = find_tithi_end(
        start_datetime_utc
    )

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------

    return {
        "number": result.number,
        "name": result.name,
        "paksha": result.paksha,
        "progress_degrees": round(
            result.progress_degrees,
            6,
        ),
        "progress_percent": round(
            result.progress_percent,
            4,
        ),
        "ends_at_utc": end_time.isoformat(),
        "ends_at_ist": format_ist(
            end_time
        ),
    }