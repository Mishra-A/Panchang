from datetime import date

from backend.app.panchang.vara import calculate_vara


def test_vara():
    result = calculate_vara(
        date(2026, 8, 14)
    )

    assert result["name"] == "Friday"
    assert result["number"] == 5