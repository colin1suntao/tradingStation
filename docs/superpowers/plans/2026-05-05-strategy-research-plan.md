# 策略研究环境实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建策略研究环境，包含策略管理、回测引擎、性能分析等核心功能，集成 VectorBT 实现高性能回测。

**Architecture:** 分层插件化架构，后端使用 FastAPI + SQLAlchemy，回测引擎集成 VectorBT，支持策略版本管理、组合回测、多订单类型。

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy 2.0, PostgreSQL, VectorBT, Plotly, Celery, Redis

---

## 文件结构映射

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── strategy.py      # 策略管理API
│   │       ├── backtest.py      # 回测管理API
│   │       └── analyze.py       # 分析与可视化API
│   ├── models/
│   │   └── strategy.py          # 策略相关模型
│   ├── schemas/
│   │   └── strategy.py          # 策略相关 schemas
│   ├── services/
│   │   ├── strategy_service.py  # 策略服务
│   │   ├── backtest_service.py  # 回测服务
│   │   └── analyze_service.py   # 分析服务
│   └── engine/
│       └── backtest_engine.py   # 回测引擎（VectorBT集成）
├── alembic/
│   └── versions/
│       └── 002_strategy_schema.py
└── tests/
    └── test_strategy.py
```

---

## Task 1: 数据模型定义

**Files:**
- Create: `/workspace/backend/app/models/strategy.py`
- Modify: `/workspace/backend/app/models/__init__.py`

- [ ] **Step 1: 创建策略模型文件**

```python
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Enum, ForeignKey
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
    status = Column(Enum(StrategyStatus), default=StrategyStatus.DRAFT)
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
    status = Column(Enum(BacktestStatus), default=BacktestStatus.PENDING)
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
```

- [ ] **Step 2: 更新 models/__init__.py**

```python
from .master import (
    AssetClass, InstrumentType, ExchangeStatus, 
    InstrumentStatus, SyncTaskStatus, Exchange, 
    Instrument, DataSource, SyncTask,
)
from .market import KlineOHLCV, TickData
from .strategy import (
    StrategyStatus, BacktestStatus, 
    Strategy, BacktestTask, BacktestResult,
)

__all__ = [
    "AssetClass", "InstrumentType", "ExchangeStatus",
    "InstrumentStatus", "SyncTaskStatus", "Exchange",
    "Instrument", "DataSource", "SyncTask",
    "KlineOHLCV", "TickData",
    "StrategyStatus", "BacktestStatus",
    "Strategy", "BacktestTask", "BacktestResult",
]
```

- [ ] **Step 3: 检查模型语法**

Run: `cd /workspace/backend && python -c "from app.models import Strategy; print('Model import successful')"`
Expected: "Model import successful"

- [ ] **Step 4: Commit**

```bash
git add app/models/strategy.py app/models/__init__.py
git commit -m "feat: add strategy models"
```

---

## Task 2: Pydantic Schemas

**Files:**
- Create: `/workspace/backend/app/schemas/strategy.py`
- Modify: `/workspace/backend/app/schemas/__init__.py`

- [ ] **Step 1: 创建策略 schemas**

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class StrategyBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    code_content: str
    parameters: Dict[str, Any]
    asset_class: str

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code_content: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class Strategy(StrategyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    version: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class BacktestTaskBase(BaseModel):
    name: str
    instrument_ids: List[int]
    timeframe: str
    start_time: datetime
    end_time: datetime
    parameters: Optional[Dict[str, Any]] = None

class BacktestTaskCreate(BacktestTaskBase):
    strategy_id: int

class BacktestTask(BacktestTaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    strategy_id: int
    status: str
    progress: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class BacktestResultBase(BaseModel):
    equity_curve: Dict[str, Any]
    stats: Dict[str, Any]
    trades: List[Dict[str, Any]]
    drawdown: Dict[str, Any]
    summary: Dict[str, Any]

class BacktestResult(BacktestResultBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    task_id: int
    strategy_id: int
    created_at: datetime

class ValidationResult(BaseModel):
    valid: bool
    message: str
    errors: List[str] = []

class MetricResult(BaseModel):
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    volatility: float
    max_consecutive_losses: int
```

