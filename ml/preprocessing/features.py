"""
Preprocessing pipeline for demand forecasting.

Converts raw sales rows (product, location, date, weather, price, etc.)
into a feature matrix the model can train/predict on. Kept separate from
training/inference code so the same transformation logic is reused by
both, avoiding train/serve skew.
"""

import pandas as pd

# Categorical columns that get one-hot encoded. Fixed vocabulary derived
# from the training data at fit time and reused at inference time.
CATEGORICAL_COLUMNS = ["product", "location", "weather_condition"]

NUMERIC_FEATURE_COLUMNS = [
    "day_of_week",
    "month",
    "is_holiday_or_event",
    "temperature_celsius",
    "price",
]

TARGET_COLUMN = "units_sold"


def add_calendar_features(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Derives day_of_week / month from a date column if not already present."""
    df = df.copy()
    dates = pd.to_datetime(df[date_col])
    if "day_of_week" not in df.columns:
        df["day_of_week"] = dates.dt.dayofweek
    if "month" not in df.columns:
        df["month"] = dates.dt.month
    return df


def build_feature_matrix(
    df: pd.DataFrame, feature_columns: list[str] | None = None
) -> pd.DataFrame:
    """
    One-hot encodes categorical columns and assembles the final numeric
    feature matrix.

    If `feature_columns` is provided (the exact columns the model was
    trained on), the output is reindexed to match exactly — filling any
    missing dummy columns with 0. This is what keeps inference features
    consistent with training features even when a single prediction
    request doesn't see every category.
    """
    df = add_calendar_features(df)
    df = df.copy()
    df["is_holiday_or_event"] = df["is_holiday_or_event"].astype(int)

    present_categoricals = [c for c in CATEGORICAL_COLUMNS if c in df.columns]
    encoded = pd.get_dummies(df, columns=present_categoricals, dummy_na=False)

    base_cols = [c for c in NUMERIC_FEATURE_COLUMNS if c in encoded.columns]
    dummy_cols = [
        c for c in encoded.columns
        if any(c.startswith(f"{cat}_") for cat in present_categoricals)
    ]
    feature_df = encoded[base_cols + dummy_cols]

    if feature_columns is not None:
        feature_df = feature_df.reindex(columns=feature_columns, fill_value=0)

    return feature_df


def split_features_and_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Convenience helper for training: builds X, y from a raw dataframe."""
    X = build_feature_matrix(df)
    y = df[TARGET_COLUMN]
    return X, y
