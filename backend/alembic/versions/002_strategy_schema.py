"""Add strategy schema

Revision ID: 002
Revises: 001
Create Date: 2026-05-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'strategies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('code_content', sa.Text(), nullable=False),
        sa.Column('parameters', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('asset_class', sa.String(length=20), nullable=False),
        sa.Column('status', sa.Enum('DRAFT', 'TESTING', 'LIVE', 'ARCHIVED', name='strategystatus'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_strategies_code'), 'strategies', ['code'], unique=True)
    op.create_index(op.f('ix_strategies_id'), 'strategies', ['id'], unique=False)

    op.create_table(
        'backtest_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('strategy_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('instrument_ids', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('timeframe', sa.String(length=10), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('parameters', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', name='backteststatus'), nullable=True),
        sa.Column('progress', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id'], ),
    )
    op.create_index(op.f('ix_backtest_tasks_id'), 'backtest_tasks', ['id'], unique=False)

    op.create_table(
        'backtest_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('strategy_id', sa.Integer(), nullable=False),
        sa.Column('equity_curve', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('stats', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('trades', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('drawdown', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('summary', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['strategy_id'], ['strategies.id'], ),
        sa.ForeignKeyConstraint(['task_id'], ['backtest_tasks.id'], ),
    )
    op.create_index(op.f('ix_backtest_results_id'), 'backtest_results', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_backtest_results_id'), table_name='backtest_results')
    op.drop_table('backtest_results')
    op.drop_index(op.f('ix_backtest_tasks_id'), table_name='backtest_tasks')
    op.drop_table('backtest_tasks')
    op.drop_index(op.f('ix_strategies_code'), table_name='strategies')
    op.drop_index(op.f('ix_strategies_id'), table_name='strategies')
    op.drop_table('strategies')
    op.execute(sa.text("DROP TYPE IF EXISTS strategystatus;"))
    op.execute(sa.text("DROP TYPE IF EXISTS backteststatus;"))
