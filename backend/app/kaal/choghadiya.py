from datetime import datetime, timedelta


DAY_SEQUENCE = {
    0: ["Udveg", "Chal", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"],
    1: ["Rog", "Udveg", "Chal", "Labh", "Amrit", "Kaal", "Shubh", "Rog"],
    2: ["Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Chal", "Labh"],
    3: ["Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Chal", "Labh", "Amrit"],
    4: ["Kaal", "Shubh", "Rog", "Udveg", "Chal", "Labh", "Amrit", "Kaal"],
    5: ["Shubh", "Rog", "Udveg", "Chal", "Labh", "Amrit", "Kaal", "Shubh"],
    6: ["Chal", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Chal"],
}


NIGHT_SEQUENCE = {
    0: ["Shubh", "Amrit", "Chal", "Rog", "Kaal", "Labh", "Udveg", "Shubh"],
    1: ["Chal", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Chal"],
    2: ["Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Chal", "Rog", "Kaal"],
    3: ["Labh", "Udveg", "Shubh", "Amrit", "Chal", "Rog", "Kaal", "Labh"],
    4: ["Udveg", "Shubh", "Amrit", "Chal", "Rog", "Kaal", "Labh", "Udveg"],
    5: ["Amrit", "Chal", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit"],
    6: ["Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Chal", "Rog"],
}


def _build_periods(
    start: datetime,
    end: datetime,
    sequence: list[str],
) -> list[dict]:

    duration = (end - start) / 8

    periods = []

    for index, name in enumerate(sequence):

        period_start = start + (
            duration * index
        )

        period_end = period_start + duration

        periods.append(
            {
                "number": index + 1,
                "type": name,
                "starts_at": period_start.isoformat(),
                "ends_at": period_end.isoformat(),
            }
        )

    return periods


def calculate_choghadiya(
    sunrise: datetime,
    sunset: datetime,
    next_sunrise: datetime,
    weekday: int,
) -> dict:

    day_periods = _build_periods(
        sunrise,
        sunset,
        DAY_SEQUENCE[weekday],
    )

    night_periods = _build_periods(
        sunset,
        next_sunrise,
        NIGHT_SEQUENCE[weekday],
    )

    return {
        "day": day_periods,
        "night": night_periods,
    }