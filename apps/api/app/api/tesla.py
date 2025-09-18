from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import get_db
from app.models.tesla_metric import TeslaMetric

router = APIRouter()

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
