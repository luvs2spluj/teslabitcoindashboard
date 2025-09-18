from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Strategy(Base):
    """User-defined trading strategies."""
    
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100))  # Supabase user ID
    name = Column(String(255), nullable=False)
    family = Column(String(100), nullable=False)  # e.g., "sma_cross", "macd_rsi"
    params_json = Column(JSON, nullable=False)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Relationships
    backtest_runs = relationship("BacktestRun", back_populates="strategy")
