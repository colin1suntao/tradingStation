from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np

from app.schemas.risk import (
    RiskConfig,
    RiskLevel,
    PositionSide,
    Position,
    RiskMetrics,
    PositionSizeRequest,
    PositionSizeResponse,
    RiskCheckRequest,
    RiskCheckResponse,
    StopLossRequest,
    TakeProfitRequest,
)


class PositionManager:
    def __init__(self):
        self._positions: Dict[str, Position] = {}
        self._closed_positions: List[Position] = []

    def add_position(self, position: Position):
        self._positions[position.symbol] = position

    def update_position(self, symbol: str, current_price: float) -> Position:
        if symbol not in self._positions:
            raise ValueError(f"Position for {symbol} not found")
        
        position = self._positions[symbol]
        position.current_price = current_price
        position.unrealized_pnl = self._calculate_pnl(position)
        position.updated_at = datetime.now()
        return position

    def close_position(self, symbol: str) -> Position:
        if symbol not in self._positions:
            raise ValueError(f"Position for {symbol} not found")
        
        position = self._positions.pop(symbol)
        position.realized_pnl += position.unrealized_pnl
        self._closed_positions.append(position)
        return position

    def get_position(self, symbol: str) -> Optional[Position]:
        return self._positions.get(symbol)

    def get_all_positions(self) -> List[Position]:
        return list(self._positions.values())

    def get_total_exposure(self) -> float:
        return sum(
            abs(p.quantity * p.current_price) 
            for p in self._positions.values()
        )

    def get_total_unrealized_pnl(self) -> float:
        return sum(p.unrealized_pnl for p in self._positions.values())

    def _calculate_pnl(self, position: Position) -> float:
        if position.side == PositionSide.LONG:
            return (position.current_price - position.entry_price) * position.quantity
        else:
            return (position.entry_price - position.current_price) * position.quantity


class RiskCalculator:
    @staticmethod
    def calculate_position_size(request: PositionSizeRequest) -> PositionSizeResponse:
        risk_amount = request.account_balance * request.risk_pct
        price_diff = abs(request.entry_price - request.stop_loss_price)
        
        if price_diff == 0:
            return PositionSizeResponse(
                position_size=0,
                quantity=0,
                risk_amount=0,
                risk_pct=0,
                leverage=request.leverage,
                stop_loss_price=request.stop_loss_price,
            )
        
        quantity = risk_amount / price_diff
        position_size = quantity * request.entry_price
        
        actual_risk = quantity * price_diff
        actual_risk_pct = actual_risk / request.account_balance if request.account_balance > 0 else 0
        
        return PositionSizeResponse(
            position_size=position_size,
            quantity=quantity,
            risk_amount=actual_risk,
            risk_pct=actual_risk_pct,
            leverage=request.leverage,
            stop_loss_price=request.stop_loss_price,
        )

    @staticmethod
    def calculate_stop_loss(
        entry_price: float, 
        side: PositionSide, 
        stop_loss_pct: float
    ) -> float:
        if side == PositionSide.LONG:
            return entry_price * (1 - stop_loss_pct)
        else:
            return entry_price * (1 + stop_loss_pct)

    @staticmethod
    def calculate_take_profit(
        entry_price: float, 
        side: PositionSide, 
        take_profit_pct: float
    ) -> float:
        if side == PositionSide.LONG:
            return entry_price * (1 + take_profit_pct)
        else:
            return entry_price * (1 - take_profit_pct)

    @staticmethod
    def calculate_liquidation_price(
        entry_price: float,
        side: PositionSide,
        leverage: float,
        maintenance_margin: float = 0.005
    ) -> float:
        if side == PositionSide.LONG:
            return entry_price * (1 - (1 / leverage) + maintenance_margin)
        else:
            return entry_price * (1 + (1 / leverage) - maintenance_margin)

    @staticmethod
    def calculate_risk_metrics(
        positions: List[Position],
        closed_positions: List[Position],
        account_balance: float,
        daily_pnl: float,
        daily_loss: float
    ) -> RiskMetrics:
        total_exposure = sum(
            abs(p.quantity * p.current_price) 
            for p in positions
        )
        total_unrealized = sum(p.unrealized_pnl for p in positions)
        total_realized = sum(p.realized_pnl for p in positions) + total_unrealized
        
        all_trades = closed_positions + [p for p in positions]
        winning_trades = [t for t in all_trades if t.realized_pnl + t.unrealized_pnl > 0]
        win_rate = len(winning_trades) / len(all_trades) if all_trades else 0
        
        available = account_balance - sum(
            p.quantity * p.current_price / p.leverage 
            for p in positions
        )
        margin_used = sum(
            p.quantity * p.current_price / p.leverage 
            for p in positions
        )
        
        risk_level = RiskCalculator._calculate_risk_level(
            total_exposure, 
            account_balance, 
            daily_loss
        )
        
        return RiskMetrics(
            total_exposure=total_exposure,
            total_unrealized_pnl=total_unrealized,
            total_realized_pnl=total_realized,
            daily_pnl=daily_pnl,
            daily_loss=daily_loss,
            win_rate=win_rate,
            account_balance=account_balance,
            available_balance=available,
            margin_used=margin_used,
            risk_level=risk_level,
        )

    @staticmethod
    def _calculate_risk_level(
        exposure: float, 
        account_balance: float,
        daily_loss: float
    ) -> RiskLevel:
        exposure_ratio = exposure / account_balance if account_balance > 0 else 0
        loss_ratio = daily_loss / account_balance if account_balance > 0 else 0
        
        if exposure_ratio > 0.8 or loss_ratio > 0.1:
            return RiskLevel.VERY_HIGH
        elif exposure_ratio > 0.6 or loss_ratio > 0.05:
            return RiskLevel.HIGH
        elif exposure_ratio > 0.4 or loss_ratio > 0.02:
            return RiskLevel.MEDIUM
        elif exposure_ratio > 0.2 or loss_ratio > 0.01:
            return RiskLevel.LOW
        else:
            return RiskLevel.VERY_LOW


