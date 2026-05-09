from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import pandas as pd
import numpy as np

from app.schemas.backtest import (
    BacktestConfig,
    StrategyWeight,
    StrategySignal,
    StrategyPerformance,
    CombinedSignal,
    SignalType,
)


class Strategy:
    def __init__(
        self,
        strategy_id: str,
        name: str,
        parameters: Optional[Dict[str, Any]] = None,
        enabled: bool = True,
    ):
        self.strategy_id = strategy_id
        self.name = name
        self.parameters = parameters or {}
        self.enabled = enabled
        self._signals: List[StrategySignal] = []

    def generate_signals(self, data: pd.DataFrame) -> List[StrategySignal]:
        raise NotImplementedError("Each strategy must implement generate_signals")

    def get_signals(self) -> List[StrategySignal]:
        return self._signals

    def clear_signals(self):
        self._signals = []


class StrategyManager:
    def __init__(self):
        self._strategies: Dict[str, Strategy] = {}
        self._weights: Dict[str, float] = {}
        self._signals: Dict[str, List[StrategySignal]] = {}

    def add_strategy(self, strategy: Strategy, weight: float = 1.0):
        self._strategies[strategy.strategy_id] = strategy
        self._weights[strategy.strategy_id] = weight

    def remove_strategy(self, strategy_id: str):
        if strategy_id in self._strategies:
            del self._strategies[strategy_id]
        if strategy_id in self._weights:
            del self._weights[strategy_id]
        if strategy_id in self._signals:
            del self._signals[strategy_id]

    def get_strategy(self, strategy_id: str) -> Optional[Strategy]:
        return self._strategies.get(strategy_id)

    def get_all_strategies(self) -> List[Strategy]:
        return list(self._strategies.values())

    def set_weight(self, strategy_id: str, weight: float):
        if strategy_id in self._strategies:
            self._weights[strategy_id] = weight

    def get_weight(self, strategy_id: str) -> float:
        return self._weights.get(strategy_id, 0.0)

    def get_weights(self) -> Dict[str, float]:
        return self._weights.copy()

    def normalize_weights(self):
        total = sum(self._weights.values())
        if total > 0:
            self._weights = {k: v / total for k, v in self._weights.items()}

    def generate_all_signals(
        self, data_dict: Dict[str, pd.DataFrame]
    ) -> Dict[str, List[StrategySignal]]:
        for strategy_id, strategy in self._strategies.items():
            if not strategy.enabled:
                continue

            strategy.clear_signals()
            signals = []

            for symbol, data in data_dict.items():
                try:
                    strategy_signals = strategy.generate_signals(data)
                    signals.extend(strategy_signals)
                except Exception as e:
                    print(f"Error generating signals for {strategy_id} on {symbol}: {e}")

            self._signals[strategy_id] = signals

        return self._signals

    def combine_signals(
        self,
        symbol: str,
        threshold_entry: float = 0.3,
        threshold_exit: float = -0.3,
    ) -> List[CombinedSignal]:
        combined: Dict[datetime, CombinedSignal] = {}

        for strategy_id, signals in self._signals.items():
            weight = self._weights.get(strategy_id, 0)

            for signal in signals:
                if signal.symbol != symbol:
                    continue

                ts = signal.timestamp
                if ts not in combined:
                    combined[ts] = CombinedSignal(
                        timestamp=ts,
                        symbol=symbol,
                        combined_signal=0,
                        confidence=0,
                        contributing_strategies=[],
                    )

                cs = combined[ts]
                cs.combined_signal += signal.strength * weight
                cs.confidence += signal.confidence * weight
                if signal.strength != 0:
                    cs.contributing_strategies.append(strategy_id)

        result = []
        for ts, cs in sorted(combined.items()):
            if len(cs.contributing_strategies) > 0:
                cs.confidence /= len(cs.contributing_strategies)
            cs.entry_signal = cs.combined_signal >= threshold_entry
            cs.exit_signal = cs.combined_signal <= threshold_exit
            result.append(cs)

        return result

    def calculate_performance(
        self,
        trades: List[Dict[str, Any]],
        equity_curve: List[float],
    ) -> StrategyPerformance:
        if not trades:
            return StrategyPerformance(
                strategy_id="",
                total_return=0,
                total_return_pct=0,
                sharpe_ratio=0,
                max_drawdown=0,
                max_drawdown_pct=0,
                win_rate=0,
                profit_factor=0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                avg_trade_pnl=0,
            )

        df = pd.DataFrame(trades)
        df['pnl'] = df.get('pnl', 0)

        winning_trades = df[df['pnl'] > 0]
        losing_trades = df[df['pnl'] < 0]

        total_return = df['pnl'].sum()
        total_return_pct = (total_return / 100000) * 100 if len(equity_curve) > 0 else 0

        equity_series = pd.Series(equity_curve)
        returns = equity_series.pct_change().dropna()

        sharpe_ratio = 0
        if len(returns) > 0 and returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)

        cumulative = (1 + returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown_pct = abs(drawdown.min()) * 100 if len(drawdown) > 0 else 0
        max_drawdown = abs(drawdown.min() * 100000) if len(drawdown) > 0 else 0

        win_rate = len(winning_trades) / len(df) if len(df) > 0 else 0
        profit_factor = (
            abs(winning_trades['pnl'].sum() / losing_trades['pnl'].sum())
            if len(losing_trades) > 0 and losing_trades['pnl'].sum() != 0
            else 0
        )

        monthly_returns = {}

        return StrategyPerformance(
            strategy_id="portfolio",
            total_return=total_return,
            total_return_pct=total_return_pct,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_pct=max_drawdown_pct,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(df),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            avg_trade_pnl=total_return / len(df) if len(df) > 0 else 0,
            monthly_returns=monthly_returns,
            equity_curve=equity_curve,
        )


class BreakoutStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> List[StrategySignal]:
        if len(data) < 20:
            return []

        signals = []
        data['high_20'] = data['high'].rolling(20).max().shift(1)
        data['low_20'] = data['low'].rolling(20).min().shift(1)

        for i in range(20, len(data)):
            row = data.iloc[i]
            timestamp = row['timestamp'] if 'timestamp' in row else data.index[i]

            if row['close'] > row['high_20']:
                strength = min((row['close'] - row['high_20']) / row['high_20'] * 10, 1)
                signals.append(
                    StrategySignal(
                        timestamp=timestamp,
                        symbol=row['symbol'] if 'symbol' in row else data.name,
                        signal_type=SignalType.ENTRY,
                        strength=strength,
                        price=row['close'],
                        confidence=0.6,
                    )
                )
            elif row['close'] < row['low_20']:
                signals.append(
                    StrategySignal(
                        timestamp=timestamp,
                        symbol=row['symbol'] if 'symbol' in row else data.name,
                        signal_type=SignalType.EXIT,
                        strength=-0.5,
                        price=row['close'],
                        confidence=0.5,
                    )
                )

        return signals


class MeanReversionStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> List[StrategySignal]:
        if len(data) < 20:
            return []

        signals = []
        data['ma_20'] = data['close'].rolling(20).mean()
        data['std_20'] = data['close'].rolling(20).std()
        data['upper_band'] = data['ma_20'] + 2 * data['std_20']
        data['lower_band'] = data['ma_20'] - 2 * data['std_20']

        for i in range(20, len(data)):
            row = data.iloc[i]
            timestamp = row['timestamp'] if 'timestamp' in row else data.index[i]

            if row['close'] < row['lower_band']:
                deviation = (row['lower_band'] - row['close']) / row['lower_band']
                signals.append(
                    StrategySignal(
                        timestamp=timestamp,
                        symbol=row['symbol'] if 'symbol' in row else data.name,
                        signal_type=SignalType.ENTRY,
                        strength=min(deviation * 5, 1),
                        price=row['close'],
                        confidence=0.7,
                    )
                )
            elif row['close'] > row['upper_band']:
                signals.append(
                    StrategySignal(
                        timestamp=timestamp,
                        symbol=row['symbol'] if 'symbol' in row else data.name,
                        signal_type=SignalType.EXIT,
                        strength=-0.6,
                        price=row['close'],
                        confidence=0.6,
                    )
                )

        return signals


class TrendFollowingStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> List[StrategySignal]:
        if len(data) < 50:
            return []

        signals = []
        data['ema_12'] = data['close'].ewm(span=12).mean()
        data['ema_26'] = data['close'].ewm(span=26).mean()
        data['macd'] = data['ema_12'] - data['ema_26']
        data['signal'] = data['macd'].ewm(span=9).mean()

        for i in range(26, len(data)):
            row = data.iloc[i]
            timestamp = row['timestamp'] if 'timestamp' in row else data.index[i]

            if i > 0:
                prev_macd = data.iloc[i-1]['macd']
                curr_macd = row['macd']
                prev_signal = data.iloc[i-1]['signal']
                curr_signal = row['signal']

                if prev_macd < prev_signal and curr_macd > curr_signal:
                    signals.append(
                        StrategySignal(
                            timestamp=timestamp,
                            symbol=row['symbol'] if 'symbol' in row else data.name,
                            signal_type=SignalType.ENTRY,
                            strength=0.7,
                            price=row['close'],
                            confidence=0.65,
                        )
                    )
                elif prev_macd > prev_signal and curr_macd < curr_signal:
                    signals.append(
                        StrategySignal(
                            timestamp=timestamp,
                            symbol=row['symbol'] if 'symbol' in row else data.name,
                            signal_type=SignalType.EXIT,
                            strength=-0.7,
                            price=row['close'],
                            confidence=0.65,
                        )
                    )

        return signals


class RSIStrategy(Strategy):
    def generate_signals(self, data: pd.DataFrame) -> List[StrategySignal]:
        if len(data) < 14:
            return []

        signals = []
        delta = data['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))

        for i in range(14, len(data)):
            row = data.iloc[i]
            timestamp = row['timestamp'] if 'timestamp' in row else data.index[i]
            rsi = row['rsi']

            if rsi < 30:
                signals.append(
                    StrategySignal(
                        timestamp=timestamp,
                        symbol=row['symbol'] if 'symbol' in row else data.name,
                        signal_type=SignalType.ENTRY,
                        strength=(30 - rsi) / 30,
                        price=row['close'],
                        confidence=0.7,
                    )
                )
            elif rsi > 70:
                signals.append(
                    StrategySignal(
                        timestamp=timestamp,
                        symbol=row['symbol'] if 'symbol' in row else data.name,
                        signal_type=SignalType.EXIT,
                        strength=-(rsi - 70) / 30,
                        price=row['close'],
                        confidence=0.6,
                    )
                )

        return signals


strategy_manager = StrategyManager()
