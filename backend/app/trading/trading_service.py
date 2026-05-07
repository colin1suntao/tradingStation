from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from app.schemas.trading import (
    OrderRequest,
    OrderResponse,
    TradeExecution,
    ExecutionResult,
    OrderSide,
    OrderType,
)
from app.schemas.risk import (
    RiskCheckRequest,
    PositionSide,
)
from app.trading.exchange_manager import exchange_manager
from app.risk.risk_manager import risk_manager


class TradingService:
    def __init__(self):
        self.execution_history: List[ExecutionResult] = []

    def execute_trade(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        price: Optional[float] = None,
        order_type: OrderType = OrderType.MARKET,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        exchange_name: str = 'default',
        risk_check: bool = True,
    ) -> ExecutionResult:
        execution_id = str(uuid.uuid4())
        
        risk_check_request = RiskCheckRequest(
            symbol=symbol,
            side=PositionSide.LONG if side == OrderSide.BUY else PositionSide.SHORT,
            quantity=quantity,
            entry_price=price or 0,
            stop_loss_price=stop_loss,
            take_profit_price=take_profit,
        )
        
        if risk_check:
            risk_result = risk_manager.check_risk(risk_check_request)
            if not risk_result.approved:
                return ExecutionResult(
                    execution_id=execution_id,
                    success=False,
                    error_message=f"Risk check failed: {'; '.join(risk_result.reasons)}",
                    risk_metrics_snapshot=risk_result.model_dump(),
                )

        order_request = OrderRequest(
            exchange='binance',
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        try:
            exchange = exchange_manager.get_exchange(exchange_name)
            if not exchange:
                return ExecutionResult(
                    execution_id=execution_id,
                    success=False,
                    error_message=f"Exchange '{exchange_name}' not configured",
                )

            order_response = exchange.create_order(order_request)

            result = ExecutionResult(
                execution_id=execution_id,
                success=True,
                order_id=order_response.order_id,
                filled_quantity=order_response.filled_quantity,
                average_price=order_response.average_price,
            )

            self.execution_history.append(result)
            return result

        except Exception as e:
            result = ExecutionResult(
                execution_id=execution_id,
                success=False,
                error_message=str(e),
            )
            self.execution_history.append(result)
            return result

    def place_order_with_protection(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        entry_price: Optional[float] = None,
        stop_loss_pct: float = 0.02,
        take_profit_pct: float = 0.05,
        exchange_name: str = 'default',
        risk_check: bool = True,
    ) -> Dict[str, Any]:
        results = {
            'entry_order': None,
            'stop_loss_order': None,
            'take_profit_order': None,
            'all_success': True,
            'errors': [],
        }

        current_price = entry_price
        if not current_price:
            exchange = exchange_manager.get_exchange(exchange_name)
            if exchange:
                ticker = exchange.fetch_ticker(symbol)
                current_price = ticker['last']

        if side == OrderSide.BUY:
            stop_loss_price = current_price * (1 - stop_loss_pct)
            take_profit_price = current_price * (1 + take_profit_pct)
        else:
            stop_loss_price = current_price * (1 + stop_loss_pct)
            take_profit_price = current_price * (1 - take_profit_pct)

        entry_result = self.execute_trade(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=entry_price,
            order_type=OrderType.MARKET,
            stop_loss=stop_loss_price,
            take_profit=take_profit_price,
            exchange_name=exchange_name,
            risk_check=risk_check,
        )
        results['entry_order'] = entry_result.model_dump()
        results['all_success'] = results['all_success'] and entry_result.success
        if not entry_result.success:
            results['errors'].append(entry_result.error_message)

        if entry_result.success and stop_loss_price:
            sl_result = self._place_protective_order(
                symbol=symbol,
                side=OrderSide.SELL if side == OrderSide.BUY else OrderSide.BUY,
                order_type=OrderType.STOP_LOSS,
                quantity=quantity,
                trigger_price=stop_loss_price,
                exchange_name=exchange_name,
            )
            results['stop_loss_order'] = sl_result.model_dump()
            results['all_success'] = results['all_success'] and sl_result.success

        if entry_result.success and take_profit_price:
            tp_result = self._place_protective_order(
                symbol=symbol,
                side=OrderSide.SELL if side == OrderSide.BUY else OrderSide.BUY,
                order_type=OrderType.TAKE_PROFIT,
                quantity=quantity,
                trigger_price=take_profit_price,
                exchange_name=exchange_name,
            )
            results['take_profit_order'] = tp_result.model_dump()
            results['all_success'] = results['all_success'] and tp_result.success

        return results

    def _place_protective_order(
        self,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: float,
        trigger_price: float,
        exchange_name: str = 'default',
    ) -> ExecutionResult:
        execution_id = str(uuid.uuid4())

        try:
            exchange = exchange_manager.get_exchange(exchange_name)
            if not exchange:
                return ExecutionResult(
                    execution_id=execution_id,
                    success=False,
                    error_message=f"Exchange '{exchange_name}' not configured",
                )

            order_request = OrderRequest(
                exchange='binance',
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                stop_price=trigger_price,
                reduce_only=True,
            )

            order_response = exchange.create_order(order_request)

            result = ExecutionResult(
                execution_id=execution_id,
                success=True,
                order_id=order_response.order_id,
            )
            return result

        except Exception as e:
            return ExecutionResult(
                execution_id=execution_id,
                success=False,
                error_message=str(e),
            )

    def close_position(
        self,
        symbol: str,
        quantity: Optional[float] = None,
        exchange_name: str = 'default',
    ) -> ExecutionResult:
        position = risk_manager.position_manager.get_position(symbol)
        if not position:
            return ExecutionResult(
                execution_id=str(uuid.uuid4()),
                success=False,
                error_message=f"No open position for {symbol}",
            )

        close_quantity = quantity or position.quantity
        side = OrderSide.SELL if position.side == PositionSide.LONG else OrderSide.BUY

        result = self.execute_trade(
            symbol=symbol,
            side=side,
            quantity=close_quantity,
            exchange_name=exchange_name,
            risk_check=False,
        )

        if result.success:
            risk_manager.position_manager.close_position(symbol)

        return result

    def get_open_positions(self) -> List[Dict[str, Any]]:
        positions = risk_manager.position_manager.get_all_positions()
        return [p.model_dump() for p in positions]

    def get_execution_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        return [e.model_dump() for e in self.execution_history[-limit:]]

    def cancel_all_orders(self, symbol: Optional[str] = None, exchange_name: str = 'default'):
        exchange = exchange_manager.get_exchange(exchange_name)
        if exchange:
            open_orders = exchange.fetch_open_orders(symbol)
            for order in open_orders:
                exchange.cancel_order(order.order_id, order.symbol)


trading_service = TradingService()
