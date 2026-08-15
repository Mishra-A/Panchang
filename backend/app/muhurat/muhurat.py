from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class MuhuratRule:
    activity: str

    allowed_choghadiya: set[str] = field(
        default_factory=set
    )

    preferred_hora: set[str] = field(
        default_factory=set
    )

    blocked_periods: set[str] = field(
        default_factory=set
    )

    panchang_conditions: dict = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class MuhuratWindow:
    activity: str
    start: datetime
    end: datetime
    status: str
    score: int
    reasons: list[str]
    warnings: list[str]


def evaluate_choghadiya(
    choghadiya_period: dict,
    rule: MuhuratRule,
) -> tuple[int, list[str], list[str]]:

    period_type = choghadiya_period["type"]

    if period_type in rule.allowed_choghadiya:
        return (
            40,
            [f"Choghadiya: {period_type}"],
            [],
        )

    return (
        0,
        [],
        [
            f"Choghadiya not preferred: "
            f"{period_type}"
        ],
    )


def evaluate_hora(
    hora_period: dict,
    rule: MuhuratRule,
) -> tuple[int, list[str], list[str]]:

    planet = hora_period["planet"]

    if planet in rule.preferred_hora:
        return (
            30,
            [f"Hora: {planet}"],
            [],
        )

    return (
        0,
        [],
        [
            f"Hora not preferred: "
            f"{planet}"
        ],
    )


def is_blocked_period(
    start: datetime,
    end: datetime,
    blocked_periods: list[dict],
) -> tuple[bool, list[str]]:

    warnings = []

    for period in blocked_periods:

        blocked_start = datetime.fromisoformat(
            period["starts_at"]
        )

        blocked_end = datetime.fromisoformat(
            period["ends_at"]
        )

        overlaps = (
            start < blocked_end
            and end > blocked_start
        )

        if overlaps:
            warnings.append(
                f"Overlaps {period['name']}"
            )

            return True, warnings

    return False, warnings


def evaluate_window(
    activity: str,
    start: datetime,
    end: datetime,
    rule: MuhuratRule,
    choghadiya_period: dict,
    hora_period: dict,
    blocked_periods: list[dict],
) -> MuhuratWindow:

    score = 0
    reasons = []
    warnings = []

    ch_score, ch_reasons, ch_warnings = (
        evaluate_choghadiya(
            choghadiya_period,
            rule,
        )
    )

    hora_score, hora_reasons, hora_warnings = (
        evaluate_hora(
            hora_period,
            rule,
        )
    )

    score += ch_score
    score += hora_score

    reasons.extend(ch_reasons)
    reasons.extend(hora_reasons)

    warnings.extend(ch_warnings)
    warnings.extend(hora_warnings)

    blocked, blocked_warnings = (
        is_blocked_period(
            start,
            end,
            blocked_periods,
        )
    )

    if blocked:
        score = 0
        warnings.extend(blocked_warnings)

    if score >= 60 and not blocked:
        status = "recommended"

    elif score > 0 and not blocked:
        status = "acceptable"

    else:
        status = "avoid"

    return MuhuratWindow(
        activity=activity,
        start=start,
        end=end,
        status=status,
        score=score,
        reasons=reasons,
        warnings=warnings,
    )