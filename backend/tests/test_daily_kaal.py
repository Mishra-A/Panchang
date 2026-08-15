from datetime import date

from backend.app.core.location import LUCKNOW
from backend.app.kaal.daily_kaal import (
    build_daily_kaal,
)


def test_daily_kaal():

    result = build_daily_kaal(
        target_date=date(2026, 8, 14),
        location=LUCKNOW,
    )

    assert result["date"] == "2026-08-14"

    assert result["sun"]["sunrise"]
    assert result["sun"]["sunset"]

    assert result["kaal"]["rahu_kaal"]
    assert result["kaal"]["yamaganda"]
    assert result["kaal"]["gulika"]

    assert result["muhurat"]["abhijit"]
    assert result["muhurat"]["brahma_muhurta"]

    assert len(
        result["choghadiya"]["day"]
    ) == 8

    assert len(
        result["choghadiya"]["night"]
    ) == 8

    assert len(
        result["hora"]["day"]
    ) == 12

    assert len(
        result["hora"]["night"]
    ) == 12