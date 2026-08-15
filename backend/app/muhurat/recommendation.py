from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from backend.app.core.rule_loader import load_rule
from backend.app.muhurat.intervals import (
    split_interval,
    find_period_at,
)
from backend.app.muhurat.muhurat import (
    MuhuratRule,
    evaluate_window,
)
from backend.app.muhurat.panchang_rules import (
    evaluate_interval_panchang,
)
from backend.app.panchang.daily_timeline import (
    build_daily_timeline,
)
from backend.app.core.location import Location


def load_muhurat_rule(
    activity: str,
) -> MuhuratRule:
    """
    Load activity-specific Muhurat rules.
    """

    rules = load_rule(
        "muhurat_rules.json"
    )

    activities = rules["activities"]

    if activity not in activities:
        raise ValueError(
            f"Unknown activity: {activity}"
        )

    config = activities[activity]

    return MuhuratRule(
        activity=activity,

        allowed_choghadiya=set(
            config.get(
                "allowed_choghadiya",
                [],
            )
        ),

        preferred_hora=set(
            config.get(
                "preferred_hora",
                [],
            )
        ),

        blocked_periods=set(
            config.get(
                "blocked_periods",
                [],
            )
        ),

        panchang_conditions=config.get(
            "panchang_conditions",
            {},
        ),
    )


def _collect_choghadiya_periods(
    daily_kaal: dict,
) -> list[dict]:
    """
    Collect day and night Choghadiya periods.
    """

    return (
        daily_kaal["choghadiya"]["day"]
        + daily_kaal["choghadiya"]["night"]
    )


def _collect_hora_periods(
    daily_kaal: dict,
) -> list[dict]:
    """
    Collect day and night Hora periods.
    """

    return (
        daily_kaal["hora"]["day"]
        + daily_kaal["hora"]["night"]
    )


def _blocked_periods(
    daily_kaal: dict,
) -> list[dict]:
    """
    Convert Kaal periods into common
    interval representation.
    """

    result = []

    for name, period in daily_kaal[
        "kaal"
    ].items():

        result.append(
            {
                "name": name,
                "starts_at": period[
                    "starts_at"
                ],
                "ends_at": period[
                    "ends_at"
                ],
            }
        )

    return result


def _calculate_final_status(
    score: int,
    warnings: list[str],
) -> str:
    """
    Convert final score and warnings
    into recommendation status.
    """

    if any(
        warning.startswith("Overlaps")
        for warning in warnings
    ):
        return "avoid"

    if score >= 60:
        return "recommended"

    if score > 0:
        return "acceptable"

    return "avoid"


def _normalize_timeline_periods(
    periods: list[dict],
) -> list[dict]:
    """
    Convert astronomical timeline periods
    from starts_at_utc / ends_at_utc
    to common starts_at / ends_at format.
    """

    normalized = []

    for period in periods:

        normalized.append(
            {
                **period,
                "starts_at": period[
                    "starts_at_utc"
                ],
                "ends_at": period[
                    "ends_at_utc"
                ],
            }
        )

    return normalized


def _normalize_period_timezone(
    periods: list[dict],
    timezone_name: str,
) -> list[dict]:
    """
    Normalize all interval timestamps to
    the requested local timezone.
    """

    tz = ZoneInfo(
        timezone_name
    )

    normalized = []

    for period in periods:

        start = datetime.fromisoformat(
            period["starts_at"]
        ).astimezone(tz)

        end = datetime.fromisoformat(
            period["ends_at"]
        ).astimezone(tz)

        normalized.append(
            {
                **period,
                "starts_at": start.isoformat(),
                "ends_at": end.isoformat(),
            }
        )

    return normalized


