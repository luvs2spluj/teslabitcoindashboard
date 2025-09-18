# Financial App Tech Stack

## Architecture
- **Monorepo**: pnpm workspace with shared packages
- **Frontend**: Next.js 14 (App Router, TypeScript)
- **Backend**: FastAPI (Python 3.11)
- **Database**: TimescaleDB (PostgreSQL extension)
- **Cache**: Redis
- **Queue**: Redis/Celery for async tasks

## Frontend Stack
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Charts**: Recharts
- **Auth**: Supabase Auth
- **State**: React Query/TanStack Query

## Backend Stack
- **Framework**: FastAPI
- **Language**: Python 3.11
- **ORM**: SQLAlchemy with Alembic migrations
- **Data Processing**: pandas, numpy, scipy
- **ML/Analytics**: scikit-learn, statsmodels
- **Backtesting**: vectorbt, backtesting.py
- **Optimization**: Optuna
- **ETL**: Prefect flows
- **Validation**: Pydantic

## Data & Analytics
- **Time Series**: TimescaleDB hypertables
- **Financial Data**: pandas-datareader, yfinance
- **Technical Analysis**: pandas-ta, TA-Lib
- **Sentiment**: VADER, transformers
- **Statistics**: statsmodels, scipy.stats

## Infrastructure
- **Containerization**: Docker & docker-compose
- **Deployment**: Vercel (frontend), Fly.io/Railway (backend)
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry, OpenTelemetry
- **Security**: Helmet, rate limiting, CSP headers

## Development Tools
- **Package Manager**: pnpm
- **Linting**: ESLint (frontend), Ruff (backend)
- **Formatting**: Prettier (frontend), Black (backend)
- **Type Checking**: TypeScript, MyPy
- **Testing**: Jest (frontend), pytest (backend)
