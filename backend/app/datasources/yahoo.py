from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import yfinance as yf
from .base import DataSource, TimeFrame

class YahooFinanceDataSource(DataSource):
    """Yahoo Finance 数据源"""
    
    @property
    def name(self) -> str:
        return "Yahoo Finance"
    
    @property
    def code(self) -> str:
        return "yahoo"
    
    def get_exchanges(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "NYSE",
                "code": "nyse",
                "country": "USA",
            },
            {
                "name": "NASDAQ",
                "code": "nasdaq",
                "country": "USA",
            },
        ]
    
    def get_instruments(self, exchange_code: Optional[str] = None) -> List[Dict[str, Any]]:
        instruments = []
        popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "SPY", "QQQ"]
        for symbol in popular_stocks:
            instruments.append({
                "symbol": symbol,
                "name": symbol,
                "exchange_code": "nasdaq",
                "asset_class": "equity",
                "instrument_type": "spot",
                "base_currency": "USD",
                "quote_currency": "USD",
                "price_precision": 2,
                "size_precision": 4,
            })
        return instruments
    
    def get_klines(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        klines = []
        try:
            tf_map = {
                TimeFrame.MIN_1: '1m',
                TimeFrame.MIN_5: '5m',
                TimeFrame.MIN_15: '15m',
                TimeFrame.MIN_30: '30m',
                TimeFrame.HOUR_1: '1h',
                TimeFrame.HOUR_4: '1h',
                TimeFrame.DAY_1: '1d',
                TimeFrame.WEEK_1: '1wk',
                TimeFrame.MONTH_1: '1mo',
            }
            tf = tf_map.get(timeframe, '1d')
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='max' if not start_time else None, 
                                interval=tf,
                                start=start_time,
                                end=end_time)
            
            if limit:
                hist = hist.tail(limit)
            
            for idx, row in hist.iterrows():
                klines.append({
                    "timestamp": idx.to_pydatetime(),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": float(row['Volume']),
                })
        except Exception as e:
            print(f"Error fetching Yahoo Finance klines: {e}")
        return klines
    
    def get_realtime_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                "symbol": symbol,
                "last_price": info.get('currentPrice'),
                "bid_price": info.get('bid'),
                "ask_price": info.get('ask'),
                "volume_24h": info.get('volume'),
                "change_24h": info.get('changePercent'),
                "timestamp": datetime.now(),
            }
        except Exception as e:
            print(f"Error fetching Yahoo Finance quote: {e}")
            return None
