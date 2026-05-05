"""
策略研究环境演示版本
不依赖数据库，使用内存存储
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import pandas as pd
import numpy as np
import ast

# 模拟数据存储
strategies = []
backtest_tasks = []
backtest_results = []
next_strategy_id = 1
next_task_id = 1
next_result_id = 1

# 状态枚举
class StrategyStatus(str, Enum):
    DRAFT = "draft"
    TESTING = "testing"
    LIVE = "live"
    ARCHIVED = "archived"

class BacktestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# Pydantic 模型
class StrategyBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    code_content: str
    parameters: Dict[str, Any]
    asset_class: str

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code_content: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class Strategy(StrategyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    version: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class BacktestTaskBase(BaseModel):
    name: str
    instrument_ids: List[int]
    timeframe: str
    start_time: datetime
    end_time: datetime
    parameters: Optional[Dict[str, Any]] = None

class BacktestTaskCreate(BacktestTaskBase):
    strategy_id: int

class BacktestTask(BacktestTaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    strategy_id: int
    status: str
    progress: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class BacktestResultBase(BaseModel):
    equity_curve: Dict[str, Any]
    stats: Dict[str, Any]
    trades: List[Dict[str, Any]]
    drawdown: Dict[str, Any]
    summary: Dict[str, Any]

class BacktestResult(BacktestResultBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    task_id: int
    strategy_id: int
    created_at: datetime

class ValidationResult(BaseModel):
    valid: bool
    message: str
    errors: List[str] = []

class MetricResult(BaseModel):
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    volatility: float
    max_consecutive_losses: int

# 回测引擎
class BacktestEngine:
    def run_strategy(self, data, strategy_code, params):
        try:
            exec_globals = {'pd': pd, 'np': np, 'params': params, 'data': data}
            exec(strategy_code, exec_globals)
            
            if 'Strategy' in exec_globals:
                strategy_class = exec_globals['Strategy']
                strategy = strategy_class(params)
                strategy.initialize({'data': data})
                
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
            
            return self._generate_mock_results(data)
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def _generate_mock_results(self, data):
        initial_equity = 10000.0
        equity = [initial_equity]
        for i in range(1, len(data)):
            change = np.random.uniform(-0.02, 0.03)
            equity.append(equity[-1] * (1 + change))
        
        equity_curve = {str(date): val for date, val in zip(data.index, equity)}
        
        total_return = (equity[-1] - equity[0]) / equity[0]
        annual_return = (1 + total_return) ** (365 / len(data)) - 1
        max_drawdown = np.min([(equity[i] - np.max(equity[:i+1])) / np.max(equity[:i+1]) for i in range(len(equity))])
        returns = [(equity[i+1]/equity[i])-1 for i in range(len(equity)-1)]
        sharpe_ratio = np.mean(returns) / np.std(returns) if returns else 0
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
        
        drawdown = {
            'max': float(max_drawdown),
            'duration': 15,
            'underwater': {str(date): float(val) for date, val in zip(data.index, np.random.uniform(-0.1, 0, len(data)))}
        }
        
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

# FastAPI 应用
app = FastAPI(title="TradingStation Strategy Research Demo", version="0.1")

# 策略管理 API
@app.get("/api/v1/strategies", response_model=List[Strategy])
async def get_strategies():
    return strategies

@app.get("/api/v1/strategies/{strategy_id}", response_model=Strategy)
async def get_strategy(strategy_id: int):
    for s in strategies:
        if s['id'] == strategy_id:
            return s
    raise HTTPException(status_code=404, detail="Strategy not found")

@app.post("/api/v1/strategies", response_model=Strategy)
async def create_strategy(strategy_in: StrategyCreate):
    global next_strategy_id
    
    for s in strategies:
        if s['code'] == strategy_in.code:
            raise HTTPException(status_code=400, detail="Strategy code already exists")
    
    errors = []
    try:
        ast.parse(strategy_in.code_content)
    except SyntaxError as e:
        errors.append(f"Syntax error: {e.msg}")
    
    if 'class Strategy' not in strategy_in.code_content:
        errors.append("Strategy class not found")
    
    if 'def on_bar' not in strategy_in.code_content:
        errors.append("on_bar method not found")
    
    if errors:
        raise HTTPException(status_code=400, detail=", ".join(errors))
    
    strategy = {
        'id': next_strategy_id,
        'name': strategy_in.name,
        'code': strategy_in.code,
        'description': strategy_in.description,
        'code_content': strategy_in.code_content,
        'parameters': strategy_in.parameters,
        'asset_class': strategy_in.asset_class,
        'status': 'draft',
        'version': 1,
        'created_at': datetime.now(),
        'updated_at': None
    }
    next_strategy_id += 1
    strategies.append(strategy)
    return strategy

@app.put("/api/v1/strategies/{strategy_id}", response_model=Strategy)
async def update_strategy(strategy_id: int, strategy_in: StrategyUpdate):
    for s in strategies:
        if s['id'] == strategy_id:
            if strategy_in.name:
                s['name'] = strategy_in.name
            if strategy_in.description:
                s['description'] = strategy_in.description
            if strategy_in.code_content:
                # 验证代码
                errors = []
                try:
                    ast.parse(strategy_in.code_content)
                except SyntaxError as e:
                    errors.append(f"Syntax error: {e.msg}")
                if 'class Strategy' not in strategy_in.code_content:
                    errors.append("Strategy class not found")
                if 'def on_bar' not in strategy_in.code_content:
                    errors.append("on_bar method not found")
                if errors:
                    raise HTTPException(status_code=400, detail=", ".join(errors))
                s['code_content'] = strategy_in.code_content
            if strategy_in.parameters:
                s['parameters'] = strategy_in.parameters
            if strategy_in.status:
                s['status'] = strategy_in.status
            s['version'] += 1
            s['updated_at'] = datetime.now()
            return s
    raise HTTPException(status_code=404, detail="Strategy not found")

@app.delete("/api/v1/strategies/{strategy_id}")
async def delete_strategy(strategy_id: int):
    global strategies
    for i, s in enumerate(strategies):
        if s['id'] == strategy_id:
            strategies.pop(i)
            return {"message": "Strategy deleted"}
    raise HTTPException(status_code=404, detail="Strategy not found")

@app.post("/api/v1/strategies/validate", response_model=ValidationResult)
async def validate_strategy(code_content: str):
    errors = []
    try:
        ast.parse(code_content)
    except SyntaxError as e:
        errors.append(f"Syntax error: {e.msg}")
    
    if 'class Strategy' not in code_content:
        errors.append("Strategy class not found")
    
    if 'def on_bar' not in code_content:
        errors.append("on_bar method not found")
    
    return ValidationResult(
        valid=len(errors) == 0,
        message="Valid" if len(errors) == 0 else "Invalid",
        errors=errors
    )

# 回测 API
@app.get("/api/v1/backtests", response_model=List[BacktestTask])
async def get_backtests():
    return backtest_tasks

@app.get("/api/v1/backtests/{task_id}", response_model=BacktestTask)
async def get_backtest(task_id: int):
    for t in backtest_tasks:
        if t['id'] == task_id:
            return t
    raise HTTPException(status_code=404, detail="Backtest not found")

@app.post("/api/v1/backtests", response_model=BacktestTask)
async def create_backtest(backtest_in: BacktestTaskCreate):
    global next_task_id
    
    task = {
        'id': next_task_id,
        'strategy_id': backtest_in.strategy_id,
        'name': backtest_in.name,
        'instrument_ids': backtest_in.instrument_ids,
        'timeframe': backtest_in.timeframe,
        'start_time': backtest_in.start_time,
        'end_time': backtest_in.end_time,
        'parameters': backtest_in.parameters,
        'status': 'pending',
        'progress': 0,
        'created_at': datetime.now(),
        'started_at': None,
        'completed_at': None
    }
    next_task_id += 1
    backtest_tasks.append(task)
    return task

@app.post("/api/v1/backtests/{task_id}/run", response_model=BacktestResult)
async def run_backtest(task_id: int):
    global next_result_id
    
    for t in backtest_tasks:
        if t['id'] == task_id:
            t['status'] = 'running'
            t['started_at'] = datetime.now()
            
            # 查找策略
            strategy = None
            for s in strategies:
                if s['id'] == t['strategy_id']:
                    strategy = s
                    break
            
            if not strategy:
                raise HTTPException(status_code=400, detail="Strategy not found")
            
            # 生成模拟数据
            dates = pd.date_range(t['start_time'], t['end_time'], freq='D')
            data = pd.DataFrame({
                'open': pd.Series([100 + i * 0.1 for i in range(len(dates))], index=dates),
                'high': pd.Series([100 + i * 0.1 + 1 for i in range(len(dates))], index=dates),
                'low': pd.Series([100 + i * 0.1 - 1 for i in range(len(dates))], index=dates),
                'close': pd.Series([100 + i * 0.1 for i in range(len(dates))], index=dates),
                'volume': pd.Series([10000 for _ in range(len(dates))], index=dates)
            })
            
            engine = BacktestEngine()
            params = t['parameters'] or {}
            result_data = engine.run_strategy(data, strategy['code_content'], params)
            
            result = {
                'id': next_result_id,
                'task_id': task_id,
                'strategy_id': t['strategy_id'],
                'equity_curve': result_data['equity_curve'],
                'stats': result_data['stats'],
                'trades': result_data['trades'],
                'drawdown': result_data['drawdown'],
                'summary': result_data['summary'],
                'created_at': datetime.now()
            }
            next_result_id += 1
            backtest_results.append(result)
            
            t['status'] = 'completed'
            t['progress'] = 100
            t['completed_at'] = datetime.now()
            
            return result
    
    raise HTTPException(status_code=404, detail="Backtest not found")

@app.delete("/api/v1/backtests/{task_id}")
async def cancel_backtest(task_id: int):
    for t in backtest_tasks:
        if t['id'] == task_id:
            if t['status'] == 'pending':
                t['status'] = 'cancelled'
                t['completed_at'] = datetime.now()
                return {"message": "Backtest cancelled"}
            else:
                raise HTTPException(status_code=400, detail="Cannot cancel running or completed backtest")
    raise HTTPException(status_code=404, detail="Backtest not found")

# 分析 API
@app.get("/api/v1/analyze/{result_id}/metrics", response_model=MetricResult)
async def get_metrics(result_id: int):
    for r in backtest_results:
        if r['id'] == result_id:
            stats = r['stats']
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
    raise HTTPException(status_code=404, detail="Result not found")

@app.get("/api/v1/analyze/{result_id}/charts")
async def get_charts(result_id: int):
    for r in backtest_results:
        if r['id'] == result_id:
            return {
                'equity_curve': r['equity_curve'],
                'drawdown': r['drawdown'].get('underwater', {}),
                'trades': r['trades']
            }
    raise HTTPException(status_code=404, detail="Result not found")

@app.get("/api/v1/analyze/{result_id}/risk")
async def get_risk_analysis(result_id: int):
    for r in backtest_results:
        if r['id'] == result_id:
            stats = r['stats']
            drawdown = r['drawdown']
            return {
                'max_drawdown': drawdown.get('max', 0.0),
                'max_drawdown_duration': drawdown.get('duration', 15),
                'sharpe_ratio': stats.get('sharpe_ratio', 0.0),
                'volatility': stats.get('volatility', 0.2),
                'risk_return_ratio': (stats.get('total_return', 0) / abs(stats.get('max_drawdown', 1.0))) if stats.get('max_drawdown') else 0,
                'total_trades': stats.get('total_trades', 0),
                'win_rate': stats.get('win_rate', 0.5)
            }
    raise HTTPException(status_code=404, detail="Result not found")

@app.get("/api/v1/analyze/{result_id}/summary")
async def get_summary(result_id: int):
    for r in backtest_results:
        if r['id'] == result_id:
            return r['summary']
    raise HTTPException(status_code=404, detail="Result not found")

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    return {"message": "TradingStation Strategy Research Demo", "version": "0.1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
