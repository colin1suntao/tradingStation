from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

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
