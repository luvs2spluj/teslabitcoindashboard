"""
Bitcoin Data API source for Bitcoin metrics and cycle analysis.
"""
import aiohttp
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
import structlog

from .base import DataSource
from app.config import settings

logger = structlog.get_logger()

class BitcoinDataSource(DataSource):
    """Bitcoin Data API source for Bitcoin metrics."""
    
    def __init__(self):
        super().__init__("bitcoin_data", settings.BITCOIN_DATA_BASE_URL)
        self.rate_limit_delay = 1.0
    
    async def fetch_data(
        self, 
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch data from Bitcoin Data API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            
            logger.info(f"Fetching Bitcoin data from {endpoint}")
            
            response_data = await self._make_request(url, params=kwargs)
            
            return {
                "data": response_data,
                "endpoint": endpoint,
                "source": "bitcoin_data",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch Bitcoin data from {endpoint}: {e}")
            raise
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate Bitcoin data."""
        if not isinstance(data, dict):
            return False
        
        if "data" not in data:
            return False
        
        return True
    
    async def fetch_price_data(
        self, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Fetch Bitcoin price data."""
        params = {}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        
        return await self.fetch_data("price", **params)
    
    async def fetch_metrics(self) -> Dict[str, Any]:
        """Fetch Bitcoin market metrics."""
        return await self.fetch_data("metrics")
    
    async def fetch_cycle_data(self) -> Dict[str, Any]:
        """Fetch Bitcoin cycle analysis data."""
        return await self.fetch_data("cycle")
    
    async def fetch_sentiment_data(self) -> Dict[str, Any]:
        """Fetch Bitcoin sentiment indicators."""
        return await self.fetch_data("sentiment")
