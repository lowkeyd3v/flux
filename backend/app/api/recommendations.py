"""
Recommendation API routes (Milestone 4).

Ties together WeatherService, DemandPredictionService, and
RecommendationService into a single vendor-facing endpoint: given a
target date, tell the vendor how much to prepare, expected revenue,
and risk -- auto-fetching weather for their location when possible.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    WeatherSummary,
)
from app.services.demand_prediction_service import (
    DemandPredictionInput,
    get_demand_prediction_service,
)
from app.services.recommendation_service import (
    RecommendationInput,
    get_recommendation_service,
)
from app.services.weather_service import WeatherServiceUnavailableError, get_weather_service

router = APIRouter(prefix="/vendors/{vendor_id}/recommend", tags=["recommendations"])


@router.post("", response_model=RecommendationResponse)
def recommend_for_vendor(
    vendor_id: uuid.UUID, payload: RecommendationRequest, db: Session = Depends(get_db)
):
    vendor = db.get(Vendor, vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")

    temperature_celsius = payload.temperature_celsius
    weather_condition = payload.weather_condition
    rainfall_mm = None
    weather_source = "manual" if (temperature_celsius is not None or weather_condition) else None

    # Only attempt an auto-fetch if the vendor didn't already supply both
    # values manually -- manual input always wins.
    if weather_source is None:
        weather_service = get_weather_service()
        try:
            forecast = weather_service.get_forecast(vendor.location, payload.target_date)
            temperature_celsius = forecast.temperature_celsius
            weather_condition = forecast.condition
            rainfall_mm = forecast.rainfall_mm
            weather_source = "auto"
        except (NotImplementedError, WeatherServiceUnavailableError):
            # No weather API configured, or it couldn't produce a
            # forecast for this location/date. Fall through: the demand
            # model defaults missing weather to a neutral 27C/clear
            # rather than failing the whole request.
            weather_source = "unavailable"

    demand_service = get_demand_prediction_service()
    prediction_input = DemandPredictionInput(
        product=vendor.product,
        location=vendor.location,
        target_date=payload.target_date,
        historical_sales=[],
        price=vendor.selling_price,
        current_inventory=vendor.current_inventory,
        weather_context={
            "temperature_celsius": temperature_celsius,
            "condition": weather_condition,
            "is_holiday_or_event": payload.is_holiday_or_event,
        },
    )

    try:
        prediction = demand_service.predict(prediction_input)
    except NotImplementedError as e:
        raise HTTPException(status_code=503, detail=str(e))

    recommendation_service = get_recommendation_service()
    recommendation = recommendation_service.recommend(
        RecommendationInput(
            prediction=prediction,
            current_inventory=vendor.current_inventory,
            budget=vendor.budget,
            unit_price=vendor.selling_price,
        )
    )

    return RecommendationResponse(
        recommended_preparation_qty=recommendation.recommended_preparation_qty,
        expected_revenue=recommendation.expected_revenue,
        estimated_surplus_or_shortage=recommendation.estimated_surplus_or_shortage,
        risk_level=recommendation.risk_level,
        explanation=recommendation.explanation,
        predicted_demand_point=prediction.predicted_demand_point,
        predicted_demand_low=prediction.predicted_demand_low,
        predicted_demand_high=prediction.predicted_demand_high,
        confidence=prediction.confidence,
        model_version=prediction.model_version,
        weather=WeatherSummary(
            source=weather_source,
            temperature_celsius=temperature_celsius,
            condition=weather_condition,
            rainfall_mm=rainfall_mm,
        ),
    )
