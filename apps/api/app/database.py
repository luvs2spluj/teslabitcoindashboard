from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import structlog

from app.config import settings

logger = structlog.get_logger()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

async def init_db():
    """Initialize database tables."""
    try:
        # Import all models to ensure they're registered
        from app.models import ticker, price, fundamental, news, reddit, benchmark, tesla_metric, strategy, backtest_run
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Enable TimescaleDB extension if using PostgreSQL
        if "postgresql" in settings.DATABASE_URL:
            with engine.connect() as conn:
                conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
                conn.commit()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
