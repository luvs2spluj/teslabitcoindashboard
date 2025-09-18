from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class Fundamental(Base):
    """Financial fundamentals data."""
    
    __tablename__ = "fundamentals"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    period_end = Column(Date, nullable=False)
    pe = Column(Float)
    eps = Column(Float)
    revenue = Column(Float)
    gross_margin = Column(Float)
    op_margin = Column(Float)
    fcf = Column(Float)
    shares_out = Column(Float)
    source = Column(String(50), default="sec")
    
    # Relationships
    ticker = relationship("Ticker", back_populates="fundamentals")
