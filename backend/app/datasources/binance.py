from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import ccxt
from .base import DataSource, TimeFrame

class BinanceDataSource(DataSource):
    """Binance 数据源"""
    
    def __init__(self):
        self._exchange = ccxt.binance({'enableRateLimit': True})
    
    @property
    def name(self) -> str:
        return "Binance"
    
    @property
    def code(self) -> str:
        return "binance"
    
    def get_exchanges(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "Binance",
                "code": "binance",
                "country": "Global",
            }
        ]
    
    def get_instruments(self, exchange_code: Optional[str] = None) -> List[Dict[str, Any]]:
        instruments = []
        try:
            markets = self._exchange.load_markets()
            for symbol, market in markets.items():
                if market.get('active'):
                    instruments.append({
                        "symbol": symbol,
                        "name": symbol,
                        "exchange_code": "binance",
                        "asset_class": "crypto",
                        "instrument_type": market.get('type', 'spot'),
                        "base_currency": market.get('base'),
                        "quote_currency": market.get('quote'),
                        "price_precision": market.get('precision', {}).get('price', 8),
                        "size_precision": market.get('precision', {}).get('amount', 8),
                        "min_size": str(market.get('limits', {}).get('amount', {}).get('min', '')),
                        "max_size": str(market.get('limits', {}).get('amount', {}).get('max', '')),
                    })
        except Exception as e:
            print(f"Error loading Binance instruments: {e}")
        return instruments
    
    def get_klines(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = 1000
    ) -> List[Dict[str, Any]]:
        klines = []
        try:
            tf_map = {
                TimeFrame.MIN_1: '1m',
                TimeFrame.MIN_5: '5m',
                TimeFrame.MIN_15: '15m',
                TimeFrame.MIN_30: '30m',
                TimeFrame.HOUR_1: '1h',
                TimeFrame.HOUR_2: '2h',
                TimeFrame.HOUR_4: '4h',
                TimeFrame.HOUR_6: '6h',
                TimeFrame.HOUR_12: '12h',
                TimeFrame.DAY_1: '1d',
                TimeFrame.WEEK_1: '1w',
                TimeFrame.MONTH_1: '1M',
            }
            tf = tf_map.get(timeframe, '1h')
            
            since = int(start_time.timestamp() * 1000) if start_time else None
            
            ohlcv = self._exchange.fetch_ohlcv(symbol, tf, since=since, limit=limit)
            
            for candle in ohlcv:
                klines.append({
                    "timestamp": datetime.fromtimestamp(candle[0] / 1000),
                    "open": candle[1],
                    "high": candle[2],
                    "low": candle[3],
                    "close": candle[4],
                    "volume": candle[5],
                })
        except Exception as e:
            print(f"Error fetching Binance klines: {e}")
        return klines
    
    def get_realtime_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        try:
            ticker = self._exchange.fetch_ticker(symbol)
            return {
                "symbol": symbol,
                "last_price": ticker.get('last'),
                "bid_price": ticker.get('bid'),
                "ask_price": ticker.get('ask'),
                "volume_24h": ticker.get('quoteVolume'),
                "change_24h": ticker.get('percentage'),
                "timestamp": datetime.fromtimestamp(ticker.get('timestamp', 0) / 1000),
            }
        except Exception as e:
            print(f"Error fetching Binance quote: {e}")
            return None
