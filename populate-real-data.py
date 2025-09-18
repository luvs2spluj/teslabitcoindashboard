#!/usr/bin/env python3
"""
Quick script to populate the Tesla dashboard with real data.
This will fetch live data and update the database.
"""

import asyncio
import sys
import os
sys.path.append('apps/api')

from apps.api.app.datasources.ycharts import YChartsDataSource
from apps.api.app.datasources.bgeometrics import BGeometricsDataSource
from apps.api.app.database import SessionLocal, engine
from apps.api.app.models.tesla_metric import TeslaMetric
from apps.api.app.models.price import Price
from apps.api.app.models.ticker import Ticker
from datetime import datetime, date
import yfinance as yf

async def populate_tesla_data():
    """Populate Tesla data from real sources."""
    print("🚀 Starting Tesla data population...")
    
    # Initialize data sources
    ycharts = YChartsDataSource()
    bgeometrics = BGeometricsDataSource()
    
    db = SessionLocal()
    
    try:
        # 1. Fetch Tesla delivery data from YCharts
        print("📊 Fetching Tesla delivery data from YCharts...")
        delivery_result = await ycharts.fetch_tesla_deliveries()
        
        if delivery_result['success']:
            data = delivery_result['data']
            print(f"✅ Found {data['total_records']} delivery records")
            
            # Store latest delivery data
            if data['latest_deliveries']:
                latest = data['latest_deliveries']
                
                # Check if record exists
                existing = db.query(TeslaMetric).filter(
                    TeslaMetric.date == latest['date']
                ).first()
                
                if not existing:
                    tesla_metric = TeslaMetric(
                        date=latest['date'],
                        vehicles_delivered=int(latest['deliveries']),
                        notes=f"Data from YCharts - {latest['quarter']}",
                        source_url="https://ycharts.com/indicators/tesla_inc_tsla_total_deliveries_quarterly"
                    )
                    db.add(tesla_metric)
                    print(f"✅ Added delivery data: {latest['deliveries']} vehicles for {latest['quarter']}")
                else:
                    print(f"ℹ️ Delivery data already exists for {latest['quarter']}")
        
        # 2. Fetch Tesla stock data
        print("📈 Fetching Tesla stock data...")
        try:
            ticker = yf.Ticker("TSLA")
            hist = ticker.history(period="1mo")
            
            if not hist.empty:
                # Ensure TSLA ticker exists
                tsla_ticker = db.query(Ticker).filter(Ticker.symbol == "TSLA").first()
                if not tsla_ticker:
                    tsla_ticker = Ticker(
                        symbol="TSLA",
                        name="Tesla, Inc.",
                        exchange="NASDAQ",
                        sector="Consumer Discretionary",
                        industry="Auto Manufacturers"
                    )
                    db.add(tsla_ticker)
                    db.flush()
                
                # Add recent price data
                for date_idx, row in hist.iterrows():
                    existing_price = db.query(Price).filter(
                        Price.ticker_id == tsla_ticker.id,
                        Price.date == date_idx.date()
                    ).first()
                    
                    if not existing_price:
                        price = Price(
                            ticker_id=tsla_ticker.id,
                            date=date_idx.date(),
                            open=float(row['Open']),
                            high=float(row['High']),
                            low=float(row['Low']),
                            close=float(row['Close']),
                            volume=int(row['Volume'])
                        )
                        db.add(price)
                
                print(f"✅ Added {len(hist)} days of Tesla stock data")
        
        except Exception as e:
            print(f"⚠️ Error fetching stock data: {e}")
        
        # 3. Commit all changes
        db.commit()
        print("✅ All data committed to database!")
        
        # 4. Show summary
        total_metrics = db.query(TeslaMetric).count()
        total_prices = db.query(Price).count()
        total_tickers = db.query(Ticker).count()
        
        print(f"""
📊 Database Summary:
- Tesla Metrics: {total_metrics} records
- Price Data: {total_prices} records  
- Tickers: {total_tickers} records

🌐 Access your data:
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs
- Database: PostgreSQL on port 5432
        """)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(populate_tesla_data())
