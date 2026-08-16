from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LocationResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    city: str
    latitude: float
    longitude: float
    timezone: str


class MuhuratWindow(BaseModel):
    model_config = ConfigDict(extra="allow")

    activity: str
    start: str
    end: str
    status: str
    score: int = Field(ge=0, le=100)
    reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class MuhuratResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    activity: str
    best_windows: list[MuhuratWindow] = Field(
        default_factory=list
    )


class DailyPanchangResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    date: str
    location: LocationResponse
    panchang: dict[str, Any]
    kaal: dict[str, Any]
    timeline: dict[str, Any]
    muhurat: MuhuratResponse | None = None