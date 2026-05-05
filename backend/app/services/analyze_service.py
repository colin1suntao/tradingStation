from typing import Dict, Any
from app.models.strategy import BacktestResult
from app.schemas.strategy import MetricResult

class AnalyzeService:
    def calculate_metrics(self, result: BacktestResult) -> MetricResult:
        """计算性能指标"""
        stats = result.stats
        return MetricResult(
            total_return=stats.get('total_return', 0.0),
            annual_return=stats.get('annual_return', 0.0),
            sharpe_ratio=stats.get('sharpe_ratio', 0.0),
            max_drawdown=stats.get('max_drawdown', 0.0),
            win_rate=stats.get('win_rate', 0.0),
            profit_factor=stats.get('profit_factor', 0.0),
            volatility=stats.get('volatility', 0.2),
            max_consecutive_losses=stats.get('max_consecutive_losses', 3)
        )
    
    def generate_charts(self, result: BacktestResult) -> Dict[str, Any]:
        """生成图表数据"""
        return {
            'equity_curve': result.equity_curve,
            'drawdown': result.drawdown.get('underwater', {}),
            'trades': result.trades
        }
    
    def risk_analysis(self, result: BacktestResult) -> Dict[str, Any]:
        """风险分析"""
        stats = result.stats
        drawdown = result.drawdown
        
        return {
            'max_drawdown': drawdown.get('max', 0.0),
            'max_drawdown_duration': drawdown.get('duration', 15),
            'sharpe_ratio': stats.get('sharpe_ratio', 0.0),
            'volatility': stats.get('volatility', 0.2),
            'risk_return_ratio': (stats.get('total_return', 0) / abs(stats.get('max_drawdown', 1.0))) if stats.get('max_drawdown') else 0,
            'total_trades': stats.get('total_trades', 0),
            'win_rate': stats.get('win_rate', 0.5)
        }
    
    def get_summary(self, result: BacktestResult) -> Dict[str, Any]:
        """获取摘要"""
        return result.summary