- [ ] **Step 2: 更新 schemas/__init__.py**

```python
from .master import (
    Exchange, ExchangeCreate, ExchangeUpdate,
    Instrument, InstrumentCreate, InstrumentUpdate,
    DataSource, DataSourceCreate,
    SyncTask, SyncTaskCreate,
)
from .market import Kline, KlineCreate, KlineQuery, Quote
from .datasource import SyncRequest, SyncResponse
from .strategy import (
    Strategy, StrategyCreate, StrategyUpdate,
    BacktestTask, BacktestTaskCreate,
    BacktestResult, BacktestResultBase,
    ValidationResult, MetricResult,
)

__all__ = [
    "Exchange", "ExchangeCreate", "ExchangeUpdate",
    "Instrument", "InstrumentCreate", "InstrumentUpdate",
    "DataSource", "DataSourceCreate",
    "SyncTask", "SyncTaskCreate",
    "Kline", "KlineCreate", "KlineQuery", "Quote",
    "SyncRequest", "SyncResponse",
    "Strategy", "StrategyCreate", "StrategyUpdate",
    "BacktestTask", "BacktestTaskCreate",
    "BacktestResult", "BacktestResultBase",
    "ValidationResult", "MetricResult",
]
```

- [ ] **Step 3: 检查 schemas**

Run: `cd /workspace/backend && python -c "from app.schemas import Strategy; print('Schema import successful')"`
Expected: "Schema import successful"

- [ ] **Step 4: Commit**

```bash
git add app/schemas/strategy.py app/schemas/__init__.py
git commit -m "feat: add strategy schemas"
```

---

## Task 3: 数据库迁移

**Files:**
- Create: `/workspace/backend/alembic/versions/002_strategy_schema.py`

- [ ] **Step 1: 创建迁移脚本**

```python
"""Add strategy schema

Revision ID: 002
Revises: 001
Create Date: 2026-05-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
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
    op.execute("DROP TYPE IF EXISTS strategystatus")
    op.execute("DROP TYPE IF EXISTS backteststatus")
```

- [ ] **Step 2: 运行迁移**

Run: `cd /workspace/backend && alembic upgrade head`
Expected: Migration completed successfully

- [ ] **Step 3: Commit**

```bash
git add alembic/versions/002_strategy_schema.py
git commit -m "feat: add strategy database migration"
```

---

## Task 4: 回测引擎（VectorBT集成）

**Files:**
- Create: `/workspace/backend/app/engine/backtest_engine.py`

- [ ] **Step 1: 创建回测引擎**

