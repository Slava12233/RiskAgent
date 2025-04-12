"""
Integration tests for the Risk Engine API.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "database" in data

def test_risk_evaluation_endpoint():
    """Test the risk evaluation endpoint."""
    # Test data
    test_data = {
        "user_id": "test_user",
        "companyName": "Test Corp",
        "debtToEquity": 2.5,
        "netProfit": -1000,
        "negativeNewsScore": 0.8,
        "latePaymentsRate": 0.2,
        "sector": "technology"
    }
    
    # Make the request
    response = client.post("/api/evaluate", json=test_data)
    
    # Assertions
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    data = response.json()
    assert "score" in data, "Response should contain a score"
    assert isinstance(data["score"], float), "Score should be a float"
    assert "explanations" in data, "Response should contain explanations"
    assert isinstance(data["explanations"], list), "Explanations should be a list"
    assert "recommendation" in data, "Response should contain a recommendation"
    
    # Since this is high risk case, recommendation should be "High Risk"
    assert data["recommendation"] == "High Risk", "Expected 'High Risk' recommendation"
    
    # Evaluation ID might be None if DB interaction fails in tests
    assert "evaluation_id" in data, "Response should contain an evaluation_id"

def test_invalid_risk_evaluation():
    """Test the risk evaluation endpoint with invalid data."""
    # Missing required fields
    invalid_data = {
        "companyName": "Invalid Corp",
        # Missing other required fields
    }
    
    # Make the request
    response = client.post("/api/evaluate", json=invalid_data)
    
    # Assertions
    assert response.status_code == 422, "Should return 422 for validation errors"
    data = response.json()
    assert "detail" in data, "Response should contain error details"

def test_get_nonexistent_evaluation():
    """Test retrieving a non-existent evaluation."""
    # Non-existent ID
    response = client.get("/api/evaluations/999999")
    
    # We should get a 404 for a non-existent evaluation
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_root_redirect():
    """Test that root URL redirects to docs."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307, "Root should redirect"
    assert response.headers["location"] == "/docs", "Should redirect to docs" 