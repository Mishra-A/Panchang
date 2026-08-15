from backend.app.muhurat.ranking import (
    rank_recommendations,
)


def test_rank_recommendations():

    recommendations = [
        {
            "activity": "vehicle_purchase",
            "start": "2026-08-14T12:00:00+05:30",
            "end": "2026-08-14T13:00:00+05:30",
            "status": "acceptable",
            "score": 50,
            "reasons": [],
            "warnings": [],
        },
        {
            "activity": "vehicle_purchase",
            "start": "2026-08-14T09:00:00+05:30",
            "end": "2026-08-14T10:00:00+05:30",
            "status": "recommended",
            "score": 70,
            "reasons": [],
            "warnings": [],
        },
        {
            "activity": "vehicle_purchase",
            "start": "2026-08-14T11:00:00+05:30",
            "end": "2026-08-14T12:00:00+05:30",
            "status": "recommended",
            "score": 90,
            "reasons": [],
            "warnings": [],
        },
        {
            "activity": "vehicle_purchase",
            "start": "2026-08-14T08:00:00+05:30",
            "end": "2026-08-14T09:00:00+05:30",
            "status": "avoid",
            "score": 0,
            "reasons": [],
            "warnings": [],
        },
    ]

    result = rank_recommendations(
        recommendations,
        limit=3,
    )

    assert len(result) == 3

    assert result[0]["score"] == 90
    assert result[1]["score"] == 70
    assert result[2]["score"] == 50