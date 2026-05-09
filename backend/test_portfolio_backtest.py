import sys
sys.path.insert(0, '/workspace/backend')

import pandas as pd
import numpy as np
from datetime import datetime

from app.backtest.backtest_service import backtest_service
from app.backtest.portfolio_engine import PortfolioBacktestEngine
from app.backtest.strategy_manager import (
    BreakoutStrategy, MeanReversionStrategy, 
    TrendFollowingStrategy, RSIStrategy, StrategyManager
)
from app.backtest.tool_aggregator import ToolAggregator, TechnicalIndicatorTool
from app.schemas.backtest import BacktestConfig, BacktestMode, AllocationMethod

print("=" * 70)
print("Multi-Strategy Portfolio Backtest Test")
print("=" * 70)


def generate_mock_data(symbol, start_date, end_date, days=252):
    dates = pd.date_range(start=start_date, end=end_date, periods=days)
    
    np.random.seed(hash(symbol) % (2**32))
    
    initial_price = 100
    returns = np.random.normal(0.0005, 0.02, days)
    prices = initial_price * (1 + returns).cumprod()
    
    data = pd.DataFrame({
        'timestamp': dates,
        'open': prices * (1 + np.random.uniform(-0.01, 0.01, days)),
        'high': prices * (1 + np.random.uniform(0, 0.02, days)),
        'low': prices * (1 - np.random.uniform(0, 0.02, days)),
        'close': prices,
        'volume': np.random.uniform(1000000, 10000000, days),
        'symbol': symbol,
    })
    
    return data


print("\n1. Testing Available Strategies:")
strategies = backtest_service.get_available_strategies()
for s in strategies:
    print(f"   - {s['name']}: {s['description']}")

print("\n2. Testing Available Tools:")
tools = backtest_service.get_available_tools()
for t in tools:
    print(f"   - {t['name']}: {t['description']}")

print("\n3. Running Single Strategy Backtest:")
config = BacktestConfig(
    mode=BacktestMode.SINGLE,
    symbols=["BTC/USDT"],
    start_date="2023-01-01",
    end_date="2023-12-31",
    initial_capital=100000,
    allocation_method=AllocationMethod.EQUAL_WEIGHT,
)

market_data = {
    "BTC/USDT": generate_mock_data("BTC/USDT", "2023-01-01", "2023-12-31")
}

result = backtest_service.run_backtest(
    config=config,
    market_data=market_data,
    strategy_ids=["breakout"],
)

print(f"   Initial Capital: ${result.initial_capital:,.2f}")
print(f"   Final Capital: ${result.final_capital:,.2f}")
print(f"   Total Return: {result.total_return_pct:.2f}%")
print(f"   Sharpe Ratio: {result.portfolio_performance.sharpe_ratio:.2f}")
print(f"   Max Drawdown: {result.portfolio_performance.max_drawdown_pct:.2f}%")
print(f"   Total Trades: {result.portfolio_performance.total_trades}")
print(f"   Win Rate: {result.portfolio_performance.win_rate * 100:.1f}%")

print("\n4. Running Multi-Strategy Backtest:")
config_multi = BacktestConfig(
    mode=BacktestMode.MULTI_STRATEGY,
    symbols=["BTC/USDT"],
    start_date="2023-01-01",
    end_date="2023-12-31",
    initial_capital=100000,
    allocation_method=AllocationMethod.EQUAL_WEIGHT,
    max_positions=3,
)

result_multi = backtest_service.run_backtest(
    config=config_multi,
    market_data=market_data,
    strategy_ids=["breakout", "mean_reversion", "trend_following"],
    strategy_weights={"breakout": 0.4, "mean_reversion": 0.3, "trend_following": 0.3},
)

print(f"   Initial Capital: ${result_multi.initial_capital:,.2f}")
print(f"   Final Capital: ${result_multi.final_capital:,.2f}")
print(f"   Total Return: {result_multi.total_return_pct:.2f}%")
print(f"   Sharpe Ratio: {result_multi.portfolio_performance.sharpe_ratio:.2f}")
print(f"   Max Drawdown: {result_multi.portfolio_performance.max_drawdown_pct:.2f}%")
print(f"   Total Trades: {result_multi.portfolio_performance.total_trades}")

print("\n5. Testing Strategy Comparison:")
comparison = backtest_service.compare_strategies(
    symbols=["BTC/USDT"],
    start_date="2023-01-01",
    end_date="2023-12-31",
    strategy_ids=["breakout", "mean_reversion", "trend_following", "rsi"],
    initial_capital=50000,
)

print("\n   Strategy Comparison:")
print("-" * 70)
print(f"{'Strategy':<20} {'Return %':<12} {'Sharpe':<10} {'Max DD %':<12} {'Win Rate':<10}")
print("-" * 70)
for sid, result in comparison.items():
    print(f"{sid:<20} {result.total_return_pct:<12.2f} {result.portfolio_performance.sharpe_ratio:<10.2f} {result.portfolio_performance.max_drawdown_pct:<12.2f} {result.portfolio_performance.win_rate*100:<10.1f}")
print("-" * 70)

best = max(comparison.items(), key=lambda x: x[1].portfolio_performance.sharpe_ratio)
print(f"\n   Best Strategy: {best[0]} (Sharpe: {best[1].portfolio_performance.sharpe_ratio:.2f})")

print("\n6. Testing Tool Aggregator:")
tool_agg = ToolAggregator()
tool_agg.add_tool(TechnicalIndicatorTool('tech', ['rsi', 'macd']))

sample_data = market_data["BTC/USDT"].tail(50)
tool_result = tool_agg.get_combined_analysis(sample_data)
print(f"   Combined Signal: {tool_result['combined_signal']:.4f}")
print(f"   Signal Direction: {tool_result['signal_direction']}")
print(f"   Tool Count: {tool_result['tool_count']}")

print("\n7. Testing Portfolio Engine Directly:")
sm = StrategyManager()
sm.add_strategy(BreakoutStrategy('breakout', 'Breakout'), 0.5)
sm.add_strategy(MeanReversionStrategy('mean_reversion', 'Mean Reversion'), 0.5)

engine = PortfolioBacktestEngine(
    config=config_multi,
    strategy_manager=sm,
)

result_engine = engine.run(market_data)
print(f"   Direct Engine Result: ${result_engine.final_capital:,.2f}")
print(f"   Return: {result_engine.total_return_pct:.2f}%")

print("\n" + "=" * 70)
print("All Portfolio Backtest Tests Passed!")
print("=" * 70)
