"""External API integrations for stock and sports data."""
import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from app.config import settings
from app.database import get_mongodb_sync


class RateLimiter:
    """Simple rate limiter using MongoDB for caching."""
    
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.db = get_mongodb_sync()
        self.cache_collection = self.db["api_cache"]
        self.rate_limit_collection = self.db["rate_limits"]
    
    def is_allowed(self, api_name: str) -> bool:
        """Check if API call is allowed within rate limit."""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        count = self.rate_limit_collection.count_documents({
            "api_name": api_name,
            "timestamp": {"$gte": window_start}
        })
        
        return count < self.max_requests
    
    def record_request(self, api_name: str):
        """Record an API request."""
        self.rate_limit_collection.insert_one({
            "api_name": api_name,
            "timestamp": datetime.utcnow()
        })
    
    def get_cached(self, cache_key: str, ttl_seconds: int = 300) -> Optional[Dict]:
        """Get cached data if still valid."""
        cached = self.cache_collection.find_one({"key": cache_key})
        if cached:
            age = (datetime.utcnow() - cached["timestamp"]).total_seconds()
            if age < ttl_seconds:
                return cached["data"]
        return None
    
    def set_cached(self, cache_key: str, data: Dict):
        """Cache data with timestamp."""
        self.cache_collection.update_one(
            {"key": cache_key},
            {
                "$set": {
                    "key": cache_key,
                    "data": data,
                    "timestamp": datetime.utcnow()
                }
            },
            upsert=True
        )


rate_limiter = RateLimiter()


class AlphaVantageAPI:
    """Alpha Vantage API client for stock data."""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    @staticmethod
    async def get_stock_data(symbol: str) -> Dict[str, Any]:
        """
        Fetch stock data from Alpha Vantage.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary containing stock data
        """
        cache_key = f"alpha_vantage_{symbol}"
        
        # Check cache first
        cached = rate_limiter.get_cached(cache_key, ttl_seconds=300)
        if cached:
            return cached
        
        # Check rate limit
        if not rate_limiter.is_allowed("alpha_vantage"):
            raise Exception("Alpha Vantage rate limit exceeded. Please try again later.")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": settings.alpha_vantage_api_key,
                "outputsize": "compact"
            }
            
            response = await client.get(AlphaVantageAPI.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Record request
            rate_limiter.record_request("alpha_vantage")
            
            # Cache the response
            rate_limiter.set_cached(cache_key, data)
            
            return data
    
    @staticmethod
    async def get_quote(symbol: str) -> Dict[str, Any]:
        """Get real-time quote for a stock."""
        cache_key = f"alpha_vantage_quote_{symbol}"
        
        cached = rate_limiter.get_cached(cache_key, ttl_seconds=60)
        if cached:
            return cached
        
        if not rate_limiter.is_allowed("alpha_vantage"):
            raise Exception("Alpha Vantage rate limit exceeded.")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": settings.alpha_vantage_api_key
            }
            
            response = await client.get(AlphaVantageAPI.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            rate_limiter.record_request("alpha_vantage")
            rate_limiter.set_cached(cache_key, data)
            
            return data


class TheOddsAPI:
    """The Odds API client for sports betting data."""
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    @staticmethod
    async def get_sports_odds(
        sport: str = "basketball_nba",
        markets: str = "h2h",
        regions: str = "us"
    ) -> List[Dict[str, Any]]:
        """
        Fetch sports odds from The Odds API.
        
        Args:
            sport: Sport key (e.g., 'basketball_nba', 'americanfootball_nfl')
            markets: Comma-separated markets (e.g., 'h2h', 'spreads', 'totals')
            regions: Comma-separated regions (e.g., 'us', 'uk')
            
        Returns:
            List of events with odds
        """
        cache_key = f"the_odds_{sport}_{markets}_{regions}"
        
        cached = rate_limiter.get_cached(cache_key, ttl_seconds=300)
        if cached:
            return cached
        
        if not rate_limiter.is_allowed("the_odds_api"):
            raise Exception("The Odds API rate limit exceeded. Please try again later.")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{TheOddsAPI.BASE_URL}/sports/{sport}/odds"
            params = {
                "apiKey": settings.the_odds_api_key,
                "markets": markets,
                "regions": regions
            }
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            rate_limiter.record_request("the_odds_api")
            rate_limiter.set_cached(cache_key, data)
            
            return data
