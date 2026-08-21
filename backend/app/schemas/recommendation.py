"""
Recommendation request/response schemas.
"""

from datetime import date

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    target_date: date = Field(..., examples=["2026-08-22"])

    # Optional manual weather override. If omitted, the backend tries to
    # auto-fetch weather for the vendor's location via WeatherService;
    # if that isn't available (no WEATHER_API_KEY, date too far out,
    # unrecognized location), it 422s asking for these explicitly.
    temperature_celsius: float | None = Field(default=None, examples=[30.0])
    weather_condition: str | None = Field(
        default=None, examples=["clear"], description="e.g. clear, rain, extreme_heat"
    )
    is_holiday_or_event: bool = Field(default=False)


class WeatherSummary(BaseModel):
    source: str  # "auto" | "manual"
    temperature_celsius: float | None
    condition: str | None
    rainfall_mm: float | None = None


class RecommendationResponse(BaseModel):
    recommended_preparation_qty: float
    expected_revenue: float
    estimated_surplus_or_shortage: float
    risk_level: str
    explanation: str

    # Transparency: show the caller what prediction/weather this was based on.
    predicted_demand_point: float
    predicted_demand_low: float
    predicted_demand_high: float
    confidence: float
    model_version: str
    weather: WeatherSummary
