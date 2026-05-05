# 数据与主数据系统实现计划

&gt; **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建量化交易平台的统一数据与主数据系统，支持多资产、多数据源，为后续研究、回测等模块奠定基础。

**Architecture:** 分层插件化架构 - API层 / 业务逻辑层 / 数据源插件层 / 数据存储层。数据源完全插件化，统一查询接口屏蔽底层差异。

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy 2.0, PostgreSQL, TimescaleDB, Redis, Celery, Docker

---

## 文件结构映射

```
tradingStation/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── data.py          # 数据查询API
│   │   │       ├── master.py        # 主数据API
│   │   │       └── datasource.py    # 数据源管理API
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # 配置管理
│   │   │   └── database.py          # 数据库连接
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── master.py            # 主数据模型
│   │   │   └── market.py            # 市场数据模型
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── master.py
│   │   │   ├── market.py
│   │   │   └── datasource.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── data_service.py      # 数据查询服务
│   │   │   ├── master_service.py    # 主数据服务
│   │   │   └── sync_service.py      # 数据同步服务
│   │   ├── datasources/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # 数据源基类
│   │   │   ├── binance.py           # Binance数据源
│   │   │   ├── yahoo.py             # Yahoo Finance数据源
│   │   │   └── registry.py          # 数据源注册器
│   │   └── __init__.py
│   ├── alembic/
│   ├── tests/
│   ├── main.py                      # FastAPI入口
│   ├── requirements.txt
│   └── Dockerfile
├── docker/
│   └── postgres/
│       └── init.sql                 # 数据库初始化
├── docker-compose.yml
└── README.md
```

---

## Task 1: 项目初始化与基础设施

**Files:**
- Create: `/workspace/backend/requirements.txt`
- Create: `/workspace/backend/Dockerfile`
- Create: `/workspace/docker-compose.yml`
- Create: `/workspace/docker/postgres/init.sql`
- Create: `/workspace/backend/app/__init__.py`
- Create: `/workspace/backend/app/core/__init__.py`
- Create: `/workspace/backend/app/core/config.py`
- Create: `/workspace/backend/app/core/database.py`

- [ ] **Step 1: 创建 backend/requirements.txt**

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
```

- [ ] **Step 2: 创建 backend/Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

- [ ] **Step 3: 创建 docker-compose.yml**

```yaml
version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg16
    container_name: tradingstation-db
    environment:
      POSTGRES_USER: tradingstation
      POSTGRES_PASSWORD: tradingstation123
      POSTGRES_DB: tradingstation
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tradingstation -d tradingstation"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: tradingstation-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
    container_name: tradingstation-backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql+asyncpg://tradingstation:tradingstation123@postgres:5432/tradingstation
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

volumes:
  postgres_data:
  redis_data:
```

- [ ] **Step 4: 创建 docker/postgres/init.sql**

```sql
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

- [ ] **Step 5: 创建 app/core/config.py**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "TradingStation"
    debug: bool = True
    
    database_url: str = "postgresql+asyncpg://tradingstation:tradingstation123@localhost:5432/tradingstation"
    sync_database_url: str = "postgresql://tradingstation:tradingstation123@localhost:5432/tradingstation"
    
    redis_url: str = "redis://localhost:6379/0"
    
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

- [ ] **Step 6: 创建 app/core/database.py**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

- [ ] **Step 7: 创建其他 __init__.py 空文件**

```python
# backend/app/__init__.py
__version__ = "0.1.0"
```

```python
# backend/app/core/__init__.py
from .config import Settings, get_settings
from .database import Base, get_db, AsyncSessionLocal, engine

__all__ = ["Settings", "get_settings", "Base", "get_db", "AsyncSessionLocal", "engine"]
```

- [ ] **Step 8: 创建 backend/main.py**

```python
from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1 import data, master, datasource

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(data.router, prefix="/api/v1/data", tags=["data"])
app.include_router(master.router, prefix="/api/v1/master", tags=["master"])
app.include_router(datasource.router, prefix="/api/v1/datasources", tags=["datasources"])

@app.get("/")
async def root():
    return {"message": "TradingStation API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Task 2: 数据模型定义

**Files:**
- Create: `/workspace/backend/app/models/master.py`
- Create: `/workspace/backend/app/models/market.py`
- Create: `/workspace/backend/app/models/__init__.py`
- Create: `/workspace/backend/app/schemas/__init__.py`
- Create: `/workspace/backend/app/schemas/master.py`
- Create: `/workspace/backend/app/schemas/market.py`
- Create: `/workspace/backend/app/schemas/datasource.py`

- [ ] **Step 1: 创建 models/master.py**

```python
from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class AssetClass(str, enum.Enum):
    EQUITY = "equity"
    FUTURE = "future"
    OPTION = "option"
    FX = "fx"
    BOND = "bond"
    CRYPTO = "crypto"

class InstrumentType(str, enum.Enum):
    SPOT = "spot"
    MARGIN = "margin"
    SWAP = "swap"
    FUTURE = "future"
    OPTION = "option"
    ETF = "etf"

class ExchangeStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"

class Exchange(Base):
    __tablename__ = "exchanges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    country = Column(String(50))
    status = Column(Enum(ExchangeStatus), default=ExchangeStatus.ACTIVE)
    config = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    instruments = relationship("Instrument", back_populates="exchange")

class InstrumentStatus(str, enum.Enum):
    ACTIVE = "active"
    DELISTED = "delisted"
    SUSPENDED = "suspended"

