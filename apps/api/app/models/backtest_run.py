from sqlalchemy import Column, Integer, Date, DateTime, String, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.database import Base

class BacktestRun(Base):
    """Backtest execution results."""
    
    __tablename__ = "backtest_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    metrics_json = Column(JSON, nullable=False)  # Performance metrics
    trades_json = Column(JSON)  # Individual trades
    equity_curve_url = Column(String(1000))  # URL to equity curve chart
    created_at = Column(DateTime, nullable=False)
    status = Column(String(50), default="completed")  # pending, running, completed, failed
    
    # Relationships
    strategy = relationship("Strategy", back_populates="backtest_runs")
    ticker = relationship("Ticker", back_populates="backtest_runs")
