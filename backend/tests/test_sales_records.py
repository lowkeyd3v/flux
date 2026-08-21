"""Tests for sales record endpoints, nested under a vendor."""

VALID_VENDOR = {
    "name": "Ramesh Kumar",
    "product": "Samosa",
    "location": "Prayagraj",
    "selling_price": 10.0,
    "current_inventory": 50.0,
    "budget": 2000.0,
}

VALID_SALES_RECORD = {
    "sale_date": "2026-08-15",
    "units_sold": 45,
    "price": 10.0,
    "is_holiday_or_event": False,
    "weather_condition": "clear",
}


def _create_vendor(client):
    return client.post("/api/vendors", json=VALID_VENDOR).json()


def test_create_sales_record(client):
    vendor = _create_vendor(client)
    response = client.post(
        f"/api/vendors/{vendor['id']}/sales", json=VALID_SALES_RECORD
    )
    assert response.status_code == 201
    body = response.json()
    assert body["vendor_id"] == vendor["id"]
    assert body["units_sold"] == 45


def test_create_sales_record_for_missing_vendor_404s(client):
    response = client.post(
        "/api/vendors/00000000-0000-0000-0000-000000000000/sales",
        json=VALID_SALES_RECORD,
    )
    assert response.status_code == 404


def test_bulk_create_sales_records(client):
    vendor = _create_vendor(client)
    payload = {
        "records": [
            {**VALID_SALES_RECORD, "sale_date": "2026-08-14", "units_sold": 30},
            {**VALID_SALES_RECORD, "sale_date": "2026-08-13", "units_sold": 60},
        ]
    }
    response = client.post(f"/api/vendors/{vendor['id']}/sales/bulk", json=payload)
    assert response.status_code == 201
    assert len(response.json()) == 2


def test_list_sales_records(client):
    vendor = _create_vendor(client)
    client.post(f"/api/vendors/{vendor['id']}/sales", json=VALID_SALES_RECORD)

    response = client.get(f"/api/vendors/{vendor['id']}/sales")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_sales_record(client):
    vendor = _create_vendor(client)
    record = client.post(
        f"/api/vendors/{vendor['id']}/sales", json=VALID_SALES_RECORD
    ).json()

    delete_response = client.delete(f"/api/vendors/{vendor['id']}/sales/{record['id']}")
    assert delete_response.status_code == 204

    list_response = client.get(f"/api/vendors/{vendor['id']}/sales")
    assert list_response.json() == []


def test_deleting_vendor_cascades_to_sales_records(client):
    vendor = _create_vendor(client)
    client.post(f"/api/vendors/{vendor['id']}/sales", json=VALID_SALES_RECORD)

    client.delete(f"/api/vendors/{vendor['id']}")

    # Vendor is gone, so its sales route also 404s.
    response = client.get(f"/api/vendors/{vendor['id']}/sales")
    assert response.status_code == 404