class Instrument(Base):
    __tablename__ = "instruments"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False, index=True)
    name = Column(String(200))
    exchange_id = Column(Integer, ForeignKey("exchanges.id"), nullable=False)
    asset_class = Column(Enum(AssetClass), nullable=False, index=True)
    instrument_type = Column(Enum(InstrumentType), nullable=False)
    status = Column(Enum(InstrumentStatus), default=InstrumentStatus.ACTIVE)
    base_currency = Column(String(10))
    quote_currency = Column(String(10))
    price_precision = Column(Integer, default=2)
    size_precision = Column(Integer, default=8)
    min_size = Column(String(50))
    max_size = Column(String(50))
    contract_size = Column(String(50))
    listed_at = Column(DateTime(timezone=True))
    delisted_at = Column(DateTime(timezone=True))
    extra = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    exchange = relationship("Exchange", back_populates="instruments")

class DataSource(Base):
    __tablename__ = "datasources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False)
    config = Column(Text)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SyncTaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class SyncTask(Base):
    __tablename__ = "sync_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    datasource_id = Column(Integer, ForeignKey("datasources.id"))
    instrument_id = Column(Integer, ForeignKey("instruments.id"))
    timeframe = Column(String(10))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    status = Column(Enum(SyncTaskStatus), default=SyncTaskStatus.PENDING)
    records_count = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
```

- [ ] **Step 2: 创建 models/market.py**

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class KlineOHLCV(Base):
    __tablename__ = "kline_ohlcv"
    
    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    timeframe = Column(String(10), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(precision=30, scale=18))
    high = Column(Numeric(precision=30, scale=18))
    low = Column(Numeric(precision=30, scale=18))
    close = Column(Numeric(precision=30, scale=18))
    volume = Column(Numeric(precision=30, scale=18))
    turnover = Column(Numeric(precision=30, scale=18))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    instrument = relationship("Instrument")
    
    __table_args__ = (
        Index('idx_kline_instrument_timeframe', 'instrument_id', 'timeframe', 'timestamp', unique=True),
    )

class TickData(Base):
    __tablename__ = "tick_data"
    
    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    bid_price = Column(Numeric(precision=30, scale=18))
    ask_price = Column(Numeric(precision=30, scale=18))
    bid_size = Column(Numeric(precision=30, scale=18))
    ask_size = Column(Numeric(precision=30, scale=18))
    last_price = Column(Numeric(precision=30, scale=18))
    last_size = Column(Numeric(precision=30, scale=18))
    volume = Column(Numeric(precision=30, scale=18))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    instrument = relationship("Instrument")
    
    __table_args__ = (
        Index('idx_tick_instrument_timestamp', 'instrument_id', 'timestamp'),
    )
```

- [ ] **Step 3: 创建 models/__init__.py**

```python
from .master import (
    AssetClass,
    InstrumentType,
    ExchangeStatus,
    InstrumentStatus,
    SyncTaskStatus,
    Exchange,
    Instrument,
    DataSource,
    SyncTask,
)
from .market import KlineOHLCV, TickData

__all__ = [
    "AssetClass",
    "InstrumentType",
    "ExchangeStatus",
    "InstrumentStatus",
    "SyncTaskStatus",
    "Exchange",
    "Instrument",
    "DataSource",
    "SyncTask",
    "KlineOHLCV",
    "TickData",
]
```

- [ ] **Step 4: 创建 schemas/master.py**

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.master import (
    AssetClass,
    InstrumentType,
    ExchangeStatus,
    InstrumentStatus,
    SyncTaskStatus,
)

class ExchangeBase(BaseModel):
    name: str
    code: str
    country: Optional[str] = None
    status: ExchangeStatus = ExchangeStatus.ACTIVE
    config: Optional[str] = None

class ExchangeCreate(ExchangeBase):
    pass

class ExchangeUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    status: Optional[ExchangeStatus] = None
    config: Optional[str] = None

