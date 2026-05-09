from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
import numpy as np
import uuid

from app.schemas.backtest import (
    BacktestConfig,
    BacktestResult,
    BacktestMode,
    AllocationMethod,
)
from app.backtest.portfolio_engine import PortfolioBacktestEngine, MultiStrategyPortfolioOptimizer
from app.backtest.strategy_manager import (
    StrategyManager,
    Strategy,
    BreakoutStrategy,
    MeanReversionStrategy,
    TrendFollowingStrategy,
    RSIStrategy,
)
from app.backtest.tool_aggregator import (
    ToolAggregator,
    TechnicalIndicatorTool,
    SentimentTool,
    PatternRecognitionTool,
    VolumeAnalysisTool,
)


class BacktestService:
    def __init__(self):
        self._history: Dict[str, BacktestResult] = {}
        self._default_strategies: Dict[str, Strategy] = {}
        self._default_tools: Dict[str, Any] = {}
        self._init_defaults()

    def _init_defaults(self):
        self._default_strategies = {
            'breakout': BreakoutStrategy('breakout', 'Breakout Strategy'),
            'mean_reversion': MeanReversionStrategy('mean_reversion', 'Mean Reversion Strategy'),
            'trend_following': TrendFollowingStrategy('trend_following', 'Trend Following Strategy'),
            'rsi': RSIStrategy('rsi', 'RSI Strategy'),
        }

        self._default_tools = {
            'technical': TechnicalIndicatorTool('technical', ['rsi', 'macd', 'bollinger', 'sma']),
            'sentiment': SentimentTool(),
            'pattern': PatternRecognitionTool(),
            'volume': VolumeAnalysisTool(),
        }

    def get_available_strategies(self) -> List[Dict[str, Any]]:
        return [
            {
                'id': 'breakout',
                'name': 'Breakout Strategy',
                'description': 'Trades breakouts of 20-day high/low',
                'parameters': {'lookback_period': 20},
            },
            {
                'id': 'mean_reversion',
                'name': 'Mean Reversion Strategy',
                'description': 'Trades when price crosses Bollinger Bands',
                'parameters': {'bb_period': 20, 'bb_std': 2},
            },
            {
                'id': 'trend_following',
                'name': 'Trend Following Strategy',
                'description': 'Uses MACD crossover for entry signals',
                'parameters': {'fast': 12, 'slow': 26, 'signal': 9},
            },
            {
                'id': 'rsi',
                'name': 'RSI Strategy',
                'description': 'Mean reversion based on RSI oversold/overbought',
                'parameters': {'rsi_period': 14, 'oversold': 30, 'overbought': 70},
            },
        ]

    def get_available_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                'id': 'technical',
                'name': 'Technical Indicators',
                'description': 'RSI, MACD, Bollinger Bands, SMA',
                'indicators': ['rsi', 'macd', 'bollinger', 'sma'],
            },
            {
                'id': 'sentiment',
                'name': 'Sentiment Analysis',
                'description': 'Analyzes market sentiment and trends',
            },
            {
                'id': 'pattern',
                'name': 'Pattern Recognition',
                'description': 'Identifies chart patterns like golden cross',
            },
            {
                'id': 'volume',
                'name': 'Volume Analysis',
                'description': 'Analyzes volume patterns',
            },
        ]

    def create_strategy_manager(
        self,
        strategy_ids: List[str],
        weights: Optional[Dict[str, float]] = None
    ) -> StrategyManager:
        manager = StrategyManager()

        for sid in strategy_ids:
            if sid in self._default_strategies:
                strategy = self._default_strategies[sid]
                weight = weights.get(sid, 1.0 / len(strategy_ids)) if weights else 1.0 / len(strategy_ids)
                manager.add_strategy(strategy, weight)

        return manager

    def create_tool_aggregator(
        self,
        tool_ids: List[str],
        weights: Optional[Dict[str, float]] = None
    ) -> ToolAggregator:
        aggregator = ToolAggregator()

        for tid in tool_ids:
            if tid in self._default_tools:
                tool = self._default_tools[tid]
                aggregator.add_tool(tool)

        return aggregator

    def run_backtest(
        self,
        config: BacktestConfig,
        market_data: Dict[str, pd.DataFrame],
        strategy_ids: Optional[List[str]] = None,
        tool_ids: Optional[List[str]] = None,
        strategy_weights: Optional[Dict[str, float]] = None,
        risk_config: Optional[Dict[str, Any]] = None,
    ) -> BacktestResult:
        if strategy_ids is None:
            strategy_ids = ['breakout', 'mean_reversion']
        if tool_ids is None:
            tool_ids = ['technical']

        strategy_manager = self.create_strategy_manager(strategy_ids, strategy_weights)
        tool_aggregator = self.create_tool_aggregator(tool_ids)

        engine = PortfolioBacktestEngine(
            config=config,
            strategy_manager=strategy_manager,
            tool_aggregator=tool_aggregator,
        )

        result = engine.run(market_data)
        result_id = str(uuid.uuid4())
        self._history[result_id] = result

        return result

    def run_multi_strategy_backtest(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        initial_capital: float = 100000,
        strategy_ids: Optional[List[str]] = None,
        strategy_weights: Optional[Dict[str, float]] = None,
        allocation_method: AllocationMethod = AllocationMethod.EQUAL_WEIGHT,
    ) -> BacktestResult:
        if strategy_ids is None:
            strategy_ids = ['breakout', 'mean_reversion', 'trend_following', 'rsi']

        config = BacktestConfig(
            mode=BacktestMode.MULTI_STRATEGY,
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            allocation_method=allocation_method,
        )

        market_data = self._fetch_market_data(symbols, start_date, end_date)

        return self.run_backtest(
            config=config,
            market_data=market_data,
            strategy_ids=strategy_ids,
            strategy_weights=strategy_weights,
        )

    def optimize_strategy_weights(
        self,
        config: BacktestConfig,
        market_data: Dict[str, pd.DataFrame],
        strategy_ids: List[str],
    ) -> Dict[str, Any]:
        strategy_manager = self.create_strategy_manager(strategy_ids)
        tool_aggregator = self.create_tool_aggregator(['technical'])

        engine = PortfolioBacktestEngine(
            config=config,
            strategy_manager=strategy_manager,
            tool_aggregator=tool_aggregator,
        )

        optimizer = MultiStrategyPortfolioOptimizer(engine)
        best_weights = optimizer.optimize_weights(market_data)

        return {
            'best_weights': best_weights,
            'optimization_history': optimizer.get_optimization_history(),
        }

    def compare_strategies(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        strategy_ids: List[str],
        initial_capital: float = 100000,
    ) -> Dict[str, BacktestResult]:
        results = {}

        for sid in strategy_ids:
            config = BacktestConfig(
                mode=BacktestMode.SINGLE,
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                initial_capital=initial_capital,
            )

            market_data = self._fetch_market_data(symbols, start_date, end_date)

            result = self.run_backtest(
                config=config,
                market_data=market_data,
                strategy_ids=[sid],
            )

            results[sid] = result

        return results

    def _fetch_market_data(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
    ) -> Dict[str, pd.DataFrame]:
        market_data = {}

        for symbol in symbols:
            try:
                import yfinance as yf
                
                ticker = symbol.replace('/', '').replace('-', '')
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                
                if not data.empty:
                    data = data.reset_index()
                    data.columns = [col.lower() for col in data.columns]
                    
                    if 'date' not in data.columns and 'datetime' not in data.columns:
                        data['timestamp'] = data['date'] if 'date' in data.columns else pd.Timestamp.now()
                    elif 'date' in data.columns:
                        data['timestamp'] = data['date']
                    else:
                        data['timestamp'] = data.index
                    
                    market_data[symbol] = data
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                market_data[symbol] = self._generate_mock_data(symbol, start_date, end_date)

        return market_data

    def _generate_mock_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        days: int = 252,
    ) -> pd.DataFrame:
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

    def get_backtest_history(self) -> List[Dict[str, Any]]:
        return [
            {
                'id': bid,
                'config': r.config,
                'final_capital': r.final_capital,
                'total_return_pct': r.total_return_pct,
                'sharpe_ratio': r.portfolio_performance.sharpe_ratio,
                'max_drawdown_pct': r.portfolio_performance.max_drawdown_pct,
            }
            for bid, r in self._history.items()
        ]

    def get_backtest_result(self, backtest_id: str) -> Optional[BacktestResult]:
        return self._history.get(backtest_id)


backtest_service = BacktestService()
