from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Ticker(Base):
    """Ticker symbol metadata."""
    
    __tablename__ = "tickers"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    sector = Column(String(100))
    currency = Column(String(3), default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Relationships
    prices = relationship("Price", back_populates="ticker")
    fundamentals = relationship("Fundamental", back_populates="ticker")
    news = relationship("News", back_populates="ticker")
    reddit_posts = relationship("RedditPost", back_populates="ticker")
    backtest_runs = relationship("BacktestRun", back_populates="ticker")
