"""
Demand prediction API routes.

Predicts expected demand for a vendor on a given date, using their
product/location plus optional weather/holiday context. Backed by the
trained ML model (see ml/training/train_demand_model.py) via
MLDemandPredictionService.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vendor import Vendor
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.demand_prediction_service import (
    DemandPredictionInput,
    get_demand_prediction_service,
)

router = APIRouter(prefix="/vendors/{vendor_id}/predict", tags=["predictions"])


@router.post("", response_model=PredictionResponse)
def predict_demand_for_vendor(
    vendor_id: uuid.UUID, payload: PredictionRequest, db: Session = Depends(get_db)
):
    vendor = db.get(Vendor, vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")

    service = get_demand_prediction_service()

    prediction_input = DemandPredictionInput(
        product=vendor.product,
        location=vendor.location,
        target_date=payload.target_date,
        historical_sales=[],  # not used by the current model version
        price=vendor.selling_price,
        current_inventory=vendor.current_inventory,
        weather_context={
            "temperature_celsius": payload.temperature_celsius,
            "condition": payload.weather_condition,
            "is_holiday_or_event": payload.is_holiday_or_event,
        },
    )

    try:
        result = service.predict(prediction_input)
    except NotImplementedError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return PredictionResponse(
        predicted_demand_low=result.predicted_demand_low,
        predicted_demand_high=result.predicted_demand_high,
        predicted_demand_point=result.predicted_demand_point,
        confidence=result.confidence,
        model_version=result.model_version,
    )
