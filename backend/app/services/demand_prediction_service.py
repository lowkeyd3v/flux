"""
DemandPredictionService interface and implementation.

Defines the contract for demand forecasting, plus the concrete
implementation added in Milestone 3: a trained scikit-learn model
(Random Forest, chosen over Linear Regression by validation MAE -- see
ml/training/train_demand_model.py) loaded via joblib.

The `ml/` package lives as a sibling directory to `backend/` (see repo
root), so it isn't installed as a normal dependency. We add the repo
root to sys.path here, once, so `import ml...` resolves the same way
whether this runs under uvicorn or pytest.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

# backend/app/services/demand_prediction_service.py -> repo root is 3 parents up.
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


@dataclass
class DemandPredictionInput:
    product: str
    location: str
    target_date: date
    historical_sales: list[float]
    price: float | None = None
    current_inventory: float | None = None
    weather_context: dict | None = None


@dataclass
class DemandPredictionResult:
    predicted_demand_low: float
    predicted_demand_high: float
    predicted_demand_point: float
    confidence: float
    model_version: str


class DemandPredictionService(ABC):
    """Contract that any demand forecasting implementation must fulfill."""

    @abstractmethod
    def predict(self, data: DemandPredictionInput) -> DemandPredictionResult:
        raise NotImplementedError


class MLDemandPredictionService(DemandPredictionService):
    """
    Real implementation, backed by the trained model in ml/models/.

    `historical_sales` and `current_inventory` on the input aren't used
    directly by this model version -- the trained model conditions on
    product/location/date/weather/price rather than a rolling window of
    past sales. They're kept on the interface so a future model version
    (e.g. one using recent sales as a feature) can use them without an
    interface change.
    """

    def predict(self, data: DemandPredictionInput) -> DemandPredictionResult:
        from ml.inference.predict import predict_demand

        weather_context = data.weather_context or {}
        result = predict_demand(
            product=data.product,
            location=data.location,
            target_date=data.target_date.isoformat(),
            price=data.price if data.price is not None else 0.0,
            temperature_celsius=weather_context.get("temperature_celsius"),
            weather_condition=weather_context.get("condition"),
            is_holiday_or_event=weather_context.get("is_holiday_or_event", False),
        )

        return DemandPredictionResult(
            predicted_demand_low=result["predicted_demand_low"],
            predicted_demand_high=result["predicted_demand_high"],
            predicted_demand_point=result["predicted_demand_point"],
            confidence=result["confidence"],
            model_version="random_forest_v1",
        )


class NotImplementedDemandPredictionService(DemandPredictionService):
    """
    Retained for environments where the trained model artifact isn't
    available (e.g. a fresh clone before running the training script).
    The API layer falls back to this with a clear error rather than
    crashing on import.
    """

    def predict(self, data: DemandPredictionInput) -> DemandPredictionResult:
        raise NotImplementedError(
            "No trained demand model found. Run "
            "`python -m ml.training.train_demand_model` from the repo root first."
        )


def get_demand_prediction_service() -> DemandPredictionService:
    """
    Factory used as a FastAPI dependency. Tries to load the real model;
    falls back to the NotImplemented stub if the model artifact is
    missing, so the API gives a clear 501-style error instead of a
    crash on startup.
    """
    from ml.inference.predict import MODEL_PATH

    if MODEL_PATH.exists():
        return MLDemandPredictionService()
    return NotImplementedDemandPredictionService()