def recommend_activity(
    activity: str,
    daily_kaal: dict,
    daily_panchang: dict,
) -> list[dict]:
    """
    Generate exact Muhurat recommendation
    windows.

    Panchang conditions are evaluated against
    the exact Tithi, Nakshatra and Yoga
    active during each interval.
    """

    # --------------------------------------------------
    # LOAD RULE
    # --------------------------------------------------

    rule = load_muhurat_rule(
        activity
    )

    # --------------------------------------------------
    # KAAL DATA
    # --------------------------------------------------

    choghadiya_periods = (
        _collect_choghadiya_periods(
            daily_kaal
        )
    )

    hora_periods = (
        _collect_hora_periods(
            daily_kaal
        )
    )

    blocked_periods = _blocked_periods(
        daily_kaal
    )

    # --------------------------------------------------
    # LOCATION
    # --------------------------------------------------

    location_data = daily_kaal[
        "location"
    ]

    location = Location(
        city=location_data["city"],
        latitude=location_data["latitude"],
        longitude=location_data["longitude"],
        timezone=location_data["timezone"],
    )

    local_tz = ZoneInfo(
        location.timezone
    )

    # Normalize Kaal/Hora/Choghadiya
    # into local timezone.

    choghadiya_periods = (
        _normalize_period_timezone(
            choghadiya_periods,
            location.timezone,
        )
    )

    hora_periods = (
        _normalize_period_timezone(
            hora_periods,
            location.timezone,
        )
    )

    blocked_periods = (
        _normalize_period_timezone(
            blocked_periods,
            location.timezone,
        )
    )

    # --------------------------------------------------
    # TARGET DATE
    # --------------------------------------------------

    target_date = datetime.fromisoformat(
        daily_kaal["date"]
    ).date()

    # Exact local calendar-day boundaries.
    day_start = datetime.combine(
        target_date,
        time.min,
        tzinfo=local_tz,
    )

    day_end = datetime.combine(
        target_date + timedelta(days=1),
        time.min,
        tzinfo=local_tz,
    )

    # --------------------------------------------------
    # COMPLETE PANCHANG TIMELINE
    # --------------------------------------------------

    daily_timeline = build_daily_timeline(
        target_date=target_date,
        location=location,
    )

    tithi_periods = (
        _normalize_timeline_periods(
            daily_timeline[
                "timeline"
            ]["tithi"]
        )
    )

    nakshatra_periods = (
        _normalize_timeline_periods(
            daily_timeline[
                "timeline"
            ]["nakshatra"]
        )
    )

    yoga_periods = (
        _normalize_timeline_periods(
            daily_timeline[
                "timeline"
            ]["yoga"]
        )
    )

    # Convert astronomical UTC timestamps
    # to local timezone.

    tithi_periods = (
        _normalize_period_timezone(
            tithi_periods,
            location.timezone,
        )
    )

    nakshatra_periods = (
        _normalize_period_timezone(
            nakshatra_periods,
            location.timezone,
        )
    )

    yoga_periods = (
        _normalize_period_timezone(
            yoga_periods,
            location.timezone,
        )
    )

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = []

    for choghadiya in choghadiya_periods:

        ch_start = datetime.fromisoformat(
            choghadiya["starts_at"]
        ).astimezone(local_tz)

        ch_end = datetime.fromisoformat(
            choghadiya["ends_at"]
        ).astimezone(local_tz)

        # --------------------------------------------------
        # STRICT LOCAL CALENDAR DAY
        # --------------------------------------------------

        ch_start = max(
            ch_start,
            day_start,
        )

        ch_end = min(
            ch_end,
            day_end,
        )

        if ch_start >= ch_end:
            continue

        # --------------------------------------------------
        # SPLIT AT EVERY IMPORTANT BOUNDARY
        # --------------------------------------------------

        intervals = split_interval(
            ch_start,
            ch_end,
            [choghadiya],
            hora_periods,
            blocked_periods,
            tithi_periods,
            nakshatra_periods,
            yoga_periods,
        )

        for start, end in intervals:

            # Never allow an interval outside
            # the requested local calendar day.

            if start < day_start:
                start = day_start

            if end > day_end:
                end = day_end

            if start >= end:
                continue

            # --------------------------------------------------
            # EXACT HORA
            # --------------------------------------------------

            hora = find_period_at(
                start,
                end,
                hora_periods,
            )

            if hora is None:
                continue

            # --------------------------------------------------
            # EXACT TITHI
            # --------------------------------------------------

            tithi = find_period_at(
                start,
                end,
                tithi_periods,
            )

            if tithi is None:
                continue

            # --------------------------------------------------
            # EXACT NAKSHATRA
            # --------------------------------------------------

            nakshatra = find_period_at(
                start,
                end,
                nakshatra_periods,
            )

            if nakshatra is None:
                continue

            # --------------------------------------------------
            # EXACT YOGA
            # --------------------------------------------------

            yoga = find_period_at(
                start,
                end,
                yoga_periods,
            )

            if yoga is None:
                continue

            # --------------------------------------------------
            # CHOGHADIYA + HORA + KAAL
            # --------------------------------------------------

            result = evaluate_window(
                activity=activity,
                start=start,
                end=end,
                rule=rule,
                choghadiya_period=choghadiya,
                hora_period=hora,
                blocked_periods=blocked_periods,
            )

            # --------------------------------------------------
            # INTERVAL-SPECIFIC PANCHANG
            # --------------------------------------------------

            interval_panchang_result = (
                evaluate_interval_panchang(
                    daily_panchang=daily_panchang,
                    tithi_period=tithi,
                    nakshatra_period=nakshatra,
                    yoga_period=yoga,
                    rule_config=rule.panchang_conditions,
                )
            )

            # --------------------------------------------------
            # FINAL SCORE
            # --------------------------------------------------

            final_score = max(
                0,
                min(
                    100,
                    result.score
                    + interval_panchang_result.score,
                ),
            )

            # --------------------------------------------------
            # REASONS
            # --------------------------------------------------

            final_reasons = (
                result.reasons
                + interval_panchang_result.reasons
            )

            # --------------------------------------------------
            # WARNINGS
            # --------------------------------------------------

            final_warnings = (
                result.warnings
                + interval_panchang_result.warnings
            )

            # --------------------------------------------------
            # STATUS
            # --------------------------------------------------

            status = _calculate_final_status(
                final_score,
                final_warnings,
            )

            # --------------------------------------------------
            # RESULT
            # --------------------------------------------------

            recommendations.append(
                {
                    "activity": result.activity,
                    "start": start.astimezone(
                        local_tz
                    ).isoformat(),
                    "end": end.astimezone(
                        local_tz
                    ).isoformat(),
                    "status": status,
                    "score": final_score,
                    "reasons": final_reasons,
                    "warnings": final_warnings,
                }
            )

    # --------------------------------------------------
    # FINAL SAFETY FILTER
    # --------------------------------------------------
    #
    # Every recommendation MUST:
    # 1. Start on target date
    # 2. End on target date
    # 3. Stay inside one Tithi
    # 4. Stay inside one Nakshatra
    # 5. Stay inside one Yoga
    #
    # --------------------------------------------------

    filtered = []

    for item in recommendations:

        start = datetime.fromisoformat(
            item["start"]
        ).astimezone(local_tz)

        end = datetime.fromisoformat(
            item["end"]
        ).astimezone(local_tz)

        if start < day_start:
            continue

        if end > day_end:
            continue

        if start >= end:
            continue

        filtered.append(
            item
        )

    return filtered
