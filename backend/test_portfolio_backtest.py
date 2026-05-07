#!/usr/bin/env python3
"""
组合回测测试脚本
"""
import asyncio
import sys
sys.path.insert(0, '/workspace/backend')

from datetime import datetime, timedelta
from app.services.portfolio_backtest_service import PortfolioBacktestService

# 策略1: 简单突破策略
strategy1_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.lookback = int(self.params.get('lookback', 20))
        self.name = "Breakout Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.lookback:
            return {'signal': 'hold'}
        
        # 计算高低点
        high = max(self.prices[-self.lookback:])
        low = min(self.prices[-self.lookback:])
        
        current_price = data['close']
        
        # 突破买入，跌破卖出
        if current_price > high * 0.99:
            return {'signal': 'buy'}
        elif current_price < low * 1.01:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略2: 均值回归策略
strategy2_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.ma_period = int(self.params.get('ma_period', 20))
        self.threshold = float(self.params.get('threshold', 0.02))
        self.name = "Mean Reversion Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.ma_period:
            return {'signal': 'hold'}
        
        # 计算移动平均线
        ma = sum(self.prices[-self.ma_period:]) / self.ma_period
        current_price = data['close']
        
        deviation = (current_price - ma) / ma
        
        # 价格低于均线过多买入，高于均线过多卖出
        if deviation < -self.threshold:
            return {'signal': 'buy'}
        elif deviation > self.threshold:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

# 策略3: 趋势跟踪策略
strategy3_code = """
class Strategy:
    def __init__(self, params=None):
        self.params = params or {}
        self.fast_period = int(self.params.get('fast_period', 10))
        self.slow_period = int(self.params.get('slow_period', 30))
        self.name = "Trend Following Strategy"
    
    def initialize(self, context):
        self.context = context
        self.prices = []
    
    def on_bar(self, data):
        self.prices.append(data['close'])
        
        if len(self.prices) < self.slow_period:
            return {'signal': 'hold'}
        
        # 计算快慢均线
        fast_ma = sum(self.prices[-self.fast_period:]) / self.fast_period
        slow_ma = sum(self.prices[-self.slow_period:]) / self.slow_period
        
        # 金叉买入，死叉卖出
        if fast_ma > slow_ma * 1.001:
            return {'signal': 'buy'}
        elif fast_ma < slow_ma * 0.999:
            return {'signal': 'sell'}
        
        return {'signal': 'hold'}
"""

async def test_portfolio_backtest():
    """测试组合回测"""
    print("=" * 60)
    print("组合回测测试")
    print("=" * 60)
    
    service = PortfolioBacktestService()
    
    # 配置参数
    end_time = datetime.now()
    start_time = end_time - timedelta(days=180)  # 6个月
    
    # 多策略配置
    strategies = [
        {
            'id': 1,
            'name': 'Breakout Strategy',
            'code': strategy1_code,
            'params': {'lookback': 20},
            'allocation': 0.4,  # 40% 资金
            'symbols': ['BTC/USDT']
        },
        {
            'id': 2,
            'name': 'Mean Reversion Strategy',
            'code': strategy2_code,
            'params': {'ma_period': 20, 'threshold': 0.02},
            'allocation': 0.3,  # 30% 资金
            'symbols': ['ETH/USDT']
        },
        {
            'id': 3,
            'name': 'Trend Following Strategy',
            'code': strategy3_code,
            'params': {'fast_period': 10, 'slow_period': 30},
            'allocation': 0.3,  # 30% 资金
            'symbols': ['BTC/USDT', 'ETH/USDT']
        }
    ]
    
    symbols = ['BTC/USDT', 'ETH/USDT']
    
    print(f"\n回测配置:")
    print(f"  时间范围: {start_time.date()} 至 {end_time.date()}")
    print(f"  标的: {', '.join(symbols)}")
    print(f"  策略数量: {len(strategies)}")
    print(f"  初始资金: $100,000")
    
    # 运行组合回测
    print("\n运行组合回测...")
    results = await service.run_portfolio_backtest(
        name="Multi-Strategy Portfolio Test",
        strategies=strategies,
        symbols=symbols,
        datasource_code='binance',
        timeframe='1d',
        start_time=start_time,
        end_time=end_time,
        initial_capital=100000.0,
        use_mock_data=True  # 使用模拟数据
    )
    
    if 'error' in results:
        print(f"回测失败: {results['error']}")
        return
    
    # 打印结果
    print("\n" + "=" * 60)
    print("回测结果")
    print("=" * 60)
    
    summary = results.get('summary', {})
    print(f"\n【组合表现】")
    print(f"  初始资金: ${summary.get('initial_capital', 0):,.2f}")
    print(f"  最终权益: ${summary.get('final_equity', 0):,.2f}")
    print(f"  总收益率: {summary.get('total_return_pct', 0):.2f}%")
    print(f"  年化收益率: {summary.get('annual_return_pct', 0):.2f}%")
    print(f"  夏普比率: {summary.get('sharpe_ratio', 0):.2f}")
    print(f"  最大回撤: {summary.get('max_drawdown_pct', 0):.2f}%")
    print(f"  总交易次数: {summary.get('total_trades', 0)}")
    print(f"  胜率: {summary.get('win_rate_pct', 0):.2f}%")
    print(f"  盈亏比: {summary.get('profit_factor', 0):.2f}")
    
    # 策略表现
    print(f"\n【各策略表现】")
    strategy_results = results.get('strategy_results', {})
    for strategy_id, s_result in strategy_results.items():
        print(f"\n  策略 {strategy_id}: {s_result.get('strategy_name')}")
        print(f"    交易次数: {s_result.get('total_trades', 0)}")
        print(f"    盈利次数: {s_result.get('winning_trades', 0)}")
        print(f"    亏损次数: {s_result.get('losing_trades', 0)}")
        print(f"    胜率: {s_result.get('win_rate', 0) * 100:.2f}%")
        print(f"    总盈亏: ${s_result.get('total_pnl', 0):,.2f}")
    
    # 计算组合指标
    print(f"\n【组合指标】")
    extended_metrics = service.calculate_portfolio_metrics(results)
    print(f"  策略数量: {extended_metrics.get('strategy_count', 0)}")
    print(f"  集中度指数: {extended_metrics.get('concentration_index', 0):.4f}")
    print(f"  分散化评分: {extended_metrics.get('diversification_score', 0):.4f}")
    
    best = extended_metrics.get('best_strategy')
    worst = extended_metrics.get('worst_strategy')
    if best:
        print(f"  最佳策略: {best['name']} (盈亏: ${best['pnl']:,.2f})")
    if worst:
        print(f"  最差策略: {worst['name']} (盈亏: ${worst['pnl']:,.2f})")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_portfolio_backtest())
