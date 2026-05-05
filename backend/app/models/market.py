from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class KlineOHLCV(Base):
    __tablename__ = "kline_ohlcv"
    
    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    timeframe = Column(String(10), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(precision=30, scale=18))
    high = Column(Numeric(precision=30, scale=18))
    low = Column(Numeric(precision=30, scale=18))
    close = Column(Numeric(precision=30, scale=18))
    volume = Column(Numeric(precision=30, scale=18))
    turnover = Column(Numeric(precision=30, scale=18))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    instrument = relationship("Instrument")
    
    __table_args__ = (
        Index('idx_kline_instrument_timeframe', 'instrument_id', 'timeframe', 'timestamp', unique=True),
    )

class TickData(Base):
    __tablename__ = "tick_data"
    
    id = Column(Integer, primary_key=True, index=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    bid_price = Column(Numeric(precision=30, scale=18))
    ask_price = Column(Numeric(precision=30, scale=18))
    bid_size = Column(Numeric(precision=30, scale=18))
    ask_size = Column(Numeric(precision=30, scale=18))
    last_price = Column(Numeric(precision=30, scale=18))
    last_size = Column(Numeric(precision=30, scale=18))
    volume = Column(Numeric(precision=30, scale=18))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    instrument = relationship("Instrument")
    
    __table_args__ = (
        Index('idx_tick_instrument_timestamp', 'instrument_id', 'timestamp'),
    )
