from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from app.schemas.backtest import (
    BacktestConfig,
    BacktestResult,
    BacktestMode,
    AllocationMethod,
    PortfolioSnapshot,
    Trade,
    Position,
    PortfolioPerformance,
    CombinedSignal,
    SignalType,
)
from app.schemas.risk import RiskConfig
from app.backtest.strategy_manager import StrategyManager, Strategy, BreakoutStrategy, MeanReversionStrategy, TrendFollowingStrategy, RSIStrategy
from app.backtest.tool_aggregator import ToolAggregator, TechnicalIndicatorTool, SentimentTool, PatternRecognitionTool, VolumeAnalysisTool


class PortfolioBacktestEngine:
    def __init__(
        self,
        config: BacktestConfig,
        strategy_manager: Optional[StrategyManager] = None,
        tool_aggregator: Optional[ToolAggregator] = None,
        risk_config: Optional[RiskConfig] = None,
    ):
        self.config = config
        self.strategy_manager = strategy_manager or StrategyManager()
        self.tool_aggregator = tool_aggregator or ToolAggregator()
        self.risk_config = risk_config or RiskConfig()
        
        self._positions: Dict[str, Position] = {}
        self._trades: List[Trade] = []
        self._portfolio_snapshots: List[PortfolioSnapshot] = []
        self._equity_curve: List[float] = []
        self._daily_returns: List[float] = []
        self._signals: List[CombinedSignal] = []
        
        self._cash = config.initial_capital
        self._current_capital = config.initial_capital

    def run(self, market_data: Dict[str, pd.DataFrame]) -> BacktestResult:
        start_time = datetime.now()
        
        if not market_data:
            return BacktestResult(
                config=self.config.model_dump(),
                start_date=datetime.fromisoformat(self.config.start_date),
                end_date=datetime.fromisoformat(self.config.end_date),
                initial_capital=self.config.initial_capital,
                final_capital=self.config.initial_capital,
                total_return=0,
                total_return_pct=0,
                portfolio_performance=PortfolioPerformance(
                    total_return=0, total_return_pct=0, annualized_return=0,
                    annualized_volatility=0, sharpe_ratio=0, max_drawdown=0,
                    max_drawdown_pct=0, win_rate=0, profit_factor=0, total_trades=0,
                    daily_returns=[], monthly_returns={}, equity_curve=[],
                ),
                errors=["No market data provided"],
            )

        self._reset()
        
        symbols = list(market_data.keys())
        
        for symbol in symbols:
            data = market_data[symbol].copy()
            data['symbol'] = symbol
        
        combined_data = pd.concat(market_data.values(), ignore_index=True)
        combined_data = combined_data.sort_values('timestamp')
        
        if self.config.mode == BacktestMode.MULTI_STRATEGY:
            self._run_multi_strategy(combined_data, symbols)
        else:
            self._run_single_mode(combined_data, symbols)
        
        self._generate_portfolio_snapshots()
        
        final_capital = self._calculate_total_value(market_data)
        
        end_time = datetime.now()
        execution_time_ms = (end_time - start_time).total_seconds() * 1000

        portfolio_perf = self._calculate_portfolio_performance(final_capital)

        result = BacktestResult(
            config=self.config.model_dump(),
            start_date=datetime.fromisoformat(self.config.start_date),
            end_date=datetime.fromisoformat(self.config.end_date),
            initial_capital=self.config.initial_capital,
            final_capital=final_capital,
            total_return=final_capital - self.config.initial_capital,
            total_return_pct=((final_capital - self.config.initial_capital) / self.config.initial_capital) * 100,
            portfolio_performance=portfolio_perf,
            trades=self._trades,
            portfolio_snapshots=self._portfolio_snapshots,
            signals=self._signals,
            execution_time_ms=execution_time_ms,
        )

        return result

    def _run_single_mode(self, data: pd.DataFrame, symbols: List[str]):
        for symbol in symbols:
            symbol_data = data[data['symbol'] == symbol].copy()
            
            for _, row in symbol_data.iterrows():
                timestamp = row['timestamp'] if 'timestamp' in row else row.name
                current_price = row['close']
                
                self._update_positions(symbol, current_price, timestamp)
                
                signal = self._generate_signal(symbol_data, timestamp)
                
                if signal and signal.entry_signal:
                    self._execute_entry(symbol, current_price, timestamp, signal.confidence)
                elif signal and signal.exit_signal:
                    self._execute_exit(symbol, current_price, timestamp)
                
                self._check_stop_loss(symbol, current_price, timestamp)
                self._check_take_profit(symbol, current_price, timestamp)

    def _run_multi_strategy(self, data: pd.DataFrame, symbols: List[str]):
        for symbol in symbols:
            symbol_data = data[data['symbol'] == symbol].copy()
            
            self.strategy_manager.generate_all_signals({symbol: symbol_data})
            
            for _, row in symbol_data.iterrows():
                timestamp = row['timestamp'] if 'timestamp' in row else row.name
                current_price = row['close']
                
                self._update_positions(symbol, current_price, timestamp)
                
                combined_signal = self.strategy_manager.combine_signals(symbol)
                relevant_signal = next((s for s in combined_signal if s.timestamp == timestamp), None)
                
                if relevant_signal:
                    self._signals.append(relevant_signal)
                    
                    if relevant_signal.entry_signal:
                        self._execute_entry(symbol, current_price, timestamp, relevant_signal.confidence)
                    elif relevant_signal.exit_signal:
                        self._execute_exit(symbol, current_price, timestamp)
                    
                    self._check_stop_loss(symbol, current_price, timestamp)
                    self._check_take_profit(symbol, current_price, timestamp)

    def _generate_signal(self, data: pd.DataFrame, timestamp) -> Optional[CombinedSignal]:
        idx = data[data['timestamp'] == timestamp].index
        if len(idx) == 0:
            return None
        
        row_idx = idx[0]
        row = data.loc[row_idx]
        
        tool_result = self.tool_aggregator.get_combined_analysis(data[data['timestamp'] <= timestamp])
        signal_value = float(tool_result['combined_signal'])
        
        signal_value = max(-1.0, min(1.0, signal_value))
        confidence = min(abs(signal_value), 1.0)
        
        entry_signal = signal_value >= 0.3
        exit_signal = signal_value <= -0.3
        
        return CombinedSignal(
            timestamp=timestamp,
            symbol=row['symbol'],
            combined_signal=signal_value,
            entry_signal=entry_signal,
            exit_signal=exit_signal,
            confidence=confidence,
            contributing_strategies=['tool_aggregator'],
        )

    def _execute_entry(
        self,
        symbol: str,
        price: float,
        timestamp,
        confidence: float = 1.0
    ):
        if len(self._positions) >= self.config.max_positions:
            return
        
        if symbol in self._positions:
            return
        
        allocation = self._calculate_allocation(symbol, price)
        quantity = allocation / price
        
        if quantity * price < 10:
            return
        
        slippage_cost = quantity * price * self.config.slippage
        commission_cost = quantity * price * self.config.commission
        
        self._cash -= (quantity * price + slippage_cost + commission_cost)
        
        position = Position(
            symbol=symbol,
            quantity=quantity,
            entry_price=price,
            current_price=price,
            entry_time=timestamp,
            pnl=0,
            pnl_pct=0,
        )
        
        self._positions[symbol] = position
        
        trade = Trade(
            timestamp=timestamp,
            symbol=symbol,
            side="buy",
            quantity=quantity,
            price=price,
            commission=commission_cost,
            slippage_cost=slippage_cost,
            order_type="market",
        )
        self._trades.append(trade)

    def _execute_exit(self, symbol: str, price: float, timestamp):
        if symbol not in self._positions:
            return
        
        position = self._positions[symbol]
        quantity = position.quantity
        
        slippage_cost = quantity * price * self.config.slippage
        commission_cost = quantity * price * self.config.commission
        
        self._cash += (quantity * price - slippage_cost - commission_cost)
        
        pnl = (price - position.entry_price) * quantity - commission_cost - slippage_cost
        
        trade = Trade(
            timestamp=timestamp,
            symbol=symbol,
            side="sell",
            quantity=quantity,
            price=price,
            commission=commission_cost,
            slippage_cost=slippage_cost,
            order_type="market",
        )
        self._trades.append(trade)
        
        del self._positions[symbol]

    def _check_stop_loss(self, symbol: str, price: float, timestamp, stop_loss_pct: float = 0.02):
        if symbol not in self._positions:
            return
        
        position = self._positions[symbol]
        loss_pct = (position.entry_price - price) / position.entry_price
        
        if loss_pct >= stop_loss_pct:
            self._execute_exit(symbol, price, timestamp)

    def _check_take_profit(self, symbol: str, price: float, timestamp, take_profit_pct: float = 0.05):
        if symbol not in self._positions:
            return
        
        position = self._positions[symbol]
        profit_pct = (price - position.entry_price) / position.entry_price
        
        if profit_pct >= take_profit_pct:
            self._execute_exit(symbol, price, timestamp)

    def _update_positions(self, symbol: str, price: float, timestamp):
        if symbol in self._positions:
            position = self._positions[symbol]
            position.current_price = price
            position.pnl = (price - position.entry_price) * position.quantity
            position.pnl_pct = ((price - position.entry_price) / position.entry_price) * 100

    def _calculate_allocation(self, symbol: str, price: float) -> float:
        total_value = self._calculate_total_value_immediate()
        
        if self.config.allocation_method == AllocationMethod.EQUAL_WEIGHT:
            per_position = total_value / self.config.max_positions
        elif self.config.allocation_method == AllocationMethod.RISK_PARITY:
            per_position = total_value * 0.02
        else:
            per_position = total_value / self.config.max_positions
        
        return min(per_position, total_value * 0.3)

    def _calculate_total_value_immediate(self) -> float:
        return self._cash + sum(
            p.quantity * p.current_price for p in self._positions.values()
        )

    def _calculate_total_value(self, market_data: Dict[str, pd.DataFrame]) -> float:
        total = self._cash
        
        for symbol, position in self._positions.items():
            if symbol in market_data:
                latest_price = market_data[symbol]['close'].iloc[-1]
                total += position.quantity * latest_price
        
        self._current_capital = total
        self._equity_curve.append(total)
        
        if len(self._equity_curve) > 1:
            daily_return = (self._equity_curve[-1] - self._equity_curve[-2]) / self._equity_curve[-2]
            self._daily_returns.append(daily_return)
        
        return total

    def _generate_portfolio_snapshots(self):
        for symbol, position in self._positions.items():
            snapshot = PortfolioSnapshot(
                timestamp=datetime.now(),
                total_value=self._current_capital,
                cash=self._cash,
                positions_value=self._current_capital - self._cash,
                daily_pnl=self._daily_returns[-1] if self._daily_returns else 0,
                total_pnl=self._current_capital - self.config.initial_capital,
                positions=[position],
                open_positions_count=len(self._positions),
            )
            self._portfolio_snapshots.append(snapshot)

    def _calculate_portfolio_performance(self, final_capital: float) -> PortfolioPerformance:
        equity = self._equity_curve if self._equity_curve else [self.config.initial_capital]
        returns = self._daily_returns if self._daily_returns else [0]
        
        returns_series = pd.Series(returns)
        
        total_return = final_capital - self.config.initial_capital
        total_return_pct = (total_return / self.config.initial_capital) * 100
        
        if len(returns_series) > 0:
            annualized_return = returns_series.mean() * 252 * 100
            annualized_volatility = returns_series.std() * np.sqrt(252) * 100
            sharpe_ratio = (returns_series.mean() / returns_series.std() * np.sqrt(252)) if returns_series.std() > 0 else 0
            
            cumulative = (1 + returns_series).cumprod()
            running_max = cumulative.cummax()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown_pct = abs(drawdown.min()) * 100 if len(drawdown) > 0 else 0
            max_drawdown = max_drawdown_pct / 100 * self.config.initial_capital
        else:
            annualized_return = 0
            annualized_volatility = 0
            sharpe_ratio = 0
            max_drawdown_pct = 0
            max_drawdown = 0
        
        winning_trades = [t for t in self._trades if t.side == "sell" and t.price > 0]
        total_trades = len([t for t in self._trades if t.side == "sell"])
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        monthly_returns = {}
        
        return PortfolioPerformance(
            total_return=total_return,
            total_return_pct=total_return_pct,
            annualized_return=annualized_return,
            annualized_volatility=annualized_volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_pct=max_drawdown_pct,
            win_rate=win_rate,
            profit_factor=0,
            total_trades=total_trades,
            daily_returns=returns,
            monthly_returns=monthly_returns,
            equity_curve=equity,
        )

    def _reset(self):
        self._positions = {}
        self._trades = []
        self._portfolio_snapshots = []
        self._equity_curve = []
        self._daily_returns = []
        self._signals = []
        self._cash = self.config.initial_capital
        self._current_capital = self.config.initial_capital


