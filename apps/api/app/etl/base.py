"""
Base ETL functionality and common utilities.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import structlog
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.config import settings

logger = structlog.get_logger()

class ETLJob(ABC):
    """Base class for ETL jobs."""
    
    def __init__(self, name: str):
        self.name = name
        self.db: Optional[Session] = None
    
    def __enter__(self):
        """Context manager entry."""
        self.db = SessionLocal()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.db:
            self.db.close()
    
    @abstractmethod
    async def extract(self, **kwargs) -> Dict[str, Any]:
        """Extract data from source."""
        pass
    
    @abstractmethod
    def transform(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform data for loading."""
        pass
    
    @abstractmethod
    def load(self, data: List[Dict[str, Any]]) -> int:
        """Load data into database."""
        pass
    
    async def run(self, **kwargs) -> Dict[str, Any]:
        """Run the complete ETL process."""
        start_time = datetime.now()
        
        try:
            logger.info(f"Starting ETL job: {self.name}")
            
            # Extract
            raw_data = await self.extract(**kwargs)
            logger.info(f"Extracted {len(raw_data.get('data', []))} records")
            
            # Transform
            transformed_data = self.transform(raw_data)
            logger.info(f"Transformed {len(transformed_data)} records")
            
            # Load
            loaded_count = self.load(transformed_data)
            logger.info(f"Loaded {loaded_count} records")
            
            duration = datetime.now() - start_time
            
            return {
                "job_name": self.name,
                "status": "success",
                "extracted": len(raw_data.get('data', [])),
                "transformed": len(transformed_data),
                "loaded": loaded_count,
                "duration_seconds": duration.total_seconds(),
                "timestamp": start_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"ETL job {self.name} failed: {e}")
            duration = datetime.now() - start_time
            
            return {
                "job_name": self.name,
                "status": "failed",
                "error": str(e),
                "duration_seconds": duration.total_seconds(),
                "timestamp": start_time.isoformat()
            }
    
    def get_last_update(self, table_name: str) -> Optional[datetime]:
        """Get the last update timestamp for a table."""
        # This would be implemented based on your specific needs
        # For now, return None to always fetch all data
        return None
    
    def should_run(self, force: bool = False) -> bool:
        """Determine if the ETL job should run."""
        if force:
            return True
        
        # Add logic to check if job should run based on schedule, last run, etc.
        return True

