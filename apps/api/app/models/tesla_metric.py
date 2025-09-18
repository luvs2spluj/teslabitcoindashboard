from sqlalchemy import Column, Integer, Float, Date, String, Text
from app.database import Base

class TeslaMetric(Base):
    """Tesla-specific business metrics."""
    
    __tablename__ = "tesla_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    vehicles_delivered = Column(Float)
    asp_auto = Column(Float)  # Average selling price automotive
    auto_gross_margin = Column(Float)
    energy_solar_mw = Column(Float)  # Solar capacity in MW
    energy_storage_mwh = Column(Float)  # Storage capacity in MWh
    asp_storage = Column(Float)  # Average selling price storage
    energy_gross_margin = Column(Float)
    notes = Column(Text)
    source_url = Column(String(1000))
