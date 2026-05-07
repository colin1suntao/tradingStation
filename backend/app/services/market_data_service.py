"""
市场数据服务 - 提供真实市场数据获取
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from app.datasources.registry import DataSourceRegistry
from app.datasources.base import TimeFrame

class MarketDataService:
    """市场数据服务"""
    
    def __init__(self):
        self.registry = DataSourceRegistry()
    
    async def get_historical_data(
        self,
        symbol: str,
        datasource_code: str,
        timeframe: str,
        start_time: datetime,
        end_time: datetime
    ) -> pd.DataFrame:
        """
        获取历史数据
        
        Args:
            symbol: 标的代码
            datasource_code: 数据源代码
            timeframe: 时间周期
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        try:
            datasource = self.registry.get_datasource(datasource_code)
            if not datasource:
                print(f"DataSource {datasource_code} not found")
                return pd.DataFrame()
            
            # 转换时间周期
            tf_map = {
                '1m': TimeFrame.MIN_1,
                '5m': TimeFrame.MIN_5,
                '15m': TimeFrame.MIN_15,
                '30m': TimeFrame.MIN_30,
                '1h': TimeFrame.HOUR_1,
                '2h': TimeFrame.HOUR_2,
                '4h': TimeFrame.HOUR_4,
                '6h': TimeFrame.HOUR_6,
                '12h': TimeFrame.HOUR_12,
                '1d': TimeFrame.DAY_1,
                '1w': TimeFrame.WEEK_1,
                '1M': TimeFrame.MONTH_1,
            }
            tf = tf_map.get(timeframe, TimeFrame.DAY_1)
            
            # 获取K线数据
            klines = datasource.get_klines(symbol, tf, start_time, end_time)
            
            if not klines:
                return pd.DataFrame()
            
            # 转换为DataFrame
            df = pd.DataFrame(klines)
            df.set_index('timestamp', inplace=True)
            df.sort_index(inplace=True)
            
            return df
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    async def get_multi_symbol_data(
        self,
        symbols: List[str],
        datasource_code: str,
        timeframe: str,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, pd.DataFrame]:
        """
        获取多个标的的历史数据
        
        Args:
            symbols: 标的代码列表
            datasource_code: 数据源代码
            timeframe: 时间周期
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            Dict[symbol, DataFrame]
        """
        data = {}
        for symbol in symbols:
            df = await self.get_historical_data(
                symbol, datasource_code, timeframe, start_time, end_time
            )
            if not df.empty:
                data[symbol] = df
        return data
    
    async def get_realtime_quote(
        self,
        symbol: str,
        datasource_code: str
    ) -> Optional[Dict[str, Any]]:
        """
        获取实时行情
        
        Args:
            symbol: 标的代码
            datasource_code: 数据源代码
            
        Returns:
            行情数据字典
        """
        try:
            datasource = self.registry.get_datasource(datasource_code)
            if not datasource:
                return None
            
            return datasource.get_realtime_quote(symbol)
            
        except Exception as e:
            print(f"Error fetching realtime quote: {e}")
            return None
    
    def generate_mock_data(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
        timeframe: str = '1d',
        trend: str = 'up'
    ) -> pd.DataFrame:
        """
        生成模拟数据（用于测试）
        
        Args:
            symbol: 标的代码
            start_time: 开始时间
            end_time: 结束时间
            timeframe: 时间周期
            trend: 趋势方向 (up, down, sideways)
            
        Returns:
            DataFrame
        """
        # 生成时间序列
        freq_map = {
            '1m': 'T', '5m': '5T', '15m': '15T', '30m': '30T',
            '1h': 'H', '2h': '2H', '4h': '4H',
            '1d': 'D', '1w': 'W', '1M': 'M'
        }
        freq = freq_map.get(timeframe, 'D')
        
        dates = pd.date_range(start=start_time, end=end_time, freq=freq)
        
        # 生成价格数据
        np.random.seed(42)  # 固定随机种子
        n = len(dates)
        
        if trend == 'up':
            base_return = 0.0005
        elif trend == 'down':
            base_return = -0.0005
        else:
            base_return = 0.0
        
        returns = np.random.normal(base_return, 0.02, n)
        
        # 从100开始
        initial_price = 100
        prices = [initial_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))
        
        # 生成OHLCV
        data = []
        for i, date in enumerate(dates):
            close = prices[i]
            high = close * (1 + abs(np.random.normal(0, 0.01)))
            low = close * (1 - abs(np.random.normal(0, 0.01)))
            open_price = close * (1 + np.random.normal(0, 0.005))
            volume = np.random.randint(100000, 1000000)
            
            data.append({
                'timestamp': date,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        return df
    
    async def get_data_for_backtest(
        self,
        symbols: List[str],
        datasource_code: str,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
        use_mock: bool = False
    ) -> Dict[str, pd.DataFrame]:
        """
        为回测获取数据
        
        Args:
            symbols: 标的列表
            datasource_code: 数据源代码
            timeframe: 时间周期
            start_time: 开始时间
            end_time: 结束时间
            use_mock: 是否使用模拟数据
            
        Returns:
            Dict[symbol, DataFrame]
        """
        if use_mock:
            # 使用模拟数据
            data = {}
            trends = ['up', 'down', 'sideways', 'up']
            for i, symbol in enumerate(symbols):
                trend = trends[i % len(trends)]
                data[symbol] = self.generate_mock_data(
                    symbol, start_time, end_time, timeframe, trend
                )
            return data
        else:
            # 使用真实数据
            return await self.get_multi_symbol_data(
                symbols, datasource_code, timeframe, start_time, end_time
            )
