from datetime import datetime


# Intervals smaller than this are considered
# duplicate/near-identical boundaries.
BOUNDARY_TOLERANCE_SECONDS = 0.01


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _add_boundary(
    boundaries: list[datetime],
    value: datetime,
) -> None:
    """
    Add a boundary unless it is effectively identical
    to an existing boundary.

    This prevents tiny microsecond intervals such as:

        15:27:38.750000
        15:27:38.750003
    """

    for existing in boundaries:

        difference = abs(
            (value - existing).total_seconds()
        )

        if difference <= BOUNDARY_TOLERANCE_SECONDS:
            return

    boundaries.append(value)


def collect_boundaries(
    start: datetime,
    end: datetime,
    *period_groups: list[dict],
) -> list[datetime]:
    """
    Collect unique interval boundaries.

    Boundaries that differ only by a very small amount
    are merged to avoid meaningless micro-intervals.
    """

    boundaries = [
        start,
        end,
    ]

    for periods in period_groups:

        for period in periods:

            period_start = _parse(
                period["starts_at"]
            )

            period_end = _parse(
                period["ends_at"]
            )

            if (
                start < period_start < end
            ):
                _add_boundary(
                    boundaries,
                    period_start,
                )

            if (
                start < period_end < end
            ):
                _add_boundary(
                    boundaries,
                    period_end,
                )

    return sorted(boundaries)


def split_interval(
    start: datetime,
    end: datetime,
    *period_groups: list[dict],
) -> list[
    tuple[datetime, datetime]
]:

    boundaries = collect_boundaries(
        start,
        end,
        *period_groups,
    )

    intervals = []

    for i in range(
        len(boundaries) - 1
    ):

        interval_start = boundaries[i]
        interval_end = boundaries[i + 1]

        # Ignore zero/near-zero intervals.
        if (
            interval_end
            <= interval_start
        ):
            continue

        if (
            interval_end - interval_start
        ).total_seconds() <= (
            BOUNDARY_TOLERANCE_SECONDS
        ):
            continue

        intervals.append(
            (
                interval_start,
                interval_end,
            )
        )

    return intervals


def find_period_at(
    start: datetime,
    end: datetime,
    periods: list[dict],
) -> dict | None:
    """
    Find the period that completely contains
    the requested interval.
    """

    for period in periods:

        period_start = _parse(
            period["starts_at"]
        )

        period_end = _parse(
            period["ends_at"]
        )

        if (
            start >= period_start
            and end <= period_end
        ):
            return period

    return None


def find_overlapping_periods(
    start: datetime,
    end: datetime,
    periods: list[dict],
) -> list[dict]:
    """
    Return all periods overlapping the interval.
    """

    result = []

    for period in periods:

        period_start = _parse(
            period["starts_at"]
        )

        period_end = _parse(
            period["ends_at"]
        )

        if (
            start < period_end
            and end > period_start
        ):
            result.append(period)

    return result