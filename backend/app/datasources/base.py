from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

class TimeFrame(str, Enum):
    MIN_1 = "1m"
    MIN_5 = "5m"
    MIN_15 = "15m"
    MIN_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"

class DataSource(ABC):
    """数据源基类，所有数据源必须实现此接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """数据源名称"""
        pass
    
    @property
    @abstractmethod
    def code(self) -> str:
        """数据源唯一标识"""
        pass
    
    @abstractmethod
    def get_exchanges(self) -> List[Dict[str, Any]]:
        """获取支持的交易所列表"""
        pass
    
    @abstractmethod
    def get_instruments(self, exchange_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取标的列表"""
        pass
    
    @abstractmethod
    def get_klines(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """获取K线数据"""
        pass
    
    @abstractmethod
    def get_realtime_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取实时行情"""
        pass
    
    def normalize_symbol(self, symbol: str) -> str:
        """标准化标的代码"""
        return symbol
    
    def normalize_timeframe(self, timeframe: TimeFrame) -> str:
        """标准化时间周期"""
        return timeframe.value
