from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime


class BacktestMode(str, Enum):
    SINGLE = "single"
    MULTI_STRATEGY = "multi_strategy"
    PORTFOLIO = "portfolio"


class AllocationMethod(str, Enum):
    EQUAL_WEIGHT = "equal_weight"
    RISK_PARITY = "risk_parity"
    MEAN_VARIANCE = "mean_variance"
    CUSTOM = "custom"


class SignalType(str, Enum):
    ENTRY = "entry"
    EXIT = "exit"
    HOLD = "hold"
    SIGNAL = "signal"


class BacktestConfig(BaseModel):
    mode: BacktestMode = Field(default=BacktestMode.SINGLE)
    symbols: List[str] = Field(default=["BTC/USDT"])
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    initial_capital: float = Field(default=100000.0, gt=0)
    commission: float = Field(default=0.001, ge=0, le=1)
    slippage: float = Field(default=0.0005, ge=0, le=1)
    allocation_method: AllocationMethod = Field(default=AllocationMethod.EQUAL_WEIGHT)
    rebalance_frequency: str = Field(default="1D")
    max_positions: int = Field(default=5, ge=1)


class StrategyWeight(BaseModel):
    strategy_id: str
    weight: float = Field(ge=0, le=1)
    enabled: bool = True
    max_allocation: Optional[float] = None


class ToolConfig(BaseModel):
    name: str
    enabled: bool = True
    parameters: Dict[str, Any] = {}


class StrategySignal(BaseModel):
    timestamp: datetime
    symbol: str
    signal_type: SignalType
    strength: float
    price: float
    confidence: float = Field(ge=0, le=1)
    metadata: Dict[str, Any] = {}


class CombinedSignal(BaseModel):
    timestamp: datetime
    symbol: str
    combined_signal: float = Field(ge=-1, le=1)
    entry_signal: bool = False
    exit_signal: bool = False
    confidence: float = Field(ge=0, le=1)
    contributing_strategies: List[str] = []
    metadata: Dict[str, Any] = {}


class Position(BaseModel):
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    entry_time: datetime
    side: Literal["long", "short"] = "long"
    pnl: float = 0.0
    pnl_pct: float = 0.0
    strategy_id: Optional[str] = None


class Trade(BaseModel):
    timestamp: datetime
    symbol: str
    side: Literal["buy", "sell"]
    quantity: float
    price: float
    commission: float = 0.0
    slippage_cost: float = 0.0
    strategy_id: Optional[str] = None
    order_type: str = "market"


class PortfolioSnapshot(BaseModel):
    timestamp: datetime
    total_value: float
    cash: float
    positions_value: float
    daily_pnl: float
    total_pnl: float
    positions: List[Position] = []
    open_positions_count: int = 0


class StrategyPerformance(BaseModel):
    strategy_id: str
    total_return: float
    total_return_pct: float
    sharpe_ratio: float
    max_drawdown: float
    max_drawdown_pct: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_trade_pnl: float
    avg_trade_duration: Optional[float] = None
    monthly_returns: Dict[str, float] = {}
    equity_curve: List[float] = []


class PortfolioPerformance(BaseModel):
    total_return: float
    total_return_pct: float
    annualized_return: float
    annualized_volatility: float
    sharpe_ratio: float
    sortino_ratio: Optional[float] = None
    max_drawdown: float
    max_drawdown_pct: float
    max_drawdown_duration: int = 0
    calmar_ratio: Optional[float] = None
    win_rate: float
    profit_factor: float
    total_trades: int
    daily_returns: List[float] = []
    monthly_returns: Dict[str, float] = {}
    equity_curve: List[float] = []
    benchmark_returns: Optional[List[float]] = None
    alpha: Optional[float] = None
    beta: Optional[float] = None


class BacktestResult(BaseModel):
    config: Dict[str, Any]
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    total_return: float
    total_return_pct: float
    portfolio_performance: PortfolioPerformance
    strategy_performances: Dict[str, StrategyPerformance] = {}
    trades: List[Trade] = []
    portfolio_snapshots: List[PortfolioSnapshot] = []
    signals: List[CombinedSignal] = []
    execution_time_ms: float = 0
    errors: List[str] = []


class RebalanceEvent(BaseModel):
    timestamp: datetime
    reason: str
    changes: Dict[str, float] = {}
    new_weights: Dict[str, float] = {}
    affected_positions: List[str] = []
