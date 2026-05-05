"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('exchanges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('country', sa.String(length=50), nullable=True),
        sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'MAINTENANCE', name='exchangestatus'), nullable=True),
        sa.Column('config', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchanges_code'), 'exchanges', ['code'], unique=True)
    op.create_index(op.f('ix_exchanges_id'), 'exchanges', ['id'], unique=False)

    op.create_table('datasources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('config', sa.Text(), nullable=True),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datasources_code'), 'datasources', ['code'], unique=True)
    op.create_index(op.f('ix_datasources_id'), 'datasources', ['id'], unique=False)

    op.create_table('instruments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=True),
        sa.Column('exchange_id', sa.Integer(), nullable=False),
        sa.Column('asset_class', sa.Enum('EQUITY', 'FUTURE', 'OPTION', 'FX', 'BOND', 'CRYPTO', name='assetclass'), nullable=False),
        sa.Column('instrument_type', sa.Enum('SPOT', 'MARGIN', 'SWAP', 'FUTURE', 'OPTION', 'ETF', name='instrumenttype'), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'DELISTED', 'SUSPENDED', name='instrumentstatus'), nullable=True),
        sa.Column('base_currency', sa.String(length=10), nullable=True),
        sa.Column('quote_currency', sa.String(length=10), nullable=True),
        sa.Column('price_precision', sa.Integer(), nullable=True),
        sa.Column('size_precision', sa.Integer(), nullable=True),
        sa.Column('min_size', sa.String(length=50), nullable=True),
        sa.Column('max_size', sa.String(length=50), nullable=True),
        sa.Column('contract_size', sa.String(length=50), nullable=True),
        sa.Column('listed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delisted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('extra', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['exchange_id'], ['exchanges.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instruments_asset_class'), 'instruments', ['asset_class'], unique=False)
    op.create_index(op.f('ix_instruments_id'), 'instruments', ['id'], unique=False)
    op.create_index(op.f('ix_instruments_symbol'), 'instruments', ['symbol'], unique=False)

    op.create_table('sync_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('datasource_id', sa.Integer(), nullable=True),
        sa.Column('instrument_id', sa.Integer(), nullable=True),
        sa.Column('timeframe', sa.String(length=10), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', name='synctaskstatus'), nullable=True),
        sa.Column('records_count', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['datasource_id'], ['datasources.id'], ),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sync_tasks_id'), 'sync_tasks', ['id'], unique=False)

    op.create_table('kline_ohlcv',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('instrument_id', sa.Integer(), nullable=False),
        sa.Column('timeframe', sa.String(length=10), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('open', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('high', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('low', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('close', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('volume', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('turnover', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_kline_instrument_timeframe', 'kline_ohlcv', ['instrument_id', 'timeframe', 'timestamp'], unique=True)
    op.create_index(op.f('ix_kline_ohlcv_id'), 'kline_ohlcv', ['id'], unique=False)

    op.create_table('tick_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('instrument_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('bid_price', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('ask_price', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('bid_size', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('ask_size', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('last_price', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('last_size', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('volume', sa.Numeric(precision=30, scale=18), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tick_instrument_timestamp', 'tick_data', ['instrument_id', 'timestamp'], unique=False)
    op.create_index(op.f('ix_tick_data_id'), 'tick_data', ['id'], unique=False)

    conn = op.get_bind()
    conn.execute(sa.text("SELECT create_hypertable('kline_ohlcv', 'timestamp');"))
    conn.execute(sa.text("SELECT create_hypertable('tick_data', 'timestamp');"))


def downgrade() -> None:
    op.drop_index(op.f('ix_tick_data_id'), table_name='tick_data')
    op.drop_index('idx_tick_instrument_timestamp', table_name='tick_data')
    op.drop_table('tick_data')
    op.drop_index(op.f('ix_kline_ohlcv_id'), table_name='kline_ohlcv')
    op.drop_index('idx_kline_instrument_timeframe', table_name='kline_ohlcv')
    op.drop_table('kline_ohlcv')
    op.drop_index(op.f('ix_sync_tasks_id'), table_name='sync_tasks')
    op.drop_table('sync_tasks')
    op.drop_index(op.f('ix_instruments_symbol'), table_name='instruments')
    op.drop_index(op.f('ix_instruments_id'), table_name='instruments')
    op.drop_index(op.f('ix_instruments_asset_class'), table_name='instruments')
    op.drop_table('instruments')
    op.drop_index(op.f('ix_datasources_id'), table_name='datasources')
    op.drop_index(op.f('ix_datasources_code'), table_name='datasources')
    op.drop_table('datasources')
    op.drop_index(op.f('ix_exchanges_id'), table_name='exchanges')
    op.drop_index(op.f('ix_exchanges_code'), table_name='exchanges')
    op.drop_table('exchanges')
    op.execute(sa.text("DROP TYPE IF EXISTS exchangestatus;"))
    op.execute(sa.text("DROP TYPE IF EXISTS assetclass;"))
    op.execute(sa.text("DROP TYPE IF EXISTS instrumenttype;"))
    op.execute(sa.text("DROP TYPE IF EXISTS instrumentstatus;"))
    op.execute(sa.text("DROP TYPE IF EXISTS synctaskstatus;"))
