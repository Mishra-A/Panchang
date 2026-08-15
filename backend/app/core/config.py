from dataclasses import dataclass


@dataclass(frozen=True)
class CalculationConfig:
    ayanamsha: int = 1  # Lahiri
    zodiac: str = "sidereal"
    house_system: str = "W"
    timezone: str = "Asia/Kolkata"


DEFAULT_CONFIG = CalculationConfig()