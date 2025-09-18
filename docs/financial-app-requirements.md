# Financial App Requirements

## Overview
Build a production-ready, open-source web app focused on Tesla analysis with comprehensive financial data ingestion, valuation, scenario analysis, and strategy backtesting capabilities.

## Core Features

### 1. Tesla-First Focus
- Tesla dashboard with comprehensive metrics (vehicles, energy, margins)
- Historical Tesla data visualization (10+ years)
- Tesla-specific valuation models and scenarios

### 2. Data Ingestion
- **Prices**: Daily OHLCV data for Tesla and benchmarks
- **Fundamentals**: Financial metrics from SEC EDGAR
- **News**: RSS feeds from Reuters, AP, CNBC, Tesla IR
- **Reddit**: Official Reddit API for Tesla discussions
- **Bitcoin**: Bitcoin cycle metrics and correlation analysis
- **Benchmarks**: SPX, Gold, UST, CPI, real yields

### 3. Valuation & Analysis
- OLS regression models with HAC errors
- Distribution fitting for PE multiples
- DCF-lite and Residual Income models
- Game-theory scenario analysis with regime modeling

### 4. Strategy Backtesting
- TrendSpider-style UI for strategy building
- Walk-forward validation with Purged K-Fold
- Comprehensive metrics (Sharpe, Sortino, Max DD, Calmar)
- Optuna optimization with constraints

## Compliance Requirements
- Use only official/free APIs and RSS feeds
- Implement caching and polite rate limiting
- No VPNs, proxies, or ban evasion
- Respect all terms of service

## Data Sources
- **Prices**: Stooq via pandas-datareader
- **Macro**: FRED API for CPI, yields
- **Bitcoin**: bitcoin-data.com API
- **Fundamentals**: SEC EDGAR
- **News**: RSS feeds (Reuters, AP, CNBC, Tesla IR)
- **Reddit**: Official Reddit API

## Success Criteria
- Docker compose launches all services
- Tesla dashboard shows historical metrics
- ETL jobs populate all data tables
- Valuation computes fair value and percentiles
- Strategy builder runs backtests with optimization
- All tests pass and code is production-ready
