from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import get_db
from app.models.benchmark import Benchmark

router = APIRouter()

@router.get("/")
async def get_benchmarks(
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    limit: int = Query(1000, ge=1, le=5000),
    db: Session = Depends(get_db)
):
    """Get market benchmarks and macro indicators."""
    query = db.query(Benchmark)
    
    if start:
        query = query.filter(Benchmark.date >= start)
    if end:
        query = query.filter(Benchmark.date <= end)
    
    benchmarks = query.order_by(Benchmark.date.desc()).limit(limit).all()
    
    return {
        "benchmarks": [
            {
                "date": benchmark.date,
                "spx": benchmark.spx,
                "gold": benchmark.gold,
                "ust_total_return": benchmark.ust_total_return,
                "cpi": benchmark.cpi,
                "real_yield": benchmark.real_yield,
                "source": benchmark.source
            }
            for benchmark in benchmarks
        ]
    }

@router.get("/latest")
async def get_latest_benchmarks(
    db: Session = Depends(get_db)
):
    """Get latest benchmark values."""
    latest_benchmark = db.query(Benchmark).order_by(
        Benchmark.date.desc()
    ).limit(1).first()
    
    if not latest_benchmark:
        raise HTTPException(status_code=404, detail="No benchmark data found")
    
    return {
        "date": latest_benchmark.date,
        "spx": latest_benchmark.spx,
        "gold": latest_benchmark.gold,
        "ust_total_return": latest_benchmark.ust_total_return,
        "cpi": latest_benchmark.cpi,
        "real_yield": latest_benchmark.real_yield,
        "source": latest_benchmark.source
    }
