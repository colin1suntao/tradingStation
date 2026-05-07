from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime


class ExchangeType(str, Enum):
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRKEN = "kraken"
    OKX = "okx"
    BYBIT = "bybit"


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    STOP_LIMIT = "stop_limit"


class TimeInForce(str, Enum):
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


class OrderRequest(BaseModel):
    exchange: ExchangeType
    symbol: str
    side: OrderSide
    order_type: OrderType = OrderType.MARKET
    quantity: Optional[float] = None
    quote_quantity: Optional[float] = None
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.GTC
    reduce_only: bool = False
    position_side: Optional[str] = None


class OrderResponse(BaseModel):
    order_id: str
    exchange: str
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float]
    status: str
    filled_quantity: float = 0.0
    average_price: Optional[float] = None
    created_at: datetime
    updated_at: datetime


class AccountBalance(BaseModel):
    exchange: str
    total_balance: float
    available_balance: float
    locked_balance: float
    positions: List[Dict[str, Any]] = []


class ExchangeConfig(BaseModel):
    exchange: ExchangeType
    api_key: str
    api_secret: str
    passphrase: Optional[str] = None
    testnet: bool = False
    max_retries: int = 3
    timeout: int = 30


class TradingPair(BaseModel):
    symbol: str
    base_currency: str
    quote_currency: str
    price_precision: int
    quantity_precision: int
    min_quantity: float
    max_quantity: float
    min_notional: float
    is_trading: bool = True


class TradeExecution(BaseModel):
    decision_id: str
    agent_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    risk_check_passed: bool
    execution_time: datetime


class ExecutionResult(BaseModel):
    execution_id: str
    success: bool
    order_id: Optional[str] = None
    filled_quantity: float = 0.0
    average_price: Optional[float] = None
    error_message: Optional[str] = None
    risk_metrics_snapshot: Dict[str, Any] = {}
