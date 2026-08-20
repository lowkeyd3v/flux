"""
DemandPredictionService interface.

Defines the contract for demand forecasting. The concrete implementation
(trained ML model, loaded via joblib) will be added in Milestone 3.

This is intentionally NOT a fake/mocked implementation — calling it before
Milestone 3 raises NotImplementedError so it's obvious the feature isn't
built yet, rather than silently returning made-up numbers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


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


class NotImplementedDemandPredictionService(DemandPredictionService):
    """
    Placeholder used during Milestone 1 so the API can be wired up
    end-to-end before the real ML model exists.
    """

    def predict(self, data: DemandPredictionInput) -> DemandPredictionResult:
        raise NotImplementedError(
            "Demand forecasting model is not implemented yet (planned: Milestone 3)."
        )
