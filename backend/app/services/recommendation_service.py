"""
RecommendationService interface.

Turns a demand prediction (plus inventory/budget/weather context) into an
actionable, explainable business recommendation. Concrete implementation
arrives in Milestone 3, after demand forecasting exists.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.services.demand_prediction_service import DemandPredictionResult


@dataclass
class RecommendationInput:
    prediction: DemandPredictionResult
    current_inventory: float
    budget: float
    unit_price: float


@dataclass
class RecommendationResult:
    recommended_preparation_qty: float
    expected_revenue: float
    estimated_surplus_or_shortage: float
    risk_level: str  # e.g. "low" | "medium" | "high"
    explanation: str


class RecommendationService(ABC):
    @abstractmethod
    def recommend(self, data: RecommendationInput) -> RecommendationResult:
        raise NotImplementedError


class NotImplementedRecommendationService(RecommendationService):
    def recommend(self, data: RecommendationInput) -> RecommendationResult:
        raise NotImplementedError(
            "Recommendation engine is not implemented yet (planned: Milestone 4)."
        )
