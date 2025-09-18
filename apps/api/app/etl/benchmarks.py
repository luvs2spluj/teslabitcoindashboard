"""
ETL job for loading benchmark data from FRED.
"""
from typing import Dict, Any, List
from datetime import date, timedelta
import structlog
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base import ETLJob
from app.datasources.fred import FREDDataSource
from app.models.benchmark import Benchmark

logger = structlog.get_logger()

class BenchmarksETL(ETLJob):
    """ETL job for benchmark data."""
    
    def __init__(self):
        super().__init__("load_benchmarks")
        self.series_mapping = {
            "SP500": "SP500",  # S&P 500
            "GOLD": "GOLDAMGBD228NLBM",  # Gold price
            "DGS10": "DGS10",  # 10-Year Treasury Rate
            "CPIAUCSL": "CPIAUCSL",  # Consumer Price Index
        }
    
    async def extract(self, **kwargs) -> Dict[str, Any]:
        """Extract benchmark data from FRED."""
        async with FREDDataSource() as fred:
            try:
                # Get last 30 days of data
                end_date = date.today()
                start_date = end_date - timedelta(days=30)
                
                benchmarks_data = await fred.fetch_benchmarks(
                    start_date=start_date,
                    end_date=end_date
                )
                
                logger.info(f"Extracted benchmark data for {len(benchmarks_data)} series")
                return {"benchmarks": benchmarks_data}
                
            except Exception as e:
                logger.error(f"Failed to extract benchmark data: {e}")
                return {"benchmarks": {}, "error": str(e)}
    
    def transform(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform benchmark data for loading."""
        if "error" in data:
            return []
        
        transformed_records = []
        
        # Create a date-indexed dictionary to combine all series
        date_data = {}
        
        for series_name, series_data in data["benchmarks"].items():
            if "error" in series_data:
                continue
                
            for record in series_data["data"]:
                date_key = record["date"]
                if date_key not in date_data:
                    date_data[date_key] = {"date": date_key}
                
                # Map series names to database columns
                if series_name == "SP500":
                    date_data[date_key]["spx"] = record["value"]
                elif series_name == "GOLD":
                    date_data[date_key]["gold"] = record["value"]
                elif series_name == "DGS10":
                    date_data[date_key]["ust_total_return"] = record["value"]
                elif series_name == "CPIAUCSL":
                    date_data[date_key]["cpi"] = record["value"]
        
        # Convert to list of records
        for date_record in date_data.values():
            transformed_records.append({
                "date": date_record["date"],
                "spx": date_record.get("spx"),
                "gold": date_record.get("gold"),
                "ust_total_return": date_record.get("ust_total_return"),
                "cpi": date_record.get("cpi"),
                "real_yield": None,  # Calculate separately
                "source": "fred"
            })
        
        return transformed_records
    
    def load(self, data: List[Dict[str, Any]]) -> int:
        """Load benchmark data into database."""
        if not self.db:
            raise RuntimeError("Database session not initialized")
        
        loaded_count = 0
        
        for record in data:
            try:
                # Check if benchmark record already exists
                existing = self.db.query(Benchmark).filter(
                    Benchmark.date == record["date"]
                ).first()
                
                if existing:
                    # Update existing record
                    if record["spx"] is not None:
                        existing.spx = record["spx"]
                    if record["gold"] is not None:
                        existing.gold = record["gold"]
                    if record["ust_total_return"] is not None:
                        existing.ust_total_return = record["ust_total_return"]
                    if record["cpi"] is not None:
                        existing.cpi = record["cpi"]
                    existing.source = record["source"]
                else:
                    # Create new record
                    benchmark = Benchmark(
                        date=record["date"],
                        spx=record["spx"],
                        gold=record["gold"],
                        ust_total_return=record["ust_total_return"],
                        cpi=record["cpi"],
                        real_yield=record["real_yield"],
                        source=record["source"]
                    )
                    self.db.add(benchmark)
                
                loaded_count += 1
                
            except Exception as e:
                logger.error(f"Failed to load benchmark record for {record['date']}: {e}")
                continue
        
        try:
            self.db.commit()
            logger.info(f"Successfully loaded {loaded_count} benchmark records")
        except Exception as e:
            logger.error(f"Failed to commit benchmark data: {e}")
            self.db.rollback()
            raise
        
        return loaded_count

