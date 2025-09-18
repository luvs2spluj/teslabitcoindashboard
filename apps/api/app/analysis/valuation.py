"""
Valuation models and analysis.
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import date, datetime
import structlog
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings

logger = structlog.get_logger()

class ValuationAnalyzer:
    """Valuation analysis using multiple models."""
    
    def __init__(self):
        self.models = {
            "ols_regression": self._ols_regression,
            "dcf_lite": self._dcf_lite,
            "residual_income": self._residual_income,
            "pe_percentile": self._pe_percentile
        }
    
    def analyze(
        self, 
        price_data: List[Dict[str, Any]], 
        fundamental_data: List[Dict[str, Any]],
        benchmark_data: List[Dict[str, Any]],
        current_price: float
    ) -> Dict[str, Any]:
        """Run comprehensive valuation analysis."""
        
        try:
            # Convert to DataFrames
            prices_df = pd.DataFrame(price_data)
            fundamentals_df = pd.DataFrame(fundamental_data)
            benchmarks_df = pd.DataFrame(benchmark_data)
            
            # Prepare data
            prepared_data = self._prepare_data(prices_df, fundamentals_df, benchmarks_df)
            
            # Run valuation models
            results = {}
            
            for model_name, model_func in self.models.items():
                try:
                    result = model_func(prepared_data, current_price)
                    results[model_name] = result
                    logger.info(f"Valuation model {model_name} completed successfully")
                except Exception as e:
                    logger.error(f"Valuation model {model_name} failed: {e}")
                    results[model_name] = {"error": str(e)}
            
            # Calculate consensus
            consensus = self._calculate_consensus(results, current_price)
            
            return {
                "current_price": current_price,
                "models": results,
                "consensus": consensus,
                "analysis_date": datetime.now().isoformat(),
                "data_points": {
                    "prices": len(price_data),
                    "fundamentals": len(fundamental_data),
                    "benchmarks": len(benchmark_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Valuation analysis failed: {e}")
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
    
    def _ols_regression(self, data: Dict[str, pd.DataFrame], current_price: float) -> Dict[str, Any]:
        """OLS regression model for valuation."""
        try:
            prices_df = data["prices"]
            fundamentals_df = data["fundamentals"]
            
            if prices_df.empty or fundamentals_df.empty:
                return {"error": "Insufficient data for OLS regression"}
            
            # Calculate features
            features = []
            targets = []
            
            for _, price_row in prices_df.iterrows():
                # Find corresponding fundamental data
                fundamental_row = fundamentals_df[
                    fundamentals_df['period_end'] <= price_row['date']
                ].iloc[-1] if not fundamentals_df.empty else None
                
                if fundamental_row is not None:
                    feature_vector = [
                        fundamental_row.get('revenue', 0),
                        fundamental_row.get('eps', 0),
                        fundamental_row.get('gross_margin', 0),
                        price_row['close']
                    ]
                    features.append(feature_vector)
                    targets.append(price_row['close'])
            
            if len(features) < 10:  # Need minimum data points
                return {"error": "Insufficient data points for OLS regression"}
            
            # Fit model
            X = np.array(features)
            y = np.array(targets)
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict current value
            latest_fundamental = fundamentals_df.iloc[-1]
            current_features = [
                latest_fundamental.get('revenue', 0),
                latest_fundamental.get('eps', 0),
                latest_fundamental.get('gross_margin', 0),
                current_price
            ]
            
            predicted_price = model.predict([current_features])[0]
            
            return {
                "model_type": "OLS Regression",
                "predicted_price": float(predicted_price),
                "upside_downside": float((predicted_price - current_price) / current_price),
                "r_squared": float(model.score(X, y)),
                "coefficients": model.coef_.tolist(),
                "intercept": float(model.intercept_)
            }
            
        except Exception as e:
            return {"error": f"OLS regression failed: {str(e)}"}
    
    def _dcf_lite(self, data: Dict[str, pd.DataFrame], current_price: float) -> Dict[str, Any]:
        """Simplified DCF model."""
        try:
            fundamentals_df = data["fundamentals"]
            
            if fundamentals_df.empty:
                return {"error": "No fundamental data for DCF"}
            
            latest = fundamentals_df.iloc[-1]
            
            # Get key metrics
            revenue = latest.get('revenue', 0)
            fcf = latest.get('fcf', 0)
            shares_out = latest.get('shares_out', 0)
            
            if revenue == 0 or shares_out == 0:
                return {"error": "Missing key metrics for DCF"}
            
            # Assumptions
            growth_rate = 0.15  # 15% growth assumption
            discount_rate = 0.10  # 10% discount rate
            terminal_growth = 0.03  # 3% terminal growth
            
            # Project cash flows
            years = 10
            projected_fcf = []
            current_fcf = fcf
            
            for year in range(years):
                current_fcf *= (1 + growth_rate)
                projected_fcf.append(current_fcf)
            
            # Calculate present value
            pv_cash_flows = []
            for i, cf in enumerate(projected_fcf):
                pv = cf / ((1 + discount_rate) ** (i + 1))
                pv_cash_flows.append(pv)
            
            # Terminal value
            terminal_value = (current_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
            pv_terminal = terminal_value / ((1 + discount_rate) ** years)
            
            # Enterprise value
            enterprise_value = sum(pv_cash_flows) + pv_terminal
            
            # Equity value per share
            equity_value_per_share = enterprise_value / shares_out
            
            return {
                "model_type": "DCF Lite",
                "predicted_price": float(equity_value_per_share),
                "upside_downside": float((equity_value_per_share - current_price) / current_price),
                "enterprise_value": float(enterprise_value),
                "terminal_value": float(pv_terminal),
                "assumptions": {
                    "growth_rate": growth_rate,
                    "discount_rate": discount_rate,
                    "terminal_growth": terminal_growth
                }
            }
            
        except Exception as e:
            return {"error": f"DCF Lite failed: {str(e)}"}
    
    def _residual_income(self, data: Dict[str, pd.DataFrame], current_price: float) -> Dict[str, Any]:
        """Residual Income model."""
        try:
            fundamentals_df = data["fundamentals"]
            
            if fundamentals_df.empty:
                return {"error": "No fundamental data for Residual Income"}
            
            latest = fundamentals_df.iloc[-1]
            
            # Get key metrics
            eps = latest.get('eps', 0)
            shares_out = latest.get('shares_out', 0)
            revenue = latest.get('revenue', 0)
            
            if eps == 0 or shares_out == 0:
                return {"error": "Missing key metrics for Residual Income"}
            
            # Assumptions
            required_return = 0.10  # 10% required return
            growth_rate = 0.05  # 5% growth rate
            
            # Book value per share (simplified)
            book_value_per_share = revenue / shares_out * 0.1  # Assume 10% of revenue is equity
            
            # Residual income
            residual_income = eps - (book_value_per_share * required_return)
            
            # Project residual income
            years = 10
            projected_ri = []
            current_ri = residual_income
            
            for year in range(years):
                current_ri *= (1 + growth_rate)
                projected_ri.append(current_ri)
            
            # Present value of residual income
            pv_ri = sum(ri / ((1 + required_return) ** (i + 1)) for i, ri in enumerate(projected_ri))
            
            # Terminal value
            terminal_ri = current_ri * (1 + growth_rate) / (required_return - growth_rate)
            pv_terminal_ri = terminal_ri / ((1 + required_return) ** years)
            
            # Total residual income value
            total_ri_value = pv_ri + pv_terminal_ri
            
            # Equity value per share
            equity_value_per_share = book_value_per_share + total_ri_value
            
            return {
                "model_type": "Residual Income",
                "predicted_price": float(equity_value_per_share),
                "upside_downside": float((equity_value_per_share - current_price) / current_price),
                "book_value_per_share": float(book_value_per_share),
                "residual_income_value": float(total_ri_value),
                "assumptions": {
                    "required_return": required_return,
                    "growth_rate": growth_rate
                }
            }
            
        except Exception as e:
            return {"error": f"Residual Income failed: {str(e)}"}
    
    def _pe_percentile(self, data: Dict[str, pd.DataFrame], current_price: float) -> Dict[str, Any]:
        """PE ratio percentile analysis."""
        try:
            fundamentals_df = data["fundamentals"]
            
            if fundamentals_df.empty:
                return {"error": "No fundamental data for PE analysis"}
            
            # Get PE ratios
            pe_ratios = fundamentals_df['pe'].dropna()
            
            if len(pe_ratios) < 5:
                return {"error": "Insufficient PE data for percentile analysis"}
            
            # Current PE
            latest_pe = pe_ratios.iloc[-1]
            
            # Calculate percentiles
            percentiles = {
                "10th": float(np.percentile(pe_ratios, 10)),
                "25th": float(np.percentile(pe_ratios, 25)),
                "50th": float(np.percentile(pe_ratios, 50)),
                "75th": float(np.percentile(pe_ratios, 75)),
                "90th": float(np.percentile(pe_ratios, 90))
            }
            
            # Current percentile
            current_percentile = float(stats.percentileofscore(pe_ratios, latest_pe))
            
            # Valuation based on median PE
            median_pe = percentiles["50th"]
            latest_eps = fundamentals_df.iloc[-1].get('eps', 0)
            
            if latest_eps > 0:
                fair_value = median_pe * latest_eps
            else:
                fair_value = current_price
            
            return {
                "model_type": "PE Percentile",
                "predicted_price": float(fair_value),
                "upside_downside": float((fair_value - current_price) / current_price),
                "current_pe": float(latest_pe),
                "current_percentile": current_percentile,
                "percentiles": percentiles,
                "median_pe": median_pe
            }
            
        except Exception as e:
            return {"error": f"PE Percentile failed: {str(e)}"}
    
    def _calculate_consensus(self, results: Dict[str, Any], current_price: float) -> Dict[str, Any]:
        """Calculate consensus valuation."""
        valid_results = [r for r in results.values() if "error" not in r and "predicted_price" in r]
        
        if not valid_results:
            return {"error": "No valid valuation models"}
        
        predicted_prices = [r["predicted_price"] for r in valid_results]
        
        consensus_price = np.mean(predicted_prices)
        consensus_upside = (consensus_price - current_price) / current_price
        
        return {
            "consensus_price": float(consensus_price),
            "consensus_upside_downside": float(consensus_upside),
            "price_range": {
                "min": float(np.min(predicted_prices)),
                "max": float(np.max(predicted_prices))
            },
            "models_count": len(valid_results),
            "confidence": "medium" if len(valid_results) >= 3 else "low"
        }

