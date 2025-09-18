from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog

from app.config import settings
from app.database import engine
from app.api import tickers, tesla, gametheory, backtest, optimize, benchmarks, btc
from app.utils.security import SecurityMiddleware
from app.utils.monitoring import metrics, health_checker, add_health_check

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI application
app = FastAPI(
    title="Financial App API",
    description="Tesla-focused financial analysis and strategy backtesting API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Add security middleware
app.middleware("http")(SecurityMiddleware.rate_limit_middleware)
app.middleware("http")(SecurityMiddleware.security_headers_middleware)

# Include API routers
app.include_router(tickers.router, prefix="/api/tickers", tags=["tickers"])
app.include_router(tesla.router, prefix="/api/tesla", tags=["tesla"])
app.include_router(btc.router, prefix="/api/btc", tags=["bitcoin"])
app.include_router(gametheory.router, prefix="/api/gametheory", tags=["gametheory"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["backtest"])
app.include_router(optimize.router, prefix="/api/optimize", tags=["optimize"])
app.include_router(benchmarks.router, prefix="/api/benchmarks", tags=["benchmarks"])

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting Financial App API")
    
    # Initialize database
    from app.database import init_db
    await init_db()
    
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Financial App API")
    
    # Close database connections
    engine.dispose()
    
    logger.info("Application shutdown complete")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Financial App API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return await health_checker.run_checks()

@app.get("/metrics")
async def get_metrics():
    """Metrics endpoint."""
    return metrics.get_metrics()

# Add health checks
@add_health_check("database")
def check_database():
    """Check database connectivity."""
    try:
        engine.execute("SELECT 1")
        return True
    except Exception:
        return False

@add_health_check("redis")
def check_redis():
    """Check Redis connectivity."""
    try:
        from app.utils.cache import cache_manager
        cache_manager.redis_client.ping()
        return True
    except Exception:
        return False
