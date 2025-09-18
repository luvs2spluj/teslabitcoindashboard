from sqlalchemy import Column, Integer, Float, Date, String
from app.database import Base

class Benchmark(Base):
    """Market benchmarks and macro indicators."""
    
    __tablename__ = "benchmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    spx = Column(Float)  # S&P 500
    gold = Column(Float)  # Gold price
    ust_total_return = Column(Float)  # US Treasury total return
    cpi = Column(Float)  # Consumer Price Index
    real_yield = Column(Float)  # Real yield (10Y Treasury - CPI)
    source = Column(String(50), default="fred")
