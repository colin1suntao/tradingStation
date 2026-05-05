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
