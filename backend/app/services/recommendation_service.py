"""
RecommendationService interface + implementation.

Turns a demand prediction (plus inventory/budget/price context) into an
actionable, explainable business recommendation: how much to prepare,
expected revenue, surplus/shortage risk, and a plain-language reason a
vendor with no data-science background can act on.

Deliberately rule-based rather than another ML model -- the hard part
(forecasting demand) is already solved by MLDemandPredictionService in
Milestone 3. This layer just turns that number into a decision, which is
arithmetic + thresholds, not something that benefits from training a
model on top of a model.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.services.demand_prediction_service import DemandPredictionResult

# Risk thresholds. A prediction is riskier to act on when the model is
# less confident, or when its low/high range is wide relative to the
# point estimate (i.e. the model itself isn't sure).
LOW_CONFIDENCE_THRESHOLD = 0.5
MEDIUM_CONFIDENCE_THRESHOLD = 0.75
HIGH_RELATIVE_SPREAD_THRESHOLD = 0.6
MEDIUM_RELATIVE_SPREAD_THRESHOLD = 0.3


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
    risk_level: str  # "low" | "medium" | "high"
    explanation: str


class RecommendationService(ABC):
    @abstractmethod
    def recommend(self, data: RecommendationInput) -> RecommendationResult:
        raise NotImplementedError


class RuleBasedRecommendationService(RecommendationService):
    """
    Real implementation.

    Steps:
    1. How many more units are needed on top of what's already in stock
       to cover the predicted demand?
    2. Cap that by what the vendor's budget can actually afford.
    3. Estimate revenue from the resulting total stock against predicted
       demand (you can't sell more than you have, or more than demand).
    4. Classify risk from the model's own confidence and low/high spread,
       plus whether budget forced preparing less than predicted demand.
    5. Explain all of the above in one short, plain-language paragraph.
    """

    def recommend(self, data: RecommendationInput) -> RecommendationResult:
        prediction = data.prediction

        needed_units = max(prediction.predicted_demand_point - data.current_inventory, 0.0)

        max_affordable_units = (
            data.budget / data.unit_price if data.unit_price > 0 else needed_units
        )
        max_affordable_units = max(max_affordable_units, 0.0)

        recommended_qty = round(min(needed_units, max_affordable_units), 1)
        budget_constrained = recommended_qty < round(needed_units, 1)

        total_available = data.current_inventory + recommended_qty
        expected_units_sold = min(total_available, prediction.predicted_demand_point)
        expected_revenue = round(expected_units_sold * data.unit_price, 2)

        surplus_or_shortage = round(total_available - prediction.predicted_demand_point, 1)

        risk_level = self._assess_risk(prediction, budget_constrained)

        explanation = self._explain(
            prediction=prediction,
            data=data,
            recommended_qty=recommended_qty,
            surplus_or_shortage=surplus_or_shortage,
            budget_constrained=budget_constrained,
            risk_level=risk_level,
        )

        return RecommendationResult(
            recommended_preparation_qty=recommended_qty,
            expected_revenue=expected_revenue,
            estimated_surplus_or_shortage=surplus_or_shortage,
            risk_level=risk_level,
            explanation=explanation,
        )

    @staticmethod
    def _assess_risk(prediction: DemandPredictionResult, budget_constrained: bool) -> str:
        spread = prediction.predicted_demand_high - prediction.predicted_demand_low
        relative_spread = (
            spread / prediction.predicted_demand_point
            if prediction.predicted_demand_point > 0
            else 1.0
        )

        if (
            prediction.confidence < LOW_CONFIDENCE_THRESHOLD
            or relative_spread > HIGH_RELATIVE_SPREAD_THRESHOLD
        ):
            return "high"
        if (
            prediction.confidence < MEDIUM_CONFIDENCE_THRESHOLD
            or relative_spread > MEDIUM_RELATIVE_SPREAD_THRESHOLD
            or budget_constrained
        ):
            return "medium"
        return "low"

    @staticmethod
    def _explain(
        *,
        prediction: DemandPredictionResult,
        data: RecommendationInput,
        recommended_qty: float,
        surplus_or_shortage: float,
        budget_constrained: bool,
        risk_level: str,
    ) -> str:
        parts = [
            f"Expected demand is about {prediction.predicted_demand_point:g} units "
            f"(likely between {prediction.predicted_demand_low:g} and "
            f"{prediction.predicted_demand_high:g})."
        ]

        if data.current_inventory > 0:
            parts.append(
                f"You already have {data.current_inventory:g} units in stock, so "
                f"prepare {recommended_qty:g} more."
            )
        else:
            parts.append(f"Prepare about {recommended_qty:g} units.")

        if budget_constrained:
            parts.append(
                "Your budget doesn't fully cover predicted demand, so this "
                "recommendation is capped by what you can afford -- expect "
                "a possible shortage if demand comes in as predicted."
            )
        elif surplus_or_shortage > 0:
            parts.append(
                f"This should leave a small surplus of about "
                f"{surplus_or_shortage:g} units as a buffer."
            )
        elif surplus_or_shortage < 0:
            parts.append(
                f"This still falls short of predicted demand by about "
                f"{abs(surplus_or_shortage):g} units."
            )

        risk_reason = {
            "low": "the forecast is fairly confident and consistent",
            "medium": "the forecast has some uncertainty, so treat this as a guide, not a guarantee",
            "high": "the forecast is quite uncertain -- consider preparing conservatively and adjusting through the day",
        }[risk_level]
        parts.append(f"Risk: {risk_level} ({risk_reason}).")

        return " ".join(parts)


class NotImplementedRecommendationService(RecommendationService):
    def recommend(self, data: RecommendationInput) -> RecommendationResult:
        raise NotImplementedError(
            "Recommendation engine is not implemented yet (planned: Milestone 4)."
        )


def get_recommendation_service() -> RecommendationService:
    """Factory used as a FastAPI dependency."""
    return RuleBasedRecommendationService()
