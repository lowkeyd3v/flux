"""
Tests for Voice and Multilingual API (Milestone 7).
"""


def test_get_supported_languages(client):
    response = client.get("/api/voice/supported-languages")
    assert response.status_code == 200
    data = response.json()
    assert "supported_languages" in data
    assert "voice_models" in data
    lang_codes = [l["code"] for l in data["supported_languages"]]
    assert "en" in lang_codes
    assert "hi" in lang_codes
    assert "hinglish" in lang_codes


def test_parse_voice_intent_scheme_query_english(client):
    payload = {
        "transcript": "How to apply for PM SVANidhi working capital loan?",
        "language": "en",
    }
    response = client.post("/api/voice/parse-intent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["transcript"] == payload["transcript"]
    assert data["intent"]["action_type"] == "query_scheme"
    assert data["intent"]["confidence"] > 0.8
    assert "parameters" in data["intent"]


def test_parse_voice_intent_scheme_query_hindi(client):
    payload = {
        "transcript": "मुझे पीएम मुद्रा योजना में लोन कैसे मिलेगा?",
        "language": "hi",
    }
    response = client.post("/api/voice/parse-intent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"]["action_type"] == "query_scheme"
    assert "सरकारी योजनाओं" in data["intent"]["feedback_text"]


def test_parse_voice_intent_demand_prediction_hinglish(client):
    payload = {
        "transcript": "Kal kitna bikega forecast batao",
        "language": "hinglish",
    }
    response = client.post("/api/voice/parse-intent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"]["action_type"] == "predict_demand"
    assert "demand forecast" in data["intent"]["feedback_text"].lower()


def test_parse_voice_intent_recommendation(client):
    payload = {
        "transcript": "How much stock should I prepare for tomorrow?",
        "language": "en",
    }
    response = client.post("/api/voice/parse-intent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"]["action_type"] == "get_recommendation"


def test_parse_voice_intent_sales_logging(client):
    payload = {
        "transcript": "Aaj 40 plate samosa becha for 400 rupees",
        "language": "hinglish",
    }
    response = client.post("/api/voice/parse-intent", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"]["action_type"] == "log_sale"
    assert data["intent"]["parameters"]["units_sold"] == 40.0
    assert data["intent"]["parameters"]["price"] == 400.0
