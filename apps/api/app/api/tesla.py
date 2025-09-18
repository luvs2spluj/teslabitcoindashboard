from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, timedelta

from app.database import get_db
from app.models.tesla_metric import TeslaMetric
from app.datasources.bgeometrics import BGeometricsDataSource
from app.datasources.stooq import StooqDataSource
from app.datasources.ycharts import YChartsDataSource

router = APIRouter()

# Initialize data sources
bgeometrics = BGeometricsDataSource()
stooq = StooqDataSource()
ycharts = YChartsDataSource()

@router.get("/metrics")
async def get_tesla_metrics(
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get Tesla business metrics."""
    query = db.query(TeslaMetric)
    
    if start:
        query = query.filter(TeslaMetric.date >= start)
    if end:
        query = query.filter(TeslaMetric.date <= end)
    
    metrics = query.order_by(TeslaMetric.date.desc()).limit(limit).all()
    
    return {
        "metrics": [
            {
                "date": metric.date,
                "vehicles_delivered": metric.vehicles_delivered,
                "asp_auto": metric.asp_auto,
                "auto_gross_margin": metric.auto_gross_margin,
                "energy_solar_mw": metric.energy_solar_mw,
                "energy_storage_mwh": metric.energy_storage_mwh,
                "asp_storage": metric.asp_storage,
                "energy_gross_margin": metric.energy_gross_margin,
                "notes": metric.notes,
                "source_url": metric.source_url
            }
            for metric in metrics
        ]
    }

@router.get("/dashboard")
async def get_tesla_dashboard(
    db: Session = Depends(get_db)
):
    """Get Tesla dashboard summary."""
    # Get latest metrics
    latest_metrics = db.query(TeslaMetric).order_by(
        TeslaMetric.date.desc()
    ).limit(1).first()
    
    # Get quarterly delivery data for chart
    delivery_data = db.query(TeslaMetric).filter(
        TeslaMetric.vehicles_delivered.isnot(None)
    ).order_by(TeslaMetric.date.desc()).limit(20).all()
    
    # Get margin data
    margin_data = db.query(TeslaMetric).filter(
        TeslaMetric.auto_gross_margin.isnot(None)
    ).order_by(TeslaMetric.date.desc()).limit(20).all()
    
    return {
        "latest_metrics": {
            "date": latest_metrics.date if latest_metrics else None,
            "vehicles_delivered": latest_metrics.vehicles_delivered if latest_metrics else None,
            "asp_auto": latest_metrics.asp_auto if latest_metrics else None,
            "auto_gross_margin": latest_metrics.auto_gross_margin if latest_metrics else None,
            "energy_solar_mw": latest_metrics.energy_solar_mw if latest_metrics else None,
            "energy_storage_mwh": latest_metrics.energy_storage_mwh if latest_metrics else None,
            "energy_gross_margin": latest_metrics.energy_gross_margin if latest_metrics else None
        } if latest_metrics else None,
        "delivery_trend": [
            {
                "date": metric.date,
                "vehicles_delivered": metric.vehicles_delivered
            }
            for metric in delivery_data
        ],
        "margin_trend": [
            {
                "date": metric.date,
                "auto_gross_margin": metric.auto_gross_margin,
                "energy_gross_margin": metric.energy_gross_margin
            }
            for metric in margin_data
        ]
    }

@router.get("/stock-data")
async def get_tesla_stock_data(
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    days: int = Query(30, ge=1, le=365, description="Number of days of data")
):
    """Get live Tesla stock data from BGeometrics with yfinance fallback."""
    try:
        # Set default date range if not provided
        if not end:
            end = date.today()
        if not start:
            start = end - timedelta(days=days)
        
        # Try BGeometrics first (primary source for Tesla)
        try:
            result = await bgeometrics.fetch_data('TSLA', start, end)
            
            if result and result.get('data'):
                return {
                    "success": True,
                    "data": result,
                    "source": "bgeometrics",
                    "message": "Tesla data fetched from BGeometrics API"
                }
        except Exception as e:
            print(f"BGeometrics failed: {e}")
        
        # Fallback to Stooq
        try:
            result = await stooq.fetch_data('TSLA', start, end)
            
            if result and result.get('data'):
                return {
                    "success": True,
                    "data": result,
                    "source": "stooq",
                    "message": "Tesla data fetched from Stooq (fallback)"
                }
        except Exception as e:
            print(f"Stooq fallback failed: {e}")
        
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch Tesla stock data from any source"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Tesla stock data: {str(e)}"
        )

@router.get("/latest-price")
async def get_tesla_latest_price():
    """Get the latest Tesla stock price."""
    try:
        # Try BGeometrics first
        try:
            result = bgeometrics.get_latest_price('TSLA')
            
            if result['success']:
                return {
                    "success": True,
                    "data": result['data'],
                    "source": "bgeometrics",
                    "message": "Latest Tesla price from BGeometrics"
                }
        except Exception as e:
            print(f"BGeometrics latest price failed: {e}")
        
        # Fallback to Stooq
        try:
            result = stooq.get_latest_price('TSLA')
            
            if result['success']:
                return {
                    "success": True,
                    "data": result['data'],
                    "source": "stooq",
                    "message": "Latest Tesla price from Stooq (fallback)"
                }
        except Exception as e:
            print(f"Stooq latest price failed: {e}")
        
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch latest Tesla price from any source"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching latest Tesla price: {str(e)}"
        )

@router.get("/deliveries")
async def get_tesla_deliveries():
    """Get Tesla delivery data from YCharts."""
    try:
        result = await ycharts.fetch_tesla_deliveries()
        
        if result['success']:
            return {
                "success": True,
                "data": result['data'],
                "source": "ycharts",
                "message": "Tesla delivery data from YCharts"
            }
        else:
            raise HTTPException(
                status_code=503,
                detail=f"Unable to fetch Tesla delivery data: {result['error']}"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Tesla delivery data: {str(e)}"
        )