def test_vehicle_recommendation_respects_nakshatra_boundary():
    from datetime import date, datetime

    from backend.app.panchang.daily_timeline import (
        build_daily_timeline,
    )

    target_date = date(2026, 8, 20)

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=LUCKNOW,
    )

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=LUCKNOW,
    )

    timeline = build_daily_timeline(
        target_date=target_date,
        location=LUCKNOW,
    )

    recommendations = recommend_activity(
        activity="vehicle_purchase",
        daily_kaal=daily_kaal,
        daily_panchang=daily_panchang,
    )

    nakshatra_periods = (
        timeline["timeline"]["nakshatra"]
    )

    for window in recommendations:

        start = datetime.fromisoformat(
            window["start"]
        )

        end = datetime.fromisoformat(
            window["end"]
        )

        contained = any(
            start >= datetime.fromisoformat(
                period["starts_at_ist"]
            )
            and end <= datetime.fromisoformat(
                period["ends_at_ist"]
            )
            for period in nakshatra_periods
        )

        assert contained, (
            "Muhurat window crosses "
            f"Nakshatra boundary: "
            f"{start} -> {end}"
        )


def test_vehicle_recommendation_respects_tithi_boundary():
    from datetime import date, datetime

    from backend.app.panchang.daily_timeline import (
        build_daily_timeline,
    )

    target_date = date(2026, 8, 20)

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=LUCKNOW,
    )

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=LUCKNOW,
    )

    timeline = build_daily_timeline(
        target_date=target_date,
        location=LUCKNOW,
    )

    recommendations = recommend_activity(
        activity="vehicle_purchase",
        daily_kaal=daily_kaal,
        daily_panchang=daily_panchang,
    )

    tithi_periods = timeline["timeline"]["tithi"]

    for window in recommendations:

        start = datetime.fromisoformat(
            window["start"]
        )

        end = datetime.fromisoformat(
            window["end"]
        )

        contained = any(
            start >= datetime.fromisoformat(
                period["starts_at_ist"]
            )
            and end <= datetime.fromisoformat(
                period["ends_at_ist"]
            )
            for period in tithi_periods
        )

        assert contained, (
            "Muhurat window crosses "
            f"Tithi boundary: "
            f"{start} -> {end}"
        )


def test_vehicle_recommendation_respects_yoga_boundary():
    from datetime import date, datetime

    from backend.app.panchang.daily_timeline import (
        build_daily_timeline,
    )

    target_date = date(2026, 8, 20)

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=LUCKNOW,
    )

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=LUCKNOW,
    )

    timeline = build_daily_timeline(
        target_date=target_date,
        location=LUCKNOW,
    )

    recommendations = recommend_activity(
        activity="vehicle_purchase",
        daily_kaal=daily_kaal,
        daily_panchang=daily_panchang,
    )

    yoga_periods = timeline["timeline"]["yoga"]

    for window in recommendations:

        start = datetime.fromisoformat(
            window["start"]
        )

        end = datetime.fromisoformat(
            window["end"]
        )

        contained = any(
            start >= datetime.fromisoformat(
                period["starts_at_ist"]
            )
            and end <= datetime.fromisoformat(
                period["ends_at_ist"]
            )
            for period in yoga_periods
        )

        assert contained, (
            "Muhurat window crosses "
            f"Yoga boundary: "
            f"{start} -> {end}"
        )


def test_travel_allows_chal_choghadiya():
    from datetime import date

    target_date = date(2026, 8, 20)

    daily_kaal = build_daily_kaal(
        target_date=target_date,
        location=LUCKNOW,
    )

    daily_panchang = build_daily_panchang(
        target_date=target_date,
        location=LUCKNOW,
    )

    recommendations = recommend_activity(
        activity="travel",
        daily_kaal=daily_kaal,
        daily_panchang=daily_panchang,
    )

    chal_windows = [
        window
        for window in recommendations
        if any(
            reason == "Choghadiya: Chal"
            for reason in window["reasons"]
        )
    ]

    assert len(chal_windows) > 0

    assert any(
        window["status"]
        == "recommended"
        for window in chal_windows
    )