```python
import vectorbt as vbt
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime

class BacktestEngine:
    """回测引擎（基于VectorBT）"""
    
    def __init__(self):
        self.portfolio = None
        self.signals = None
    
    def run_strategy(
        self,
        data: pd.DataFrame,
        strategy_code: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """运行策略回测"""
        try:
            exec_globals = {
                'vbt': vbt,
                'pd': pd,
                'np': np,
                'params': params,
                'data': data
            }
            
            exec(strategy_code, exec_globals)
            
            if 'Strategy' in exec_globals:
                strategy_class = exec_globals['Strategy']
                strategy = strategy_class(params)
                
                context = {'data': data}
                strategy.initialize(context)
                
                signals = []
                for i in range(len(data)):
                    bar_data = {
                        'open': data['open'].iloc[i],
                        'high': data['high'].iloc[i],
                        'low': data['low'].iloc[i],
                        'close': data['close'].iloc[i],
                        'volume': data['volume'].iloc[i],
                    }
                    signal = strategy.on_bar(bar_data)
                    signals.append(signal.get('signal', 'hold'))
                
                self.signals = pd.Series(signals, index=data.index)
                
                entries = self.signals == 'buy'
                exits = self.signals == 'sell'
                
                self.portfolio = vbt.Portfolio.from_signals(
                    data['close'],
                    entries=entries,
                    exits=exits,
                    fees=params.get('fees', 0.001),
                    slippage=params.get('slippage', 0.001)
                )
                
                return self._generate_results()
            
            return {'error': 'Strategy class not found'}
        
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_results(self) -> Dict[str, Any]:
        """生成回测结果"""
        if self.portfolio is None:
            return {}
        
        equity_curve = self.portfolio.equity().to_dict()
        
        stats = {
            'total_return': float(self.portfolio.total_return().iloc[0]),
            'annual_return': float(self.portfolio.annualized_return().iloc[0]),
            'sharpe_ratio': float(self.portfolio.sharpe_ratio().iloc[0]),
            'max_drawdown': float(self.portfolio.max_drawdown().iloc[0]),
            'win_rate': float(self.portfolio.win_rate().iloc[0]),
            'profit_factor': float(self.portfolio.profit_factor().iloc[0]),
            'total_trades': int(self.portfolio.total_trades().iloc[0]),
        }
        
        drawdown = {
            'max': float(self.portfolio.max_drawdown().iloc[0]),
            'duration': int(self.portfolio.max_drawdown_duration().iloc[0]),
            'underwater': self.portfolio.underwater().to_dict()
        }
        
        trades = []
        if hasattr(self.portfolio, 'trades'):
            for trade in self.portfolio.trades.records:
                trades.append({
                    'entry_time': trade['entry_time'].isoformat() if isinstance(trade['entry_time'], datetime) else str(trade['entry_time']),
                    'exit_time': trade['exit_time'].isoformat() if isinstance(trade['exit_time'], datetime) else str(trade['exit_time']),
                    'entry_price': float(trade['entry_price']),
                    'exit_price': float(trade['exit_price']),
                    'return': float(trade['return']),
                    'size': float(trade.get('size', 0)),
                })
        
        summary = {
            'start_date': str(self.portfolio.start_date),
            'end_date': str(self.portfolio.end_date),
            'total_return_pct': float(self.portfolio.total_return().iloc[0] * 100),
            'cagr': float(self.portfolio.annualized_return().iloc[0] * 100),
            'sharpe_ratio': float(self.portfolio.sharpe_ratio().iloc[0]),
            'max_drawdown_pct': float(self.portfolio.max_drawdown().iloc[0] * 100),
            'total_trades': int(self.portfolio.total_trades().iloc[0]),
            'win_rate_pct': float(self.portfolio.win_rate().iloc[0] * 100),
        }
        
        return {
            'equity_curve': equity_curve,
            'stats': stats,
            'trades': trades,
            'drawdown': drawdown,
            'summary': summary,
            'success': True,
        }
```

- [ ] **Step 2: 测试回测引擎**

```python
# 测试代码
if __name__ == "__main__":
    engine = BacktestEngine()
    
    strategy_code = """
class Strategy:
    name = "Test Strategy"
    params = {"ma_window": 20}
    
    def __init__(self, params=None):
        self.params = params or self.params
    
    def initialize(self, context):
        self.context = context
    
    def on_bar(self, data):
        close = data["close"]
        if close > 100:
            return {"signal": "buy"}
        elif close < 90:
            return {"signal": "sell"}
        return {"signal": "hold"}
"""
    
    data = pd.DataFrame({
        'open': np.random.uniform(95, 105, 100),
        'high': np.random.uniform(100, 110, 100),
        'low': np.random.uniform(90, 100, 100),
        'close': np.random.uniform(95, 105, 100),
        'volume': np.random.uniform(1000, 10000, 100),
    }, index=pd.date_range('2024-01-01', periods=100))
    
    result = engine.run_strategy(data, strategy_code, {"ma_window": 20})
    print("Test result:", result.get('success', False))
```

