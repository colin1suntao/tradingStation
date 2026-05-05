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
