"""
Tests for Government Scheme RAG and recommendation endpoints (Milestone 5).
"""

VALID_VENDOR = {
    "name": "Ramesh Kumar",
    "product": "Samosa & Chai Stall",
    "location": "Prayagraj",
    "selling_price": 10.0,
    "current_inventory": 50.0,
    "budget": 2000.0,
}

ARTISAN_VENDOR = {
    "name": "Kishan Lal",
    "product": "Handmade Clay Pottery & Diyas",
    "location": "Varanasi",
    "selling_price": 40.0,
    "current_inventory": 100.0,
    "budget": 5000.0,
}


def _create_vendor(client, **overrides):
    payload = {**VALID_VENDOR, **overrides}
    return client.post("/api/vendors", json=payload).json()


def test_list_all_schemes(client):
    response = client.get("/api/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) >= 5
    scheme_ids = [s["id"] for s in schemes]
    assert "pm-svanidhi" in scheme_ids
    assert "pm-mudra-yojana" in scheme_ids
    assert "pm-vishwakarma" in scheme_ids
    assert "e-shram-portal" in scheme_ids


def test_list_schemes_with_category_filter(client):
    response = client.get("/api/schemes?category=Loan")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) >= 2
    for s in schemes:
        assert "loan" in s["category"].lower()


def test_get_scheme_by_id(client):
    response = client.get("/api/schemes/pm-svanidhi")
    assert response.status_code == 200
    scheme = response.json()
    assert scheme["id"] == "pm-svanidhi"
    assert "PM SVANidhi" in scheme["name"]
    assert "eligibility" in scheme and len(scheme["eligibility"]) > 0
    assert "benefits" in scheme and len(scheme["benefits"]) > 0
    assert "documents_required" in scheme and len(scheme["documents_required"]) > 0
    assert "application_steps" in scheme and len(scheme["application_steps"]) > 0
    assert scheme["official_url"] == "https://pmsvanidhi.mohua.gov.in"
    assert scheme["collateral_required"] is False


def test_get_scheme_not_found_returns_404(client):
    response = client.get("/api/schemes/non-existent-scheme")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_query_schemes_rag_pm_svanidhi(client):
    payload = {
        "query": "How do I get a 10000 rupee working capital loan under PM SVANidhi?",
        "top_k": 4,
    }
    response = client.post("/api/schemes/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == payload["query"]
    assert "SVANidhi" in data["answer"] or "working capital" in data["answer"].lower()
    assert len(data["sources"]) > 0
    assert data["sources"][0]["score"] > 0
    assert any("pmsvanidhi" in (s.get("official_url") or "") for s in data["sources"])
    assert len(data["suggested_followups"]) > 0


def test_query_schemes_rag_mudra(client):
    payload = {
        "query": "What are the loan limits for Shishu and Kishore under PM MUDRA?",
        "top_k": 3,
    }
    response = client.post("/api/schemes/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "50,000" in data["answer"] or "Shishu" in data["answer"]
    assert any(s["source"] == "Pradhan Mantri MUDRA Yojana (PMMY)" for s in data["sources"])


def test_query_schemes_with_vendor_context(client):
    vendor = _create_vendor(client)
    payload = {
        "query": "What schemes can help me finance my stock and stall?",
        "vendor_id": vendor["id"],
        "top_k": 4,
    }
    response = client.post("/api/schemes/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["sources"]) > 0
    assert len(data["matched_schemes"]) > 0


def test_get_recommended_schemes_for_vendor(client):
    vendor = _create_vendor(client)
    response = client.get(f"/api/vendors/{vendor['id']}/schemes/recommended")
    assert response.status_code == 200
    data = response.json()
    assert data["vendor_id"] == vendor["id"]
    assert data["vendor_name"] == vendor["name"]
    recommendations = data["recommendations"]
    assert len(recommendations) >= 2
    rec_ids = [r["scheme"]["id"] for r in recommendations]
    assert "pm-svanidhi" in rec_ids
    assert "pm-mudra-yojana" in rec_ids
    for r in recommendations:
        assert len(r["match_reason"]) > 0
        assert len(r["recommended_action"]) > 0


def test_get_recommended_schemes_for_artisan_vendor(client):
    artisan = client.post("/api/vendors", json=ARTISAN_VENDOR).json()
    response = client.get(f"/api/vendors/{artisan['id']}/schemes/recommended")
    assert response.status_code == 200
    data = response.json()
    rec_ids = [r["scheme"]["id"] for r in data["recommendations"]]
    assert "pm-vishwakarma" in rec_ids


def test_get_recommended_schemes_missing_vendor_404(client):
    response = client.get("/api/vendors/00000000-0000-0000-0000-000000000000/schemes/recommended")
    assert response.status_code == 404
