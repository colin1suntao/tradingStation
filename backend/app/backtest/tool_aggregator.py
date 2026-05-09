from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import pandas as pd
import numpy as np

from app.schemas.backtest import ToolConfig, CombinedSignal


class BaseTool:
    def __init__(self, name: str, parameters: Optional[Dict[str, Any]] = None):
        self.name = name
        self.parameters = parameters or {}
        self.enabled = True

    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        raise NotImplementedError("Each tool must implement analyze method")

    def get_value(self) -> float:
        return 0.0


class TechnicalIndicatorTool(BaseTool):
    def __init__(self, name: str, indicators: List[str], parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, parameters)
        self.indicators = indicators

    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {'tool': self.name, 'signals': {}}

        for indicator in self.indicators:
            if indicator == 'rsi':
                results['signals']['rsi'] = self._calculate_rsi(data)
            elif indicator == 'macd':
                results['signals']['macd'] = self._calculate_macd(data)
            elif indicator == 'bollinger':
                results['signals']['bollinger'] = self._calculate_bollinger(data)
            elif indicator == 'sma':
                results['signals']['sma'] = self._calculate_sma(data)
            elif indicator == 'atr':
                results['signals']['atr'] = self._calculate_atr(data)
            elif indicator == 'stochastic':
                results['signals']['stochastic'] = self._calculate_stochastic(data)

        return results

    def _calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> Dict[str, float]:
        delta = data['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return {'value': rsi.iloc[-1], 'signal': 'neutral'}

    def _calculate_macd(self, data: pd.DataFrame) -> Dict[str, float]:
        ema12 = data['close'].ewm(span=12).mean()
        ema26 = data['close'].ewm(span=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        return {'value': macd.iloc[-1], 'signal': macd.iloc[-1], 'histogram': (macd - signal).iloc[-1]}

    def _calculate_bollinger(self, data: pd.DataFrame, period: int = 20) -> Dict[str, float]:
        sma = data['close'].rolling(period).mean()
        std = data['close'].rolling(period).std()
        upper = sma + 2 * std
        lower = sma - 2 * std
        return {'value': data['close'].iloc[-1], 'upper': upper.iloc[-1], 'lower': lower.iloc[-1], 'sma': sma.iloc[-1]}

    def _calculate_sma(self, data: pd.DataFrame, periods: List[int] = None) -> Dict[str, float]:
        if periods is None:
            periods = [20, 50, 200]
        return {f'sma_{p}': data['close'].rolling(p).mean().iloc[-1] for p in periods}

    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> Dict[str, float]:
        high_low = data['high'] - data['low']
        high_close = abs(data['high'] - data['close'].shift())
        low_close = abs(data['low'] - data['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(period).mean()
        return {'value': atr.iloc[-1]}

    def _calculate_stochastic(self, data: pd.DataFrame, period: int = 14) -> Dict[str, float]:
        low_min = data['low'].rolling(period).min()
        high_max = data['high'].rolling(period).max()
        k = 100 * (data['close'] - low_min) / (high_max - low_min)
        d = k.rolling(3).mean()
        return {'k': k.iloc[-1], 'd': d.iloc[-1]}


class SentimentTool(BaseTool):
    def __init__(self, name: str = "sentiment", source: str = "mock"):
        super().__init__(name)
        self.source = source

    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {'tool': self.name, 'signals': {}}

        if len(data) > 20:
            returns = data['close'].pct_change()
            volatility = returns.rolling(20).std().iloc[-1]
            trend = returns.rolling(20).mean().iloc[-1]

            sentiment_score = 0.5
            if trend > 0:
                sentiment_score = min(0.5 + abs(trend) * 10, 1.0)
            elif trend < 0:
                sentiment_score = max(0.5 - abs(trend) * 10, 0.0)

            results['signals']['sentiment'] = {
                'score': sentiment_score,
                'trend': trend,
                'volatility': volatility,
                'signal': 'bullish' if sentiment_score > 0.6 else ('bearish' if sentiment_score < 0.4 else 'neutral')
            }

        return results


class PatternRecognitionTool(BaseTool):
    def __init__(self, name: str = "pattern"):
        super().__init__(name)

    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {'tool': self.name, 'signals': {}, 'patterns': []}

        if len(data) >= 50:
            recent = data.tail(50)

            if self._is_golden_cross(recent):
                results['patterns'].append('golden_cross')
                results['signals']['pattern'] = 0.8
            elif self._is_death_cross(recent):
                results['patterns'].append('death_cross')
                results['signals']['pattern'] = -0.8
            elif self._is_doji(recent.iloc[-1]):
                results['patterns'].append('doji')
                results['signals']['pattern'] = 0.0

        return results

    def _is_golden_cross(self, data: pd.DataFrame) -> bool:
        if len(data) < 200:
            return False
        sma_50 = data['close'].rolling(50).mean()
        sma_200 = data['close'].rolling(200).mean()
        return sma_50.iloc[-1] > sma_200.iloc[-1] and sma_50.iloc[-2] <= sma_200.iloc[-2]

    def _is_death_cross(self, data: pd.DataFrame) -> bool:
        if len(data) < 200:
            return False
        sma_50 = data['close'].rolling(50).mean()
        sma_200 = data['close'].rolling(200).mean()
        return sma_50.iloc[-1] < sma_200.iloc[-1] and sma_50.iloc[-2] >= sma_200.iloc[-2]

    def _is_doji(self, candle) -> bool:
        body = abs(candle['close'] - candle['open'])
        upper_shadow = candle['high'] - max(candle['close'], candle['open'])
        lower_shadow = min(candle['close'], candle['open']) - candle['low']
        return body < (candle['high'] - candle['low']) * 0.1


class VolumeAnalysisTool(BaseTool):
    def __init__(self, name: str = "volume"):
        super().__init__(name)

    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {'tool': self.name, 'signals': {}}

        if len(data) >= 20:
            volume = data['volume']
            vol_ma = volume.rolling(20).mean()
            current_vol = volume.iloc[-1]
            avg_vol = vol_ma.iloc[-1]

            vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1

            price_change = (data['close'].iloc[-1] - data['close'].iloc[-2]) / data['close'].iloc[-2]

            if vol_ratio > 1.5 and price_change > 0:
                signal = 0.6
            elif vol_ratio > 1.5 and price_change < 0:
                signal = -0.6
            else:
                signal = 0.0

            results['signals']['volume'] = {
                'ratio': vol_ratio,
                'signal': signal,
                'avg_volume': avg_vol,
                'current_volume': current_vol
            }

        return results


class ToolAggregator:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._tool_configs: Dict[str, ToolConfig] = {}

    def add_tool(self, tool: BaseTool, config: Optional[ToolConfig] = None):
        self._tools[tool.name] = tool
        if config:
            self._tool_configs[tool.name] = config

    def remove_tool(self, name: str):
        if name in self._tools:
            del self._tools[name]
        if name in self._tool_configs:
            del self._tool_configs[name]

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())

    def analyze_with_all_tools(self, data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        results = {}
        for name, tool in self._tools.items():
            if tool.enabled:
                try:
                    results[name] = tool.analyze(data)
                except Exception as e:
                    results[name] = {'tool': name, 'error': str(e)}
        return results

    def aggregate_signals(
        self,
        tool_results: Dict[str, Dict[str, Any]],
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        if not tool_results:
            return 0.0

        total_signal = 0.0
        total_weight = 0.0

        for tool_name, result in tool_results.items():
            if 'error' in result:
                continue

            weight = weights.get(tool_name, 1.0) if weights else 1.0
            signal = self._extract_signal(result)
            total_signal += signal * weight
            total_weight += weight

        return total_signal / total_weight if total_weight > 0 else 0.0

    def _extract_signal(self, result: Dict[str, Any]) -> float:
        signals = result.get('signals', {})

        signal_values = []
        for key, value in signals.items():
            if isinstance(value, dict):
                if 'signal' in value:
                    v = value['signal']
                    if isinstance(v, (int, float)):
                        signal_values.append(v)
                    elif isinstance(v, str):
                        if v == 'bullish':
                            signal_values.append(1)
                        elif v == 'bearish':
                            signal_values.append(-1)
                if 'pattern' in value:
                    v = value['pattern']
                    if isinstance(v, (int, float)):
                        signal_values.append(v)
                if 'score' in value:
                    score = value['score']
                    if isinstance(score, (int, float)):
                        signal_values.append(score * 2 - 1)
            elif isinstance(value, (int, float)):
                if abs(value) < 100:
                    signal_values.append(value)

        if signal_values:
            return sum(signal_values) / len(signal_values)
        return 0.0

    def get_combined_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = self.analyze_with_all_tools(data)
        combined_signal = self.aggregate_signals(results)

        return {
            'timestamp': datetime.now(),
            'combined_signal': combined_signal,
            'signal_strength': abs(combined_signal),
            'signal_direction': 'bullish' if combined_signal > 0.3 else ('bearish' if combined_signal < -0.3 else 'neutral'),
            'tool_results': results,
            'tool_count': len(results),
        }


tool_aggregator = ToolAggregator()
