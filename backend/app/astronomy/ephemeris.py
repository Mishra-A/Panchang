from pathlib import Path

import swisseph as swe


EPHEMERIS_PATH = (
    Path(__file__).resolve().parents[3] / "data" / "ephemeris"
)

swe.set_ephe_path(str(EPHEMERIS_PATH))
swe.set_sid_mode(swe.SIDM_LAHIRI)


def get_planet_position(
    julian_day: float,
    planet: int,
    sidereal: bool = False,
):
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    if sidereal:
        flags |= swe.FLG_SIDEREAL

    position, retflag, serr = swe.calc_ut(
        julian_day,
        planet,
        flags,
    )

    return {
        "longitude": position[0],
        "latitude": position[1],
        "distance": position[2],
        "speed_longitude": position[3],
        "retflag": retflag,
        "error": serr,
    }


def get_sun_moon(julian_day: float):
    return {
        "sun": get_planet_position(
            julian_day,
            swe.SUN,
            sidereal=False,
        ),
        "moon": get_planet_position(
            julian_day,
            swe.MOON,
            sidereal=False,
        ),
    }


def get_sidereal_sun_moon(julian_day: float):
    return {
        "sun": get_planet_position(
            julian_day,
            swe.SUN,
            sidereal=True,
        ),
        "moon": get_planet_position(
            julian_day,
            swe.MOON,
            sidereal=True,
        ),
    }