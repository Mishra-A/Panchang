from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    city: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"


LUCKNOW = Location(
    city="Lucknow",
    latitude=26.8467,
    longitude=80.9462,
    timezone="Asia/Kolkata",
)