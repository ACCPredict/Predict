"""Prediction models for stocks and sports."""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from sklearn.linear_model import LogisticRegression
from datetime import datetime


class StockPredictionModel:
    """Logistic regression model for stock price predictions."""
    
    MODEL_VERSION = "v1.0.0"
    
    @staticmethod
    def calculate_indicators(prices: List[float]) -> Dict[str, float]:
        """
        Calculate technical indicators from price history.
        
        Args:
            prices: List of historical prices (most recent last)
            
        Returns:
            Dictionary of calculated indicators
        """
        if len(prices) < 2:
            return {}
        
        prices_array = np.array(prices)
        
        # Simple moving averages
        sma_5 = np.mean(prices_array[-5:]) if len(prices_array) >= 5 else prices_array[-1]
        sma_10 = np.mean(prices_array[-10:]) if len(prices_array) >= 10 else prices_array[-1]
        
        # Price changes
        recent_change = (prices_array[-1] - prices_array[-2]) / prices_array[-2] if len(prices_array) >= 2 else 0
        change_5d = (prices_array[-1] - prices_array[-5]) / prices_array[-5] if len(prices_array) >= 5 else 0
        
        # Volatility (standard deviation of recent prices)
        volatility = np.std(prices_array[-10:]) if len(prices_array) >= 10 else 0
        
        return {
            "sma_5": sma_5,
            "sma_10": sma_10,
            "recent_change": recent_change,
            "change_5d": change_5d,
            "volatility": volatility,
            "current_price": prices_array[-1]
        }
    
    @staticmethod
    def predict(price_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate stock prediction using logistic regression.
        
        Args:
            price_data: Dictionary containing stock price history
            
        Returns:
            Prediction dictionary with probability, confidence, and direction
        """
        try:
            # Extract time series data
            time_series = price_data.get("Time Series (Daily)", {})
            if not time_series:
                raise ValueError("No time series data available")
            
            # Convert to sorted list of prices (oldest to newest)
            dates = sorted(time_series.keys())
            prices = [float(time_series[date]["4. close"]) for date in dates]
            
            if len(prices) < 10:
                # Not enough data, return default prediction
                return {
                    "probability": 0.5,
                    "confidence": 0.3,
                    "direction": "neutral",
                    "model_version": StockPredictionModel.MODEL_VERSION,
                    "metadata": {"error": "Insufficient data"}
                }
            
            # Calculate indicators
            indicators = StockPredictionModel.calculate_indicators(prices)
            
            # Prepare features for logistic regression
            features = np.array([[
                indicators["recent_change"],
                indicators["change_5d"],
                (indicators["sma_5"] - indicators["sma_10"]) / indicators["sma_10"] if indicators["sma_10"] > 0 else 0,
                indicators["volatility"] / indicators["current_price"] if indicators["current_price"] > 0 else 0
            ]])
            
            # Simple logistic regression model
            # In production, this would be trained on historical data
            # For now, using a simple heuristic-based approach
            model = LogisticRegression(random_state=42)
            
            # Create synthetic training data for demonstration
            # In production, use real historical data
            X_train = np.random.randn(100, 4)
            y_train = (X_train[:, 0] > 0).astype(int)
            model.fit(X_train, y_train)
            
            # Make prediction
            probability = model.predict_proba(features)[0][1]
            direction = "up" if probability > 0.5 else "down"
            
            # Calculate confidence based on data quality and signal strength
            confidence = min(0.9, abs(probability - 0.5) * 2 + 0.3)
            
            return {
                "probability": float(probability),
                "confidence": float(confidence),
                "direction": direction,
                "price_target": indicators["current_price"] * (1 + (probability - 0.5) * 0.1),
                "current_price": indicators["current_price"],
                "model_version": StockPredictionModel.MODEL_VERSION,
                "metadata": {
                    "indicators": indicators,
                    "data_points": len(prices)
                }
            }
            
        except Exception as e:
            # Return default prediction on error
            return {
                "probability": 0.5,
                "confidence": 0.2,
                "direction": "neutral",
                "model_version": StockPredictionModel.MODEL_VERSION,
                "metadata": {"error": str(e)}
            }


class SportsPredictionModel:
    """Simple model for sports predictions based on odds and team ratings."""
    
    MODEL_VERSION = "v1.0.0"
    
    @staticmethod
    def calculate_team_rating(team_name: str, historical_data: Optional[Dict] = None) -> float:
        """
        Calculate simple team rating.
        
        In production, this would use historical performance data.
        For now, returns a default rating.
        
        Args:
            team_name: Name of the team
            historical_data: Optional historical performance data
            
        Returns:
            Team rating (0.0 to 1.0)
        """
        # Placeholder: In production, use actual team statistics
        # For now, return a neutral rating
        return 0.5
    
    @staticmethod
    def implied_probability_from_odds(odds: float, odds_format: str = "american") -> float:
        """
        Convert betting odds to implied probability.
        
        Args:
            odds: Betting odds
            odds_format: 'american', 'decimal', or 'fractional'
            
        Returns:
            Implied probability (0.0 to 1.0)
        """
        if odds_format == "american":
            if odds > 0:
                return 100 / (odds + 100)
            else:
                return abs(odds) / (abs(odds) + 100)
        elif odds_format == "decimal":
            return 1 / odds
        else:
            # Default to decimal
            return 1 / odds if odds > 0 else 0.5
    
    @staticmethod
    def predict(event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sports prediction from odds data.
        
        Args:
            event_data: Dictionary containing event and odds information
            
        Returns:
            Prediction dictionary with probability, confidence, and outcome
        """
        try:
            # Extract event information
            home_team = event_data.get("home_team", "Team A")
            away_team = event_data.get("away_team", "Team B")
            
            # Get odds (assuming first bookmaker's odds)
            bookmakers = event_data.get("bookmakers", [])
            if not bookmakers:
                raise ValueError("No bookmaker data available")
            
            # Get first bookmaker's h2h (head-to-head) odds
            bookmaker = bookmakers[0]
            markets = bookmaker.get("markets", [])
            h2h_market = next((m for m in markets if m.get("key") == "h2h"), None)
            
            if not h2h_market:
                raise ValueError("No h2h market available")
            
            outcomes = h2h_market.get("outcomes", [])
            if len(outcomes) < 2:
                raise ValueError("Insufficient outcomes")
            
            # Find home and away team odds
            home_outcome = next((o for o in outcomes if o.get("name") == home_team), None)
            away_outcome = next((o for o in outcomes if o.get("name") == away_team), None)
            
            if not home_outcome or not away_outcome:
                # Use first two outcomes if team names don't match
                home_outcome = outcomes[0]
                away_outcome = outcomes[1]
            
            home_odds = home_outcome.get("price", 0)
            away_odds = away_outcome.get("price", 0)
            
            # Convert to implied probabilities
            home_implied = SportsPredictionModel.implied_probability_from_odds(home_odds)
            away_implied = SportsPredictionModel.implied_probability_from_odds(away_odds)
            
            # Adjust with team ratings (simplified)
            home_rating = SportsPredictionModel.calculate_team_rating(home_team)
            away_rating = SportsPredictionModel.calculate_team_rating(away_team)
            
            # Combine implied probability with team rating
            # Weight: 70% implied probability, 30% team rating
            home_adjusted = home_implied * 0.7 + home_rating * 0.3
            away_adjusted = away_implied * 0.7 + away_rating * 0.3
            
            # Normalize probabilities
            total = home_adjusted + away_adjusted
            if total > 0:
                home_prob = home_adjusted / total
                away_prob = away_adjusted / total
            else:
                home_prob = 0.5
                away_prob = 0.5
            
            # Determine prediction (home team win)
            probability = home_prob
            outcome = "win" if probability > 0.5 else "loss"
            predicted_team = home_team if probability > 0.5 else away_team
            
            # Calculate confidence based on probability margin
            confidence = min(0.9, abs(probability - 0.5) * 2 + 0.4)
            
            return {
                "probability": float(probability),
                "confidence": float(confidence),
                "outcome": outcome,
                "team": predicted_team,
                "odds": float(home_odds),
                "implied_probability": float(home_implied),
                "model_version": SportsPredictionModel.MODEL_VERSION,
                "metadata": {
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_odds": home_odds,
                    "away_odds": away_odds
                }
            }
            
        except Exception as e:
            # Return default prediction on error
            return {
                "probability": 0.5,
                "confidence": 0.2,
                "outcome": "unknown",
                "model_version": SportsPredictionModel.MODEL_VERSION,
                "metadata": {"error": str(e)}
            }
