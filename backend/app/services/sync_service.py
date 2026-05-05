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
    ) -> SyncTask:
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
    
    async def run_sync_task(self, task_id: int, datasource_code: str) -> SyncTask:
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
