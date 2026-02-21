"""Unit tests for prediction models."""
import pytest
from app.services.prediction_models import StockPredictionModel, SportsPredictionModel


def test_stock_prediction_model():
    """Test stock prediction model."""
    # Mock price data
    price_data = {
        "Time Series (Daily)": {
            "2024-01-01": {"4. close": "100.0"},
            "2024-01-02": {"4. close": "101.0"},
            "2024-01-03": {"4. close": "102.0"},
            "2024-01-04": {"4. close": "103.0"},
            "2024-01-05": {"4. close": "104.0"},
            "2024-01-06": {"4. close": "105.0"},
            "2024-01-07": {"4. close": "106.0"},
            "2024-01-08": {"4. close": "107.0"},
            "2024-01-09": {"4. close": "108.0"},
            "2024-01-10": {"4. close": "109.0"},
        }
    }
    
    result = StockPredictionModel.predict(price_data)
    
    assert "probability" in result
    assert "confidence" in result
    assert "direction" in result
    assert "model_version" in result
    assert 0.0 <= result["probability"] <= 1.0
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["direction"] in ["up", "down", "neutral"]


def test_sports_prediction_model():
    """Test sports prediction model."""
    # Mock event data
    event_data = {
        "id": "test_event_1",
        "home_team": "Team A",
        "away_team": "Team B",
        "bookmakers": [
            {
                "key": "draftkings",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Team A", "price": -110},
                            {"name": "Team B", "price": -110}
                        ]
                    }
                ]
            }
        ]
    }
    
    result = SportsPredictionModel.predict(event_data)
    
    assert "probability" in result
    assert "confidence" in result
    assert "outcome" in result
    assert "model_version" in result
    assert 0.0 <= result["probability"] <= 1.0
    assert 0.0 <= result["confidence"] <= 1.0
