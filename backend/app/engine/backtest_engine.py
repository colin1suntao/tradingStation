import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime

# 模拟 VectorBT 引擎，避免依赖安装问题
# 实际生产环境请安装 vectorbt==0.25.0

class BacktestEngine:
    """回测引擎（模拟版）"""
    
    def __init__(self):
        self.portfolio = None
        self.signals = None
    
    def run_strategy(
        self,
        data: pd.DataFrame,
        strategy_code: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """运行策略回测"""
        try:
            exec_globals = {
                'pd': pd,
                'np': np,
                'params': params,
                'data': data
            }
            
            exec(strategy_code, exec_globals)
            
            if 'Strategy' in exec_globals:
                strategy_class = exec_globals['Strategy']
                strategy = strategy_class(params)
                
                context = {'data': data}
                strategy.initialize(context)
                
                signals = []
                for i in range(len(data)):
                    bar_data = {
                        'open': data['open'].iloc[i],
                        'high': data['high'].iloc[i],
                        'low': data['low'].iloc[i],
                        'close': data['close'].iloc[i],
                        'volume': data['volume'].iloc[i],
                    }
                    signal = strategy.on_bar(bar_data)
                    signals.append(signal.get('signal', 'hold'))
                
                self.signals = pd.Series(signals, index=data.index)
                
                # 模拟回测结果
                return self._generate_mock_results(data)
            
            return {'error': 'Strategy class not found', 'success': False}
        
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def _generate_mock_results(self, data: pd.DataFrame) -> Dict[str, Any]:
        """生成模拟回测结果"""
        # 生成模拟权益曲线
        initial_equity = 10000.0
        equity = [initial_equity]
        for i in range(1, len(data)):
            change = np.random.uniform(-0.02, 0.03)
            equity.append(equity[-1] * (1 + change))
        
        equity_curve = {str(date): val for date, val in zip(data.index, equity)}
        
        # 统计指标
        total_return = (equity[-1] - equity[0]) / equity[0]
        annual_return = (1 + total_return) ** (365 / len(data)) - 1
        max_drawdown = np.min([(equity[i] - np.max(equity[:i+1])) / np.max(equity[:i+1]) for i in range(len(equity))])
        sharpe_ratio = np.mean([(equity[i+1]/equity[i])-1 for i in range(len(equity)-1)]) / np.std([(equity[i+1]/equity[i])-1 for i in range(len(equity)-1)])
        win_rate = 0.55 + np.random.uniform(-0.1, 0.1)
        profit_factor = 1.2 + np.random.uniform(0, 0.5)
        
        stats = {
            'total_return': float(total_return),
            'annual_return': float(annual_return),
            'sharpe_ratio': float(sharpe_ratio),
            'max_drawdown': float(max_drawdown),
            'win_rate': float(win_rate),
            'profit_factor': float(profit_factor),
            'total_trades': int(len(data) * 0.3),
            'volatility': 0.2,
            'max_consecutive_losses': 3
        }
        
        # 模拟交易记录
        trades = []
        for i in range(0, len(data), 5):
            entry_idx = i
            exit_idx = min(i + 3, len(data) - 1)
            trades.append({
                'entry_time': str(data.index[entry_idx]),
                'exit_time': str(data.index[exit_idx]),
                'entry_price': float(data['close'].iloc[entry_idx]),
                'exit_price': float(data['close'].iloc[exit_idx]),
                'return': float((data['close'].iloc[exit_idx] - data['close'].iloc[entry_idx]) / data['close'].iloc[entry_idx]),
                'size': 100.0
            })
        
        # 回撤数据
        drawdown = {
            'max': float(max_drawdown),
            'duration': 15,
            'underwater': {str(date): val for date, val in zip(data.index, np.random.uniform(-0.1, 0, len(data)))}
        }
        
        # 摘要信息
        summary = {
            'start_date': str(data.index[0]),
            'end_date': str(data.index[-1]),
            'total_return_pct': float(total_return * 100),
            'cagr': float(annual_return * 100),
            'sharpe_ratio': float(sharpe_ratio),
            'max_drawdown_pct': float(max_drawdown * 100),
            'total_trades': int(len(data) * 0.3),
            'win_rate_pct': float(win_rate * 100)
        }
        
        return {
            'equity_curve': equity_curve,
            'stats': stats,
            'trades': trades,
            'drawdown': drawdown,
            'summary': summary,
            'success': True
        }


# 测试代码
if __name__ == "__main__":
    engine = BacktestEngine()
    
    strategy_code = """
class Strategy:
    name = "Test Strategy"
    params = {"ma_window": 20}
    
    def __init__(self, params=None):
        self.params = params or self.params
    
    def initialize(self, context):
        self.context = context
    
    def on_bar(self, data):
        close = data["close"]
        if close > 100:
            return {"signal": "buy"}
        elif close < 90:
            return {"signal": "sell"}
        return {"signal": "hold"}
"""
    
    # 生成测试数据
    dates = pd.date_range('2024-01-01', periods=100)
    data = pd.DataFrame({
        'open': np.random.uniform(95, 105, 100),
        'high': np.random.uniform(100, 110, 100),
        'low': np.random.uniform(90, 100, 100),
        'close': np.random.uniform(95, 105, 100),
        'volume': np.random.uniform(1000, 10000, 100),
    }, index=dates)
    
    result = engine.run_strategy(data, strategy_code, {"ma_window": 20})
    print(f"✅ 测试完成！Success: {result.get('success', False)}")
    if result.get('success'):
        print(f"📊 总收益率: {result['stats']['total_return']:.2%}")
        print(f"📈 夏普比率: {result['stats']['sharpe_ratio']:.2f}")
        print(f"📉 最大回撤: {result['stats']['max_drawdown']:.2%}")
        print(f"✅ 胜率: {result['stats']['win_rate']:.2%}")
