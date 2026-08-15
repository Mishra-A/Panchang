from datetime import datetime


PLANETS = [
    "Sun",
    "Venus",
    "Mercury",
    "Moon",
    "Saturn",
    "Jupiter",
    "Mars",
]


# Planetary-hour sequence repeats continuously.
# The first Hora of the day is ruled by the weekday lord.
WEEKDAY_LORDS = {
    0: "Moon",     # Monday
    1: "Mars",     # Tuesday
    2: "Mercury",  # Wednesday
    3: "Jupiter",  # Thursday
    4: "Venus",    # Friday
    5: "Saturn",   # Saturday
    6: "Sun",      # Sunday
}


def _planet_sequence(start_planet: str, count: int) -> list[str]:
    start_index = PLANETS.index(start_planet)

    return [
        PLANETS[(start_index + i) % len(PLANETS)]
        for i in range(count)
    ]


def _build_horas(
    start: datetime,
    end: datetime,
    planets: list[str],
    period_count: int,
    start_number: int,
) -> list[dict]:

    duration = (end - start) / period_count

    result = []

    for i in range(period_count):

        period_start = start + (
            duration * i
        )

        period_end = period_start + duration

        result.append(
            {
                "number": start_number + i,
                "planet": planets[i],
                "starts_at": period_start.isoformat(),
                "ends_at": period_end.isoformat(),
            }
        )

    return result


def calculate_hora(
    sunrise: datetime,
    sunset: datetime,
    next_sunrise: datetime,
    weekday: int,
) -> dict:

    day_lord = WEEKDAY_LORDS[weekday]

    sequence = _planet_sequence(
        day_lord,
        24,
    )

    day_planets = sequence[:12]
    night_planets = sequence[12:24]

    day_horas = _build_horas(
        sunrise,
        sunset,
        day_planets,
        12,
        1,
    )

    night_horas = _build_horas(
        sunset,
        next_sunrise,
        night_planets,
        12,
        13,
    )

    return {
        "day": day_horas,
        "night": night_horas,
    }