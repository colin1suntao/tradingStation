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
