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
    ) -> List[KlineOHLCV]:
        stmt = select(KlineOHLCV).where(
            and_(
                KlineOHLCV.instrument_id == query.instrument_id,
                KlineOHLCV.timeframe == query.timeframe,
            )
        )
        
        if query.start_time:
            stmt = stmt.where(KlineOHLCV.timestamp >= query.start_time)
        if query.end_time:
            stmt = stmt.where(KlineOHLCV.timestamp <= query.end_time)
        
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
    
    def _need_fill(self, klines: List[KlineOHLCV], query: KlineQuery) -> bool:
        if not klines:
            return True
        
        if query.start_time and klines[0].timestamp > query.start_time:
            return True
        
        if query.end_time and klines[-1].timestamp < query.end_time:
            return True
        
        return False
    
    async def _fill_missing_data(self, query: KlineQuery):
        pass
    
    async def save_klines(self, klines: List[KlineCreate]) -> int:
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
