from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from backend.app.core.rule_loader import load_rule

IST = ZoneInfo("Asia/Kolkata")





def _parse_ist(value: str) -> datetime:
    dt = datetime.fromisoformat(value)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)

    return dt.astimezone(IST)


def _segment_time(
    sunrise: datetime,
    sunset: datetime,
    segment: int,
) -> tuple[datetime, datetime]:

    day_duration = sunset - sunrise
    segment_duration = day_duration / 8

    start = sunrise + (
        segment_duration * segment
    )

    end = start + segment_duration

    return start, end


def calculate_kaal_period(
    sunrise_ist: datetime,
    sunset_ist: datetime,
    weekday: int,
    segment_map: dict[int, int],
) -> dict:

    segment = segment_map[weekday]

    start, end = _segment_time(
        sunrise_ist,
        sunset_ist,
        segment,
    )

    return {
        "segment": segment + 1,
        "starts_at": start.isoformat(),
        "ends_at": end.isoformat(),
    }


def calculate_day_kaal(
    sunrise_ist: datetime,
    sunset_ist: datetime,
    target_date,
) -> dict:

    weekday = target_date.weekday()

    rahu_segments = _load_kaal_segments(
        "rahu_kaal"
    )

    yamaganda_segments = _load_kaal_segments(
        "yamaganda"
    )

    gulika_segments = _load_kaal_segments(
        "gulika"
    )

    return {
        "rahu_kaal": calculate_kaal_period(
            sunrise_ist,
            sunset_ist,
            weekday,
            rahu_segments,
        ),

        "yamaganda": calculate_kaal_period(
            sunrise_ist,
            sunset_ist,
            weekday,
            yamaganda_segments,
        ),

        "gulika": calculate_kaal_period(
            sunrise_ist,
            sunset_ist,
            weekday,
            gulika_segments,
        ),
    }
def calculate_abhijit_muhurat(
    sunrise_ist: datetime,
    sunset_ist: datetime,
) -> dict:
    """
    Calculate Abhijit Muhurat around local solar noon.

    Daytime is divided into 15 equal Muhurta periods.
    Abhijit is the 8th daytime Muhurta.
    """

    day_duration = sunset_ist - sunrise_ist
    muhurta_duration = day_duration / 15

    start = sunrise_ist + (
        muhurta_duration * 7
    )

    end = start + muhurta_duration

    return {
        "name": "Abhijit Muhurat",
        "starts_at": start.isoformat(),
        "ends_at": end.isoformat(),
    }


def calculate_brahma_muhurta(
    previous_sunrise_ist: datetime,
    current_sunrise_ist: datetime,
) -> dict:
    """
    Calculate Brahma Muhurta before the current sunrise.

    Traditional calculation:
    Brahma Muhurta begins 2 Muhurtas before sunrise
    and lasts for one Muhurta.

    One Muhurta = night duration / 15.
    """

    night_duration = (
        current_sunrise_ist
        - previous_sunrise_ist
    )

    muhurta_duration = night_duration / 15

    start = current_sunrise_ist - (
        muhurta_duration * 2
    )

    end = current_sunrise_ist - muhurta_duration

    return {
        "name": "Brahma Muhurta",
        "starts_at": start.isoformat(),
        "ends_at": end.isoformat(),
    }
WEEKDAY_KEYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def _load_kaal_segments(rule_name: str) -> dict[int, int]:
    rules = load_rule("kaal_rules.json")

    segments = rules[rule_name]["segments"]

    return {
        index: segments[WEEKDAY_KEYS[index]]
        for index in range(7)
    }