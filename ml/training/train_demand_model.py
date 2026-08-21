"""
Trains the FLUX demand forecasting model.

Uses a time-series-appropriate split (train on earlier dates, validate on
later dates — never a random shuffle split, which would leak future
information into training for time-series data).

Two models are compared:
  1. Baseline: Linear Regression
  2. Stronger model: Random Forest Regressor

The better performer (by validation MAE) is serialized via joblib for
the inference service to load.

Usage:
    python -m ml.training.train_demand_model
"""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score

from ml.preprocessing.features import build_feature_matrix, TARGET_COLUMN

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "synthetic_sales_data.csv"
MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
MODEL_PATH = MODEL_DIR / "demand_model.joblib"
METADATA_PATH = MODEL_DIR / "demand_model_metadata.json"

# Fraction of the date range (by time, not row count) held out for
# validation. Because vendors have staggered date ranges of equal length
# here, splitting by date works well across the whole dataset.
VALIDATION_FRACTION = 0.2


def time_series_split(df: pd.DataFrame, date_col: str = "date", val_fraction: float = VALIDATION_FRACTION):
    """
    Splits by date, not randomly: earliest (1 - val_fraction) of the date
    range is training data, the most recent val_fraction is validation.
    This avoids leaking future information into the training set, which
    a random shuffle split would do for time-series data.
    """
    df = df.sort_values(date_col)
    dates = pd.to_datetime(df[date_col])
    cutoff = dates.quantile(1 - val_fraction)
    train_df = df[dates <= cutoff]
    val_df = df[dates > cutoff]
    return train_df, val_df


def evaluate(model, X_val, y_val) -> dict:
    preds = model.predict(X_val)
    preds = np.clip(preds, a_min=0, a_max=None)  # demand can't be negative
    return {
        "mae": float(mean_absolute_error(y_val, preds)),
        "mape": float(mean_absolute_percentage_error(y_val, preds)),
        "r2": float(r2_score(y_val, preds)),
    }


def train():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Training data not found at {DATA_PATH}. "
            "Run `python -m ml.data.generate_synthetic_data` first."
        )

    df = pd.read_csv(DATA_PATH)
    train_df, val_df = time_series_split(df)
    print(f"Train rows: {len(train_df)}, Validation rows: {len(val_df)}")

    X_train = build_feature_matrix(train_df)
    y_train = train_df[TARGET_COLUMN]

    # Validation features are reindexed to match the training feature
    # columns exactly, so category vocab mismatches don't break scoring.
    X_val = build_feature_matrix(val_df, feature_columns=X_train.columns.tolist())
    y_val = val_df[TARGET_COLUMN]

    candidates = {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=200, max_depth=8, random_state=42, n_jobs=-1
        ),
    }

    results = {}
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        metrics = evaluate(model, X_val, y_val)
        results[name] = metrics
        print(f"[{name}] MAE={metrics['mae']:.2f}  MAPE={metrics['mape']:.2%}  R2={metrics['r2']:.3f}")

    best_name = min(results, key=lambda n: results[n]["mae"])
    best_model = candidates[best_name]
    print(f"\nBest model: {best_name} (lowest validation MAE)")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": best_model,
            "feature_columns": X_train.columns.tolist(),
        },
        MODEL_PATH,
    )

    metadata = {
        "model_type": best_name,
        "trained_on": "synthetic_sales_data.csv (SYNTHETIC/DEMO data, not real vendor data)",
        "train_rows": len(train_df),
        "validation_rows": len(val_df),
        "metrics": results[best_name],
        "all_candidates": results,
        "feature_columns": X_train.columns.tolist(),
        "version": "v1",
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2))

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")


if __name__ == "__main__":
    train()
