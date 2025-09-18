"""
Bollinger Bands Mean Reversion Strategy.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
import structlog

from .base import Strategy

logger = structlog.get_logger()

class BollingerBandsStrategy(Strategy):
    """Bollinger Bands Mean Reversion Strategy."""
    
    def __init__(self, params: Dict[str, Any]):
        super().__init__("Bollinger Bands", params)
        self.period = params.get("period", 20)
        self.std_dev = params.get("std_dev", 2.0)
        self.exit_threshold = params.get("exit_threshold", 0.5)
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate strategy parameters."""
        required_params = ["period", "std_dev", "exit_threshold"]
        
        for param in required_params:
            if param not in params:
                logger.error(f"Missing required parameter: {param}")
                return False
            
            if param == "period":
                if not isinstance(params[param], int) or params[param] <= 0:
                    logger.error(f"Invalid parameter {param}: must be positive integer")
                    return False
            else:
                if not isinstance(params[param], (int, float)) or params[param] <= 0:
                    logger.error(f"Invalid parameter {param}: must be positive number")
                    return False
        
        return True
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals based on Bollinger Bands."""
        try:
            # Calculate Bollinger Bands
            data['sma'] = data['close'].rolling(window=self.period).mean()
            data['std'] = data['close'].rolling(window=self.period).std()
            data['upper_band'] = data['sma'] + (data['std'] * self.std_dev)
            data['lower_band'] = data['sma'] - (data['std'] * self.std_dev)
            
            # Calculate position relative to bands
            data['bb_position'] = (data['close'] - data['lower_band']) / (data['upper_band'] - data['lower_band'])
            
            # Generate signals
            data['signal'] = 0
            
            # Buy signal: price touches or goes below lower band
            buy_condition = data['close'] <= data['lower_band']
            data.loc[buy_condition, 'signal'] = 1
            
            # Sell signal: price touches or goes above upper band
            sell_condition = data['close'] >= data['upper_band']
            data.loc[sell_condition, 'signal'] = -1
            
            # Exit signal: price returns to middle band
            exit_condition = (
                (data['bb_position'] >= 0.5 - self.exit_threshold) & 
                (data['bb_position'] <= 0.5 + self.exit_threshold)
            )
            data.loc[exit_condition, 'signal'] = 0
            
            # Clean up
            data = data.drop(['sma', 'std', 'upper_band', 'lower_band', 'bb_position'], axis=1)
            
            return data
            
        except Exception as e:
            logger.error(f"Signal generation failed: {e}")
            return data

