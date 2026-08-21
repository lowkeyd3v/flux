"""
Inference for the FLUX demand forecasting model.

Loads the joblib-serialized model + feature column list once, and
exposes a single `predict_demand` function the backend service calls.
Kept separate from training code (ml/training/) per project convention.
"""

from pathlib import Path
from functools import lru_cache

import joblib
import numpy as np
import pandas as pd

from ml.preprocessing.features import build_feature_matrix

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "demand_model.joblib"


@lru_cache(maxsize=1)
def _load_model_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No trained model found at {MODEL_PATH}. "
            "Run `python -m ml.training.train_demand_model` first."
        )
    return joblib.load(MODEL_PATH)


def predict_demand(
    product: str,
    location: str,
    target_date: str,
    price: float,
    temperature_celsius: float | None = None,
    weather_condition: str | None = None,
    is_holiday_or_event: bool = False,
) -> dict:
    """
    Predicts expected demand (units) for a single vendor/day.

    Returns a dict with a point estimate and a low/high range derived
    from the Random Forest's individual tree predictions (when available)
    so the frontend can show an honest uncertainty band rather than a
    single falsely-precise number.
    """
    bundle = _load_model_bundle()
    model = bundle["model"]
    feature_columns = bundle["feature_columns"]

    row = pd.DataFrame([{
        "product": product,
        "location": location,
        "date": target_date,
        "price": price,
        "temperature_celsius": temperature_celsius if temperature_celsius is not None else 27.0,
        "weather_condition": weather_condition or "clear",
        "is_holiday_or_event": is_holiday_or_event,
    }])

    X = build_feature_matrix(row, feature_columns=feature_columns)

    point_estimate = float(model.predict(X)[0])
    point_estimate = max(0.0, point_estimate)

    # Random Forest exposes per-tree predictions, which gives us a cheap,
    # honest uncertainty range. Other model types fall back to a fixed
    # +/-15% band around the point estimate.
    if hasattr(model, "estimators_"):
        X_values = X.values
        tree_preds = np.array([tree.predict(X_values)[0] for tree in model.estimators_])
        low = float(max(0.0, np.percentile(tree_preds, 10)))
        high = float(np.percentile(tree_preds, 90))
        confidence = float(1 - (np.std(tree_preds) / (np.mean(tree_preds) + 1e-6)))
        confidence = max(0.0, min(1.0, confidence))
    else:
        low = point_estimate * 0.85
        high = point_estimate * 1.15
        confidence = 0.6

    return {
        "predicted_demand_point": round(point_estimate, 1),
        "predicted_demand_low": round(low, 1),
        "predicted_demand_high": round(high, 1),
        "confidence": round(confidence, 2),
    }
