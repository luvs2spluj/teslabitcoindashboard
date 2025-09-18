from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, timedelta

from app.database import get_db
from app.datasources.bitcoin_data import BitcoinDataSource

router = APIRouter()

# Initialize Bitcoin data source
bitcoin_source = BitcoinDataSource()

@router.get("/price")
async def get_bitcoin_price(
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    days: int = Query(30, ge=1, le=365, description="Number of days of data")
):
    """Get Bitcoin price data from BGeometrics."""
    try:
        # Set default date range if not provided
        if not end:
            end = date.today()
        if not start:
            start = end - timedelta(days=days)
        
        result = await bitcoin_source.fetch_price_data(start, end)
        
        return {
            "success": True,
            "data": result,
            "source": "bgeometrics_bitcoin",
            "message": "Bitcoin price data from BGeometrics API"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Bitcoin price data: {str(e)}"
        )

@router.get("/comprehensive-metrics")
async def get_bitcoin_comprehensive_metrics(
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    days: int = Query(365, ge=1, le=365, description="Number of days of data")
):
    """Get comprehensive Bitcoin on-chain metrics from BGeometrics."""
    try:
        # Set default date range if not provided
        if not end:
            end = date.today()
        if not start:
            start = end - timedelta(days=days)
        
        result = await bitcoin_source.fetch_comprehensive_metrics(start, end)
        
        return {
            "success": True,
            "data": result,
            "source": "bgeometrics_comprehensive",
            "message": "Comprehensive Bitcoin metrics from BGeometrics API"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Bitcoin comprehensive metrics: {str(e)}"
        )

@router.get("/derivatives")
async def get_bitcoin_derivatives(
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    days: int = Query(30, ge=1, le=90, description="Number of days of data")
):
    """Get Bitcoin derivatives data (Basis, Open Interest, Funding Rate)."""
    try:
        # Set default date range if not provided
        if not end:
            end = date.today()
        if not start:
            start = end - timedelta(days=days)
        
        result = await bitcoin_source.fetch_derivatives_data(start, end)
        
        return {
            "success": True,
            "data": result,
            "source": "bgeometrics_derivatives",
            "message": "Bitcoin derivatives data from BGeometrics API"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Bitcoin derivatives data: {str(e)}"
        )

@router.get("/technical-indicators")
async def get_bitcoin_technical_indicators(
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    days: int = Query(365, ge=1, le=365, description="Number of days of data")
):
    """Get Bitcoin technical indicators (RSI, MACD, SMA, EMA)."""
    try:
        # Set default date range if not provided
        if not end:
            end = date.today()
        if not start:
            start = end - timedelta(days=days)
        
        result = await bitcoin_source.fetch_technical_indicators(start, end)
        
        return {
            "success": True,
            "data": result,
            "source": "bgeometrics_technical",
            "message": "Bitcoin technical indicators from BGeometrics API"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Bitcoin technical indicators: {str(e)}"
        )

@router.get("/cycle-analysis")
async def get_bitcoin_cycle_analysis():
    """Get Bitcoin cycle analysis data."""
    try:
        result = await bitcoin_source.fetch_cycle_data()
        
        return {
            "success": True,
            "data": result,
            "source": "bgeometrics_cycle",
            "message": "Bitcoin cycle analysis from BGeometrics API"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Bitcoin cycle analysis: {str(e)}"
        )

@router.get("/sentiment")
async def get_bitcoin_sentiment():
    """Get Bitcoin sentiment indicators."""
    try:
        result = await bitcoin_source.fetch_sentiment_data()
        
        return {
            "success": True,
            "data": result,
            "source": "bgeometrics_sentiment",
            "message": "Bitcoin sentiment data from BGeometrics API"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Bitcoin sentiment data: {str(e)}"
        )

@router.get("/dashboard")
async def get_bitcoin_dashboard():
    """Get comprehensive Bitcoin dashboard data."""
    try:
        # Get data for the last 30 days
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        # Fetch multiple data sources in parallel
        price_data = await bitcoin_source.fetch_price_data(start_date, end_date)
        comprehensive_metrics = await bitcoin_source.fetch_comprehensive_metrics(start_date, end_date)
        derivatives_data = await bitcoin_source.fetch_derivatives_data(start_date, end_date)
        technical_indicators = await bitcoin_source.fetch_technical_indicators(start_date, end_date)
        
        return {
            "success": True,
            "data": {
                "price": price_data,
                "comprehensive_metrics": comprehensive_metrics,
                "derivatives": derivatives_data,
                "technical_indicators": technical_indicators,
                "date_range": {
                    "start": start_date,
                    "end": end_date
                }
            },
            "source": "bgeometrics_dashboard",
            "message": "Comprehensive Bitcoin dashboard data from BGeometrics API"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Bitcoin dashboard data: {str(e)}"
        )
