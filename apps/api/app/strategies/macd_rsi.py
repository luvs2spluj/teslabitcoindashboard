"""
MACD + RSI Strategy.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
import structlog

from .base import Strategy

logger = structlog.get_logger()

class MACDRSIStrategy(Strategy):
    """MACD + RSI Strategy."""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__("MACD + RSI", params)
        self.macd_fast = params.get("macd_fast", 12)
        self.macd_slow = params.get("macd_slow", 26)
        self.macd_signal = params.get("macd_signal", 9)
        self.rsi_period = params.get("rsi_period", 14)
        self.rsi_oversold = params.get("rsi_oversold", 30)
        self.rsi_overbought = params.get("rsi_overbought", 70)
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate strategy parameters."""
        required_params = ["macd_fast", "macd_slow", "macd_signal", "rsi_period"]
        
        for param in required_params:
            if param not in params:
                logger.error(f"Missing required parameter: {param}")
                return False
            
            if not isinstance(params[param], int) or params[param] <= 0:
                logger.error(f"Invalid parameter {param}: must be positive integer")
                return False
        
        if params["macd_fast"] >= params["macd_slow"]:
            logger.error("macd_fast must be less than macd_slow")
            return False
        
        return True
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on MACD and RSI."""
        try:
            # Calculate MACD
            exp1 = data['close'].ewm(span=self.macd_fast).mean()
            exp2 = data['close'].ewm(span=self.macd_slow).mean()
            data['macd'] = exp1 - exp2
            data['macd_signal'] = data['macd'].ewm(span=self.macd_signal).mean()
            data['macd_histogram'] = data['macd'] - data['macd_signal']
            
            # Calculate RSI
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
            rs = gain / loss
            data['rsi'] = 100 - (100 / (1 + rs))
            
            # Generate signals
            data['signal'] = 0
            
            # Buy signal: MACD crosses above signal AND RSI is oversold
            buy_condition = (
                (data['macd'] > data['macd_signal']) & 
                (data['macd'].shift(1) <= data['macd_signal'].shift(1)) &
                (data['rsi'] < self.rsi_overbought)
            )
            data.loc[buy_condition, 'signal'] = 1
            
            # Sell signal: MACD crosses below signal AND RSI is overbought
            sell_condition = (
                (data['macd'] < data['macd_signal']) & 
                (data['macd'].shift(1) >= data['macd_signal'].shift(1)) &
                (data['rsi'] > self.rsi_oversold)
            )
            data.loc[sell_condition, 'signal'] = -1
            
            # Clean up
            data = data.drop(['macd', 'macd_signal', 'macd_histogram', 'rsi'], axis=1)
            
            return data
            
        except Exception as e:
            logger.error(f"Signal generation failed: {e}")
            return data

