from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from enum import Enum

class StrategyStatus(str, Enum):
    DRAFT = "draft"
    TESTING = "testing"
    LIVE = "live"
    ARCHIVED = "archived"

class BacktestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    code_content = Column(Text, nullable=False)
    parameters = Column(JSON, nullable=False)
    asset_class = Column(String(20), nullable=False)
    status = Column(ENUM(StrategyStatus, name="strategystatus"), default=StrategyStatus.DRAFT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    version = Column(Integer, default=1)
    
    backtest_tasks = relationship("BacktestTask", back_populates="strategy")

class BacktestTask(Base):
    __tablename__ = "backtest_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    instrument_ids = Column(JSON, nullable=False)
    timeframe = Column(String(10), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    parameters = Column(JSON)
    status = Column(ENUM(BacktestStatus, name="backteststatus"), default=BacktestStatus.PENDING)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    strategy = relationship("Strategy", back_populates="backtest_tasks")
    result = relationship("BacktestResult", uselist=False, back_populates="task")

class BacktestResult(Base):
    __tablename__ = "backtest_results"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("backtest_tasks.id"), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    equity_curve = Column(JSON, nullable=False)
    stats = Column(JSON, nullable=False)
    trades = Column(JSON, nullable=False)
    drawdown = Column(JSON, nullable=False)
    summary = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    task = relationship("BacktestTask", back_populates="result")
