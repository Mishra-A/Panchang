from datetime import datetime


def rank_recommendations(
    recommendations: list[dict],
    limit: int = 3,
) -> list[dict]:
    """
    Rank Muhurat recommendation windows.

    Priority:
    1. Recommended
    2. Acceptable
    3. Avoid

    Within the same status:
    higher score first
    then earlier start time.
    """

    status_priority = {
        "recommended": 0,
        "acceptable": 1,
        "avoid": 2,
    }

    def sort_key(item: dict):
        status = item.get(
            "status",
            "avoid",
        )

        score = item.get(
            "score",
            0,
        )

        start = datetime.fromisoformat(
            item["start"]
        )

        return (
            status_priority.get(
                status,
                99,
            ),
            -score,
            start,
        )

    ranked = sorted(
        recommendations,
        key=sort_key,
    )

    return ranked[:limit]
def get_best_recommendations(
    recommendations: list[dict],
    limit: int = 3,
) -> list[dict]:
    """
    Return only recommended/acceptable
    windows, ranked by quality.
    """

    usable = [
        item
        for item in recommendations
        if item.get("status")
        in {
            "recommended",
            "acceptable",
        }
    ]

    return rank_recommendations(
        usable,
        limit=limit,
    )