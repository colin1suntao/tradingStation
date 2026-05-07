from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime
from decimal import Decimal


class RiskLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class PositionSide(str, Enum):
    LONG = "long"
    SHORT = "short"
    BOTH = "both"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    STOP_LIMIT = "stop_limit"


class OrderStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Position(BaseModel):
    symbol: str
    side: PositionSide
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    leverage: float = 1.0
    margin_used: float = 0.0
    liquidation_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    opened_at: datetime
    updated_at: datetime


class RiskConfig(BaseModel):
    max_position_size: float = Field(default=10000.0, description="最大持仓金额（USD）")
    max_position_pct: float = Field(default=0.2, ge=0, le=1, description="最大持仓比例（占总资金）")
    max_loss_per_trade: float = Field(default=0.02, ge=0, le=1, description="单笔最大亏损比例")
    max_daily_loss: float = Field(default=0.05, ge=0, le=1, description="日最大亏损比例")
    max_leverage: float = Field(default=1.0, ge=1, le=100, description="最大杠杆倍数")
    max_open_positions: int = Field(default=5, ge=1, description="最大同时持仓数")
    stop_loss_pct: float = Field(default=0.02, ge=0, le=1, description="默认止损比例")
    take_profit_pct: float = Field(default=0.05, ge=0, le=1, description="默认止盈比例")
    trailing_stop_pct: Optional[float] = Field(default=None, ge=0, le=1, description="移动止损比例")
    risk_per_trade_pct: float = Field(default=0.01, ge=0, le=0.1, description="每笔交易风险比例")


class PositionSizeRequest(BaseModel):
    account_balance: float
    entry_price: float
    stop_loss_price: float
    risk_pct: float = Field(default=0.01, ge=0, le=0.1)
    leverage: float = Field(default=1.0, ge=1, le=100)


class PositionSizeResponse(BaseModel):
    position_size: float
    quantity: float
    risk_amount: float
    risk_pct: float
    leverage: float
    stop_loss_price: float
    take_profit_price: Optional[float] = None


class RiskMetrics(BaseModel):
    total_exposure: float
    total_unrealized_pnl: float
    total_realized_pnl: float
    daily_pnl: float
    daily_loss: float
    win_rate: float
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    account_balance: float
    available_balance: float
    margin_used: float
    risk_level: RiskLevel


class StopLossRequest(BaseModel):
    symbol: str
    stop_loss_price: Optional[float] = None
    stop_loss_pct: Optional[float] = None
    trailing_stop: bool = False
    trailing_stop_pct: Optional[float] = None


class TakeProfitRequest(BaseModel):
    symbol: str
    take_profit_price: Optional[float] = None
    take_profit_pct: Optional[float] = None


class RiskCheckRequest(BaseModel):
    symbol: str
    side: PositionSide
    quantity: float
    entry_price: float
    stop_loss_price: Optional[float] = None
    take_profit_price: Optional[float] = None
    leverage: float = 1.0


class RiskCheckResponse(BaseModel):
    approved: bool
    risk_level: RiskLevel
    reasons: List[str] = []
    warnings: List[str] = []
    position_size: Optional[float] = None
    risk_amount: Optional[float] = None
    max_position_allowed: Optional[float] = None
