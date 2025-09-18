"""
BGeometrics data source adapter for Tesla, Bitcoin, and other financial data.
Primary data source with yfinance as fallback.
"""

import requests
import pandas as pd
import yfinance as yf
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta, date
import time
import random
import structlog
from .base import DataSource

logger = structlog.get_logger()


class BGeometricsDataSource(DataSource):
    """BGeometrics data source for Tesla, Bitcoin, and other financial data."""
    
    def __init__(self):
        super().__init__("bgeometrics")
        self.base_url = "https://bitcoin-data.com/api"
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
        self.rate_limit_delay = 2.0  # Conservative rate limiting
    
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
        symbol: str, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Fetch data from BGeometrics with yfinance fallback.
        
        Args:
            symbol: Stock symbol (e.g., 'TSLA', 'BTC-USD')
            start_date: Start date
            end_date: End date
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the fetched data
        """
        try:
            # Set default date range if not provided
            if not end_date:
                end_date = date.today()
            if not start_date:
                start_date = end_date - timedelta(days=365)
            
            logger.info(f"Fetching {symbol} data from BGeometrics", 
                       start_date=start_date, end_date=end_date)
            
            # Try BGeometrics first for Tesla
            if symbol.upper() == 'TSLA':
                result = self._fetch_tesla_data(start_date, end_date)
            elif symbol.upper() in ['BTC', 'BTC-USD']:
                result = self._fetch_bitcoin_data(start_date, end_date)
            elif symbol.upper() in ['GOOGL', 'NVDA', 'META', 'AAPL', 'AMZN', 'MSFT']:
                result = self._fetch_stock_data(symbol, start_date, end_date)
            else:
                # For other symbols, go directly to yfinance
                result = self._fetch_yfinance_data(symbol, start_date, end_date)
            
            if result['success']:
                return result['data']
            else:
                logger.warning(f"BGeometrics failed for {symbol}, using yfinance fallback")
                return self._fetch_yfinance_data(symbol, start_date, end_date)['data']
                
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {e}")
            # Fallback to yfinance on any error
            return self._fetch_yfinance_data(symbol, start_date, end_date)['data']
    
    def _fetch_tesla_data(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Fetch Tesla data from BGeometrics."""
        try:
            result = self._make_request("tesla", {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            })
            
            if result['success']:
                # Convert BGeometrics format to our standard format
                data = []
                for item in result['data']:
                    data.append({
                        'date': datetime.strptime(item['date'], '%Y-%m-%d').date(),
                        'open': float(item.get('open', 0)),
                        'high': float(item.get('high', 0)),
                        'low': float(item.get('low', 0)),
                        'close': float(item.get('close', 0)),
                        'volume': int(item.get('volume', 0))
                    })
                
                return {
                    'success': True,
                    'data': {
                        'data': data,
                        'symbol': 'TSLA',
                        'source': 'bgeometrics',
                        'start_date': start_date,
                        'end_date': end_date,
                        'count': len(data)
                    }
                }
            
            return {'success': False, 'error': result['error']}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _fetch_bitcoin_data(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Fetch Bitcoin on-chain data from BGeometrics."""
        try:
            # Fetch multiple Bitcoin metrics
            metrics = ['price', 'realized_price', 'nupl', 'mvrv_zscore', 'sopr']
            all_data = {}
            
            for metric in metrics:
                result = self._make_request(f"bitcoin/{metric}", {
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                })
                
                if result['success']:
                    all_data[metric] = result['data']
            
            # Convert price data to our standard format
            if 'price' in all_data:
                data = []
                for item in all_data['price']:
                    data.append({
                        'date': datetime.strptime(item['date'], '%Y-%m-%d').date(),
                        'open': float(item.get('open', item.get('price', 0))),
                        'high': float(item.get('high', item.get('price', 0))),
                        'low': float(item.get('low', item.get('price', 0))),
                        'close': float(item.get('close', item.get('price', 0))),
                        'volume': int(item.get('volume', 0))
                    })
                
                return {
                    'success': True,
                    'data': {
                        'data': data,
                        'symbol': 'BTC',
                        'source': 'bgeometrics',
                        'start_date': start_date,
                        'end_date': end_date,
                        'count': len(data),
                        'metrics': all_data  # Include additional metrics
                    }
                }
            
            return {'success': False, 'error': 'No price data available'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _fetch_stock_data(self, symbol: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """Fetch stock data from BGeometrics."""
        try:
            result = self._make_request(f"stocks/{symbol.lower()}", {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            })
            
            if result['success']:
                data = []
                for item in result['data']:
                    data.append({
                        'date': datetime.strptime(item['date'], '%Y-%m-%d').date(),
                        'open': float(item.get('open', 0)),
                        'high': float(item.get('high', 0)),
                        'low': float(item.get('low', 0)),
                        'close': float(item.get('close', 0)),
                        'volume': int(item.get('volume', 0))
                    })
                
                return {
                    'success': True,
                    'data': {
                        'data': data,
                        'symbol': symbol.upper(),
                        'source': 'bgeometrics',
                        'start_date': start_date,
                        'end_date': end_date,
                        'count': len(data)
                    }
                }
            
            return {'success': False, 'error': result['error']}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _fetch_yfinance_data(self, symbol: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        Fallback method using yfinance with proxy and rate limiting.
        """
        try:
            # Rate limiting for yfinance
            time.sleep(random.uniform(0.5, 2.0))
            
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Fetch historical data
            df = ticker.history(start=start_date, end=end_date)
            
            if df.empty:
                return {
                    'success': False,
                    'data': {
                        'data': [],
                        'symbol': symbol,
                        'source': 'yfinance',
                        'start_date': start_date,
                        'end_date': end_date,
                        'count': 0
                    }
                }
            
            # Convert to our standard format
            data = []
            for date_idx, row in df.iterrows():
                data.append({
                    'date': date_idx.date(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume'])
                })
            
            return {
                'success': True,
                'data': {
                    'data': data,
                    'symbol': symbol,
                    'source': 'yfinance',
                    'start_date': start_date,
                    'end_date': end_date,
                    'count': len(data)
                }
            }
            
        except Exception as e:
            logger.error(f"yfinance fallback failed for {symbol}: {e}")
            return {
                'success': False,
                'data': {
                    'data': [],
                    'symbol': symbol,
                    'source': 'yfinance',
                    'start_date': start_date,
                    'end_date': end_date,
                    'count': 0
                }
            }
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate BGeometrics data."""
        if not isinstance(data, dict):
            return False
        
        if "data" not in data or not isinstance(data["data"], list):
            return False
        
        if not data["data"]:
            return False
        
        # Validate first data point
        first_point = data["data"][0]
        required_fields = ["date", "open", "high", "low", "close", "volume"]
        
        for field in required_fields:
            if field not in first_point:
                return False
        
        return True
