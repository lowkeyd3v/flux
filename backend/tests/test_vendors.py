"""Tests for vendor profile CRUD endpoints."""

VALID_VENDOR = {
    "name": "Ramesh Kumar",
    "product": "Samosa",
    "location": "Prayagraj",
    "selling_price": 10.0,
    "current_inventory": 50.0,
    "budget": 2000.0,
}


def test_create_vendor(client):
    response = client.post("/api/vendors", json=VALID_VENDOR)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == VALID_VENDOR["name"]
    assert "id" in body
    assert "created_at" in body


def test_create_vendor_rejects_invalid_price(client):
    payload = {**VALID_VENDOR, "selling_price": -5}
    response = client.post("/api/vendors", json=payload)
    assert response.status_code == 422


def test_list_vendors(client):
    client.post("/api/vendors", json=VALID_VENDOR)
    client.post("/api/vendors", json={**VALID_VENDOR, "name": "Sunita Devi"})

    response = client.get("/api/vendors")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_get_vendor_by_id(client):
    created = client.post("/api/vendors", json=VALID_VENDOR).json()
    response = client.get(f"/api/vendors/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_vendor_not_found(client):
    response = client.get("/api/vendors/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_vendor_partial(client):
    created = client.post("/api/vendors", json=VALID_VENDOR).json()
    response = client.patch(f"/api/vendors/{created['id']}", json={"current_inventory": 10})
    assert response.status_code == 200
    body = response.json()
    assert body["current_inventory"] == 10
    # Unchanged fields should remain the same.
    assert body["name"] == VALID_VENDOR["name"]


def test_delete_vendor(client):
    created = client.post("/api/vendors", json=VALID_VENDOR).json()
    delete_response = client.delete(f"/api/vendors/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/vendors/{created['id']}")
    assert get_response.status_code == 404
