import swisseph as swe

from backend.app.astronomy.ephemeris import get_sun_moon


def test_sun_moon_calculation():
    julian_day = swe.julday(2026, 8, 14, 12.0)

    result = get_sun_moon(julian_day)

    assert "sun" in result
    assert "moon" in result

    assert 0 <= result["sun"]["longitude"] < 360
    assert 0 <= result["moon"]["longitude"] < 360