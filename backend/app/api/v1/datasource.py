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