class MultiStrategyPortfolioOptimizer:
    def __init__(self, engine: PortfolioBacktestEngine):
        self.engine = engine
        self._results: List[BacktestResult] = []

    def optimize_weights(
        self,
        market_data: Dict[str, pd.DataFrame],
        weight_ranges: List[float] = None
    ) -> Dict[str, float]:
        if weight_ranges is None:
            weight_ranges = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        best_sharpe = -999
        best_weights = {}
        
        strategies = list(self.engine.strategy_manager._strategies.keys())
        
        if not strategies:
            return {}
        
        for w1 in weight_ranges:
            remaining = 1.0 - w1
            for w2 in weight_ranges:
                if w1 + w2 > 1.0:
                    continue
                remaining_2 = 1.0 - w1 - w2
                if len(strategies) > 2:
                    for w3 in weight_ranges:
                        if w1 + w2 + w3 > 1.0:
                            continue
                        weights = {
                            strategies[0]: w1,
                            strategies[1]: w2,
                            strategies[2]: w3,
                        }
                else:
                    weights = {
                        strategies[0]: w1,
                        strategies[1]: w2,
                    }
                    if len(strategies) > 2:
                        weights[strategies[2]] = remaining_2
                
                for sid, w in weights.items():
                    self.engine.strategy_manager.set_weight(sid, w)
                self.engine.strategy_manager.normalize_weights()
                
                result = self.engine.run(market_data)
                sharpe = result.portfolio_performance.sharpe_ratio
                
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_weights = self.engine.strategy_manager.get_weights().copy()
                    self._results.append(result)
        
        return best_weights

    def get_optimization_history(self) -> List[BacktestResult]:
        return self._results