Run: `cd /workspace/backend && python app/engine/backtest_engine.py`
Expected: "Test result: True"

- [ ] **Step 3: Commit**

```bash
git add app/engine/backtest_engine.py
git commit -m "feat: add backtest engine with VectorBT"
```

---

## Task 5: 核心服务层

**Files:**
- Create: `/workspace/backend/app/services/strategy_service.py`
- Create: `/workspace/backend/app/services/backtest_service.py`
- Create: `/workspace/backend/app/services/analyze_service.py`
- Modify: `/workspace/backend/app/services/__init__.py`

- [ ] **Step 1: 创建 StrategyService**

```python
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.strategy import Strategy, StrategyStatus
from app.schemas.strategy import StrategyCreate, StrategyUpdate, ValidationResult
import ast

class StrategyService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_strategy(self, strategy_in: StrategyCreate) -> Strategy:
        strategy = Strategy(**strategy_in.model_dump())
        self.db.add(strategy)
        await self.db.commit()
        await self.db.refresh(strategy)
        return strategy
    
    async def get_strategy(self, strategy_id: int) -> Optional[Strategy]:
        result = await self.db.execute(select(Strategy).where(Strategy.id == strategy_id))
        return result.scalar_one_or_none()
    
    async def get_strategy_by_code(self, code: str) -> Optional[Strategy]:
        result = await self.db.execute(select(Strategy).where(Strategy.code == code))
        return result.scalar_one_or_none()
    
    async def get_all_strategies(self) -> List[Strategy]:
        result = await self.db.execute(select(Strategy))
        return list(result.scalars().all())
    
    async def update_strategy(self, strategy_id: int, strategy_in: StrategyUpdate) -> Strategy:
        strategy = await self.get_strategy(strategy_id)
        if not strategy:
            raise ValueError("Strategy not found")
        
        update_data = strategy_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(strategy, key, value)
        
        strategy.version += 1
        await self.db.commit()
        await self.db.refresh(strategy)
        return strategy
    
    async def delete_strategy(self, strategy_id: int) -> bool:
        strategy = await self.get_strategy(strategy_id)
        if not strategy:
            return False
        
        await self.db.delete(strategy)
        await self.db.commit()
        return True
    
    def validate_strategy(self, code_content: str) -> ValidationResult:
        errors = []
        try:
            ast.parse(code_content)
        except SyntaxError as e:
            errors.append(f"Syntax error: {e.msg}")
        
        if 'class Strategy' not in code_content:
            errors.append("Strategy class not found")
        
        if 'def on_bar' not in code_content:
            errors.append("on_bar method not found")
        
        return ValidationResult(
            valid=len(errors) == 0,
            message="Valid" if len(errors) == 0 else "Invalid",
            errors=errors
        )
```

- [ ] **Step 2: 创建 BacktestService**