class RiskManager:
    def __init__(self, config: Optional[RiskConfig] = None):
        self.config = config or RiskConfig()
        self.position_manager = PositionManager()
        self.trade_history: List[Dict[str, Any]] = []
        self.daily_stats = {
            "pnl": 0.0,
            "loss": 0.0,
            "trades": 0,
            "wins": 0,
            "losses": 0,
        }

    def set_config(self, config: RiskConfig):
        self.config = config

    def check_risk(self, request: RiskCheckRequest) -> RiskCheckResponse:
        reasons = []
        warnings = []
        approved = True

        account_balance = self._get_account_balance()
        current_exposure = self.position_manager.get_total_exposure()
        position = self.position_manager.get_position(request.symbol)

        position_value = request.quantity * request.entry_price
        new_exposure = current_exposure + position_value
        
        max_position_value = min(
            self.config.max_position_size,
            account_balance * self.config.max_position_pct
        )
        
        if position_value > max_position_value:
            reasons.append(
                f"Position size ${position_value:.2f} exceeds maximum ${max_position_value:.2f}"
            )
            approved = False
        
        if len(self.position_manager.get_all_positions()) >= self.config.max_open_positions:
            if position is None:
                reasons.append(
                    f"Maximum open positions ({self.config.max_open_positions}) reached"
                )
                approved = False
            else:
                warnings.append(
                    f"Approaching maximum positions ({len(self.position_manager.get_all_positions())}/{self.config.max_open_positions})"
                )
        
        max_exposure = account_balance * 0.95
        if new_exposure > max_exposure:
            reasons.append(
                f"Total exposure ${new_exposure:.2f} would exceed safe limit ${max_exposure:.2f}"
            )
            approved = False
        
        if request.leverage > self.config.max_leverage:
            reasons.append(
                f"Leverage {request.leverage}x exceeds maximum {self.config.max_leverage}x"
            )
            approved = False
        
        risk_amount = 0
        if request.stop_loss_price:
            price_diff = abs(request.entry_price - request.stop_loss_price)
            risk_amount = price_diff * request.quantity
            max_risk = account_balance * self.config.max_loss_per_trade
            if risk_amount > max_risk:
                reasons.append(
                    f"Risk amount ${risk_amount:.2f} exceeds maximum ${max_risk:.2f}"
                )
                approved = False
        
        daily_loss_threshold = account_balance * self.config.max_daily_loss
        if self.daily_stats["loss"] + risk_amount > daily_loss_threshold:
            reasons.append(
                f"Daily loss would exceed threshold ${daily_loss_threshold:.2f}"
            )
            approved = False
        
        if approved and risk_amount > account_balance * 0.05:
            warnings.append(
                f"Large position risk: ${risk_amount:.2f} ({risk_amount/account_balance*100:.1f}% of account)"
            )

        risk_level = self._calculate_risk_level()

        return RiskCheckResponse(
            approved=approved,
            risk_level=risk_level,
            reasons=reasons,
            warnings=warnings,
            position_size=position_value,
            risk_amount=risk_amount,
            max_position_allowed=max_position_value,
        )

    def update_position_price(self, symbol: str, current_price: float):
        position = self.position_manager.update_position(symbol, current_price)
        self._check_stop_loss(position)
        self._check_take_profit(position)

    def _check_stop_loss(self, position: Position):
        if not position.stop_loss:
            return
        
        triggered = False
        if position.side == PositionSide.LONG and position.current_price <= position.stop_loss:
            triggered = True
        elif position.side == PositionSide.SHORT and position.current_price >= position.stop_loss:
            triggered = True
        
        if triggered:
            self._trigger_stop_loss(position)

    def _check_take_profit(self, position: Position):
        if not position.take_profit:
            return
        
        triggered = False
        if position.side == PositionSide.LONG and position.current_price >= position.take_profit:
            triggered = True
        elif position.side == PositionSide.SHORT and position.current_price <= position.take_profit:
            triggered = True
        
        if triggered:
            self._trigger_take_profit(position)

    def _trigger_stop_loss(self, position: Position):
        self.log_trade(position.symbol, "stop_loss", position.unrealized_pnl)
        self.daily_stats["loss"] += abs(position.unrealized_pnl) if position.unrealized_pnl < 0 else 0

    def _trigger_take_profit(self, position: Position):
        self.log_trade(position.symbol, "take_profit", position.unrealized_pnl)
        self.daily_stats["pnl"] += position.unrealized_pnl if position.unrealized_pnl > 0 else 0

    def log_trade(self, symbol: str, trade_type: str, pnl: float):
        self.trade_history.append({
            "symbol": symbol,
            "type": trade_type,
            "pnl": pnl,
            "timestamp": datetime.now(),
        })
        self.daily_stats["trades"] += 1
        if pnl > 0:
            self.daily_stats["wins"] += 1
        else:
            self.daily_stats["losses"] += 1

    def get_metrics(self, account_balance: float) -> RiskMetrics:
        return RiskCalculator.calculate_risk_metrics(
            positions=self.position_manager.get_all_positions(),
            closed_positions=self.position_manager._closed_positions,
            account_balance=account_balance,
            daily_pnl=self.daily_stats["pnl"],
            daily_loss=self.daily_stats["loss"],
        )

    def _get_account_balance(self) -> float:
        positions = self.position_manager.get_all_positions()
        if not positions:
            return 100000.0
        return sum(p.quantity * p.current_price for p in positions) + 10000

    def _calculate_risk_level(self) -> RiskLevel:
        exposure = self.position_manager.get_total_exposure()
        account_balance = self._get_account_balance()
        return RiskCalculator._calculate_risk_level(
            exposure, 
            account_balance,
            self.daily_stats["loss"]
        )

    def reset_daily_stats(self):
        self.daily_stats = {
            "pnl": 0.0,
            "loss": 0.0,
            "trades": 0,
            "wins": 0,
            "losses": 0,
        }


risk_manager = RiskManager()
