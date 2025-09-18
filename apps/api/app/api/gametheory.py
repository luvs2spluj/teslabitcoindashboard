from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import date, timedelta

from app.database import get_db
from app.models.ticker import Ticker
from app.models.price import Price
from app.models.fundamental import Fundamental
from app.models.benchmark import Benchmark
from app.analysis.scenarios import ScenarioAnalyzer

router = APIRouter()

@router.get("/{symbol}/scenarios")
async def get_scenario_analysis(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Get game-theory scenario analysis for a ticker."""
    ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    try:
        # Get data for analysis
        end_date = date.today()
        start_date = end_date - timedelta(days=365*2)  # 2 years of data
        
        # Get price data
        prices = db.query(Price).filter(
            Price.ticker_id == ticker.id,
            Price.date >= start_date,
            Price.date <= end_date
        ).order_by(Price.date).all()
        
        # Get fundamental data
        fundamentals = db.query(Fundamental).filter(
            Fundamental.ticker_id == ticker.id,
            Fundamental.period_end >= start_date
        ).order_by(Fundamental.period_end).all()
        
        # Get benchmark data
        benchmarks = db.query(Benchmark).filter(
            Benchmark.date >= start_date,
            Benchmark.date <= end_date
        ).order_by(Benchmark.date).all()
        
        # Convert to dictionaries
        price_data = [
            {
                "date": p.date,
                "open": p.open,
                "high": p.high,
                "low": p.low,
                "close": p.close,
                "volume": p.volume
            }
            for p in prices
        ]
        
        fundamental_data = [
            {
                "period_end": f.period_end,
                "pe": f.pe,
                "eps": f.eps,
                "revenue": f.revenue,
                "gross_margin": f.gross_margin,
                "op_margin": f.op_margin,
                "fcf": f.fcf,
                "shares_out": f.shares_out
            }
            for f in fundamentals
        ]
        
        benchmark_data = [
            {
                "date": b.date,
                "spx": b.spx,
                "gold": b.gold,
                "ust_total_return": b.ust_total_return,
                "cpi": b.cpi,
                "real_yield": b.real_yield
            }
            for b in benchmarks
        ]
        
        # Run scenario analysis
        analyzer = ScenarioAnalyzer()
        result = analyzer.analyze(price_data, fundamental_data, benchmark_data)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "symbol": symbol.upper(),
            "scenarios": result["regime_probabilities"],
            "expected_returns": result["expected_returns"],
            "current_regime": result["current_regime"],
            "monte_carlo": result["monte_carlo"],
            "analysis_date": result["analysis_date"],
            "methodology": "Monte Carlo simulation with regime detection"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario analysis failed: {str(e)}")
