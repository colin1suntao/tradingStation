"""
组合回测引擎 - 支持多策略多资产组合回测
"""
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
import numpy as np
import ast

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass
class Order:
    """订单"""
    symbol: str
    side: OrderSide
    order_type: OrderType
    size: float
    price: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    strategy_id: Optional[int] = None

@dataclass
class Position:
    """持仓"""
    symbol: str
    size: float
    avg_price: float
    strategy_id: Optional[int] = None
    
    @property
    def market_value(self, current_price: float) -> float:
        return self.size * current_price
    
    @property
    def unrealized_pnl(self, current_price: float) -> float:
        return self.size * (current_price - self.avg_price)

@dataclass
class Trade:
    """交易记录"""
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
    """单个策略的回测结果"""
    strategy_id: int
    strategy_name: str
    equity_curve: pd.Series = field(default_factory=lambda: pd.Series())
    trades: List[Trade] = field(default_factory=list)
    positions: Dict[str, Position] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)

class PortfolioBacktestEngine:
    """
    组合回测引擎
    支持多策略、多资产、权重配置
    """
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission_rate: float = 0.001,
        slippage: float = 0.0005
    ):
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage = slippage
        
        # 组合状态
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.orders: List[Order] = []
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict[str, Any]] = []
        
        # 策略管理
        self.strategies: Dict[int, Dict[str, Any]] = {}
        self.strategy_results: Dict[int, StrategyResult] = {}
        self.strategy_allocations: Dict[int, float] = {}  # 策略资金分配比例
        
        # 数据
        self.data: Dict[str, pd.DataFrame] = {}  # symbol -> DataFrame
        self.current_time: Optional[datetime] = None
        
    def add_strategy(
        self,
        strategy_id: int,
        strategy_name: str,
        strategy_code: str,
        symbols: List[str],
        allocation: float = 1.0,  # 资金分配比例
        params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        添加策略到组合
        
        Args:
            strategy_id: 策略ID
            strategy_name: 策略名称
            strategy_code: 策略代码
            symbols: 交易的标的列表
            allocation: 资金分配比例 (0-1)
            params: 策略参数
        """
        try:
            # 编译策略代码
            exec_globals = {}
            exec(strategy_code, exec_globals)
            
            if 'Strategy' not in exec_globals:
                print(f"Strategy class not found in strategy {strategy_id}")
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
            self.strategy_results[strategy_id] = StrategyResult(
                strategy_id=strategy_id,
                strategy_name=strategy_name
            )
            
            return True
            
        except Exception as e:
            print(f"Error adding strategy {strategy_id}: {e}")
            return False
    
    def load_data(
        self,
        data_source: Callable[[str, datetime, datetime], pd.DataFrame],
        symbols: List[str],
        start_time: datetime,
        end_time: datetime
    ):
        """
        加载历史数据
        
        Args:
            data_source: 数据源函数 (symbol, start, end) -> DataFrame
            symbols: 标的列表
            start_time: 开始时间
            end_time: 结束时间
        """
        for symbol in symbols:
            try:
                df = data_source(symbol, start_time, end_time)
                if not df.empty:
                    self.data[symbol] = df
                    print(f"Loaded data for {symbol}: {len(df)} bars")
            except Exception as e:
                print(f"Error loading data for {symbol}: {e}")
    
    def set_data(self, data: Dict[str, pd.DataFrame]):
        """直接设置数据"""
        self.data = data
    
    def run_backtest(self) -> Dict[str, Any]:
        """
        运行组合回测
        
        Returns:
            回测结果字典
        """
        if not self.data:
            return {'error': 'No data loaded'}
        
        # 获取所有时间戳
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
            
            # 获取当前时刻所有标的的数据
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
                            self._process_signal(
                                strategy_id=strategy_id,
                                symbol=symbol,
                                signal=signal['signal'],
                                price=bar_data['close'],
                                timestamp=timestamp
                            )
                    except Exception as e:
                        print(f"Error processing signal for {symbol}: {e}")
            
            # 更新权益曲线
            self._update_equity_curve(timestamp, current_data)
        
        # 计算结果
        return self._calculate_results()
    
    def _process_signal(
        self,
        strategy_id: int,
        symbol: str,
        signal: str,
        price: float,
        timestamp: datetime
    ):
        """处理交易信号"""
        # 获取策略分配的资金
        allocation = self.strategy_allocations.get(strategy_id, 1.0)
        strategy_cash = self.cash * allocation
        
        # 简单的固定仓位管理：每次使用10%可用资金
        position_size = strategy_cash * 0.1 / price
        
        if signal == 'buy':
            # 检查是否已有持仓
            position_key = f"{strategy_id}_{symbol}"
            
            if position_key not in self.positions:
                # 开新仓
                order = Order(
                    symbol=symbol,
                    side=OrderSide.BUY,
                    order_type=OrderType.MARKET,
                    size=position_size,
                    price=price * (1 + self.slippage),
                    timestamp=timestamp,
                    strategy_id=strategy_id
                )
                self._execute_order(order)
                
        elif signal == 'sell':
            position_key = f"{strategy_id}_{symbol}"
            
            if position_key in self.positions:
                # 平仓
                position = self.positions[position_key]
                order = Order(
                    symbol=symbol,
                    side=OrderSide.SELL,
                    order_type=OrderType.MARKET,
                    size=position.size,
                    price=price * (1 - self.slippage),
                    timestamp=timestamp,
                    strategy_id=strategy_id
                )
                self._execute_order(order)
    
    def _execute_order(self, order: Order):
        """执行订单"""
        fill_price = order.price or self._get_current_price(order.symbol)
        
        if not fill_price:
            return
        
        commission = fill_price * order.size * self.commission_rate
        total_cost = fill_price * order.size + commission
        
        if order.side == OrderSide.BUY:
            if total_cost > self.cash:
                print(f"Insufficient cash for buy order: {order.symbol}")
                return
            
            self.cash -= total_cost
            
            position_key = f"{order.strategy_id}_{order.symbol}"
            if position_key in self.positions:
                # 加仓
                position = self.positions[position_key]
                total_value = position.size * position.avg_price + order.size * fill_price
                position.size += order.size
                position.avg_price = total_value / position.size
            else:
                # 新建仓
                self.positions[position_key] = Position(
                    symbol=order.symbol,
                    size=order.size,
                    avg_price=fill_price,
                    strategy_id=order.strategy_id
                )
        
        else:  # SELL
            position_key = f"{order.strategy_id}_{order.symbol}"
            if position_key not in self.positions:
                return
            
            position = self.positions[position_key]
            
            if order.size > position.size:
                order.size = position.size
            
            # 计算盈亏
            pnl = (fill_price - position.avg_price) * order.size - commission
            pnl_pct = (fill_price - position.avg_price) / position.avg_price * 100
            
            # 记录交易
            trade = Trade(
                symbol=order.symbol,
                entry_time=position,  # 简化处理，实际需要记录入场时间
                exit_time=order.timestamp,
                entry_price=position.avg_price,
                exit_price=fill_price,
                size=order.size,
                side='long',
                pnl=pnl,
                pnl_pct=pnl_pct,
                strategy_id=order.strategy_id
            )
            self.trades.append(trade)
            
            # 更新策略结果
            if order.strategy_id in self.strategy_results:
                self.strategy_results[order.strategy_id].trades.append(trade)
            
            # 更新资金和持仓
            self.cash += fill_price * order.size - commission
            position.size -= order.size
            
            if position.size <= 0:
                del self.positions[position_key]
        
        self.orders.append(order)
    
    def _get_current_price(self, symbol: str) -> Optional[float]:
        """获取当前价格"""
        if symbol in self.data and self.current_time in self.data[symbol].index:
            return self.data[symbol].loc[self.current_time, 'close']
        return None
    
    def _update_equity_curve(self, timestamp: datetime, current_data: Dict[str, Any]):
        """更新权益曲线"""
        total_equity = self.cash
        
        for position_key, position in self.positions.items():
            if position.symbol in current_data:
                price = current_data[position.symbol]['close']
                total_equity += position.size * price
        
        self.equity_curve.append({
            'timestamp': timestamp,
            'equity': total_equity,
            'cash': self.cash
        })
    
    def _calculate_results(self) -> Dict[str, Any]:
        """计算回测结果"""
        if not self.equity_curve:
            return {'error': 'No equity curve data'}
        
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df.set_index('timestamp', inplace=True)
        
        # 计算收益率
        total_return = (equity_df['equity'].iloc[-1] - self.initial_capital) / self.initial_capital
        
        # 计算年化收益率
        days = (equity_df.index[-1] - equity_df.index[0]).days
        if days > 0:
            annual_return = (1 + total_return) ** (365 / days) - 1
        else:
            annual_return = 0
        
        # 计算最大回撤
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak']
        max_drawdown = equity_df['drawdown'].min()
        
        # 计算夏普比率
        returns = equity_df['equity'].pct_change().dropna()
        if returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
        else:
            sharpe_ratio = 0
        
        # 计算胜率
        winning_trades = [t for t in self.trades if t.pnl > 0]
        win_rate = len(winning_trades) / len(self.trades) if self.trades else 0
        
        # 计算盈亏比
        avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        losing_trades = [t for t in self.trades if t.pnl <= 0]
        avg_loss = abs(np.mean([t.pnl for t in losing_trades])) if losing_trades else 1
        profit_factor = avg_win / avg_loss if avg_loss > 0 else 0
        
        # 策略结果
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
                'total_pnl': sum(t.pnl for t in strategy_trades),
                'trades': [
                    {
                        'symbol': t.symbol,
                        'entry_time': t.entry_time.isoformat() if isinstance(t.entry_time, datetime) else str(t.entry_time),
                        'exit_time': t.exit_time.isoformat(),
                        'entry_price': t.entry_price,
                        'exit_price': t.exit_price,
                        'size': t.size,
                        'pnl': t.pnl,
                        'pnl_pct': t.pnl_pct
                    }
                    for t in strategy_trades
                ]
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
            'trades': [
                {
                    'symbol': t.symbol,
                    'entry_time': t.entry_time.isoformat() if isinstance(t.entry_time, datetime) else str(t.entry_time),
                    'exit_time': t.exit_time.isoformat(),
                    'entry_price': t.entry_price,
                    'exit_price': t.exit_price,
                    'size': t.size,
                    'pnl': t.pnl,
                    'pnl_pct': t.pnl_pct,
                    'strategy_id': t.strategy_id
                }
                for t in self.trades
            ],
            'strategy_results': strategy_results,
            'positions': [
                {
                    'symbol': p.symbol,
                    'size': p.size,
                    'avg_price': p.avg_price,
                    'strategy_id': p.strategy_id
                }
                for p in self.positions.values()
            ]
        }
