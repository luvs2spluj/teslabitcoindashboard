"""
FRED (Federal Reserve Economic Data) data source for macro indicators.
"""
import aiohttp
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
import structlog

from .base import DataSource
from app.config import settings

logger = structlog.get_logger()

class FREDDataSource(DataSource):
    """FRED data source for macro economic indicators."""
    
    def __init__(self):
        super().__init__("fred", "https://api.stlouisfed.org/fred")
        self.api_key = settings.FRED_API_KEY
        self.rate_limit_delay = 0.5
    
    async def fetch_data(
        self, 
        series_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch data from FRED API."""
        if not self.api_key:
            raise ValueError("FRED API key not configured")
        
        try:
            # Set default date range
            if not end_date:
                end_date = date.today()
            if not start_date:
                start_date = end_date - timedelta(days=365*2)
            
            url = f"{self.base_url}/series/observations"
            params = {
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
                "observation_start": start_date.strftime("%Y-%m-%d"),
                "observation_end": end_date.strftime("%Y-%m-%d"),
                "sort_order": "desc"
            }
            
            logger.info(f"Fetching {series_id} from FRED", 
                       start_date=start_date, end_date=end_date)
            
            response_data = await self._make_request(url, params=params)
            
            if "observations" not in response_data:
                logger.warning(f"No observations found for {series_id}")
                return {"data": [], "series_id": series_id, "source": "fred"}
            
            # Process observations
            data = []
            for obs in response_data["observations"]:
                if obs["value"] != ".":  # Skip missing values
                    data.append({
                        "date": datetime.strptime(obs["date"], "%Y-%m-%d").date(),
                        "value": float(obs["value"])
                    })
            
            return {
                "data": data,
                "series_id": series_id,
                "source": "fred",
                "start_date": start_date,
                "end_date": end_date,
                "count": len(data)
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch FRED data for {series_id}: {e}")
            raise
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate FRED data."""
        if not isinstance(data, dict):
            return False
        
        if "data" not in data or not isinstance(data["data"], list):
            return False
        
        if not data["data"]:
            return False
        
        # Validate first data point
        first_point = data["data"][0]
        required_fields = ["date", "value"]
        
        for field in required_fields:
            if field not in first_point:
                return False
        
        return True
    
    async def fetch_benchmarks(
        self, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Fetch common benchmark indicators."""
        benchmarks = {
            "SP500": "SP500",  # S&P 500
            "GOLD": "GOLDAMGBD228NLBM",  # Gold price
            "DGS10": "DGS10",  # 10-Year Treasury Rate
            "CPIAUCSL": "CPIAUCSL",  # Consumer Price Index
        }
        
        results = {}
        
        for name, series_id in benchmarks.items():
            try:
                data = await self.fetch_data(series_id, start_date, end_date)
                results[name] = data
            except Exception as e:
                logger.error(f"Failed to fetch {name}: {e}")
                results[name] = {"data": [], "error": str(e)}
        
        return results
