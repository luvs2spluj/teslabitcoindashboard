"""
BGeometrics Bitcoin Data API source for comprehensive Bitcoin metrics and cycle analysis.
Enhanced with on-chain data, derivatives, and technical indicators.
"""
import aiohttp
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
import structlog
import time
import random

from .base import DataSource
from app.config import settings

logger = structlog.get_logger()

class BitcoinDataSource(DataSource):
    """BGeometrics Bitcoin Data API source for comprehensive Bitcoin metrics."""
    
    def __init__(self):
        super().__init__("bitcoin_data", "https://bitcoin-data.com/api")
        self.rate_limit_delay = 2.0
        self.session = requests.Session()
        # Add random user agents to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Make a rate-limited request to BGeometrics API."""
        try:
            # Rate limiting: wait 1-3 seconds between requests
            time.sleep(random.uniform(1, 3))
            
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json(),
                    'error': None
                }
            elif response.status_code == 429:  # Rate limited
                # Wait longer and retry once
                time.sleep(random.uniform(5, 10))
                response = self.session.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    return {
                        'success': True,
                        'data': response.json(),
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'data': None,
                        'error': f'Rate limited: {response.status_code}'
                    }
            else:
                return {
                    'success': False,
                    'data': None,
                    'error': f'HTTP {response.status_code}: {response.text}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': f'Request error: {str(e)}'
            }
    
    async def fetch_data(
        self, 
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch data from BGeometrics Bitcoin Data API."""
        try:
            logger.info(f"Fetching Bitcoin data from BGeometrics: {endpoint}")
            
            result = self._make_request(endpoint, kwargs)
            
            if result['success']:
                return {
                    "data": result['data'],
                    "endpoint": endpoint,
                    "source": "bgeometrics_bitcoin",
                    "timestamp": datetime.now().isoformat(),
                    "success": True
                }
            else:
                logger.warning(f"BGeometrics API failed for {endpoint}: {result['error']}")
                return {
                    "data": None,
                    "endpoint": endpoint,
                    "source": "bgeometrics_bitcoin",
                    "timestamp": datetime.now().isoformat(),
                    "success": False,
                    "error": result['error']
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
        """Fetch Bitcoin price data from BGeometrics."""
        params = {}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        
        return await self.fetch_data("bitcoin/price", **params)
    
    async def fetch_comprehensive_metrics(
        self, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Fetch comprehensive Bitcoin on-chain metrics."""
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=365)
        
        # Fetch multiple Bitcoin metrics
        metrics = {
            'price': 'bitcoin/price',
            'realized_price': 'bitcoin/realized_price',
            'nupl': 'bitcoin/nupl',
            'mvrv_zscore': 'bitcoin/mvrv_zscore',
            'sopr': 'bitcoin/sopr',
            'hashrate': 'bitcoin/hashrate',
            'puell_multiple': 'bitcoin/puell_multiple',
            'active_addresses': 'bitcoin/active_addresses',
            'hodl_waves': 'bitcoin/hodl_waves',
            'supply_in_profit': 'bitcoin/supply_in_profit',
            'cdd': 'bitcoin/cdd',
            'vdd': 'bitcoin/vdd',
            'liveliness': 'bitcoin/liveliness'
        }
        
        all_data = {}
        params = {
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d")
        }
        
        for metric_name, endpoint in metrics.items():
            try:
                result = await self.fetch_data(endpoint, **params)
                if result['success']:
                    all_data[metric_name] = result['data']
                    logger.info(f"Successfully fetched {metric_name}")
                else:
                    logger.warning(f"Failed to fetch {metric_name}: {result.get('error', 'Unknown error')}")
                    all_data[metric_name] = None
            except Exception as e:
                logger.error(f"Error fetching {metric_name}: {e}")
                all_data[metric_name] = None
        
        return {
            "data": all_data,
            "source": "bgeometrics_comprehensive",
            "timestamp": datetime.now().isoformat(),
            "start_date": start_date,
            "end_date": end_date,
            "metrics_count": len([k for k, v in all_data.items() if v is not None])
        }
    
    async def fetch_derivatives_data(
        self, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Fetch Bitcoin derivatives data (Basis, Open Interest, Funding Rate)."""
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        derivatives = {
            'basis': 'bitcoin/basis',
            'open_interest': 'bitcoin/open_interest',
            'funding_rate': 'bitcoin/funding_rate',
            'global_futures': 'bitcoin/global_futures',
            'taker_metrics': 'bitcoin/taker_metrics'
        }
        
        all_data = {}
        params = {
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d")
        }
        
        for metric_name, endpoint in derivatives.items():
            try:
                result = await self.fetch_data(endpoint, **params)
                if result['success']:
                    all_data[metric_name] = result['data']
                else:
                    all_data[metric_name] = None
            except Exception as e:
                logger.error(f"Error fetching {metric_name}: {e}")
                all_data[metric_name] = None
        
        return {
            "data": all_data,
            "source": "bgeometrics_derivatives",
            "timestamp": datetime.now().isoformat(),
            "start_date": start_date,
            "end_date": end_date
        }
    
    async def fetch_technical_indicators(
        self, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Fetch Bitcoin technical indicators (RSI, MACD, SMA, EMA)."""
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=365)
        
        indicators = {
            'rsi': 'bitcoin/rsi',
            'macd': 'bitcoin/macd',
            'sma': 'bitcoin/sma',
            'ema': 'bitcoin/ema'
        }
        
        all_data = {}
        params = {
            'start_date': start_date.strftime("%Y-%m-%d"),
            'end_date': end_date.strftime("%Y-%m-%d")
        }
        
        for indicator_name, endpoint in indicators.items():
            try:
                result = await self.fetch_data(endpoint, **params)
                if result['success']:
                    all_data[indicator_name] = result['data']
                else:
                    all_data[indicator_name] = None
            except Exception as e:
                logger.error(f"Error fetching {indicator_name}: {e}")
                all_data[indicator_name] = None
        
        return {
            "data": all_data,
            "source": "bgeometrics_technical",
            "timestamp": datetime.now().isoformat(),
            "start_date": start_date,
            "end_date": end_date
        }
    
    async def fetch_cycle_data(self) -> Dict[str, Any]:
        """Fetch Bitcoin cycle analysis data."""
        return await self.fetch_data("bitcoin/cycle")
    
    async def fetch_sentiment_data(self) -> Dict[str, Any]:
        """Fetch Bitcoin sentiment indicators."""
        return await self.fetch_data("bitcoin/sentiment")
