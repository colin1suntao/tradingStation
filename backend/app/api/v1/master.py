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
