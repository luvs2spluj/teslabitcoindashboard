"""
Scenario analysis and game-theory modeling.
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import date, datetime
import structlog
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings

logger = structlog.get_logger()

class ScenarioAnalyzer:
    """Scenario analysis using regime detection and Monte Carlo simulation."""
    
    def __init__(self):
        self.regimes = {
            "bear": {"probability": 0.15, "expected_return_5y": -0.30, "expected_return_10y": -0.20, "expected_return_25y": 0.00},
            "sideways": {"probability": 0.25, "expected_return_5y": 0.00, "expected_return_10y": 0.05, "expected_return_25y": 0.10},
            "base": {"probability": 0.35, "expected_return_5y": 0.10, "expected_return_10y": 0.15, "expected_return_25y": 0.20},
            "bull": {"probability": 0.20, "expected_return_5y": 0.25, "expected_return_10y": 0.30, "expected_return_25y": 0.35},
            "hypergrowth": {"probability": 0.05, "expected_return_5y": 0.50, "expected_return_10y": 0.60, "expected_return_25y": 0.70}
        }
    
    def analyze(
        self, 
        price_data: List[Dict[str, Any]], 
        fundamental_data: List[Dict[str, Any]],
        benchmark_data: List[Dict[str, Any]],
        news_data: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run comprehensive scenario analysis."""
        
        try:
            # Convert to DataFrames
            prices_df = pd.DataFrame(price_data)
            fundamentals_df = pd.DataFrame(fundamental_data)
            benchmarks_df = pd.DataFrame(benchmark_data)
            
            # Prepare data
            prepared_data = self._prepare_data(prices_df, fundamentals_df, benchmarks_df)
            
            # Detect current regime
            current_regime = self._detect_regime(prepared_data)
            
            # Calculate regime probabilities
            regime_probabilities = self._calculate_regime_probabilities(prepared_data)
            
            # Run Monte Carlo simulation
            monte_carlo_results = self._monte_carlo_simulation(prepared_data, regime_probabilities)
            
            # Calculate expected returns
            expected_returns = self._calculate_expected_returns(regime_probabilities)
            
            return {
                "current_regime": current_regime,
                "regime_probabilities": regime_probabilities,
                "expected_returns": expected_returns,
                "monte_carlo": monte_carlo_results,
                "analysis_date": datetime.now().isoformat(),
                "data_points": {
                    "prices": len(price_data),
                    "fundamentals": len(fundamental_data),
                    "benchmarks": len(benchmark_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Scenario analysis failed: {e}")
            return {"error": str(e)}
    
    def _prepare_data(
        self, 
        prices_df: pd.DataFrame, 
        fundamentals_df: pd.DataFrame, 
        benchmarks_df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """Prepare data for analysis."""
        
        # Ensure date columns are datetime
        if not prices_df.empty:
            prices_df['date'] = pd.to_datetime(prices_df['date'])
            prices_df = prices_df.sort_values('date')
            
            # Calculate returns
            prices_df['returns'] = prices_df['close'].pct_change()
            prices_df['volatility'] = prices_df['returns'].rolling(window=20).std()
            prices_df['momentum'] = prices_df['close'] / prices_df['close'].shift(20) - 1
        
        if not fundamentals_df.empty:
            fundamentals_df['period_end'] = pd.to_datetime(fundamentals_df['period_end'])
            fundamentals_df = fundamentals_df.sort_values('period_end')
        
        if not benchmarks_df.empty:
            benchmarks_df['date'] = pd.to_datetime(benchmarks_df['date'])
            benchmarks_df = benchmarks_df.sort_values('date')
        
        return {
            "prices": prices_df,
            "fundamentals": fundamentals_df,
            "benchmarks": benchmarks_df
        }
    
    def _detect_regime(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Detect current market regime."""
        try:
            prices_df = data["prices"]
            
            if prices_df.empty:
                return {"regime": "unknown", "confidence": 0.0}
            
            # Get latest metrics
            latest = prices_df.iloc[-1]
            
            # Simple regime detection based on momentum and volatility
            momentum = latest.get('momentum', 0)
            volatility = latest.get('volatility', 0)
            
            # Regime classification
            if momentum < -0.2:
                regime = "bear"
                confidence = min(abs(momentum), 1.0)
            elif momentum > 0.3:
                regime = "hypergrowth"
                confidence = min(momentum, 1.0)
            elif momentum > 0.1:
                regime = "bull"
                confidence = min(momentum * 2, 1.0)
            elif abs(momentum) < 0.05:
                regime = "sideways"
                confidence = 1.0 - abs(momentum) * 10
            else:
                regime = "base"
                confidence = 0.5
            
            return {
                "regime": regime,
                "confidence": float(confidence),
                "momentum": float(momentum),
                "volatility": float(volatility)
            }
            
        except Exception as e:
            logger.error(f"Regime detection failed: {e}")
            return {"regime": "unknown", "confidence": 0.0, "error": str(e)}
    
    def _calculate_regime_probabilities(self, data: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """Calculate probabilities for each regime."""
        try:
            # Start with base probabilities
            probabilities = {regime: info["probability"] for regime, info in self.regimes.items()}
            
            # Adjust based on current data
            current_regime = self._detect_regime(data)
            
            if current_regime["regime"] != "unknown":
                # Increase probability of current regime
                current_regime_name = current_regime["regime"]
                confidence = current_regime["confidence"]
                
                # Adjust probabilities
                boost = confidence * 0.2  # Boost current regime by up to 20%
                probabilities[current_regime_name] += boost
                
                # Normalize probabilities
                total = sum(probabilities.values())
                probabilities = {k: v/total for k, v in probabilities.items()}
            
            return probabilities
            
        except Exception as e:
            logger.error(f"Regime probability calculation failed: {e}")
            return {regime: info["probability"] for regime, info in self.regimes.items()}
    
    def _monte_carlo_simulation(
        self, 
        data: Dict[str, pd.DataFrame], 
        regime_probabilities: Dict[str, float],
        n_simulations: int = 10000
    ) -> Dict[str, Any]:
        """Run Monte Carlo simulation for future returns."""
        try:
            prices_df = data["prices"]
            
            if prices_df.empty:
                return {"error": "No price data for Monte Carlo simulation"}
            
            # Get historical returns
            returns = prices_df['returns'].dropna()
            
            if len(returns) < 30:
                return {"error": "Insufficient historical data for simulation"}
            
            # Calculate historical statistics
            mean_return = returns.mean()
            std_return = returns.std()
            
            # Run simulations
            simulation_results = []
            
            for _ in range(n_simulations):
                # Select regime based on probabilities
                regime = np.random.choice(
                    list(regime_probabilities.keys()),
                    p=list(regime_probabilities.values())
                )
                
                # Get regime-specific parameters
                regime_info = self.regimes[regime]
                
                # Simulate returns for different time horizons
                simulated_returns = {}
                
                for horizon in [5, 10, 25]:
                    # Use regime-specific expected return
                    expected_return = regime_info[f"expected_return_{horizon}y"]
                    
                    # Add some randomness
                    random_component = np.random.normal(0, std_return * 0.5)
                    simulated_return = expected_return + random_component
                    
                    simulated_returns[f"{horizon}_year"] = simulated_return
                
                simulation_results.append({
                    "regime": regime,
                    "returns": simulated_returns
                })
            
            # Calculate percentiles
            percentiles = {}
            for horizon in [5, 10, 25]:
                horizon_returns = [r["returns"][f"{horizon}_year"] for r in simulation_results]
                
                percentiles[f"{horizon}_year"] = {
                    "5th": float(np.percentile(horizon_returns, 5)),
                    "10th": float(np.percentile(horizon_returns, 10)),
                    "25th": float(np.percentile(horizon_returns, 25)),
                    "50th": float(np.percentile(horizon_returns, 50)),
                    "75th": float(np.percentile(horizon_returns, 75)),
                    "90th": float(np.percentile(horizon_returns, 90)),
                    "95th": float(np.percentile(horizon_returns, 95))
                }
            
            return {
                "n_simulations": n_simulations,
                "percentiles": percentiles,
                "regime_distribution": {
                    regime: len([r for r in simulation_results if r["regime"] == regime]) / n_simulations
                    for regime in self.regimes.keys()
                }
            }
            
        except Exception as e:
            logger.error(f"Monte Carlo simulation failed: {e}")
            return {"error": str(e)}
    
    def _calculate_expected_returns(self, regime_probabilities: Dict[str, float]) -> Dict[str, float]:
        """Calculate expected returns based on regime probabilities."""
        expected_returns = {}
        
        for horizon in [5, 10, 25]:
            expected_return = sum(
                regime_probabilities[regime] * self.regimes[regime][f"expected_return_{horizon}y"]
                for regime in self.regimes.keys()
            )
            expected_returns[f"{horizon}_year"] = float(expected_return)
        
        return expected_returns

