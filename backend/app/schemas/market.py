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
