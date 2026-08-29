"""
Integration Tests for REST API Endpoints
"""

def test_api_patients_list(client):
    """Test GET /api/v1/patients endpoint."""
    response = client.get("/api/v1/patients")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "items" in data["data"]


def test_api_triage_evaluate(client):
    """Test POST /api/v1/triage/evaluate real-time calculator."""
    payload = {
        "patient_id": 1,
        "chief_complaint": "Acute shortness of breath",
        "pain_score": 6,
        "heart_rate": 95,
        "oxygen_saturation": 97.0,
        "estimated_resource_count": 2
    }
    response = client.post("/api/v1/triage/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["triage_level"] == 3
