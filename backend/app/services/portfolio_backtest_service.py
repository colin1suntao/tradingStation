"""
组合回测服务 - 处理多策略多资产回测
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from app.engine.portfolio_backtest_engine import PortfolioBacktestEngine
from app.services.market_data_service import MarketDataService

class PortfolioBacktestService:
    """组合回测服务"""
    
    def __init__(self):
        self.market_data_service = MarketDataService()
    
    async def run_portfolio_backtest(
        self,
        name: str,
        strategies: List[Dict[str, Any]],
        symbols: List[str],
        datasource_code: str,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
        initial_capital: float = 100000.0,
        use_mock_data: bool = False
    ) -> Dict[str, Any]:
        """
        运行组合回测
        
        Args:
            name: 回测名称
            strategies: 策略列表 [{'id': int, 'name': str, 'code': str, 'params': dict, 'allocation': float, 'symbols': List[str]}]
            symbols: 所有标的列表
            datasource_code: 数据源代码
            timeframe: 时间周期
            start_time: 开始时间
            end_time: 结束时间
            initial_capital: 初始资金
            use_mock_data: 是否使用模拟数据
            
        Returns:
            回测结果
        """
        try:
            # 1. 获取市场数据
            print(f"Fetching market data for {len(symbols)} symbols...")
            data = await self.market_data_service.get_data_for_backtest(
                symbols=symbols,
                datasource_code=datasource_code,
                timeframe=timeframe,
                start_time=start_time,
                end_time=end_time,
                use_mock=use_mock_data
            )
            
            if not data:
                return {'error': 'No data available for backtest'}
            
            print(f"Loaded data for {len(data)} symbols")
            
            # 2. 创建回测引擎
            engine = PortfolioBacktestEngine(
                initial_capital=initial_capital,
                commission_rate=0.001,
                slippage=0.0005
            )
            
            # 3. 设置数据
            engine.set_data(data)
            
            # 4. 添加策略
            for strategy_config in strategies:
                success = engine.add_strategy(
                    strategy_id=strategy_config['id'],
                    strategy_name=strategy_config['name'],
                    strategy_code=strategy_config['code'],
                    symbols=strategy_config.get('symbols', symbols),
                    allocation=strategy_config.get('allocation', 1.0 / len(strategies)),
                    params=strategy_config.get('params', {})
                )
                
                if success:
                    print(f"Added strategy: {strategy_config['name']}")
                else:
                    print(f"Failed to add strategy: {strategy_config['name']}")
            
            # 5. 运行回测
            print("Running backtest...")
            results = engine.run_backtest()
            
            # 6. 添加元数据
            results['name'] = name
            results['start_time'] = start_time.isoformat()
            results['end_time'] = end_time.isoformat()
            results['timeframe'] = timeframe
            results['datasource'] = datasource_code
            results['strategies_count'] = len(strategies)
            results['symbols'] = symbols
            
            return results
            
        except Exception as e:
            print(f"Error running portfolio backtest: {e}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    async def run_single_strategy_backtest(
        self,
        strategy_id: int,
        strategy_name: str,
        strategy_code: str,
        symbols: List[str],
        datasource_code: str,
        timeframe: str,
        start_time: datetime,
        end_time: datetime,
        params: Optional[Dict[str, Any]] = None,
        initial_capital: float = 100000.0,
        use_mock_data: bool = False
    ) -> Dict[str, Any]:
        """
        运行单策略回测（兼容旧接口）
        """
        strategies = [{
            'id': strategy_id,
            'name': strategy_name,
            'code': strategy_code,
            'symbols': symbols,
            'allocation': 1.0,
            'params': params or {}
        }]
        
        return await self.run_portfolio_backtest(
            name=f"Single Strategy - {strategy_name}",
            strategies=strategies,
            symbols=symbols,
            datasource_code=datasource_code,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
            initial_capital=initial_capital,
            use_mock_data=use_mock_data
        )
    
    def calculate_portfolio_metrics(
        self,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        计算组合层面的额外指标
        
        Args:
            results: 回测结果
            
        Returns:
            扩展的指标字典
        """
        if 'error' in results:
            return results
        
        summary = results.get('summary', {})
        strategy_results = results.get('strategy_results', {})
        
        # 计算策略相关性（简化版）
        strategy_returns = {}
        for strategy_id, s_result in strategy_results.items():
            trades = s_result.get('trades', [])
            if trades:
                returns = [t.get('pnl_pct', 0) for t in trades]
                strategy_returns[strategy_id] = returns
        
        # 计算组合集中度
        if strategy_results:
            allocations = [1.0 / len(strategy_results)] * len(strategy_results)
            concentration = sum(a ** 2 for a in allocations)
        else:
            concentration = 0
        
        # 扩展指标
        extended_metrics = {
            **summary,
            'strategy_count': len(strategy_results),
            'concentration_index': concentration,
            'diversification_score': 1 - concentration if concentration < 1 else 0,
            'best_strategy': None,
            'worst_strategy': None
        }
        
        # 找出最佳和最差策略
        if strategy_results:
            sorted_by_pnl = sorted(
                strategy_results.items(),
                key=lambda x: x[1].get('total_pnl', 0),
                reverse=True
            )
            
            if sorted_by_pnl:
                extended_metrics['best_strategy'] = {
                    'id': sorted_by_pnl[0][0],
                    'name': sorted_by_pnl[0][1].get('strategy_name'),
                    'pnl': sorted_by_pnl[0][1].get('total_pnl', 0)
                }
                extended_metrics['worst_strategy'] = {
                    'id': sorted_by_pnl[-1][0],
                    'name': sorted_by_pnl[-1][1].get('strategy_name'),
                    'pnl': sorted_by_pnl[-1][1].get('total_pnl', 0)
                }
        
        return extended_metrics
