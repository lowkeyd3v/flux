"""
Synthetic sales data generator for FLUX demand forecasting.

============================================================
IMPORTANT: THIS DATA IS SYNTHETIC / DEMO DATA — NOT REAL SALES DATA.
============================================================

No real vendor sales data was available at hackathon time, so this
script generates realistic-*looking* daily sales data for a handful of
street-vendor archetypes (product x location combinations), following
patterns a domain-literate person would expect:

- Weekly seasonality (weekends busier for food vendors)
- Monthly/seasonal trend (e.g. chai sells more in winter)
- Holiday/event spikes
- Weather sensitivity (rain reduces footfall for outdoor vendors, heat
  increases cold-drink demand, etc.)
- Random day-to-day noise

The schema (columns) is designed to match `SalesRecord` /
`app/services/demand_prediction_service.py` so real vendor data can
later replace this file without changing the ML pipeline.

Usage:
    python -m ml.data.generate_synthetic_data
"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

RNG_SEED = 42
OUTPUT_PATH = Path(__file__).parent / "synthetic_sales_data.csv"

# Vendor archetypes: (product, location, base_demand, price, weather_sensitivity)
# weather_sensitivity: how much rain/heat swings demand for this product.
VENDOR_ARCHETYPES = [
    {"product": "Samosa", "location": "Prayagraj", "base_demand": 60, "price": 10, "rain_effect": -0.30, "heat_effect": -0.05},
    {"product": "Samosa", "location": "Varanasi", "base_demand": 55, "price": 10, "rain_effect": -0.30, "heat_effect": -0.05},
    {"product": "Chai", "location": "Varanasi", "base_demand": 90, "price": 15, "rain_effect": 0.15, "heat_effect": -0.20},
    {"product": "Chai", "location": "Lucknow", "base_demand": 85, "price": 15, "rain_effect": 0.15, "heat_effect": -0.20},
    {"product": "Sugarcane Juice", "location": "Prayagraj", "base_demand": 70, "price": 20, "rain_effect": -0.15, "heat_effect": 0.35},
    {"product": "Sugarcane Juice", "location": "Kanpur", "base_demand": 65, "price": 20, "rain_effect": -0.15, "heat_effect": 0.35},
    {"product": "Chaat", "location": "Lucknow", "base_demand": 75, "price": 25, "rain_effect": -0.25, "heat_effect": -0.05},
    {"product": "Momos", "location": "Varanasi", "base_demand": 50, "price": 30, "rain_effect": -0.10, "heat_effect": -0.10},
]

# A handful of fixed "holiday/event" dates for the synthetic year, standing
# in for festivals/local events. Not tied to any specific real calendar.
SYNTHETIC_HOLIDAYS = {
    "2025-10-02", "2025-10-20", "2025-10-21", "2025-11-01",
    "2025-12-25", "2026-01-14", "2026-01-26", "2026-03-06",
    "2026-03-25", "2026-08-15",
}

START_DATE = date(2025, 9, 1)
END_DATE = date(2026, 8, 20)  # up to "today" in-universe


def _synthetic_weather(day: date, rng: np.random.Generator) -> dict:
    """
    Generates plausible synthetic weather for North Indian cities by month.
    NOT real historical weather — a simplified seasonal model for demo data.
    """
    month = day.month
    if month in (12, 1, 2):  # winter
        temp = rng.normal(15, 4)
        rain_prob = 0.05
    elif month in (3, 4, 5):  # summer
        temp = rng.normal(35, 5)
        rain_prob = 0.05
    elif month in (6, 7, 8, 9):  # monsoon
        temp = rng.normal(29, 3)
        rain_prob = 0.45
    else:  # autumn (Oct, Nov)
        temp = rng.normal(24, 4)
        rain_prob = 0.10

    is_rain = rng.random() < rain_prob
    condition = "rain" if is_rain else ("extreme_heat" if temp > 38 else "clear")
    return {"temperature_celsius": round(float(temp), 1), "condition": condition}


def generate_synthetic_dataset(seed: int = RNG_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    for vendor in VENDOR_ARCHETYPES:
        current = START_DATE
        while current <= END_DATE:
            weather = _synthetic_weather(current, rng)
            is_holiday = current.isoformat() in SYNTHETIC_HOLIDAYS

            # --- demand model ---
            demand = vendor["base_demand"]

            # weekly seasonality: weekends busier (Fri=4, Sat=5, Sun=6)
            dow = current.weekday()
            if dow in (4, 5, 6):
                demand *= 1.25

            # holiday/event spike
            if is_holiday:
                demand *= 1.6

            # weather effects
            if weather["condition"] == "rain":
                demand *= (1 + vendor["rain_effect"])
            elif weather["condition"] == "extreme_heat":
                demand *= (1 + vendor["heat_effect"])

            # mild upward trend over the year (growing customer base)
            days_elapsed = (current - START_DATE).days
            demand *= (1 + 0.0003 * days_elapsed)

            # random day-to-day noise
            demand *= rng.normal(1.0, 0.12)
            demand = max(0, round(demand))

            rows.append({
                "product": vendor["product"],
                "location": vendor["location"],
                "date": current.isoformat(),
                "day_of_week": dow,
                "month": current.month,
                "is_holiday_or_event": is_holiday,
                "temperature_celsius": weather["temperature_celsius"],
                "weather_condition": weather["condition"],
                "price": vendor["price"],
                "units_sold": demand,
            })

            current += timedelta(days=1)

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = generate_synthetic_dataset()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df)} synthetic rows across {df['product'].nunique()} products "
          f"and {df['location'].nunique()} locations.")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nReminder: this is SYNTHETIC/DEMO data, not real vendor sales data.")
