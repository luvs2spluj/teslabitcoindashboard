# Financial App Backend Architecture

## FastAPI Application Structure
```
apps/api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── api/                   # API routes
│   ├── datasources/           # Data source adapters
│   ├── etl/                   # ETL jobs and flows
│   ├── analysis/              # Analytics modules
│   ├── strategies/            # Strategy and backtesting
│   └── utils/                 # Utility functions
├── alembic/                   # Database migrations
├── tests/                     # Test suite
└── requirements.txt           # Python dependencies
```

## Database Models (TimescaleDB)

### Core Tables
- **tickers**: Symbol metadata (id, symbol, name, sector, currency)
- **prices_daily**: OHLCV data as Timescale hypertable
- **fundamentals**: Financial metrics (PE, EPS, revenue, margins)
- **news**: News articles with sentiment
- **reddit**: Reddit posts/comments with sentiment
- **benchmarks**: Macro indicators (SPX, Gold, UST, CPI)
- **tesla_metrics**: Tesla-specific metrics (deliveries, ASPs, margins)
- **strategies**: User-defined strategies
- **backtest_runs**: Backtest results and metrics

## Data Sources Architecture

### DataSource Interface
```python
class DataSource(ABC):
    @abstractmethod
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        pass
```

### Implemented Sources
- **StooqDataSource**: Equity prices via pandas-datareader
- **FREDDataSource**: Macro data from Federal Reserve
- **BitcoinDataSource**: Bitcoin metrics from bitcoin-data.com
- **SECDataSource**: SEC EDGAR filings
- **RSSDataSource**: News feeds via feedparser
- **RedditDataSource**: Reddit API integration

## ETL Pipeline (Prefect)

### Flow Structure
- **load_prices_daily**: Hourly price updates
- **load_benchmarks**: Daily macro data
- **load_fundamentals**: Quarterly financial data
- **load_news**: Hourly news updates
- **load_reddit**: Hourly Reddit data
- **load_tesla_metrics**: Quarterly Tesla metrics
- **load_btc_metrics**: Daily Bitcoin data

### Error Handling
- Exponential backoff with jitter
- Circuit breaker pattern
- Dead letter queue for failed records
- Comprehensive logging and monitoring

## Analytics Modules

### Valuation
- OLS regression with HAC standard errors
- Distribution fitting (log-normal, skew-t)
- DCF-lite and Residual Income models
- Monte Carlo simulation for uncertainty

### Scenario Analysis
- Regime detection (Bear/Sideways/Base/Bull/Hypergrowth)
- Markov transition matrices
- Forward simulation with percentile bands
- Expected return calculations (5/10/25 year)

## Strategy Engine

### Backtesting Framework
- vectorbt and backtesting.py integration
- Walk-forward validation
- Purged K-Fold cross-validation
- Comprehensive performance metrics

### Optimization
- Optuna hyperparameter optimization
- Constraint handling (max DD, turnover caps)
- Multi-objective optimization
- Parallel execution support

## API Design

### RESTful Endpoints
- `/api/tickers/*`: Ticker data and search
- `/api/tesla/*`: Tesla-specific endpoints
- `/api/gametheory/*`: Scenario analysis
- `/api/backtest/*`: Strategy backtesting
- `/api/optimize/*`: Parameter optimization

### Features
- OpenAPI documentation
- Pydantic validation
- Rate limiting per IP
- API key authentication for write endpoints
- Comprehensive error handling