```python
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.strategy import BacktestTask, BacktestResult, BacktestStatus
from app.schemas.strategy import BacktestTaskCreate, BacktestResultBase
from app.engine.backtest_engine import BacktestEngine
from app.services.data_service import DataService
import pandas as pd

class BacktestService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.engine = BacktestEngine()
    
    async def create_backtest(self, backtest_in: BacktestTaskCreate) -> BacktestTask:
        task = BacktestTask(**backtest_in.model_dump())
        task.status = BacktestStatus.PENDING
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def get_backtest(self, task_id: int) -> Optional[BacktestTask]:
        result = await self.db.execute(select(BacktestTask).where(BacktestTask.id == task_id))
        return result.scalar_one_or_none()
    
    async def get_all_backtests(self) -> List[BacktestTask]:
        result = await self.db.execute(select(BacktestTask))
        return list(result.scalars().all())
    
    async def run_backtest(self, task_id: int) -> BacktestResult:
        task = await self.get_backtest(task_id)
        if not task:
            raise ValueError("Backtest task not found")
        
        task.status = BacktestStatus.RUNNING
        task.started_at = datetime.now()
        await self.db.commit()
        
        try:
            data_service = DataService(self.db)
            
            klines = []
            for instrument_id in task.instrument_ids:
                from app.schemas.market import KlineQuery
                query = KlineQuery(
                    instrument_id=instrument_id,
                    timeframe=task.timeframe,
                    start_time=task.start_time,
                    end_time=task.end_time,
                )
                kline_data = await data_service.get_klines(query)
                klines.extend(kline_data)
            
            if not klines:
                raise ValueError("No data found")
            
            df = pd.DataFrame([{
                'open': k.open,
                'high': k.high,
                'low': k.low,
                'close': k.close,
                'volume': k.volume,
            } for k in klines])
            
            df['timestamp'] = [k.timestamp for k in klines]
            df = df.set_index('timestamp')
            
            strategy = await self.db.get(BacktestTask, task.strategy_id)
            if not strategy:
                raise ValueError("Strategy not found")
            
            params = task.parameters or {}
            result_data = self.engine.run_strategy(df, strategy.code_content, params)
            
            if not result_data.get('success'):
                raise ValueError(result_data.get('error', 'Backtest failed'))
            
            result = BacktestResult(
                task_id=task.id,
                strategy_id=strategy.id,
                **result_data
            )
            self.db.add(result)
            
            task.status = BacktestStatus.COMPLETED
            task.progress = 100
            task.completed_at = datetime.now()
            
            await self.db.commit()
            await self.db.refresh(result)
            return result
        
        except Exception as e:
            task.status = BacktestStatus.FAILED
            task.completed_at = datetime.now()
            await self.db.commit()
            raise
    
    async def cancel_backtest(self, task_id: int) -> bool:
        task = await self.get_backtest(task_id)
        if not task:
            return False
        
        if task.status == BacktestStatus.PENDING:
            task.status = BacktestStatus.CANCELLED
            task.completed_at = datetime.now()
            await self.db.commit()
            return True
        
        return False
```

- [ ] **Step 3: 创建 AnalyzeService**

```python
from typing import Dict, Any
from app.models.strategy import BacktestResult
from app.schemas.strategy import MetricResult

class AnalyzeService:
    def calculate_metrics(self, result: BacktestResult) -> MetricResult:
        stats = result.stats
        return MetricResult(
            total_return=stats.get('total_return', 0),
            annual_return=stats.get('annual_return', 0),
            sharpe_ratio=stats.get('sharpe_ratio', 0),
            max_drawdown=stats.get('max_drawdown', 0),
            win_rate=stats.get('win_rate', 0),
            profit_factor=stats.get('profit_factor', 0),
            volatility=stats.get('volatility', 0) if 'volatility' in stats else 0,
            max_consecutive_losses=stats.get('max_consecutive_losses', 0) if 'max_consecutive_losses' in stats else 0,
        )
    
    def generate_charts(self, result: BacktestResult) -> Dict[str, Any]:
        return {
            'equity_curve': result.equity_curve,
            'drawdown': result.drawdown.get('underwater', {}),
            'trades': result.trades,
        }
    
    def risk_analysis(self, result: BacktestResult) -> Dict[str, Any]:
        stats = result.stats
        drawdown = result.drawdown
        
        return {
            'max_drawdown': drawdown.get('max', 0),
            'max_drawdown_duration': drawdown.get('duration', 0),
            'sharpe_ratio': stats.get('sharpe_ratio', 0),
            'volatility': stats.get('volatility', 0) if 'volatility' in stats else 0,
            'risk_return_ratio': (stats.get('total_return', 0) / abs(stats.get('max_drawdown', 1))) if stats.get('max_drawdown') else 0,
            'total_trades': stats.get('total_trades', 0),
            'win_rate': stats.get('win_rate', 0),
        }
    
    def get_summary(self, result: BacktestResult) -> Dict[str, Any]:
        return result.summary
```

- [ ] **Step 4: 更新 services/__init__.py**

