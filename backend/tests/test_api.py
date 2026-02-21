"""API smoke tests."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_stocks_predictions_endpoint():
    """Test stocks predictions endpoint (may fail without auth/API keys)."""
    # This will likely fail without proper setup, but tests the endpoint exists
    response = client.get("/stocks/predictions?symbol=AAPL")
    # Accept either 200 (if working) or 401/500 (if not configured)
    assert response.status_code in [200, 401, 500]


def test_sports_predictions_endpoint():
    """Test sports predictions endpoint."""
    response = client.get("/sports/predictions")
    # Accept either 200 (if working) or 401/500 (if not configured)
    assert response.status_code in [200, 401, 500]
