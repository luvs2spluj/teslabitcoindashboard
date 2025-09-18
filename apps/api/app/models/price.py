from sqlalchemy import Column, Integer, Float, Date, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class Price(Base):
    """Daily price data (TimescaleDB hypertable)."""
    
    __tablename__ = "prices_daily"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)
    source = Column(String(50), default="stooq")
    
    # Relationships
    ticker = relationship("Ticker", back_populates="prices")
    
    # Composite index for TimescaleDB
    __table_args__ = (
        {"postgresql_partition_by": "RANGE (date)"},
    )
