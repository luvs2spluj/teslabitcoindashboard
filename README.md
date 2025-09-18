# Financial App - Tesla Analysis & Strategy Backtesting

A comprehensive financial analysis platform focused on Tesla with advanced strategy backtesting capabilities, built with modern web technologies.

## 🚀 Features

### Tesla-First Analysis
- **Tesla Dashboard**: Comprehensive metrics for vehicles, energy, and margins
- **Historical Data**: 10+ years of Tesla business metrics
- **Scenario Analysis**: Game-theory based regime modeling and Monte Carlo simulation
- **Valuation Models**: DCF, OLS regression, and percentile analysis

### Data Sources
- **Prices**: Daily OHLCV data via Stooq API
- **Fundamentals**: SEC EDGAR financial data
- **News**: RSS feeds with sentiment analysis
- **Reddit**: Social sentiment tracking
- **Bitcoin**: Cycle analysis and correlation metrics
- **Benchmarks**: SPX, Gold, UST, CPI, real yields

### Strategy Backtesting
- **Strategy Builder**: Visual strategy configuration
- **Backtesting Engine**: Comprehensive performance metrics
- **Optimization**: Optuna-based parameter optimization
- **Walk-Forward Validation**: Purged K-Fold cross-validation

## 🏗️ Architecture

### Monorepo Structure
```
/apps
  /web        # Next.js 14 (App Router, TypeScript), Tailwind, shadcn/ui
  /api        # FastAPI (Python 3.11): ETL, analytics, backtests
/packages
  /shared     # Shared types and utilities
/infra
  /db         # TimescaleDB migrations and seeders
  /docker     # Docker Compose configuration
  /ci         # GitHub Actions workflows
/docs         # Project documentation
```

### Tech Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, Recharts
- **Backend**: FastAPI, Python 3.11, SQLAlchemy, Alembic
- **Database**: TimescaleDB (PostgreSQL extension)
- **Cache**: Redis
- **ETL**: Prefect flows
- **Analytics**: pandas, numpy, scipy, statsmodels
- **Backtesting**: vectorbt, backtesting.py, Optuna

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- pnpm

### Development Setup

1. **Clone and install dependencies**
   ```bash
   git clone <repository-url>
   cd financial-app
   pnpm install
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API keys
   ```

3. **Start development environment**
   ```bash
   make dev
   ```

4. **Initialize database**
   ```bash
   make migrate
   make seed
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Available Commands

```bash
# Development
make dev          # Start all services
make build        # Build all applications
make test         # Run all tests
make lint         # Lint all code
make format       # Format all code

# Database
make migrate      # Run database migrations
make seed         # Seed database with sample data
make etl          # Run ETL jobs

# Cleanup
make clean        # Clean up containers and volumes
```

## 📊 Data Pipeline

### ETL Jobs (Prefect)
- **load_prices_daily**: Hourly price updates
- **load_benchmarks**: Daily macro data
- **load_fundamentals**: Quarterly financial data
- **load_news**: Hourly news updates
- **load_reddit**: Hourly Reddit data
- **load_tesla_metrics**: Quarterly Tesla metrics
- **load_btc_metrics**: Daily Bitcoin data

### Data Sources
- **Stooq**: Equity prices via pandas-datareader
- **FRED**: Macro indicators from Federal Reserve
- **Bitcoin Data API**: Bitcoin metrics and cycle analysis
- **SEC EDGAR**: Financial filings
- **RSS Feeds**: News with sentiment analysis
- **Reddit API**: Social sentiment tracking

## 🔧 API Endpoints

### Ticker Data
- `GET /api/tickers/search` - Search tickers
- `GET /api/tickers/{symbol}/overview` - Ticker overview
- `GET /api/tickers/{symbol}/prices` - Price data
- `GET /api/tickers/{symbol}/fundamentals` - Financial data
- `GET /api/tickers/{symbol}/news` - News with sentiment
- `GET /api/tickers/{symbol}/reddit` - Reddit posts

### Tesla-Specific
- `GET /api/tesla/metrics` - Tesla business metrics
- `GET /api/tesla/dashboard` - Tesla dashboard data

### Analysis
- `GET /api/gametheory/{symbol}/scenarios` - Scenario analysis
- `GET /api/benchmarks` - Market benchmarks

### Strategy Backtesting
- `POST /api/backtest/run` - Run backtest
- `GET /api/backtest/{id}` - Get backtest results
- `POST /api/optimize` - Start optimization
- `GET /api/optimize/{study_id}` - Get optimization results

## 🎨 Frontend Pages

- **/** - Home page with feature overview
- **/tsla** - Tesla dashboard with comprehensive metrics
- **/stock/[symbol]** - Individual stock analysis
- **/strategies** - Strategy builder and gallery
- **/backtests/[id]** - Backtest results visualization
- **/btc** - Bitcoin analysis and cycle timing
- **/compare** - Benchmark comparison tools

## 🔒 Security & Compliance

- **No secret keys in client** - All sensitive data server-side only
- **Input validation** - Comprehensive validation with Pydantic/Zod
- **Rate limiting** - Respectful API usage with exponential backoff
- **Caching** - Redis-based caching with ETag support
- **Terms of Service** - Compliant with all data source TOS

## 📈 Performance

- **TimescaleDB** - Optimized for time-series data
- **Redis caching** - Aggressive caching for frequently accessed data
- **Code splitting** - Optimized bundle sizes
- **Server components** - Reduced client-side JavaScript
- **CDN ready** - Optimized for global distribution

## 🚀 Deployment

### Production Stack
- **Frontend**: Vercel
- **Backend**: Fly.io or Railway
- **Database**: Supabase or managed PostgreSQL
- **Cache**: Redis Cloud
- **Monitoring**: Sentry, OpenTelemetry

### CI/CD Pipeline
- **Lint/Typecheck**: Automated code quality checks
- **Testing**: Comprehensive test suite
- **Build**: Optimized production builds
- **Deploy**: Automated deployment to staging/production

## 📚 Documentation

- **[Requirements](docs/financial-app-requirements.md)** - Feature specifications
- **[Tech Stack](docs/financial-app-techStack.md)** - Technology choices
- **[Backend](docs/financial-app-backend.md)** - API architecture
- **[Frontend](docs/financial-app-frontend.md)** - UI/UX design
- **[Implementation](docs/financial-app-implementation.md)** - Development guide
- **[Security](docs/financial-app-security.md)** - Security guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for Tesla investors and quantitative traders**