```python
from .master_service import MasterDataService
from .data_service import DataService
from .sync_service import SyncService
from .strategy_service import StrategyService
from .backtest_service import BacktestService
from .analyze_service import AnalyzeService

__all__ = [
    "MasterDataService",
    "DataService",
    "SyncService",
    "StrategyService",
    "BacktestService",
    "AnalyzeService",
]
```

- [ ] **Step 5: Commit**

```bash
git add app/services/strategy_service.py app/services/backtest_service.py app/services/analyze_service.py app/services/__init__.py
git commit -m "feat: add strategy services"
```

---

## Task 6: API 路由

**Files:**
- Create: `/workspace/backend/app/api/v1/strategy.py`
- Create: `/workspace/backend/app/api/v1/backtest.py`
- Create: `/workspace/backend/app/api/v1/analyze.py`
- Modify: `/workspace/backend/main.py`

- [ ] **Step 1: 创建策略管理API**

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.strategy import Strategy, StrategyCreate, StrategyUpdate, ValidationResult
from app.services import StrategyService

router = APIRouter(prefix="/strategies", tags=["strategies"])

@router.get("/", response_model=List[Strategy])
async def get_strategies(db: AsyncSession = Depends(get_db)):
    service = StrategyService(db)
    return await service.get_all_strategies()

@router.get("/{strategy_id}", response_model=Strategy)
async def get_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    service = StrategyService(db)
    strategy = await service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.post("/", response_model=Strategy)
async def create_strategy(strategy_in: StrategyCreate, db: AsyncSession = Depends(get_db)):
    service = StrategyService(db)
    existing = await service.get_strategy_by_code(strategy_in.code)
    if existing:
        raise HTTPException(status_code=400, detail="Strategy code already exists")
    
    validation = service.validate_strategy(strategy_in.code_content)
    if not validation.valid:
        raise HTTPException(status_code=400, detail=validation.message)
    
    return await service.create_strategy(strategy_in)

