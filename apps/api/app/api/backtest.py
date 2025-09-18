from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import date

from app.database import get_db
from app.models.strategy import Strategy
from app.models.backtest_run import BacktestRun
from app.models.ticker import Ticker
from app.strategies.backtest_engine import BacktestEngine

router = APIRouter()

class BacktestRequest(BaseModel):
    """Request model for running a backtest."""
    strategy_family: str
    symbol: str
    start_date: date
    end_date: date
    params: Dict[str, Any]
    initial_capital: float = 100000.0
    commission: float = 0.001

class BacktestResponse(BaseModel):
    """Response model for backtest results."""
    run_id: int
    status: str
    message: str

@router.post("/run", response_model=BacktestResponse)
async def run_backtest(
    request: BacktestRequest,
    db: Session = Depends(get_db)
):
    """Run a backtest for a given strategy."""
    # Validate ticker exists
    ticker = db.query(Ticker).filter(Ticker.symbol == request.symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    try:
        # Run backtest
        engine = BacktestEngine()
        result = engine.run_backtest(
            strategy_family=request.strategy_family,
            symbol=request.symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            params=request.params,
            initial_capital=request.initial_capital,
            commission=request.commission,
            db=db
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Save result to database
        run_id = engine.save_backtest_result(result, user_id="system", db=db)
        
        return BacktestResponse(
            run_id=run_id,
            status="completed",
            message="Backtest completed successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")

@router.get("/{run_id}")
async def get_backtest_results(
    run_id: int,
    db: Session = Depends(get_db)
):
    """Get backtest results by run ID."""
    backtest_run = db.query(BacktestRun).filter(BacktestRun.id == run_id).first()
    if not backtest_run:
        raise HTTPException(status_code=404, detail="Backtest run not found")
    
    # Get strategy and ticker info
    strategy = db.query(Strategy).filter(Strategy.id == backtest_run.strategy_id).first()
    ticker = db.query(Ticker).filter(Ticker.id == backtest_run.ticker_id).first()
    
    return {
        "run_id": backtest_run.id,
        "strategy": {
            "name": strategy.name if strategy else "Unknown",
            "family": strategy.family if strategy else "Unknown",
            "params": strategy.params_json if strategy else {}
        },
        "ticker": {
            "symbol": ticker.symbol if ticker else "Unknown",
            "name": ticker.name if ticker else "Unknown"
        },
        "period": {
            "start_date": backtest_run.start_date,
            "end_date": backtest_run.end_date
        },
        "metrics": backtest_run.metrics_json,
        "trades": backtest_run.trades_json,
        "equity_curve_url": backtest_run.equity_curve_url,
        "status": backtest_run.status,
        "created_at": backtest_run.created_at
    }
