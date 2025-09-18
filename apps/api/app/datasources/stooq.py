"""
Stooq data source for equity prices and market data.
"""
import pandas as pd
import pandas_datareader as pdr
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
import structlog

from .base import DataSource

logger = structlog.get_logger()

class StooqDataSource(DataSource):
    """Stooq data source for equity prices."""
    
    def __init__(self):
        super().__init__("stooq")
        self.rate_limit_delay = 0.5  # Stooq allows faster requests
    
    async def fetch_data(
        self, 
        symbol: str, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch price data from Stooq."""
        try:
            # Convert symbol to Stooq format
            stooq_symbol = self._convert_symbol(symbol)
            
            # Set default date range if not provided
            if not end_date:
                end_date = date.today()
            if not start_date:
                start_date = end_date - timedelta(days=365)
            
            logger.info(f"Fetching {symbol} data from Stooq", 
                       start_date=start_date, end_date=end_date)
            
            # Use pandas-datareader to fetch data
            df = pdr.get_data_stooq(stooq_symbol, start=start_date, end=end_date)
            
            if df.empty:
                logger.warning(f"No data found for {symbol}")
                return {"data": [], "symbol": symbol, "source": "stooq"}
            
            # Convert to list of dictionaries
            data = []
            for date_idx, row in df.iterrows():
                data.append({
                    "date": date_idx.date(),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"])
                })
            
            return {
                "data": data,
                "symbol": symbol,
                "source": "stooq",
                "start_date": start_date,
                "end_date": end_date,
                "count": len(data)
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {e}")
            raise
    
    def _convert_symbol(self, symbol: str) -> str:
        """Convert symbol to Stooq format."""
        symbol = symbol.upper()
        
        # Add exchange suffix if not present
        if symbol == "SPY":
            return "SPY.US"
        elif symbol == "GLD":
            return "GLD.US"
        elif symbol == "QQQ":
            return "QQQ.US"
        elif symbol == "TSLA":
            return "TSLA.US"
        else:
            # Default to US exchange
            return f"{symbol}.US"
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate Stooq data."""
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
