#!/usr/bin/env python3
"""
组合回测独立测试脚本 - 不依赖数据库
"""
import asyncio
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import pandas as pd
import numpy as np

# 直接在脚本中定义必要的类

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass
class Order:
    symbol: str
    side: OrderSide
    order_type: OrderType
    size: float
    price: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    strategy_id: Optional[int] = None

@dataclass
class Position:
    symbol: str
    size: float
    avg_price: float
    strategy_id: Optional[int] = None

@dataclass
class Trade:
    symbol: str
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    size: float
    side: str
    pnl: float
    pnl_pct: float
    strategy_id: Optional[int] = None

@dataclass
class StrategyResult:
    strategy_id: int
    strategy_name: str
    trades: List[Trade] = field(default_factory=list)

class PortfolioBacktestEngine:
    """组合回测引擎"""
    
    def __init__(self, initial_capital: float = 100000.0, commission_rate: float = 0.001, slippage: float = 0.0005):
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage = slippage
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.orders: List[Order] = []
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict[str, Any]] = []
        self.strategies: Dict[int, Dict[str, Any]] = {}
        self.strategy_results: Dict[int, StrategyResult] = {}
        self.strategy_allocations: Dict[int, float] = {}
        self.data: Dict[str, pd.DataFrame] = {}
        self.current_time: Optional[datetime] = None
    
    def add_strategy(self, strategy_id: int, strategy_name: str, strategy_code: str, 
                     symbols: List[str], allocation: float = 1.0, params: Optional[Dict[str, Any]] = None) -> bool:
        try:
            exec_globals = {}
            exec(strategy_code, exec_globals)
            
            if 'Strategy' not in exec_globals:
                return False
            
            strategy_class = exec_globals['Strategy']
            strategy_instance = strategy_class(params or {})
            
            self.strategies[strategy_id] = {
                'id': strategy_id,
                'name': strategy_name,
                'instance': strategy_instance,
                'symbols': symbols,
                'code': strategy_code,
                'params': params or {}
            }
            
            self.strategy_allocations[strategy_id] = allocation
            self.strategy_results[strategy_id] = StrategyResult(strategy_id=strategy_id, strategy_name=strategy_name)
            
            return True
        except Exception as e:
            print(f"Error adding strategy {strategy_id}: {e}")
            return False
    
    def set_data(self, data: Dict[str, pd.DataFrame]):
        self.data = data
    
    def run_backtest(self) -> Dict[str, Any]:
        if not self.data:
            return {'error': 'No data loaded'}
        
        all_timestamps = set()
        for df in self.data.values():
            all_timestamps.update(df.index)
        
        sorted_timestamps = sorted(all_timestamps)
        if not sorted_timestamps:
            return {'error': 'No timestamps found'}
        
        # 初始化策略
        for strategy_id, strategy_info in self.strategies.items():
            strategy_info['instance'].initialize({
                'cash': self.initial_capital * self.strategy_allocations.get(strategy_id, 1.0),
                'symbols': strategy_info['symbols']
            })
        
        # 逐日回测
        for timestamp in sorted_timestamps:
            self.current_time = timestamp
            
            current_data = {}
            for symbol, df in self.data.items():
                if timestamp in df.index:
                    row = df.loc[timestamp]
                    current_data[symbol] = {
                        'open': row['open'],
                        'high': row['high'],
                        'low': row['low'],
                        'close': row['close'],
                        'volume': row['volume'],
                        'timestamp': timestamp
                    }
            
            if not current_data:
                continue
            
            # 为每个策略生成信号
            for strategy_id, strategy_info in self.strategies.items():
                strategy = strategy_info['instance']
                
                for symbol in strategy_info['symbols']:
                    if symbol not in current_data:
                        continue
                    
                    bar_data = current_data[symbol]
                    
                    try:
                        signal = strategy.on_bar(bar_data)
                        
                        if signal and signal.get('signal') in ['buy', 'sell']:
                            self._process_signal(strategy_id=strategy_id, symbol=symbol, 
                                               signal=signal['signal'], price=bar_data['close'], timestamp=timestamp)
                    except Exception as e:
                        pass
            
            self._update_equity_curve(timestamp, current_data)
        
        return self._calculate_results()
    
    def _process_signal(self, strategy_id: int, symbol: str, signal: str, price: float, timestamp: datetime):
        allocation = self.strategy_allocations.get(strategy_id, 1.0)
        strategy_cash = self.cash * allocation
        position_size = strategy_cash * 0.1 / price
        
        position_key = f"{strategy_id}_{symbol}"
        
        if signal == 'buy' and position_key not in self.positions:
            order = Order(symbol=symbol, side=OrderSide.BUY, order_type=OrderType.MARKET,
                         size=position_size, price=price * (1 + self.slippage),
                         timestamp=timestamp, strategy_id=strategy_id)
            self._execute_order(order)
        
        elif signal == 'sell' and position_key in self.positions:
            position = self.positions[position_key]
            order = Order(symbol=symbol, side=OrderSide.SELL, order_type=OrderType.MARKET,
                         size=position.size, price=price * (1 - self.slippage),
                         timestamp=timestamp, strategy_id=strategy_id)
            self._execute_order(order)
    
    def _execute_order(self, order: Order):
        fill_price = order.price
        if not fill_price:
            return
        
        commission = fill_price * order.size * self.commission_rate
        total_cost = fill_price * order.size + commission
        
        position_key = f"{order.strategy_id}_{order.symbol}"
        
        if order.side == OrderSide.BUY:
            if total_cost > self.cash:
                return
            
            self.cash -= total_cost
            
            if position_key in self.positions:
                position = self.positions[position_key]
                total_value = position.size * position.avg_price + order.size * fill_price
                position.size += order.size
                position.avg_price = total_value / position.size
            else:
                self.positions[position_key] = Position(symbol=order.symbol, size=order.size,
                                                       avg_price=fill_price, strategy_id=order.strategy_id)
        else:
            if position_key not in self.positions:
                return
            
            position = self.positions[position_key]
            
            if order.size > position.size:
                order.size = position.size
            
            pnl = (fill_price - position.avg_price) * order.size - commission
            pnl_pct = (fill_price - position.avg_price) / position.avg_price * 100
            
            trade = Trade(symbol=order.symbol, entry_time=position.avg_price, exit_time=order.timestamp,
                         entry_price=position.avg_price, exit_price=fill_price, size=order.size,
                         side='long', pnl=pnl, pnl_pct=pnl_pct, strategy_id=order.strategy_id)
            
            self.trades.append(trade)
            
            if order.strategy_id in self.strategy_results:
                self.strategy_results[order.strategy_id].trades.append(trade)
            
            self.cash += fill_price * order.size - commission
            position.size -= order.size
            
            if position.size <= 0:
                del self.positions[position_key]
        
        self.orders.append(order)
    
    def _update_equity_curve(self, timestamp: datetime, current_data: Dict[str, Any]):
        total_equity = self.cash
        
        for position_key, position in self.positions.items():
            if position.symbol in current_data:
                price = current_data[position.symbol]['close']
                total_equity += position.size * price
        
        self.equity_curve.append({'timestamp': timestamp, 'equity': total_equity, 'cash': self.cash})
    
    def _calculate_results(self) -> Dict[str, Any]:
        if not self.equity_curve:
            return {'error': 'No equity curve data'}
        
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df.set_index('timestamp', inplace=True)
        
        total_return = (equity_df['equity'].iloc[-1] - self.initial_capital) / self.initial_capital
        
        days = (equity_df.index[-1] - equity_df.index[0]).days
        annual_return = (1 + total_return) ** (365 / days) - 1 if days > 0 else 0
        
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak']
        max_drawdown = equity_df['drawdown'].min()
        
        returns = equity_df['equity'].pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        
        winning_trades = [t for t in self.trades if t.pnl > 0]
        win_rate = len(winning_trades) / len(self.trades) if self.trades else 0
        
        avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        losing_trades = [t for t in self.trades if t.pnl <= 0]
        avg_loss = abs(np.mean([t.pnl for t in losing_trades])) if losing_trades else 1
        profit_factor = avg_win / avg_loss if avg_loss > 0 else 0
        
        strategy_results = {}
        for strategy_id, result in self.strategy_results.items():
            strategy_trades = result.trades
            strategy_winning = [t for t in strategy_trades if t.pnl > 0]
            
            strategy_results[strategy_id] = {
                'strategy_name': result.strategy_name,
                'total_trades': len(strategy_trades),
                'winning_trades': len(strategy_winning),
                'losing_trades': len(strategy_trades) - len(strategy_winning),
                'win_rate': len(strategy_winning) / len(strategy_trades) if strategy_trades else 0,
                'total_pnl': sum(t.pnl for t in strategy_trades)
            }
        
        return {
            'summary': {
                'initial_capital': self.initial_capital,
                'final_equity': equity_df['equity'].iloc[-1],
                'total_return': total_return,
                'total_return_pct': total_return * 100,
                'annual_return': annual_return,
                'annual_return_pct': annual_return * 100,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'max_drawdown_pct': max_drawdown * 100,
                'total_trades': len(self.trades),
                'win_rate': win_rate,
                'win_rate_pct': win_rate * 100,
                'profit_factor': profit_factor,
                'volatility': returns.std() * np.sqrt(252) if len(returns) > 0 else 0
            },
            'equity_curve': equity_df['equity'].to_dict(),
            'drawdown': equity_df['drawdown'].to_dict(),
            'strategy_results': strategy_results
        }


