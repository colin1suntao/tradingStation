from .base import DataSource, TimeFrame
from .registry import DataSourceRegistry
from .binance import BinanceDataSource
from .yahoo import YahooFinanceDataSource

registry = DataSourceRegistry()
registry.register(BinanceDataSource())
registry.register(YahooFinanceDataSource())

__all__ = [
    "DataSource",
    "TimeFrame",
    "DataSourceRegistry",
    "BinanceDataSource",
    "YahooFinanceDataSource",
    "registry",
]
