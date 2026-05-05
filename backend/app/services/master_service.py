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
    
    async def get_exchanges(self) -> List[Exchange]:
        result = await self.db.execute(select(Exchange))
        return list(result.scalars().all())
    
    async def get_exchange_by_code(self, code: str) -> Optional[Exchange]:
        result = await self.db.execute(select(Exchange).where(Exchange.code == code))
        return result.scalar_one_or_none()
    
    async def create_exchange(self, exchange_in: ExchangeCreate) -> Exchange:
        exchange = Exchange(**exchange_in.model_dump())
        self.db.add(exchange)
        await self.db.commit()
        await self.db.refresh(exchange)
        return exchange
    
    async def update_exchange(self, exchange_id: int, exchange_in: ExchangeUpdate) -> Optional[Exchange]:
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
    ) -> List[Instrument]:
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
    
    async def get_instrument_by_id(self, instrument_id: int) -> Optional[Instrument]:
        result = await self.db.execute(
            select(Instrument).options(selectinload(Instrument.exchange)).where(Instrument.id == instrument_id)
        )
        return result.scalar_one_or_none()
    
    async def get_instrument_by_symbol_and_exchange(self, symbol: str, exchange_code: str) -> Optional[Instrument]:
        result = await self.db.execute(
            select(Instrument)
            .options(selectinload(Instrument.exchange))
            .join(Exchange)
            .where(Instrument.symbol == symbol, Exchange.code == exchange_code)
        )
        return result.scalar_one_or_none()
    
    async def create_instrument(self, instrument_in: InstrumentCreate) -> Instrument:
        instrument = Instrument(**instrument_in.model_dump())
        self.db.add(instrument)
        await self.db.commit()
        await self.db.refresh(instrument)
        return instrument
    
    async def update_instrument(self, instrument_id: int, instrument_in: InstrumentUpdate) -> Optional[Instrument]:
        instrument = await self.db.get(Instrument, instrument_id)
        if not instrument:
            return None
        
        update_data = instrument_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(instrument, key, value)
        
        await self.db.commit()
        await self.db.refresh(instrument)
        return instrument
    
    async def get_datasources(self) -> List[DataSource]:
        result = await self.db.execute(select(DataSource))
        return list(result.scalars().all())
    
    async def get_datasource_by_code(self, code: str) -> Optional[DataSource]:
        result = await self.db.execute(select(DataSource).where(DataSource.code == code))
        return result.scalar_one_or_none()
    
    async def create_datasource(self, datasource_in: DataSourceCreate) -> DataSource:
        datasource = DataSource(**datasource_in.model_dump())
        self.db.add(datasource)
        await self.db.commit()
        await self.db.refresh(datasource)
        return datasource
    
    async def get_sync_tasks(self, limit: int = 100) -> List[SyncTask]:
        result = await self.db.execute(
            select(SyncTask).order_by(SyncTask.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_sync_task(self, task_id: int) -> Optional[SyncTask]:
        return await self.db.get(SyncTask, task_id)