def generate_mock_data(symbol: str, start_time: datetime, end_time: datetime, 
                       timeframe: str = '1d', trend: str = 'up') -> pd.DataFrame:
    """生成模拟数据"""
    freq_map = {'1m': 'T', '5m': '5T', '15m': '15T', '30m': '30T',
                '1h': 'H', '2h': '2H', '4h': '4H',
                '1d': 'D', '1w': 'W', '1M': 'M'}
    freq = freq_map.get(timeframe, 'D')
    
    dates = pd.date_range(start=start_time, end=end_time, freq=freq)
    np.random.seed(hash(symbol) % 2**32)
    n = len(dates)
    
    if trend == 'up':
        base_return = 0.0005
    elif trend == 'down':
        base_return = -0.0005
    else:
        base_return = 0.0
    
    returns = np.random.normal(base_return, 0.02, n)
    
    initial_price = 100
    prices = [initial_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    data = []
    for i, date in enumerate(dates):
        close = prices[i]
        high = close * (1 + abs(np.random.normal(0, 0.01)))
        low = close * (1 - abs(np.random.normal(0, 0.01)))
        open_price = close * (1 + np.random.normal(0, 0.005))
        volume = np.random.randint(100000, 1000000)
        
        data.append({'timestamp': date, 'open': open_price, 'high': high, 
                    'low': low, 'close': close, 'volume': volume})
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df


# 策略代码
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
    
    def initialize(self, context):
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        current_price = data['close']
        
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
    
    def initialize(self, context):
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        deviation = (current_price - ma) / ma
        
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
    
    def initialize(self, context):
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""


def main():
    print("=" * 70)
    print("组合回测测试 (多策略多资产)")
    print("=" * 70)
    
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    # 生成模拟数据
    print(f"\n生成模拟数据...")
    data = {}
    trends = ['up', 'down', 'sideways']
    for i, symbol in enumerate(symbols):
        trend = trends[i % len(trends)]
        data[symbol] = generate_mock_data(symbol, start_time, end_time, '1d', trend)
        print(f"  {symbol}: {len(data[symbol])} 根K线 (趋势: {trend})")
    
    # 创建回测引擎
    engine = PortfolioBacktestEngine(initial_capital=100000.0)
    engine.set_data(data)
    
    # 添加多个策略
    strategies = [
        {'id': 1, 'name': '突破策略', 'code': strategy1_code, 'symbols': ['BTC/USDT'], 
         'allocation': 0.4, 'params': {'lookback': 20}},
        {'id': 2, 'name': '均值回归', 'code': strategy2_code, 'symbols': ['ETH/USDT'],
         'allocation': 0.3, 'params': {'ma_period': 20, 'threshold': 0.02}},
        {'id': 3, 'name': '趋势跟踪', 'code': strategy3_code, 'symbols': ['BTC/USDT', 'SOL/USDT'],
         'allocation': 0.3, 'params': {'fast_period': 10, 'slow_period': 30}}
    ]
    
    print(f"\n添加策略...")
    for s in strategies:
        success = engine.add_strategy(s['id'], s['name'], s['code'], s['symbols'], 
                                     s['allocation'], s['params'])
        print(f"  {'✓' if success else '✗'} {s['name']} (资金分配: {s['allocation']*100:.0f}%)")
    
    # 运行回测
    print(f"\n运行组合回测...")
    results = engine.run_backtest()
    
    if 'error' in results:
        print(f"回测失败: {results['error']}")
        return
    
    # 打印结果
    print("\n" + "=" * 70)
    print("回测结果")
    print("=" * 70)
    
    summary = results['summary']
    print(f"\n【组合表现】")
    print(f"  初始资金: ${summary['initial_capital']:,.2f}")
    print(f"  最终权益: ${summary['final_equity']:,.2f}")
    print(f"  总收益率: {summary['total_return_pct']:.2f}%")
    print(f"  年化收益率: {summary['annual_return_pct']:.2f}%")
    print(f"  夏普比率: {summary['sharpe_ratio']:.2f}")
    print(f"  最大回撤: {summary['max_drawdown_pct']:.2f}%")
    print(f"  总交易次数: {summary['total_trades']}")
    print(f"  胜率: {summary['win_rate_pct']:.2f}%")
    print(f"  盈亏比: {summary['profit_factor']:.2f}")
    
    print(f"\n【各策略表现】")
    for strategy_id, s_result in results['strategy_results'].items():
        print(f"\n  策略 {strategy_id}: {s_result['strategy_name']}")
        print(f"    交易次数: {s_result['total_trades']}")
        print(f"    盈利/亏损: {s_result['winning_trades']}/{s_result['losing_trades']}")
        print(f"    胜率: {s_result['win_rate']*100:.2f}%")
        print(f"    总盈亏: ${s_result['total_pnl']:,.2f}")
    
    # 计算组合指标
    strategy_count = len(results['strategy_results'])
    allocations = [0.4, 0.3, 0.3]
    concentration = sum(a**2 for a in allocations)
    
    print(f"\n【组合分析】")
    print(f"  策略数量: {strategy_count}")
    print(f"  集中度指数: {concentration:.4f}")
    print(f"  分散化评分: {1-concentration:.4f}")
    
    sorted_strategies = sorted(results['strategy_results'].items(), 
                              key=lambda x: x[1]['total_pnl'], reverse=True)
    if sorted_strategies:
        best = sorted_strategies[0]
        worst = sorted_strategies[-1]
        print(f"  最佳策略: {best[1]['strategy_name']} (${best[1]['total_pnl']:,.2f})")
        print(f"  最差策略: {worst[1]['strategy_name']} (${worst[1]['total_pnl']:,.2f})")
    
    print("\n" + "=" * 70)
    print("✓ 组合回测完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()
