"""
Prediction request/response schemas.
"""

from datetime import date

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    target_date: date = Field(..., examples=["2026-08-22"])
    temperature_celsius: float | None = Field(default=None, examples=[30.0])
    weather_condition: str | None = Field(
        default=None, examples=["clear"], description="e.g. clear, rain, extreme_heat"
    )
    is_holiday_or_event: bool = Field(default=False)


class PredictionResponse(BaseModel):
    predicted_demand_low: float
    predicted_demand_high: float
    predicted_demand_point: float
    confidence: float
    model_version: str
