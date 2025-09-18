from sqlalchemy import Column, Integer, DateTime, Text, String, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from app.database import Base

class RedditPost(Base):
    """Reddit posts and comments with sentiment."""
    
    __tablename__ = "reddit"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    created_utc = Column(DateTime, nullable=False, index=True)
    subreddit = Column(String(100), nullable=False)
    author = Column(String(100))
    score = Column(BigInteger, default=0)
    permalink = Column(String(500), nullable=False)
    title = Column(String(500))
    body = Column(Text)
    sentiment = Column(Float)  # -1 to 1 sentiment score
    
    # Relationships
    ticker = relationship("Ticker", back_populates="reddit_posts")
