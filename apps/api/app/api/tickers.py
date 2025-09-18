from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.ticker import Ticker
from app.models.price import Price
from app.models.fundamental import Fundamental
from app.models.news import News
from app.models.reddit import RedditPost

router = APIRouter()

@router.get("/search")
async def search_tickers(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search for tickers by symbol or name."""
    tickers = db.query(Ticker).filter(
        (Ticker.symbol.ilike(f"%{q}%")) | 
        (Ticker.name.ilike(f"%{q}%"))
    ).limit(limit).all()
    
    return {
        "tickers": [
            {
                "id": ticker.id,
                "symbol": ticker.symbol,
                "name": ticker.name,
                "sector": ticker.sector,
                "currency": ticker.currency
            }
            for ticker in tickers
        ]
    }

@router.get("/{symbol}/overview")
async def get_ticker_overview(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Get ticker overview with latest data."""
    ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    # Get latest price
    latest_price = db.query(Price).filter(
        Price.ticker_id == ticker.id
    ).order_by(Price.date.desc()).first()
    
    # Get latest fundamentals
    latest_fundamental = db.query(Fundamental).filter(
        Fundamental.ticker_id == ticker.id
    ).order_by(Fundamental.period_end.desc()).first()
    
    return {
        "ticker": {
            "id": ticker.id,
            "symbol": ticker.symbol,
            "name": ticker.name,
            "sector": ticker.sector,
            "currency": ticker.currency
        },
        "latest_price": {
            "date": latest_price.date if latest_price else None,
            "close": latest_price.close if latest_price else None,
            "volume": latest_price.volume if latest_price else None
        } if latest_price else None,
        "latest_fundamental": {
            "period_end": latest_fundamental.period_end if latest_fundamental else None,
            "pe": latest_fundamental.pe if latest_fundamental else None,
            "eps": latest_fundamental.eps if latest_fundamental else None,
            "revenue": latest_fundamental.revenue if latest_fundamental else None
        } if latest_fundamental else None
    }

@router.get("/{symbol}/prices")
async def get_ticker_prices(
    symbol: str,
    tf: str = Query("1d", description="Time frame"),
    start: Optional[date] = Query(None, description="Start date"),
    end: Optional[date] = Query(None, description="End date"),
    limit: int = Query(1000, ge=1, le=5000),
    db: Session = Depends(get_db)
):
    """Get ticker price data."""
    ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    query = db.query(Price).filter(Price.ticker_id == ticker.id)
    
    if start:
        query = query.filter(Price.date >= start)
    if end:
        query = query.filter(Price.date <= end)
    
    prices = query.order_by(Price.date.desc()).limit(limit).all()
    
    return {
        "symbol": symbol.upper(),
        "timeframe": tf,
        "prices": [
            {
                "date": price.date,
                "open": price.open,
                "high": price.high,
                "low": price.low,
                "close": price.close,
                "volume": price.volume
            }
            for price in prices
        ]
    }

@router.get("/{symbol}/fundamentals")
async def get_ticker_fundamentals(
    symbol: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get ticker fundamentals data."""
    ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    fundamentals = db.query(Fundamental).filter(
        Fundamental.ticker_id == ticker.id
    ).order_by(Fundamental.period_end.desc()).limit(limit).all()
    
    return {
        "symbol": symbol.upper(),
        "fundamentals": [
            {
                "period_end": fundamental.period_end,
                "pe": fundamental.pe,
                "eps": fundamental.eps,
                "revenue": fundamental.revenue,
                "gross_margin": fundamental.gross_margin,
                "op_margin": fundamental.op_margin,
                "fcf": fundamental.fcf,
                "shares_out": fundamental.shares_out
            }
            for fundamental in fundamentals
        ]
    }

@router.get("/{symbol}/news")
async def get_ticker_news(
    symbol: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get ticker news with sentiment."""
    ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    news = db.query(News).filter(
        News.ticker_id == ticker.id
    ).order_by(News.published_at.desc()).limit(limit).all()
    
    return {
        "symbol": symbol.upper(),
        "news": [
            {
                "published_at": news_item.published_at,
                "source": news_item.source,
                "title": news_item.title,
                "url": news_item.url,
                "summary": news_item.summary,
                "sentiment": news_item.sentiment
            }
            for news_item in news
        ]
    }

@router.get("/{symbol}/reddit")
async def get_ticker_reddit(
    symbol: str,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get ticker Reddit posts with sentiment."""
    ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    reddit_posts = db.query(RedditPost).filter(
        RedditPost.ticker_id == ticker.id
    ).order_by(RedditPost.created_utc.desc()).limit(limit).all()
    
    return {
        "symbol": symbol.upper(),
        "reddit_posts": [
            {
                "created_utc": post.created_utc,
                "subreddit": post.subreddit,
                "author": post.author,
                "score": post.score,
                "permalink": post.permalink,
                "title": post.title,
                "body": post.body,
                "sentiment": post.sentiment
            }
            for post in reddit_posts
        ]
    }
