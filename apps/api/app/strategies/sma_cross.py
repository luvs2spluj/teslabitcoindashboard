"""
Simple Moving Average Crossover Strategy.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
import structlog

from .base import Strategy

logger = structlog.get_logger()

class SMACrossoverStrategy(Strategy):
    """Simple Moving Average Crossover Strategy."""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__("SMA Crossover", params)
        self.short_window = params.get("short_window", 20)
        self.long_window = params.get("long_window", 50)
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate strategy parameters."""
        required_params = ["short_window", "long_window"]
        
        for param in required_params:
            if param not in params:
                logger.error(f"Missing required parameter: {param}")
                return False
            
            if not isinstance(params[param], int) or params[param] <= 0:
                logger.error(f"Invalid parameter {param}: must be positive integer")
                return False
        
        if params["short_window"] >= params["long_window"]:
            logger.error("short_window must be less than long_window")
            return False
        
        return True
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on SMA crossover."""
        try:
            # Calculate moving averages
            data['sma_short'] = data['close'].rolling(window=self.short_window).mean()
            data['sma_long'] = data['close'].rolling(window=self.long_window).mean()
            
            # Generate signals
            data['signal'] = 0
            
            # Buy signal: short SMA crosses above long SMA
            data.loc[data['sma_short'] > data['sma_long'], 'signal'] = 1
            
            # Sell signal: short SMA crosses below long SMA
            data.loc[data['sma_short'] < data['sma_long'], 'signal'] = -1
            
            # Only change position on crossover
            data['position'] = data['signal'].diff()
            data['signal'] = data['position']
            
            # Clean up
            data = data.drop(['sma_short', 'sma_long', 'position'], axis=1)
            
            return data
            
        except Exception as e:
            logger.error(f"Signal generation failed: {e}")
            return data

