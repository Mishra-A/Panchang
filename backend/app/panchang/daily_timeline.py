from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from backend.app.core.location import Location
from backend.app.panchang.tithi import get_tithi_with_end_time
from backend.app.panchang.nakshatra import get_nakshatra_with_end_time
from backend.app.panchang.yoga import get_yoga_with_end_time
from backend.app.panchang.karana import get_karana_with_end_time
from backend.app.core.time_utils import format_ist


UTC = ZoneInfo("UTC")


def _local_day_bounds_utc(
    target_date: date,
    timezone_name: str,
) -> tuple[datetime, datetime]:
    """
    Convert the local calendar day into UTC boundaries.
    """

    tz = ZoneInfo(timezone_name)

    start_local = datetime.combine(
        target_date,
        time.min,
        tzinfo=tz,
    )

    end_local = datetime.combine(
        target_date + timedelta(days=1),
        time.min,
        tzinfo=tz,
    )

    return (
        start_local.astimezone(UTC),
        end_local.astimezone(UTC),
    )


def build_daily_timeline(
    target_date: date,
    location: Location,
) -> dict:
    """
    Build Tithi, Nakshatra, Yoga and Karana
    timeline for the complete local day.
    """

    day_start_utc, day_end_utc = (
        _local_day_bounds_utc(
            target_date,
            location.timezone,
        )
    )

    timelines = {
        "tithi": [],
        "nakshatra": [],
        "yoga": [],
        "karana": [],
    }

    engines = {
        "tithi": get_tithi_with_end_time,
        "nakshatra": get_nakshatra_with_end_time,
        "yoga": get_yoga_with_end_time,
        "karana": get_karana_with_end_time,
    }

    # --------------------------------------------------
    # Build each astronomical timeline
    # --------------------------------------------------

    for category, engine in engines.items():

        current_time = day_start_utc

        while current_time < day_end_utc:

            # Calculate current event
            result = engine(current_time)

            # Get transition time
            end_time = datetime.fromisoformat(
                result["ends_at_utc"]
            )

            # Safety check
            if end_time <= current_time:
                raise RuntimeError(
                    f"{category} engine returned "
                    f"invalid transition time: "
                    f"{end_time}"
                )

            # Do not allow an event to extend
            # beyond the local day's end.
            event_end = min(
                end_time,
                day_end_utc,
            )

            event_start = current_time

            # --------------------------------------------------
            # IMPORTANT:
            # append MUST be INSIDE the while loop
            # --------------------------------------------------

            timelines[category].append(
                {
                    **result,

                    "starts_at_utc":
                        event_start.isoformat(),

                    "starts_at_ist":
                        format_ist(event_start),

                    "ends_at_utc":
                        event_end.isoformat(),

                    "ends_at_ist":
                        format_ist(event_end),
                }
            )

            # --------------------------------------------------
            # Move to the next astronomical event
            # --------------------------------------------------

            if end_time >= day_end_utc:
                break

            current_time = end_time

    return {
        "date": target_date.isoformat(),

        "location": {
            "city": location.city,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone": location.timezone,
        },

        "timeline": timelines,
    }