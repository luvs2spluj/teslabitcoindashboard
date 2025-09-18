"""
Database seeding script for initial data.
"""
import asyncio
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models.ticker import Ticker
from app.models.price import Price
from app.models.benchmark import Benchmark
from app.models.tesla_metric import TeslaMetric
import pandas as pd
import numpy as np

def create_sample_tickers(db: Session):
    """Create sample ticker data."""
    tickers = [
        Ticker(
            symbol="TSLA",
            name="Tesla, Inc.",
            sector="Automotive",
            currency="USD",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Ticker(
            symbol="SPY",
            name="SPDR S&P 500 ETF Trust",
            sector="ETF",
            currency="USD",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Ticker(
            symbol="GLD",
            name="SPDR Gold Trust",
            sector="ETF",
            currency="USD",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Ticker(
            symbol="QQQ",
            name="Invesco QQQ Trust",
            sector="ETF",
            currency="USD",
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
    
    for ticker in tickers:
        existing = db.query(Ticker).filter(Ticker.symbol == ticker.symbol).first()
        if not existing:
            db.add(ticker)
    
    db.commit()
    print("✓ Created sample tickers")

def create_sample_prices(db: Session):
    """Create sample price data."""
    ticker = db.query(Ticker).filter(Ticker.symbol == "TSLA").first()
    if not ticker:
        print("❌ TSLA ticker not found")
        return
    
    # Generate sample price data for the last 2 years
    start_date = date(2022, 1, 1)
    end_date = date(2023, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Generate realistic price data with trend and volatility
    np.random.seed(42)
    base_price = 200
    trend = np.linspace(0, 100, len(dates))  # Upward trend
    noise = np.random.normal(0, 10, len(dates))  # Random noise
    prices = base_price + trend + noise
    
    for i, (dt, price) in enumerate(zip(dates, prices)):
        # Skip weekends
        if dt.weekday() >= 5:
            continue
            
        # Create OHLC data
        daily_range = np.random.uniform(2, 8)
        high = price + daily_range
        low = price - daily_range
        open_price = price + np.random.uniform(-2, 2)
        close_price = price + np.random.uniform(-2, 2)
        volume = np.random.randint(20000000, 80000000)
        
        existing = db.query(Price).filter(
            Price.ticker_id == ticker.id,
            Price.date == dt.date()
        ).first()
        
        if not existing:
            price_record = Price(
                ticker_id=ticker.id,
                date=dt.date(),
                open=round(open_price, 2),
                high=round(high, 2),
                low=round(low, 2),
                close=round(close_price, 2),
                volume=volume,
                source="stooq"
            )
            db.add(price_record)
    
    db.commit()
    print("✓ Created sample TSLA price data")

def create_sample_benchmarks(db: Session):
    """Create sample benchmark data."""
    # Generate sample benchmark data
    start_date = date(2022, 1, 1)
    end_date = date(2023, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    np.random.seed(42)
    
    for dt in dates:
        # Skip weekends
        if dt.weekday() >= 5:
            continue
            
        existing = db.query(Benchmark).filter(Benchmark.date == dt.date()).first()
        if not existing:
            benchmark = Benchmark(
                date=dt.date(),
                spx=4000 + np.random.normal(0, 50),
                gold=1800 + np.random.normal(0, 20),
                ust_total_return=100 + np.random.normal(0, 2),
                cpi=7.5 + np.random.normal(0, 0.5),
                real_yield=1.5 + np.random.normal(0, 0.3),
                source="fred"
            )
            db.add(benchmark)
    
    db.commit()
    print("✓ Created sample benchmark data")

def create_sample_tesla_metrics(db: Session):
    """Create sample Tesla metrics data."""
    # Quarterly Tesla metrics for the last 2 years
    quarters = [
        (date(2022, 3, 31), 310048, 54000, 0.19, 85, 846, 2800),
        (date(2022, 6, 30), 254695, 57000, 0.14, 106, 1137, 2800),
        (date(2022, 9, 30), 343830, 55000, 0.27, 94, 2102, 2800),
        (date(2022, 12, 31), 405278, 53000, 0.25, 100, 2462, 2800),
        (date(2023, 3, 31), 422875, 47000, 0.19, 67, 3889, 2800),
        (date(2023, 6, 30), 466140, 47000, 0.18, 66, 3653, 2800),
        (date(2023, 9, 30), 435059, 44000, 0.18, 48, 3995, 2800),
        (date(2023, 12, 31), 484507, 44000, 0.19, 66, 2959, 2800),
    ]
    
    for quarter_date, vehicles, asp, margin, solar_mw, storage_mwh, asp_storage in quarters:
        existing = db.query(TeslaMetric).filter(TeslaMetric.date == quarter_date).first()
        if not existing:
            metric = TeslaMetric(
                date=quarter_date,
                vehicles_delivered=vehicles,
                asp_auto=asp,
                auto_gross_margin=margin,
                energy_solar_mw=solar_mw,
                energy_storage_mwh=storage_mwh,
                asp_storage=asp_storage,
                energy_gross_margin=0.24,
                notes=f"Q{quarter_date.month//3 + 1} {quarter_date.year} results",
                source_url="https://ir.tesla.com"
            )
            db.add(metric)
    
    db.commit()
    print("✓ Created sample Tesla metrics data")

async def main():
    """Main seeding function."""
    print("🌱 Starting database seeding...")
    
    # Initialize database
    await init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create sample data
        create_sample_tickers(db)
        create_sample_prices(db)
        create_sample_benchmarks(db)
        create_sample_tesla_metrics(db)
        
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
