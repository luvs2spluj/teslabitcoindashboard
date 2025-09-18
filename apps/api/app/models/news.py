from sqlalchemy import Column, Integer, DateTime, Text, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class News(Base):
    """News articles with sentiment analysis."""
    
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    published_at = Column(DateTime, nullable=False, index=True)
    source = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False)
    summary = Column(Text)
    sentiment = Column(Float)  # -1 to 1 sentiment score
    
    # Relationships
    ticker = relationship("Ticker", back_populates="news")
