from datetime import date


VARA_NAMES = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def calculate_vara(target_date: date) -> dict:
    weekday = target_date.weekday()

    return {
        "number": weekday + 1,
        "name": VARA_NAMES[weekday],
    }