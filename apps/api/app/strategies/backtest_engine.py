"""
Backtesting engine for running strategy tests.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import structlog
from sqlalchemy.orm import Session

from .base import Strategy
from .sma_cross import SMACrossoverStrategy
from .macd_rsi import MACDRSIStrategy
from .bollinger import BollingerBandsStrategy
from app.database import get_db
from app.models.ticker import Ticker
from app.models.price import Price
from app.models.strategy import Strategy as StrategyModel
from app.models.backtest_run import BacktestRun

logger = structlog.get_logger()

class BacktestEngine:
    """Engine for running strategy backtests."""
    
    def __init__(self):
        self.strategy_classes = {
            "sma_crossover": SMACrossoverStrategy,
            "macd_rsi": MACDRSIStrategy,
            "bollinger_bands": BollingerBandsStrategy
        }
    
    def run_backtest(
        self,
        strategy_family: str,
        symbol: str,
        start_date: date,
        end_date: date,
        params: Dict[str, Any],
        initial_capital: float = 100000.0,
        commission: float = 0.001,
        db: Session = None
    ) -> Dict[str, Any]:
        """Run a backtest for a given strategy."""
        try:
            # Get price data
            price_data = self._get_price_data(symbol, start_date, end_date, db)
            
            if not price_data:
                return {"error": f"No price data found for {symbol}"}
            
            # Convert to DataFrame
            df = pd.DataFrame(price_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Create strategy instance
            strategy_class = self.strategy_classes.get(strategy_family)
            if not strategy_class:
                return {"error": f"Unknown strategy family: {strategy_family}"}
            
            strategy = strategy_class(params)
            
            # Validate parameters
            if not strategy.validate_params(params):
                return {"error": "Invalid strategy parameters"}
            
            # Run backtest
            result = strategy.backtest(df, initial_capital, commission)
            
            if "error" in result:
                return result
            
            # Add metadata
            result.update({
                "symbol": symbol,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "initial_capital": initial_capital,
                "commission": commission,
                "strategy_family": strategy_family
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            return {"error": str(e)}
    
    def _get_price_data(
        self, 
        symbol: str, 
        start_date: date, 
        end_date: date,
        db: Session
    ) -> List[Dict[str, Any]]:
        """Get price data from database."""
        try:
            # Get ticker
            ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
            if not ticker:
                logger.error(f"Ticker {symbol} not found")
                return []
            
            # Get price data
            prices = db.query(Price).filter(
                Price.ticker_id == ticker.id,
                Price.date >= start_date,
                Price.date <= end_date
            ).order_by(Price.date).all()
            
            return [
                {
                    "date": price.date,
                    "open": price.open,
                    "high": price.high,
                    "low": price.low,
                    "close": price.close,
                    "volume": price.volume
                }
                for price in prices
            ]
            
        except Exception as e:
            logger.error(f"Failed to get price data: {e}")
            return []
    
    def save_backtest_result(
        self,
        result: Dict[str, Any],
        user_id: str = "system",
        db: Session = None
    ) -> int:
        """Save backtest result to database."""
        try:
            # Get ticker
            ticker = db.query(Ticker).filter(
                Ticker.symbol == result["symbol"].upper()
            ).first()
            
            if not ticker:
                raise ValueError(f"Ticker {result['symbol']} not found")
            
            # Create strategy record
            strategy = StrategyModel(
                user_id=user_id,
                name=f"{result['strategy_family']} - {result['symbol']}",
                family=result["strategy_family"],
                params_json=result["parameters"],
                version=1,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(strategy)
            db.flush()  # Get the ID
            
            # Create backtest run record
            backtest_run = BacktestRun(
                strategy_id=strategy.id,
                ticker_id=ticker.id,
                start_date=date.fromisoformat(result["start_date"]),
                end_date=date.fromisoformat(result["end_date"]),
                metrics_json=result["metrics"],
                trades_json=result["trades"],
                created_at=datetime.now(),
                status="completed"
            )
            db.add(backtest_run)
            db.commit()
            
            logger.info(f"Saved backtest result with ID: {backtest_run.id}")
            return backtest_run.id
            
        except Exception as e:
            logger.error(f"Failed to save backtest result: {e}")
            db.rollback()
            raise

