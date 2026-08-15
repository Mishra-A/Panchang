from backend.app.panchang.karana import (
    calculate_karana,
    calculate_karana_from_separation,
)


def test_first_karana():

    result = calculate_karana_from_separation(0.0)

    assert result.name == "Kimstughna"
    assert result.type == "fixed"


def test_first_movable_karana():

    result = calculate_karana_from_separation(6.0)

    assert result.name == "Bava"
    assert result.type == "movable"


def test_movable_sequence():

    result = calculate_karana_from_separation(12.0)

    assert result.name == "Balava"


def test_vishti():

    result = calculate_karana_from_separation(42.0)

    assert result.name == "Vishti"


def test_karana_from_sun_moon():

    result = calculate_karana(
        sun_longitude=141.72937454572937,
        moon_longitude=165.03730574860634,
    )

    assert result.name
    assert result.type in [
        "movable",
        "fixed",
    ]
from datetime import datetime, timezone

from backend.app.panchang.karana import (
    get_karana_with_end_time,
)


def test_karana_has_end_time():

    start = datetime(
        2026,
        8,
        14,
        12,
        0,
        0,
        tzinfo=timezone.utc,
    )

    result = get_karana_with_end_time(start)

    assert result["name"]
    assert result["type"] in [
        "movable",
        "fixed",
    ]

    assert result["ends_at_utc"]
    assert result["ends_at_ist"]

    end_time = datetime.fromisoformat(
        result["ends_at_utc"]
    )

    assert end_time > start    