@router.put("/{strategy_id}", response_model=Strategy)
async def update_strategy(strategy_id: int, strategy_in: StrategyUpdate, db: AsyncSession = Depends(get_db)):
    service = StrategyService(db)
    
    if strategy_in.code_content:
        validation = service.validate_strategy(strategy_in.code_content)
        if not validation.valid:
            raise HTTPException(status_code=400, detail=validation.message)
    
    try:
        return await service.update_strategy(strategy_id, strategy_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Strategy not found")

@router.delete("/{strategy_id}")
async def delete_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    service = StrategyService(db)
    success = await service.delete_strategy(strategy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return {"message": "Strategy deleted"}

@router.post("/validate", response_model=ValidationResult)
async def validate_strategy(code_content: str):
    service = StrategyService(None)
    return service.validate_strategy(code_content)
```

- [ ] **Step 2: 创建回测管理API**

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.strategy import BacktestTask, BacktestTaskCreate, BacktestResult
from app.services import BacktestService

router = APIRouter(prefix="/backtests", tags=["backtests"])

@router.get("/", response_model=List[BacktestTask])
async def get_backtests(db: AsyncSession = Depends(get_db)):
    service = BacktestService(db)
    return await service.get_all_backtests()

@router.get("/{task_id}", response_model=BacktestTask)
async def get_backtest(task_id: int, db: AsyncSession = Depends(get_db)):
    service = BacktestService(db)
    task = await service.get_backtest(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return task

@router.post("/", response_model=BacktestTask)
async def create_backtest(backtest_in: BacktestTaskCreate, db: AsyncSession = Depends(get_db)):
    service = BacktestService(db)
    return await service.create_backtest(backtest_in)

@router.post("/{task_id}/run", response_model=BacktestResult)
async def run_backtest(task_id: int, db: AsyncSession = Depends(get_db)):
    service = BacktestService(db)
    try:
        return await service.run_backtest(task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}")
async def cancel_backtest(task_id: int, db: AsyncSession = Depends(get_db)):
    service = BacktestService(db)
    success = await service.cancel_backtest(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel backtest")
    return {"message": "Backtest cancelled"}
```

- [ ] **Step 3: 创建分析API**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.strategy import BacktestResult
from app.schemas.strategy import MetricResult
from app.services import AnalyzeService

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.get("/{result_id}/metrics", response_model=MetricResult)
async def get_metrics(result_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.calculate_metrics(result)

@router.get("/{result_id}/charts")
async def get_charts(result_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.generate_charts(result)

@router.get("/{result_id}/risk")
async def get_risk_analysis(result_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.risk_analysis(result)

@router.get("/{result_id}/summary")
async def get_summary(result_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.get_summary(result)
```

- [ ] **Step 4: 更新 main.py**

```python
from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1 import data, master, datasource, strategy, backtest, analyze

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(data.router, prefix="/api/v1/data", tags=["data"])
app.include_router(master.router, prefix="/api/v1/master", tags=["master"])
app.include_router(datasource.router, prefix="/api/v1/datasources", tags=["datasources"])
app.include_router(strategy.router, prefix="/api/v1", tags=["strategies"])
app.include_router(backtest.router, prefix="/api/v1", tags=["backtests"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])

@app.get("/")
async def root():
    return {"message": "TradingStation API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

- [ ] **Step 5: 测试API**

Run: `cd /workspace/backend && uvicorn main:app --host 0.0.0.0 --port 8000`
Expected: Server starts successfully

- [ ] **Step 6: Commit**

```bash
git add app/api/v1/strategy.py app/api/v1/backtest.py app/api/v1/analyze.py main.py
git commit -m "feat: add strategy APIs"
```

---

## Task 7: 更新依赖和文档

**Files:**
- Modify: `/workspace/backend/requirements.txt`
- Modify: `/workspace/README.md`

- [ ] **Step 1: 更新 requirements.txt**

```txt
fastapi==0.115.0
uvicorn==0.32.0
sqlalchemy==2.0.35
alembic==1.14.0
psycopg2-binary==2.9.10
asyncpg==0.30.0
pydantic==2.10.0
pydantic-settings==2.6.0
python-dotenv==1.0.1
python-multipart==0.0.12
celery==5.4.0
redis==5.2.0
ccxt==4.4.30
yfinance==0.2.44
pandas==2.2.3
numpy==2.2.2
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.27.2
vectorbt==0.25.0
plotly==5.20.0
```

- [ ] **Step 2: 更新 README.md**

```markdown
# TradingStation

## Strategy Research Module

### API Endpoints

**Strategies**
- `GET /api/v1/strategies` - List strategies
- `GET /api/v1/strategies/{id}` - Get strategy
- `POST /api/v1/strategies` - Create strategy
- `PUT /api/v1/strategies/{id}` - Update strategy
- `DELETE /api/v1/strategies/{id}` - Delete strategy
- `POST /api/v1/strategies/validate` - Validate strategy code

**Backtests**
- `GET /api/v1/backtests` - List backtests
- `GET /api/v1/backtests/{id}` - Get backtest
- `POST /api/v1/backtests` - Create backtest
- `POST /api/v1/backtests/{id}/run` - Run backtest
- `DELETE /api/v1/backtests/{id}` - Cancel backtest

**Analysis**
- `GET /api/v1/analyze/{id}/metrics` - Get metrics
- `GET /api/v1/analyze/{id}/charts` - Get chart data
- `GET /api/v1/analyze/{id}/risk` - Get risk analysis
- `GET /api/v1/analyze/{id}/summary` - Get summary
```

- [ ] **Step 3: Commit**

```bash
git add backend/requirements.txt README.md
git commit -m "docs: update requirements and README"
```

---

## 执行选项

**Plan complete and saved to `docs/superpowers/plans/2026-05-05-strategy-research-plan.md`.**

**Two execution options:**

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
