"""
ETL job for loading Tesla-specific metrics.
"""
from typing import Dict, Any, List
from datetime import date, datetime
import structlog
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base import ETLJob
from app.models.tesla_metric import TeslaMetric

logger = structlog.get_logger()

class TeslaMetricsETL(ETLJob):
    """ETL job for Tesla metrics."""
    
    def __init__(self):
        super().__init__("load_tesla_metrics")
    
    async def extract(self, **kwargs) -> Dict[str, Any]:
        """Extract Tesla metrics data."""
        # For now, this is a placeholder that would extract from Tesla IR PDFs
        # In a real implementation, this would parse Tesla's quarterly reports
        
        # Mock data for demonstration
        mock_data = [
            {
                "date": date(2023, 12, 31),
                "vehicles_delivered": 484507,
                "asp_auto": 44000,
                "auto_gross_margin": 0.19,
                "energy_solar_mw": 66,
                "energy_storage_mwh": 2959,
                "asp_storage": 2800,
                "energy_gross_margin": 0.24,
                "notes": "Q4 2023 results",
                "source_url": "https://ir.tesla.com"
            }
        ]
        
        logger.info(f"Extracted {len(mock_data)} Tesla metric records")
        return {"metrics": mock_data}
    
    def transform(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform Tesla metrics data for loading."""
        transformed_records = []
        
        for metric in data["metrics"]:
            transformed_records.append({
                "date": metric["date"],
                "vehicles_delivered": metric["vehicles_delivered"],
                "asp_auto": metric["asp_auto"],
                "auto_gross_margin": metric["auto_gross_margin"],
                "energy_solar_mw": metric["energy_solar_mw"],
                "energy_storage_mwh": metric["energy_storage_mwh"],
                "asp_storage": metric["asp_storage"],
                "energy_gross_margin": metric["energy_gross_margin"],
                "notes": metric["notes"],
                "source_url": metric["source_url"]
            })
        
        return transformed_records
    
    def load(self, data: List[Dict[str, Any]]) -> int:
        """Load Tesla metrics data into database."""
        if not self.db:
            raise RuntimeError("Database session not initialized")
        
        loaded_count = 0
        
        for record in data:
            try:
                # Check if Tesla metric record already exists
                existing = self.db.query(TeslaMetric).filter(
                    TeslaMetric.date == record["date"]
                ).first()
                
                if existing:
                    # Update existing record
                    existing.vehicles_delivered = record["vehicles_delivered"]
                    existing.asp_auto = record["asp_auto"]
                    existing.auto_gross_margin = record["auto_gross_margin"]
                    existing.energy_solar_mw = record["energy_solar_mw"]
                    existing.energy_storage_mwh = record["energy_storage_mwh"]
                    existing.asp_storage = record["asp_storage"]
                    existing.energy_gross_margin = record["energy_gross_margin"]
                    existing.notes = record["notes"]
                    existing.source_url = record["source_url"]
                else:
                    # Create new record
                    metric = TeslaMetric(
                        date=record["date"],
                        vehicles_delivered=record["vehicles_delivered"],
                        asp_auto=record["asp_auto"],
                        auto_gross_margin=record["auto_gross_margin"],
                        energy_solar_mw=record["energy_solar_mw"],
                        energy_storage_mwh=record["energy_storage_mwh"],
                        asp_storage=record["asp_storage"],
                        energy_gross_margin=record["energy_gross_margin"],
                        notes=record["notes"],
                        source_url=record["source_url"]
                    )
                    self.db.add(metric)
                
                loaded_count += 1
                
            except Exception as e:
                logger.error(f"Failed to load Tesla metric record for {record['date']}: {e}")
                continue
        
        try:
            self.db.commit()
            logger.info(f"Successfully loaded {loaded_count} Tesla metric records")
        except Exception as e:
            logger.error(f"Failed to commit Tesla metrics data: {e}")
            self.db.rollback()
            raise
        
        return loaded_count

