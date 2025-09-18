"""
Base data source interface and common functionality.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import asyncio
import aiohttp
import structlog
from datetime import datetime, timedelta
import time

logger = structlog.get_logger()

class DataSource(ABC):
    """Base class for all data sources."""
    
    def __init__(self, name: str, base_url: Optional[str] = None):
        self.name = name
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_delay = 1.0  # Default 1 second between requests
        self.last_request_time = 0.0
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'financial-app/0.1 (https://github.com/your-repo)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def _rate_limit(self):
        """Implement rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    async def _make_request(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with rate limiting and error handling."""
        await self._rate_limit()
        
        if not self.session:
            raise RuntimeError("DataSource not initialized. Use async context manager.")
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    logger.warning(f"Rate limited by {self.name}, retrying...")
                    await asyncio.sleep(5)
                    return await self._make_request(url, params, headers)
                else:
                    logger.error(f"HTTP {response.status} from {self.name}: {url}")
                    response.raise_for_status()
        except Exception as e:
            logger.error(f"Request failed for {self.name}: {e}")
            raise
    
    @abstractmethod
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """Fetch data from the source."""
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate fetched data."""
        pass
    
    def get_cache_key(self, **kwargs) -> str:
        """Generate cache key for this request."""
        params = sorted(kwargs.items())
        return f"{self.name}:{':'.join(f'{k}={v}' for k, v in params)}"
