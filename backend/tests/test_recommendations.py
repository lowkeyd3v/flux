"""Tests for the recommendation endpoint (Milestone 4).

No WEATHER_API_KEY is set in the test environment (see .env.example),
so these exercise the "weather unavailable -> demand model falls back
to defaults" path automatically, plus the manual-weather-override path.
"""

VALID_VENDOR = {
    "name": "Sunita Devi",
    "product": "Chaat",
    "location": "Lucknow",
    "selling_price": 15.0,
    "current_inventory": 10.0,
    "budget": 500.0,
}


def _create_vendor(client, **overrides):
    payload = {**VALID_VENDOR, **overrides}
    return client.post("/api/vendors", json=payload).json()


def test_recommend_for_vendor(client):
    vendor = _create_vendor(client)
    response = client.post(
        f"/api/vendors/{vendor['id']}/recommend",
        json={
            "target_date": "2026-08-22",
            "temperature_celsius": 29,
            "weather_condition": "clear",
            "is_holiday_or_event": False,
        },
    )
    assert response.status_code == 200
    body = response.json()

    assert body["recommended_preparation_qty"] >= 0
    assert body["expected_revenue"] >= 0
    assert body["risk_level"] in {"low", "medium", "high"}
    assert body["explanation"]
    assert body["weather"]["source"] == "manual"
    assert body["weather"]["temperature_celsius"] == 29
    assert body["weather"]["condition"] == "clear"


def test_recommend_missing_vendor_404s(client):
    response = client.post(
        "/api/vendors/00000000-0000-0000-0000-000000000000/recommend",
        json={"target_date": "2026-08-22"},
    )
    assert response.status_code == 404


def test_recommend_requires_target_date(client):
    vendor = _create_vendor(client)
    response = client.post(f"/api/vendors/{vendor['id']}/recommend", json={})
    assert response.status_code == 422


def test_recommend_without_manual_weather_falls_back_gracefully(client):
    """
    With no WEATHER_API_KEY configured, omitting weather should not
    error -- it should fall back to the demand model's defaults and
    report weather.source == "unavailable".
    """
    vendor = _create_vendor(client)
    response = client.post(
        f"/api/vendors/{vendor['id']}/recommend",
        json={"target_date": "2026-08-22"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["weather"]["source"] == "unavailable"
    assert body["predicted_demand_point"] > 0


def test_recommendation_respects_existing_inventory(client):
    """More starting inventory should mean less additional prep needed."""
    low_stock_vendor = _create_vendor(client, current_inventory=0.0)
    high_stock_vendor = _create_vendor(client, current_inventory=1000.0)

    payload = {
        "target_date": "2026-08-22",
        "temperature_celsius": 29,
        "weather_condition": "clear",
    }

    low_stock_result = client.post(
        f"/api/vendors/{low_stock_vendor['id']}/recommend", json=payload
    ).json()
    high_stock_result = client.post(
        f"/api/vendors/{high_stock_vendor['id']}/recommend", json=payload
    ).json()

    assert (
        high_stock_result["recommended_preparation_qty"]
        < low_stock_result["recommended_preparation_qty"]
    )
    assert high_stock_result["recommended_preparation_qty"] == 0


def test_recommendation_capped_by_budget(client):
    """A very small budget should cap prep qty below the raw shortfall."""
    vendor = _create_vendor(client, current_inventory=0.0, budget=1.0, selling_price=15.0)
    response = client.post(
        f"/api/vendors/{vendor['id']}/recommend",
        json={
            "target_date": "2026-08-22",
            "temperature_celsius": 29,
            "weather_condition": "clear",
        },
    )
    body = response.json()
    # Budget of 1.0 at 15.0/unit affords far less than a day's typical demand.
    assert body["recommended_preparation_qty"] <= 1.0 / 15.0 + 0.05
    assert body["risk_level"] in {"medium", "high"}
