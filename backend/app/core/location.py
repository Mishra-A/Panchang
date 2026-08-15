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


DELHI = Location(
    city="Delhi",
    latitude=28.6139,
    longitude=77.2090,
    timezone="Asia/Kolkata",
)


MUMBAI = Location(
    city="Mumbai",
    latitude=19.0760,
    longitude=72.8777,
    timezone="Asia/Kolkata",
)


KOLKATA = Location(
    city="Kolkata",
    latitude=22.5726,
    longitude=88.3639,
    timezone="Asia/Kolkata",
)


CHENNAI = Location(
    city="Chennai",
    latitude=13.0827,
    longitude=80.2707,
    timezone="Asia/Kolkata",
)


BENGALURU = Location(
    city="Bengaluru",
    latitude=12.9716,
    longitude=77.5946,
    timezone="Asia/Kolkata",
)


HYDERABAD = Location(
    city="Hyderabad",
    latitude=17.3850,
    longitude=78.4867,
    timezone="Asia/Kolkata",
)


JAIPUR = Location(
    city="Jaipur",
    latitude=26.9124,
    longitude=75.7873,
    timezone="Asia/Kolkata",
)


AHMEDABAD = Location(
    city="Ahmedabad",
    latitude=23.0225,
    longitude=72.5714,
    timezone="Asia/Kolkata",
)


PUNE = Location(
    city="Pune",
    latitude=18.5204,
    longitude=73.8567,
    timezone="Asia/Kolkata",
)