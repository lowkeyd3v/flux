"""Tests for the demand prediction endpoint."""

VALID_VENDOR = {
    "name": "Ramesh Kumar",
    "product": "Samosa",
    "location": "Prayagraj",
    "selling_price": 10.0,
    "current_inventory": 50.0,
    "budget": 2000.0,
}


def _create_vendor(client):
    return client.post("/api/vendors", json=VALID_VENDOR).json()


def test_predict_demand_for_vendor(client):
    vendor = _create_vendor(client)
    response = client.post(
        f"/api/vendors/{vendor['id']}/predict",
        json={
            "target_date": "2026-08-22",
            "temperature_celsius": 29,
            "weather_condition": "rain",
            "is_holiday_or_event": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_demand_point"] > 0
    assert body["predicted_demand_low"] <= body["predicted_demand_point"] <= body["predicted_demand_high"]
    assert 0 <= body["confidence"] <= 1
    assert body["model_version"]


def test_predict_demand_missing_vendor_404s(client):
    response = client.post(
        "/api/vendors/00000000-0000-0000-0000-000000000000/predict",
        json={"target_date": "2026-08-22"},
    )
    assert response.status_code == 404


def test_predict_demand_requires_target_date(client):
    vendor = _create_vendor(client)
    response = client.post(f"/api/vendors/{vendor['id']}/predict", json={})
    assert response.status_code == 422


def test_holiday_increases_predicted_demand(client):
    """
    Sanity check that the model actually responds to the holiday flag in
    the expected direction, using the same product/location/weather for
    both requests so holiday is the only varying factor.
    """
    vendor = _create_vendor(client)
    base_payload = {
        "target_date": "2026-08-15",
        "temperature_celsius": 28,
        "weather_condition": "clear",
    }

    normal = client.post(
        f"/api/vendors/{vendor['id']}/predict",
        json={**base_payload, "is_holiday_or_event": False},
    ).json()
    holiday = client.post(
        f"/api/vendors/{vendor['id']}/predict",
        json={**base_payload, "is_holiday_or_event": True},
    ).json()

    assert holiday["predicted_demand_point"] > normal["predicted_demand_point"]
