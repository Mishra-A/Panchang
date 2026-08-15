from dataclasses import dataclass


@dataclass(frozen=True)
class PanchangEvaluation:
    score: int
    reasons: list[str]
    warnings: list[str]


def _get_name(value) -> str | None:
    """
    Safely extract a Panchang item's name.

    Supports:
        None
        "Friday"
        {"name": "Friday"}
    """

    if value is None:
        return None

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        return value.get("name")

    return None


def _get_conditions(rule_config: dict) -> dict:
    """
    Normalize Panchang rule configuration.

    recommendation.py passes:
        rule.panchang_conditions

    Therefore rule_config is already the
    panchang_conditions dictionary.
    """

    if not isinstance(rule_config, dict):
        return {}

    return rule_config


def evaluate_panchang(
    daily_panchang: dict,
    rule_config: dict,
) -> PanchangEvaluation:
    """
    Evaluate daily-level Panchang conditions.

    Used when evaluating the complete daily
    Panchang snapshot.

    Evaluates:
        Tithi
        Nakshatra
        Yoga
        Vara
    """

    score = 0
    reasons = []
    warnings = []

    conditions = _get_conditions(
        rule_config
    )

    if not isinstance(daily_panchang, dict):
        daily_panchang = {}

    panchang_data = (
        daily_panchang.get("panchang")
        or {}
    )

    if not isinstance(panchang_data, dict):
        panchang_data = {}

    # --------------------------------------------------
    # TITHI
    # --------------------------------------------------

    tithi_name = _get_name(
        panchang_data.get("tithi")
    )

    tithi_config = (
        conditions.get("tithi")
        or {}
    )

    if tithi_name in tithi_config.get(
        "preferred",
        [],
    ):
        score += tithi_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Tithi: {tithi_name}"
        )

    elif tithi_name in tithi_config.get(
        "avoid",
        [],
    ):
        score -= tithi_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Tithi not preferred: "
            f"{tithi_name}"
        )

    # --------------------------------------------------
    # NAKSHATRA
    # --------------------------------------------------

    nakshatra_name = _get_name(
        panchang_data.get("nakshatra")
    )

    nakshatra_config = (
        conditions.get("nakshatra")
        or {}
    )

    if nakshatra_name in nakshatra_config.get(
        "preferred",
        [],
    ):
        score += nakshatra_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Nakshatra: {nakshatra_name}"
        )

    elif nakshatra_name in nakshatra_config.get(
        "avoid",
        [],
    ):
        score -= nakshatra_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Nakshatra not preferred: "
            f"{nakshatra_name}"
        )

    # --------------------------------------------------
    # YOGA
    # --------------------------------------------------

    yoga_name = _get_name(
        panchang_data.get("yoga")
    )

    yoga_config = (
        conditions.get("yoga")
        or {}
    )

    if yoga_name in yoga_config.get(
        "preferred",
        [],
    ):
        score += yoga_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Yoga: {yoga_name}"
        )

    elif yoga_name in yoga_config.get(
        "avoid",
        [],
    ):
        score -= yoga_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Yoga not preferred: "
            f"{yoga_name}"
        )

    # --------------------------------------------------
    # VARA
    # --------------------------------------------------

    vara_name = _get_name(
        daily_panchang.get("vara")
    )

    vara_config = (
        conditions.get("vara")
        or {}
    )

    if vara_name in vara_config.get(
        "preferred",
        [],
    ):
        score += vara_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Vara: {vara_name}"
        )

    elif vara_name in vara_config.get(
        "avoid",
        [],
    ):
        score -= vara_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Vara not preferred: "
            f"{vara_name}"
        )

    return PanchangEvaluation(
        score=score,
        reasons=reasons,
        warnings=warnings,
    )


def evaluate_interval_panchang(
    daily_panchang: dict,
    tithi_period: dict | None,
    nakshatra_period: dict | None,
    yoga_period: dict | None,
    rule_config: dict,
) -> PanchangEvaluation:
    """
    Evaluate Panchang conditions for one
    exact Muhurat interval.

    Tithi, Nakshatra and Yoga come from
    the astronomical daily timeline.

    Vara comes from the daily Panchang.

    rule_config must be the actual
    panchang_conditions dictionary.
    """

    score = 0
    reasons = []
    warnings = []

    conditions = _get_conditions(
        rule_config
    )

    if not isinstance(daily_panchang, dict):
        daily_panchang = {}

    # --------------------------------------------------
    # TITHI
    # --------------------------------------------------

    tithi_name = _get_name(
        tithi_period
    )

    tithi_config = (
        conditions.get("tithi")
        or {}
    )

    if tithi_name in tithi_config.get(
        "preferred",
        [],
    ):
        score += tithi_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Tithi: {tithi_name}"
        )

    elif tithi_name in tithi_config.get(
        "avoid",
        [],
    ):
        score -= tithi_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Tithi not preferred: "
            f"{tithi_name}"
        )

    # --------------------------------------------------
    # NAKSHATRA
    # --------------------------------------------------

    nakshatra_name = _get_name(
        nakshatra_period
    )

    nakshatra_config = (
        conditions.get("nakshatra")
        or {}
    )

    if nakshatra_name in nakshatra_config.get(
        "preferred",
        [],
    ):
        score += nakshatra_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Nakshatra: {nakshatra_name}"
        )

    elif nakshatra_name in nakshatra_config.get(
        "avoid",
        [],
    ):
        score -= nakshatra_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Nakshatra not preferred: "
            f"{nakshatra_name}"
        )

    # --------------------------------------------------
    # YOGA
    # --------------------------------------------------

    yoga_name = _get_name(
        yoga_period
    )

    yoga_config = (
        conditions.get("yoga")
        or {}
    )

    if yoga_name in yoga_config.get(
        "preferred",
        [],
    ):
        score += yoga_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Yoga: {yoga_name}"
        )

    elif yoga_name in yoga_config.get(
        "avoid",
        [],
    ):
        score -= yoga_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Yoga not preferred: "
            f"{yoga_name}"
        )

    # --------------------------------------------------
    # VARA
    # --------------------------------------------------

    vara_name = _get_name(
        daily_panchang.get("vara")
    )

    vara_config = (
        conditions.get("vara")
        or {}
    )

    if vara_name in vara_config.get(
        "preferred",
        [],
    ):
        score += vara_config.get(
            "preferred_score",
            0,
        )

        reasons.append(
            f"Vara: {vara_name}"
        )

    elif vara_name in vara_config.get(
        "avoid",
        [],
    ):
        score -= vara_config.get(
            "avoid_score",
            0,
        )

        warnings.append(
            f"Vara not preferred: "
            f"{vara_name}"
        )

    return PanchangEvaluation(
        score=score,
        reasons=reasons,
        warnings=warnings,
    )