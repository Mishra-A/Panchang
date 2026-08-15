from datetime import datetime, timezone

import swisseph as swe


def _julian_day(dt: datetime) -> float:
    if dt.tzinfo is None:
        raise ValueError(
            "Datetime must be timezone-aware"
        )

    dt = dt.astimezone(timezone.utc)

    hour = (
        dt.hour
        + dt.minute / 60
        + dt.second / 3600
    )

    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        hour,
    )


def _datetime_from_jd(jd: float) -> datetime:
    year, month, day, hour = swe.revjul(
        jd,
        swe.GREG_CAL,
    )

    hour_int = int(hour)
    minute_float = (
        hour - hour_int
    ) * 60

    minute_int = int(minute_float)
    second = int(
        round(
            (minute_float - minute_int)
            * 60
        )
    )

    if second == 60:
        second = 59

    return datetime(
        year,
        month,
        day,
        hour_int,
        minute_int,
        second,
        tzinfo=timezone.utc,
    )


def calculate_sunrise_sunset(
    target_date,
    latitude: float,
    longitude: float,
) -> dict:

    jd = swe.julday(
        target_date.year,
        target_date.month,
        target_date.day,
        0.0,
    )

    geopos = (
        longitude,
        latitude,
        0.0,
    )

    sunrise_result = swe.rise_trans(
        jd,
        swe.SUN,
        swe.CALC_RISE,
        geopos,
    )

    sunset_result = swe.rise_trans(
        jd,
        swe.SUN,
        swe.CALC_SET,
        geopos,
    )

    sunrise_jd = sunrise_result[1][0]
    sunset_jd = sunset_result[1][0]

    sunrise = _datetime_from_jd(
        sunrise_jd
    )

    sunset = _datetime_from_jd(
        sunset_jd
    )

    return {
        "sunrise_utc": sunrise.isoformat(),
        "sunset_utc": sunset.isoformat(),
    }
from datetime import datetime, timezone

import swisseph as swe


def _julian_day_for_date(target_date) -> float:
    return swe.julday(
        target_date.year,
        target_date.month,
        target_date.day,
        0.0,
    )


def _jd_to_datetime_utc(jd: float) -> datetime:
    year, month, day, hour = swe.revjul(
        jd,
        swe.GREG_CAL,
    )

    hour_int = int(hour)
    minute_float = (hour - hour_int) * 60
    minute_int = int(minute_float)
    second = round(
        (minute_float - minute_int) * 60
    )

    if second >= 60:
        second = 59

    return datetime(
        year,
        month,
        day,
        hour_int,
        minute_int,
        second,
        tzinfo=timezone.utc,
    )


def calculate_sunrise_sunset(
    target_date,
    latitude: float,
    longitude: float,
) -> dict:

    jd = _julian_day_for_date(target_date)

    geopos = (
        longitude,
        latitude,
        0.0,
    )

    sunrise = swe.rise_trans(
        jd,
        swe.SUN,
        swe.CALC_RISE,
        geopos,
    )

    sunset = swe.rise_trans(
        jd,
        swe.SUN,
        swe.CALC_SET,
        geopos,
    )

    sunrise_jd = sunrise[1][0]
    sunset_jd = sunset[1][0]

    sunrise_dt = _jd_to_datetime_utc(
        sunrise_jd
    )

    sunset_dt = _jd_to_datetime_utc(
        sunset_jd
    )

    return {
        "sunrise_utc": sunrise_dt.isoformat(),
        "sunset_utc": sunset_dt.isoformat(),
    }