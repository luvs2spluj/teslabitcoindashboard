"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tickers table
    op.create_table('tickers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('sector', sa.String(length=100), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickers_id'), 'tickers', ['id'], unique=False)
    op.create_index(op.f('ix_tickers_symbol'), 'tickers', ['symbol'], unique=True)

    # Create prices_daily table (TimescaleDB hypertable)
    op.create_table('prices_daily',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open', sa.Float(), nullable=False),
        sa.Column('high', sa.Float(), nullable=False),
        sa.Column('low', sa.Float(), nullable=False),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.BigInteger(), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prices_daily_id'), 'prices_daily', ['id'], unique=False)
    op.create_index(op.f('ix_prices_daily_date'), 'prices_daily', ['date'], unique=False)

    # Create fundamentals table
    op.create_table('fundamentals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('pe', sa.Float(), nullable=True),
        sa.Column('eps', sa.Float(), nullable=True),
        sa.Column('revenue', sa.Float(), nullable=True),
        sa.Column('gross_margin', sa.Float(), nullable=True),
        sa.Column('op_margin', sa.Float(), nullable=True),
        sa.Column('fcf', sa.Float(), nullable=True),
        sa.Column('shares_out', sa.Float(), nullable=True),
        sa.Column('source', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fundamentals_id'), 'fundamentals', ['id'], unique=False)

    # Create news table
    op.create_table('news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.Column('source', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('url', sa.String(length=1000), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('sentiment', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_news_id'), 'news', ['id'], unique=False)
    op.create_index(op.f('ix_news_published_at'), 'news', ['published_at'], unique=False)

    # Create reddit table
    op.create_table('reddit',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('created_utc', sa.DateTime(), nullable=False),
        sa.Column('subreddit', sa.String(length=100), nullable=False),
        sa.Column('author', sa.String(length=100), nullable=True),
        sa.Column('score', sa.BigInteger(), nullable=True),
        sa.Column('permalink', sa.String(length=500), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('sentiment', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reddit_id'), 'reddit', ['id'], unique=False)
    op.create_index(op.f('ix_reddit_created_utc'), 'reddit', ['created_utc'], unique=False)

    # Create benchmarks table
    op.create_table('benchmarks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('spx', sa.Float(), nullable=True),
        sa.Column('gold', sa.Float(), nullable=True),
        sa.Column('ust_total_return', sa.Float(), nullable=True),
        sa.Column('cpi', sa.Float(), nullable=True),
        sa.Column('real_yield', sa.Float(), nullable=True),
        sa.Column('source', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_benchmarks_id'), 'benchmarks', ['id'], unique=False)
    op.create_index(op.f('ix_benchmarks_date'), 'benchmarks', ['date'], unique=False)

    # Create tesla_metrics table
    op.create_table('tesla_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('vehicles_delivered', sa.Float(), nullable=True),
        sa.Column('asp_auto', sa.Float(), nullable=True),
        sa.Column('auto_gross_margin', sa.Float(), nullable=True),
        sa.Column('energy_solar_mw', sa.Float(), nullable=True),
        sa.Column('energy_storage_mwh', sa.Float(), nullable=True),
        sa.Column('asp_storage', sa.Float(), nullable=True),
        sa.Column('energy_gross_margin', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('source_url', sa.String(length=1000), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tesla_metrics_id'), 'tesla_metrics', ['id'], unique=False)
    op.create_index(op.f('ix_tesla_metrics_date'), 'tesla_metrics', ['date'], unique=False)

    # Create strategies table
    op.create_table('strategies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('family', sa.String(length=100), nullable=False),
        sa.Column('params_json', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_strategies_id'), 'strategies', ['id'], unique=False)

    # Create backtest_runs table
    op.create_table('backtest_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('strategy_id', sa.Integer(), nullable=False),
        sa.Column('ticker_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('metrics_json', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('trades_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('equity_curve_url', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id'], ),
        sa.ForeignKeyConstraint(['ticker_id'], ['tickers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backtest_runs_id'), 'backtest_runs', ['id'], unique=False)

    # Create TimescaleDB hypertable for prices_daily
    op.execute("SELECT create_hypertable('prices_daily', 'date');")


def downgrade() -> None:
    op.drop_index(op.f('ix_backtest_runs_id'), table_name='backtest_runs')
    op.drop_table('backtest_runs')
    op.drop_index(op.f('ix_strategies_id'), table_name='strategies')
    op.drop_table('strategies')
    op.drop_index(op.f('ix_tesla_metrics_date'), table_name='tesla_metrics')
    op.drop_index(op.f('ix_tesla_metrics_id'), table_name='tesla_metrics')
    op.drop_table('tesla_metrics')
    op.drop_index(op.f('ix_benchmarks_date'), table_name='benchmarks')
    op.drop_index(op.f('ix_benchmarks_id'), table_name='benchmarks')
    op.drop_table('benchmarks')
    op.drop_index(op.f('ix_reddit_created_utc'), table_name='reddit')
    op.drop_index(op.f('ix_reddit_id'), table_name='reddit')
    op.drop_table('reddit')
    op.drop_index(op.f('ix_news_published_at'), table_name='news')
    op.drop_index(op.f('ix_news_id'), table_name='news')
    op.drop_table('news')
    op.drop_index(op.f('ix_fundamentals_id'), table_name='fundamentals')
    op.drop_table('fundamentals')
    op.drop_index(op.f('ix_prices_daily_date'), table_name='prices_daily')
    op.drop_index(op.f('ix_prices_daily_id'), table_name='prices_daily')
    op.drop_table('prices_daily')
    op.drop_index(op.f('ix_tickers_symbol'), table_name='tickers')
    op.drop_index(op.f('ix_tickers_id'), table_name='tickers')
    op.drop_table('tickers')
