"""
ETL job for loading daily price data from Stooq.
"""
from typing import Dict, Any, List
from datetime import date, timedelta
import structlog
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base import ETLJob
from app.datasources.stooq import StooqDataSource
from app.models.ticker import Ticker
from app.models.price import Price

logger = structlog.get_logger()

class PricesETL(ETLJob):
    """ETL job for daily price data."""
    
    def __init__(self):
        super().__init__("load_prices_daily")
        self.symbols = ["TSLA", "SPY", "GLD", "QQQ"]
    
    async def extract(self, symbols: List[str] = None, **kwargs) -> Dict[str, Any]:
        """Extract price data from Stooq."""
        symbols = symbols or self.symbols
        all_data = {}
        
        async with StooqDataSource() as stooq:
            for symbol in symbols:
                try:
                    # Get last 30 days of data by default
                    end_date = date.today()
                    start_date = end_date - timedelta(days=30)
                    
                    data = await stooq.fetch_data(
                        symbol=symbol,
                        start_date=start_date,
                        end_date=end_date
                    )
                    
                    if stooq.validate_data(data):
                        all_data[symbol] = data
                        logger.info(f"Extracted {len(data['data'])} price records for {symbol}")
                    else:
                        logger.warning(f"Invalid data received for {symbol}")
                        
                except Exception as e:
                    logger.error(f"Failed to extract data for {symbol}: {e}")
                    all_data[symbol] = {"data": [], "error": str(e)}
        
        return {"symbols": all_data}
    
    def transform(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform price data for loading."""
        transformed_records = []
        
        for symbol, symbol_data in data["symbols"].items():
            if "error" in symbol_data:
                continue
                
            for price_record in symbol_data["data"]:
                transformed_records.append({
                    "symbol": symbol,
                    "date": price_record["date"],
                    "open": price_record["open"],
                    "high": price_record["high"],
                    "low": price_record["low"],
                    "close": price_record["close"],
                    "volume": price_record["volume"],
                    "source": "stooq"
                })
        
        return transformed_records
    
    def load(self, data: List[Dict[str, Any]]) -> int:
        """Load price data into database."""
        if not self.db:
            raise RuntimeError("Database session not initialized")
        
        loaded_count = 0
        
        for record in data:
            try:
                # Get ticker
                ticker = self.db.query(Ticker).filter(
                    Ticker.symbol == record["symbol"]
                ).first()
                
                if not ticker:
                    logger.warning(f"Ticker {record['symbol']} not found, skipping")
                    continue
                
                # Check if price record already exists
                existing = self.db.query(Price).filter(
                    and_(
                        Price.ticker_id == ticker.id,
                        Price.date == record["date"]
                    )
                ).first()
                
                if existing:
                    # Update existing record
                    existing.open = record["open"]
                    existing.high = record["high"]
                    existing.low = record["low"]
                    existing.close = record["close"]
                    existing.volume = record["volume"]
                    existing.source = record["source"]
                else:
                    # Create new record
                    price = Price(
                        ticker_id=ticker.id,
                        date=record["date"],
                        open=record["open"],
                        high=record["high"],
                        low=record["low"],
                        close=record["close"],
                        volume=record["volume"],
                        source=record["source"]
                    )
                    self.db.add(price)
                
                loaded_count += 1
                
            except Exception as e:
                logger.error(f"Failed to load price record for {record['symbol']}: {e}")
                continue
        
        try:
            self.db.commit()
            logger.info(f"Successfully loaded {loaded_count} price records")
        except Exception as e:
            logger.error(f"Failed to commit price data: {e}")
            self.db.rollback()
            raise
        
        return loaded_count

