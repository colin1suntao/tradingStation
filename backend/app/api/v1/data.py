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
