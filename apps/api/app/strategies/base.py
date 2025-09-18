"""
Base strategy classes and common functionality.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, date
import structlog

logger = structlog.get_logger()

class Strategy(ABC):
    """Base class for all trading strategies."""
    
    def __init__(self, name: str, params: Dict[str, Any]):
        self.name = name
        self.params = params
        self.positions = []
        self.trades = []
        self.equity_curve = []
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals."""
        pass
    
    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate strategy parameters."""
        pass
    
    def backtest(
        self, 
        data: pd.DataFrame, 
        initial_capital: float = 100000.0,
        commission: float = 0.001
    ) -> Dict[str, Any]:
        """Run backtest for the strategy."""
        try:
            # Generate signals
            signals_df = self.generate_signals(data.copy())
            
            # Execute trades
            trades = self._execute_trades(signals_df, initial_capital, commission)
            
            # Calculate performance metrics
            metrics = self._calculate_metrics(trades, initial_capital)
            
            return {
                "strategy_name": self.name,
                "parameters": self.params,
                "trades": trades,
                "metrics": metrics,
                "equity_curve": self.equity_curve,
                "backtest_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Backtest failed for strategy {self.name}: {e}")
            return {"error": str(e)}
    
    def _execute_trades(
        self, 
        signals_df: pd.DataFrame, 
        initial_capital: float,
        commission: float
    ) -> List[Dict[str, Any]]:
        """Execute trades based on signals."""
        trades = []
        position = 0
        cash = initial_capital
        equity = initial_capital
        
        for i, (date, row) in enumerate(signals_df.iterrows()):
            signal = row.get('signal', 0)
            price = row['close']
            
            # Execute trade if signal changes
            if signal != position:
                if position != 0:  # Close existing position
                    trade = {
                        "date": date,
                        "action": "close",
                        "price": price,
                        "shares": -position,
                        "value": abs(position) * price,
                        "commission": abs(position) * price * commission,
                        "cash_flow": position * price - abs(position) * price * commission
                    }
                    trades.append(trade)
                    cash += trade["cash_flow"]
                
                if signal != 0:  # Open new position
                    shares = int(cash * 0.95 / price)  # Use 95% of cash
                    if shares > 0:
                        trade = {
                            "date": date,
                            "action": "open",
                            "price": price,
                            "shares": shares * signal,
                            "value": shares * price,
                            "commission": shares * price * commission,
                            "cash_flow": -shares * price - shares * price * commission
                        }
                        trades.append(trade)
                        cash += trade["cash_flow"]
                        position = shares * signal
                    else:
                        position = 0
                else:
                    position = 0
            
            # Calculate equity
            equity = cash + position * price
            self.equity_curve.append({
                "date": date,
                "equity": equity,
                "cash": cash,
                "position": position,
                "price": price
            })
        
        return trades
    
    def _calculate_metrics(self, trades: List[Dict[str, Any]], initial_capital: float) -> Dict[str, Any]:
        """Calculate performance metrics."""
        if not trades:
            return {"error": "No trades executed"}
        
        # Calculate returns
        equity_values = [ec["equity"] for ec in self.equity_curve]
        returns = pd.Series(equity_values).pct_change().dropna()
        
        # Basic metrics
        total_return = (equity_values[-1] - initial_capital) / initial_capital
        annualized_return = (1 + total_return) ** (252 / len(returns)) - 1
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annualized_return / volatility if volatility > 0 else 0
        
        # Drawdown
        peak = pd.Series(equity_values).expanding().max()
        drawdown = (pd.Series(equity_values) - peak) / peak
        max_drawdown = drawdown.min()
        
        # Trade metrics
        trade_returns = []
        for i in range(0, len(trades), 2):
            if i + 1 < len(trades):
                open_trade = trades[i]
                close_trade = trades[i + 1]
                trade_return = (close_trade["price"] - open_trade["price"]) / open_trade["price"]
                trade_returns.append(trade_return)
        
        win_rate = len([r for r in trade_returns if r > 0]) / len(trade_returns) if trade_returns else 0
        avg_win = np.mean([r for r in trade_returns if r > 0]) if any(r > 0 for r in trade_returns) else 0
        avg_loss = np.mean([r for r in trade_returns if r < 0]) if any(r < 0 for r in trade_returns) else 0
        
        return {
            "total_return": float(total_return),
            "annualized_return": float(annualized_return),
            "volatility": float(volatility),
            "sharpe_ratio": float(sharpe_ratio),
            "max_drawdown": float(max_drawdown),
            "calmar_ratio": float(annualized_return / abs(max_drawdown)) if max_drawdown != 0 else 0,
            "win_rate": float(win_rate),
            "avg_win": float(avg_win),
            "avg_loss": float(avg_loss),
            "profit_factor": float(abs(avg_win / avg_loss)) if avg_loss != 0 else 0,
            "total_trades": len(trades) // 2,
            "final_equity": float(equity_values[-1])
        }