class Exchange(ExchangeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class InstrumentBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    exchange_id: int
    asset_class: AssetClass
    instrument_type: InstrumentType
    status: InstrumentStatus = InstrumentStatus.ACTIVE
    base_currency: Optional[str] = None
    quote_currency: Optional[str] = None
    price_precision: int = 2
    size_precision: int = 8
    min_size: Optional[str] = None
    max_size: Optional[str] = None
    contract_size: Optional[str] = None
    listed_at: Optional[datetime] = None
    delisted_at: Optional[datetime] = None
    extra: Optional[str] = None

class InstrumentCreate(InstrumentBase):
    pass

class InstrumentUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[InstrumentStatus] = None
    extra: Optional[str] = None

class Instrument(InstrumentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    exchange: Optional[Exchange] = None

class DataSourceBase(BaseModel):
    name: str
    code: str
    type: str
    config: Optional[str] = None
    status: bool = True

class DataSourceCreate(DataSourceBase):
    pass

class DataSource(DataSourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SyncTaskBase(BaseModel):
    datasource_id: Optional[int] = None
    instrument_id: Optional[int] = None
    timeframe: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class SyncTaskCreate(SyncTaskBase):
    pass

class SyncTask(SyncTaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: SyncTaskStatus
    records_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

- [ ] **Step 5: 创建 schemas/market.py**

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class KlineBase(BaseModel):
    instrument_id: int
    timeframe: str
    timestamp: datetime
    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    close: Optional[Decimal] = None
    volume: Optional[Decimal] = None
    turnover: Optional[Decimal] = None

class KlineCreate(KlineBase):
    pass

class Kline(KlineBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class KlineQuery(BaseModel):
    instrument_id: int
    timeframe: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: Optional[int] = 1000
    auto_fill: bool = False

class Quote(BaseModel):
    symbol: str
    last_price: Optional[Decimal] = None
    bid_price: Optional[Decimal] = None
    ask_price: Optional[Decimal] = None
    volume_24h: Optional[Decimal] = None
    change_24h: Optional[Decimal] = None
    timestamp: datetime
```

- [ ] **Step 6: 创建 schemas/datasource.py**

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SyncRequest(BaseModel):
    datasource_code: str
    instrument_id: Optional[int] = None
    symbol: Optional[str] = None
    timeframe: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class SyncResponse(BaseModel):
    task_id: int
    status: str
    message: str
```

- [ ] **Step 7: 创建 schemas/__init__.py**

```python
from .master import (
    Exchange,
    ExchangeCreate,
    ExchangeUpdate,
    Instrument,
    InstrumentCreate,
    InstrumentUpdate,
    DataSource,
    DataSourceCreate,
    SyncTask,
    SyncTaskCreate,
)
from .market import Kline, KlineCreate, KlineQuery, Quote
from .datasource import SyncRequest, SyncResponse

__all__ = [
    "Exchange",
    "ExchangeCreate",
    "ExchangeUpdate",
    "Instrument",
    "InstrumentCreate",
    "InstrumentUpdate",
    "DataSource",
    "DataSourceCreate",
    "SyncTask",
    "SyncTaskCreate",
    "Kline",
    "KlineCreate",
    "KlineQuery",
    "Quote",
    "SyncRequest",
    "SyncResponse",
]
```

---

## Task 3: 数据源插件层

**Files:**
- Create: `/workspace/backend/app/datasources/base.py`
- Create: `/workspace/backend/app/datasources/registry.py`
- Create: `/workspace/backend/app/datasources/binance.py`
- Create: `/workspace/backend/app/datasources/yahoo.py`
- Create: `/workspace/backend/app/datasources/__init__.py`

- [ ] **Step 1: 创建 datasources/base.py**

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

class TimeFrame(str, Enum):
    MIN_1 = "1m"
    MIN_5 = "5m"
    MIN_15 = "15m"
    MIN_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"

class DataSource(ABC):
    """数据源基类，所有数据源必须实现此接口"""
    
    @property
    @abstractmethod
    def name(self) -&gt; str:
        """数据源名称"""
        pass
    
    @property
    @abstractmethod
    def code(self) -&gt; str:
        """数据源唯一标识"""
        pass
    
    @abstractmethod
    def get_exchanges(self) -&gt; List[Dict[str, Any]]:
        """获取支持的交易所列表"""
        pass
    
    @abstractmethod
    def get_instruments(self, exchange_code: Optional[str] = None) -&gt; List[Dict[str, Any]]:
        """获取标的列表"""
        pass
    
    @abstractmethod
    def get_klines(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -&gt; List[Dict[str, Any]]:
        """获取K线数据"""
        pass
    
    @abstractmethod
    def get_realtime_quote(self, symbol: str) -&gt; Optional[Dict[str, Any]]:
        """获取实时行情"""
        pass
    
    def normalize_symbol(self, symbol: str) -&gt; str:
        """标准化标的代码"""
        return symbol
    
    def normalize_timeframe(self, timeframe: TimeFrame) -&gt; str:
        """标准化时间周期"""
        return timeframe.value
```

- [ ] **Step 2: 创建 datasources/registry.py**

```python
from typing import Dict, List, Optional
from .base import DataSource

class DataSourceRegistry:
    _registry: Dict[str, DataSource] = {}
    
    @classmethod
    def register(cls, datasource: DataSource):
        """注册数据源"""
        cls._registry[datasource.code] = datasource
    
    @classmethod
    def get(cls, code: str) -&gt; Optional[DataSource]:
        """获取指定数据源"""
        return cls._registry.get(code)
    
    @classmethod
    def list_all(cls) -&gt; List[DataSource]:
        """列出所有已注册的数据源"""
        return list(cls._registry.values())
    
    @classmethod
    def list_codes(cls) -&gt; List[str]:
        """列出所有已注册的数据源代码"""
        return list(cls._registry.keys())
```

- [ ] **Step 3: 创建 datasources/binance.py**

```python
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import ccxt
from .base import DataSource, TimeFrame

class BinanceDataSource(DataSource):
    """Binance 数据源"""
    
    def __init__(self):
        self._exchange = ccxt.binance({'enableRateLimit': True})
    
    @property
    def name(self) -&gt; str:
        return "Binance"
    
    @property
    def code(self) -&gt; str:
        return "binance"
    
    def get_exchanges(self) -&gt; List[Dict[str, Any]]:
        return [
            {
                "name": "Binance",
                "code": "binance",
                "country": "Global",
            }
        ]
    
    def get_instruments(self, exchange_code: Optional[str] = None) -&gt; List[Dict[str, Any]]:
        instruments = []
        try:
            markets = self._exchange.load_markets()
            for symbol, market in markets.items():
                if market.get('active'):
                    instruments.append({
                        "symbol": symbol,
                        "name": symbol,
                        "exchange_code": "binance",
                        "asset_class": "crypto",
                        "instrument_type": market.get('type', 'spot'),
                        "base_currency": market.get('base'),
                        "quote_currency": market.get('quote'),
                        "price_precision": market.get('precision', {}).get('price', 8),
                        "size_precision": market.get('precision', {}).get('amount', 8),
                        "min_size": str(market.get('limits', {}).get('amount', {}).get('min', '')),
                        "max_size": str(market.get('limits', {}).get('amount', {}).get('max', '')),
                    })
        except Exception as e:
            print(f"Error loading Binance instruments: {e}")
        return instruments
    
    def get_klines(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = 1000
    ) -&gt; List[Dict[str, Any]]:
        klines = []
        try:
            tf_map = {
                TimeFrame.MIN_1: '1m',
                TimeFrame.MIN_5: '5m',
                TimeFrame.MIN_15: '15m',
                TimeFrame.MIN_30: '30m',
                TimeFrame.HOUR_1: '1h',
                TimeFrame.HOUR_2: '2h',
                TimeFrame.HOUR_4: '4h',
                TimeFrame.HOUR_6: '6h',
                TimeFrame.HOUR_12: '12h',
                TimeFrame.DAY_1: '1d',
                TimeFrame.WEEK_1: '1w',
                TimeFrame.MONTH_1: '1M',
            }
            tf = tf_map.get(timeframe, '1h')
            
            since = int(start_time.timestamp() * 1000) if start_time else None
            
            ohlcv = self._exchange.fetch_ohlcv(symbol, tf, since=since, limit=limit)
            
            for candle in ohlcv:
                klines.append({
                    "timestamp": datetime.fromtimestamp(candle[0] / 1000),
                    "open": candle[1],
                    "high": candle[2],
                    "low": candle[3],
                    "close": candle[4],
                    "volume": candle[5],
                })
        except Exception as e:
            print(f"Error fetching Binance klines: {e}")
        return klines
    
    def get_realtime_quote(self, symbol: str) -&gt; Optional[Dict[str, Any]]:
        try:
            ticker = self._exchange.fetch_ticker(symbol)
            return {
                "symbol": symbol,
                "last_price": ticker.get('last'),
                "bid_price": ticker.get('bid'),
                "ask_price": ticker.get('ask'),
                "volume_24h": ticker.get('quoteVolume'),
                "change_24h": ticker.get('percentage'),
                "timestamp": datetime.fromtimestamp(ticker.get('timestamp', 0) / 1000),
            }
        except Exception as e:
            print(f"Error fetching Binance quote: {e}")
            return None
```

- [ ] **Step 4: 创建 datasources/yahoo.py**

```python
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import yfinance as yf
from .base import DataSource, TimeFrame

class YahooFinanceDataSource(DataSource):
    """Yahoo Finance 数据源"""
    
    @property
    def name(self) -&gt; str:
        return "Yahoo Finance"
    
    @property
    def code(self) -&gt; str:
        return "yahoo"
    
    def get_exchanges(self) -&gt; List[Dict[str, Any]]:
        return [
            {
                "name": "NYSE",
                "code": "nyse",
                "country": "USA",
            },
            {
                "name": "NASDAQ",
                "code": "nasdaq",
                "country": "USA",
            },
        ]
    
    def get_instruments(self, exchange_code: Optional[str] = None) -&gt; List[Dict[str, Any]]:
        instruments = []
        popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "SPY", "QQQ"]
        for symbol in popular_stocks:
            instruments.append({
                "symbol": symbol,
                "name": symbol,
                "exchange_code": "nasdaq",
                "asset_class": "equity",
                "instrument_type": "spot",
                "base_currency": "USD",
                "quote_currency": "USD",
                "price_precision": 2,
                "size_precision": 4,
            })
        return instruments
    
    def get_klines(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -&gt; List[Dict[str, Any]]:
        klines = []
        try:
            tf_map = {
                TimeFrame.MIN_1: '1m',
                TimeFrame.MIN_5: '5m',
                TimeFrame.MIN_15: '15m',
                TimeFrame.MIN_30: '30m',
                TimeFrame.HOUR_1: '1h',
                TimeFrame.HOUR_4: '1h',
                TimeFrame.DAY_1: '1d',
                TimeFrame.WEEK_1: '1wk',
                TimeFrame.MONTH_1: '1mo',
            }
            tf = tf_map.get(timeframe, '1d')
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='max' if not start_time else None, 
                                interval=tf,
                                start=start_time,
                                end=end_time)
            
            if limit:
                hist = hist.tail(limit)
            
            for idx, row in hist.iterrows():
                klines.append({
                    "timestamp": idx.to_pydatetime(),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": float(row['Volume']),
                })
        except Exception as e:
            print(f"Error fetching Yahoo Finance klines: {e}")
        return klines
    
    def get_realtime_quote(self, symbol: str) -&gt; Optional[Dict[str, Any]]:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                "symbol": symbol,
                "last_price": info.get('currentPrice'),
                "bid_price": info.get('bid'),
                "ask_price": info.get('ask'),
                "volume_24h": info.get('volume'),
                "change_24h": info.get('changePercent'),
                "timestamp": datetime.now(),
            }
        except Exception as e:
            print(f"Error fetching Yahoo Finance quote: {e}")
            return None
```

- [ ] **Step 5: 创建 datasources/__init__.py**

```python
from .base import DataSource, TimeFrame
from .registry import DataSourceRegistry
from .binance import BinanceDataSource
from .yahoo import YahooFinanceDataSource

registry = DataSourceRegistry()
registry.register(BinanceDataSource())
registry.register(YahooFinanceDataSource())

__all__ = [
    "DataSource",
    "TimeFrame",
    "DataSourceRegistry",
    "BinanceDataSource",
    "YahooFinanceDataSource",
    "registry",
]
```

---

## Task 4: 业务逻辑服务层

**Files:**
- Create: `/workspace/backend/app/services/__init__.py`
- Create: `/workspace/backend/app/services/master_service.py`
- Create: `/workspace/backend/app/services/data_service.py`
- Create: `/workspace/backend/app/services/sync_service.py`

- [ ] **Step 1: 创建 services/master_service.py**

```python
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.models.master import (
    Exchange,
    Instrument,
    DataSource,
    SyncTask,
    AssetClass,
    InstrumentType,
)
from app.schemas.master import (
    ExchangeCreate,
    ExchangeUpdate,
    InstrumentCreate,
    InstrumentUpdate,
    DataSourceCreate,
)

class MasterDataService:
    """主数据服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_exchanges(self) -&gt; List[Exchange]:
        result = await self.db.execute(select(Exchange))
        return list(result.scalars().all())
    
    async def get_exchange_by_code(self, code: str) -&gt; Optional[Exchange]:
        result = await self.db.execute(select(Exchange).where(Exchange.code == code))
        return result.scalar_one_or_none()
    
    async def create_exchange(self, exchange_in: ExchangeCreate) -&gt; Exchange:
        exchange = Exchange(**exchange_in.model_dump())
        self.db.add(exchange)
        await self.db.commit()
        await self.db.refresh(exchange)
        return exchange
    
    async def update_exchange(self, exchange_id: int, exchange_in: ExchangeUpdate) -&gt; Optional[Exchange]:
        exchange = await self.db.get(Exchange, exchange_id)
        if not exchange:
            return None
        
        update_data = exchange_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(exchange, key, value)
        
        await self.db.commit()
        await self.db.refresh(exchange)
        return exchange
    
    async def get_instruments(
        self,
        exchange_id: Optional[int] = None,
        asset_class: Optional[AssetClass] = None,
        instrument_type: Optional[InstrumentType] = None,
        symbol: Optional[str] = None,
    ) -&gt; List[Instrument]:
        query = select(Instrument).options(selectinload(Instrument.exchange))
        
        if exchange_id:
            query = query.where(Instrument.exchange_id == exchange_id)
        if asset_class:
            query = query.where(Instrument.asset_class == asset_class)
        if instrument_type:
            query = query.where(Instrument.instrument_type == instrument_type)
        if symbol:
            query = query.where(Instrument.symbol.ilike(f"%{symbol}%"))
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_instrument_by_id(self, instrument_id: int) -&gt; Optional[Instrument]:
        result = await self.db.execute(
            select(Instrument).options(selectinload(Instrument.exchange)).where(Instrument.id == instrument_id)
        )
        return result.scalar_one_or_none()
    
    async def get_instrument_by_symbol_and_exchange(self, symbol: str, exchange_code: str) -&gt; Optional[Instrument]:
        result = await self.db.execute(
            select(Instrument)
            .options(selectinload(Instrument.exchange))
            .join(Exchange)
            .where(Instrument.symbol == symbol, Exchange.code == exchange_code)
        )
        return result.scalar_one_or_none()
    
    async def create_instrument(self, instrument_in: InstrumentCreate) -&gt; Instrument:
        instrument = Instrument(**instrument_in.model_dump())
        self.db.add(instrument)
        await self.db.commit()
        await self.db.refresh(instrument)
        return instrument
    
    async def update_instrument(self, instrument_id: int, instrument_in: InstrumentUpdate) -&gt; Optional[Instrument]:
        instrument = await self.db.get(Instrument, instrument_id)
        if not instrument:
            return None
        
        update_data = instrument_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(instrument, key, value)
        
        await self.db.commit()
        await self.db.refresh(instrument)
        return instrument
    
    async def get_datasources(self) -&gt; List[DataSource]:
        result = await self.db.execute(select(DataSource))
        return list(result.scalars().all())
    
    async def get_datasource_by_code(self, code: str) -&gt; Optional[DataSource]:
        result = await self.db.execute(select(DataSource).where(DataSource.code == code))
        return result.scalar_one_or_none()
    
    async def create_datasource(self, datasource_in: DataSourceCreate) -&gt; DataSource:
        datasource = DataSource(**datasource_in.model_dump())
        self.db.add(datasource)
        await self.db.commit()
        await self.db.refresh(datasource)
        return datasource
    
    async def get_sync_tasks(self, limit: int = 100) -&gt; List[SyncTask]:
        result = await self.db.execute(
            select(SyncTask).order_by(SyncTask.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_sync_task(self, task_id: int) -&gt; Optional[SyncTask]:
        return await self.db.get(SyncTask, task_id)
```

- [ ] **Step 2: 创建 services/data_service.py**

```python
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.market import KlineOHLCV
from app.models.master import Instrument
from app.schemas.market import KlineQuery, KlineCreate
from app.datasources import registry, TimeFrame

class DataService:
    """数据查询服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_klines(
        self,
        query: KlineQuery,
    ) -&gt; List[KlineOHLCV]:
        stmt = select(KlineOHLCV).where(
            and_(
                KlineOHLCV.instrument_id == query.instrument_id,
                KlineOHLCV.timeframe == query.timeframe,
            )
        )
        
        if query.start_time:
            stmt = stmt.where(KlineOHLCV.timestamp &gt;= query.start_time)
        if query.end_time:
            stmt = stmt.where(KlineOHLCV.timestamp &lt;= query.end_time)
        
        stmt = stmt.order_by(KlineOHLCV.timestamp.desc())
        
        if query.limit:
            stmt = stmt.limit(query.limit)
        
        result = await self.db.execute(stmt)
        klines = list(reversed(result.scalars().all()))
        
        if query.auto_fill and self._need_fill(klines, query):
            await self._fill_missing_data(query)
            result = await self.db.execute(stmt)
            klines = list(reversed(result.scalars().all()))
        
        return klines
    
    def _need_fill(self, klines: List[KlineOHLCV], query: KlineQuery) -&gt; bool:
        if not klines:
            return True
        
        if query.start_time and klines[0].timestamp &gt; query.start_time:
            return True
        
        if query.end_time and klines[-1].timestamp &lt; query.end_time:
            return True
        
        return False
    
    async def _fill_missing_data(self, query: KlineQuery):
        pass
    
    async def save_klines(self, klines: List[KlineCreate]) -&gt; int:
        saved = 0
        for kline_in in klines:
            stmt = select(KlineOHLCV).where(
                and_(
                    KlineOHLCV.instrument_id == kline_in.instrument_id,
                    KlineOHLCV.timeframe == kline_in.timeframe,
                    KlineOHLCV.timestamp == kline_in.timestamp,
                )
            )
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                for key, value in kline_in.model_dump(exclude_unset=True).items():
                    setattr(existing, key, value)
            else:
                kline = KlineOHLCV(**kline_in.model_dump())
                self.db.add(kline)
            saved += 1
        
        await self.db.commit()
        return saved
```

- [ ] **Step 3: 创建 services/sync_service.py**

```python
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.master import SyncTask, SyncTaskStatus, Instrument
from app.models.market import KlineOHLCV
from app.schemas.master import SyncTaskCreate
from app.datasources import registry, TimeFrame
from .data_service import DataService

class SyncService:
    """数据同步服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.data_service = DataService(db)
    
    async def create_sync_task(
        self,
        datasource_code: str,
        instrument_id: Optional[int] = None,
        symbol: Optional[str] = None,
        timeframe: str = "1d",
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -&gt; SyncTask:
        task_in = SyncTaskCreate(
            instrument_id=instrument_id,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )
        task = SyncTask(**task_in.model_dump())
        task.status = SyncTaskStatus.PENDING
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def run_sync_task(self, task_id: int, datasource_code: str) -&gt; SyncTask:
        task = await self.db.get(SyncTask, task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        datasource = registry.get(datasource_code)
        if not datasource:
            raise ValueError(f"Datasource {datasource_code} not found")
        
        task.status = SyncTaskStatus.RUNNING
        task.started_at = datetime.now()
        await self.db.commit()
        
        try:
            instrument = await self.db.get(Instrument, task.instrument_id)
            if not instrument:
                raise ValueError(f"Instrument {task.instrument_id} not found")
            
            tf = TimeFrame(task.timeframe)
            
            end_time = task.end_time or datetime.now()
            start_time = task.start_time or (end_time - timedelta(days=365))
            
            klines_data = datasource.get_klines(
                symbol=instrument.symbol,
                timeframe=tf,
                start_time=start_time,
                end_time=end_time,
            )
            
            from app.schemas.market import KlineCreate
            klines_create = []
            for k in klines_data:
                klines_create.append(KlineCreate(
                    instrument_id=instrument.id,
                    timeframe=task.timeframe,
                    timestamp=k["timestamp"],
                    open=k.get("open"),
                    high=k.get("high"),
                    low=k.get("low"),
                    close=k.get("close"),
                    volume=k.get("volume"),
                    turnover=k.get("turnover"),
                ))
            
            saved_count = await self.data_service.save_klines(klines_create)
            
            task.status = SyncTaskStatus.COMPLETED
            task.records_count = saved_count
            task.completed_at = datetime.now()
            
        except Exception as e:
            task.status = SyncTaskStatus.FAILED
            task.error_message = str(e)
            task.completed_at = datetime.now()
        
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def sync_instruments_from_datasource(self, datasource_code: str):
        datasource = registry.get(datasource_code)
        if not datasource:
            raise ValueError(f"Datasource {datasource_code} not found")
        
        from .master_service import MasterDataService
        master_service = MasterDataService(self.db)
        
        exchanges = datasource.get_exchanges()
        for exch_data in exchanges:
            existing = await master_service.get_exchange_by_code(exch_data["code"])
            if not existing:
                from app.schemas.master import ExchangeCreate
                await master_service.create_exchange(ExchangeCreate(
                    name=exch_data["name"],
                    code=exch_data["code"],
                    country=exch_data.get("country"),
                ))
        
        instruments = datasource.get_instruments()
        for inst_data in instruments:
            exchange = await master_service.get_exchange_by_code(inst_data["exchange_code"])
            if exchange:
                existing = await master_service.get_instrument_by_symbol_and_exchange(
                    inst_data["symbol"], inst_data["exchange_code"]
                )
                if not existing:
                    from app.schemas.master import InstrumentCreate
                    await master_service.create_instrument(InstrumentCreate(
                        symbol=inst_data["symbol"],
                        name=inst_data.get("name", inst_data["symbol"]),
                        exchange_id=exchange.id,
                        asset_class=inst_data["asset_class"],
                        instrument_type=inst_data["instrument_type"],
                        base_currency=inst_data.get("base_currency"),
                        quote_currency=inst_data.get("quote_currency"),
                        price_precision=inst_data.get("price_precision", 2),
                        size_precision=inst_data.get("size_precision", 8),
                        min_size=inst_data.get("min_size"),
                        max_size=inst_data.get("max_size"),
                    ))
```

- [ ] **Step 4: 创建 services/__init__.py**

```python
from .master_service import MasterDataService
from .data_service import DataService
from .sync_service import SyncService

__all__ = [
    "MasterDataService",
    "DataService",
    "SyncService",
]
```

---

## Task 5: API 层

**Files:**
- Create: `/workspace/backend/app/api/__init__.py`
- Create: `/workspace/backend/app/api/v1/__init__.py`
- Create: `/workspace/backend/app/api/v1/master.py`
- Create: `/workspace/backend/app/api/v1/data.py`
- Create: `/workspace/backend/app/api/v1/datasource.py`

- [ ] **Step 1: 创建 api/v1/__init__.py**

```python
# Empty
```

- [ ] **Step 2: 创建 api/__init__.py**

```python
# Empty
```

- [ ] **Step 3: 创建 api/v1/master.py**

```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.master import AssetClass, InstrumentType
from app.schemas.master import (
    Exchange,
    ExchangeCreate,
    ExchangeUpdate,
    Instrument,
    InstrumentCreate,
    InstrumentUpdate,
    DataSource,
    SyncTask,
)
from app.services import MasterDataService

router = APIRouter()

@router.get("/exchanges", response_model=List[Exchange])
async def list_exchanges(db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    return await service.get_exchanges()

@router.get("/exchanges/{code}", response_model=Exchange)
async def get_exchange(code: str, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    exchange = await service.get_exchange_by_code(code)
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return exchange

@router.post("/exchanges", response_model=Exchange)
async def create_exchange(exchange_in: ExchangeCreate, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    existing = await service.get_exchange_by_code(exchange_in.code)
    if existing:
        raise HTTPException(status_code=400, detail="Exchange already exists")
    return await service.create_exchange(exchange_in)

@router.put("/exchanges/{exchange_id}", response_model=Exchange)
async def update_exchange(exchange_id: int, exchange_in: ExchangeUpdate, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    exchange = await service.update_exchange(exchange_id, exchange_in)
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return exchange

@router.get("/instruments", response_model=List[Instrument])
async def list_instruments(
    exchange_id: Optional[int] = Query(None),
    asset_class: Optional[AssetClass] = Query(None),
    instrument_type: Optional[InstrumentType] = Query(None),
    symbol: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = MasterDataService(db)
    return await service.get_instruments(
        exchange_id=exchange_id,
        asset_class=asset_class,
        instrument_type=instrument_type,
        symbol=symbol,
    )

@router.get("/instruments/{instrument_id}", response_model=Instrument)
async def get_instrument(instrument_id: int, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    instrument = await service.get_instrument_by_id(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return instrument

@router.post("/instruments", response_model=Instrument)
async def create_instrument(instrument_in: InstrumentCreate, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    return await service.create_instrument(instrument_in)

@router.put("/instruments/{instrument_id}", response_model=Instrument)
async def update_instrument(instrument_id: int, instrument_in: InstrumentUpdate, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    instrument = await service.update_instrument(instrument_id, instrument_in)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return instrument

@router.get("/datasources", response_model=List[DataSource])
async def list_datasources(db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    return await service.get_datasources()

@router.get("/sync-tasks", response_model=List[SyncTask])
async def list_sync_tasks(limit: int = 100, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    return await service.get_sync_tasks(limit=limit)

@router.get("/sync-tasks/{task_id}", response_model=SyncTask)
async def get_sync_task(task_id: int, db: AsyncSession = Depends(get_db)):
    service = MasterDataService(db)
    task = await service.get_sync_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

- [ ] **Step 4: 创建 api/v1/data.py**

```python
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.market import Kline, KlineQuery, Quote
from app.services import DataService
from app.datasources import registry

router = APIRouter()

@router.get("/klines", response_model=List[Kline])
async def get_klines(
    instrument_id: int,
    timeframe: str,
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: Optional[int] = 1000,
    auto_fill: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    service = DataService(db)
    query = KlineQuery(
        instrument_id=instrument_id,
        timeframe=timeframe,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
        auto_fill=auto_fill,
    )
    return await service.get_klines(query)

@router.get("/quote", response_model=Quote)
async def get_quote(symbol: str, datasource_code: str = "binance"):
    datasource = registry.get(datasource_code)
    if not datasource:
        raise HTTPException(status_code=404, detail="Datasource not found")
    
    quote = datasource.get_realtime_quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    return Quote(**quote)
```

- [ ] **Step 5: 创建 api/v1/datasource.py**

```python
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.datasource import SyncRequest, SyncResponse
from app.services import SyncService
from app.datasources import registry

router = APIRouter()

@router.get("/")
async def list_available_datasources():
    datasources = registry.list_all()
    return [
        {"code": ds.code, "name": ds.name}
        for ds in datasources
    ]

@router.post("/sync-instruments")
async def sync_instruments(datasource_code: str, db: AsyncSession = Depends(get_db)):
    datasource = registry.get(datasource_code)
    if not datasource:
        raise HTTPException(status_code=404, detail="Datasource not found")
    
    service = SyncService(db)
    await service.sync_instruments_from_datasource(datasource_code)
    
    return {"message": "Instruments sync completed", "datasource": datasource_code}

@router.post("/sync", response_model=SyncResponse)
async def sync_data(
    request: SyncRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    datasource = registry.get(request.datasource_code)
    if not datasource:
        raise HTTPException(status_code=404, detail="Datasource not found")
    
    service = SyncService(db)
    
    if request.symbol and not request.instrument_id:
        from app.services import MasterDataService
        master_service = MasterDataService(db)
        instruments = await master_service.get_instruments(symbol=request.symbol)
        if instruments:
            request.instrument_id = instruments[0].id
    
    if not request.instrument_id:
        raise HTTPException(status_code=400, detail="instrument_id or symbol required")
    
    task = await service.create_sync_task(
        datasource_code=request.datasource_code,
        instrument_id=request.instrument_id,
        timeframe=request.timeframe,
        start_time=request.start_time,
        end_time=request.end_time,
    )
    
    background_tasks.add_task(service.run_sync_task, task.id, request.datasource_code)
    
    return SyncResponse(
        task_id=task.id,
        status=task.status.value,
        message="Sync task created",
    )
```

---

## Task 6: 数据库迁移配置

**Files:**
- Create: `/workspace/backend/alembic.ini`
- Create: `/workspace/backend/alembic/env.py`
- Create: `/workspace/backend/alembic/script.py.mako`
- Create: `/workspace/backend/alembic/versions/__init__.py`

- [ ] **Step 1: 创建 alembic.ini**

```ini
[alembic]
script_location = alembic
file_template = %%(year)d%%(month).2d%%(day).2d_%(hour).2d%%(minute).2d_%(rev)s_%(slug)s
prepend_sys_path = .
sqlalchemy.url = postgresql://tradingstation:tradingstation123@localhost:5432/tradingstation

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

- [ ] **Step 2: 创建 alembic/env.py**

```python
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import Base
from app.models import master, market
from app.core.config import get_settings

config = context.config
settings = get_settings()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.sync_database_url)

target_metadata = Base.metadata

def run_migrations_offline() -&gt; None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -&gt; None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -&gt; None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -&gt; None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 3: 创建 alembic/script.py.mako**

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -&gt; None:
    ${upgrades if upgrades else "pass"}


def downgrade() -&gt; None:
    ${downgrades if downgrades else "pass"}
```

- [ ] **Step 4: 创建 alembic/versions/__init__.py**

```python
# Empty
```

---

## Task 7: 初始化迁移脚本与种子数据

**Files:**
- Create: `/workspace/backend/alembic/versions/001_initial_schema.py`
- Create: `/workspace/backend/init_db.py`

- [ ] **Step 1: 创建初始迁移脚本**

```python
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


def upgrade() -&gt; None:
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
```

- [ ] **Step 2: 创建 init_db.py**

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.database import Base
from app.core.config import get_settings
from app.models.master import Exchange, DataSource

async def init_db():
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
```

---

## Task 8: 项目文档与README

**Files:**
- Modify: `/workspace/README.md`
- Create: `/workspace/CONTRIBUTING.md`

- [ ] **Step 1: 更新 README.md**

```markdown
# TradingStation

面向个人量化团队的全球多资产、多 Agent 协作量化交易平台。

## 架构设计

- **后端**: Python 3.11+ / FastAPI / SQLAlchemy 2.0
- **数据库**: PostgreSQL + TimescaleDB (时序数据优化)
- **前端**: React + TypeScript (待开发)
- **部署**: Docker + Docker Compose

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 启动开发环境

```bash
# 克隆项目
git clone https://github.com/your-org/tradingstation.git
cd tradingstation

# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

### 访问服务

- API 文档: http://localhost:8000/docs
- API 健康检查: http://localhost:8000/health
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 初始化数据

```bash
# 进入 backend 容器
docker-compose exec backend bash

# 同步标的数据 (Binance)
curl -X POST "http://localhost:8000/api/v1/datasources/sync-instruments?datasource_code=binance"

# 同步标的数据 (Yahoo Finance)
curl -X POST "http://localhost:8000/api/v1/datasources/sync-instruments?datasource_code=yahoo"
```

## API 文档

### 主数据 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/master/exchanges` | GET | 获取交易所列表 |
| `/api/v1/master/exchanges/{code}` | GET | 获取指定交易所 |
| `/api/v1/master/instruments` | GET | 获取标的列表 |
| `/api/v1/master/instruments/{id}` | GET | 获取指定标的 |

### 数据查询 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/data/klines` | GET | 获取K线数据 |
| `/api/v1/data/quote` | GET | 获取实时行情 |

### 数据源管理 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/datasources` | GET | 列出可用数据源 |
| `/api/v1/datasources/sync-instruments` | POST | 同步标的数据 |
| `/api/v1/datasources/sync` | POST | 同步K线数据 |
| `/api/v1/datasources/sync-tasks` | GET | 查看同步任务 |

## 项目结构

```
tradingstation/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic 模型
│   │   ├── services/    # 业务逻辑
│   │   └── datasources/ # 数据源插件
│   ├── alembic/         # 数据库迁移
│   └── main.py
├── frontend/            # 前端代码 (待开发)
├── docker/              # Docker 配置
├── docker-compose.yml
└── README.md
```

## 支持的数据源

- **Binance**: 加密货币现货、合约
- **Yahoo Finance**: 美股、ETF
- 更多数据源可以通过插件扩展

## 支持的资产类型

- ✅ 股票 / ETF
- ✅ 期货 / 期权
- ✅ 外汇 / 债券
- ✅ 加密货币

## 开发计划

- [x] 统一数据与主数据系统
- [ ] 策略研究环境 (JupyterLab 集成)
- [ ] 回测引擎
- [ ] 组合管理
- [ ] 风险管理
- [ ] 模拟交易
- [ ] 实盘交易对接
- [ ] 多 Agent 协作框架
- [ ] 监控与复盘
- [ ] 前端界面

## 贡献指南

请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 许可证

MIT License
```

- [ ] **Step 2: 创建 CONTRIBUTING.md**

```markdown
# 贡献指南

欢迎贡献！请先阅读本文档。

## 开发环境设置

```bash
# 安装 Python 依赖
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 本地启动 (使用 Docker 数据库)
docker-compose up -d postgres redis
uvicorn main:app --reload
```

## 代码规范

- 使用 `black` 格式化 Python 代码
- 使用 `isort` 整理 import
- 使用 `mypy` 进行类型检查
- 遵循 FastAPI 最佳实践

## 提交规范

使用 conventional commits:

```
<type>(<scope>): <subject>

<type>: feat, fix, docs, style, refactor, test, chore
```

## 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "Add xxx table"

# 执行迁移
alembic upgrade head
```

## 测试

```bash
# 运行测试
pytest tests/
```
```

---

## 计划完成！

现在你可以选择执行方式:

1. **Subagent-Driven (推荐)**: 使用子代理逐个执行任务，中间进行审核
2. **Inline Execution**: 在当前会话中使用执行计划技能批量执行任务

请选择你偏好的方式！

