from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, List, Dict, Any
from app.schemas.trading import (
    OrderRequest,
    OrderResponse,
    ExchangeType,
    ExchangeConfig,
    TradingPair,
    OrderSide,
    OrderType,
)
from app.schemas.risk import PositionSide
from app.trading.trading_service import trading_service
from app.trading.exchange_manager import exchange_manager

router = APIRouter(prefix="/trading", tags=["Trading"])


@router.post("/exchange/connect", summary="Connect to exchange")
async def connect_exchange(
    name: str = "default",
    exchange_type: ExchangeType = ExchangeType.BINANCE,
    api_key: str = "",
    api_secret: str = "",
    testnet: bool = True,
):
    try:
        exchange_manager.add_exchange(
            name=name,
            exchange_type=exchange_type,
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet,
        )
        return {
            "success": True,
            "message": f"Connected to {exchange_type.value}",
            "exchange": name,
            "testnet": testnet,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/exchange/{name}", summary="Disconnect from exchange")
async def disconnect_exchange(name: str = "default"):
    exchange_manager.remove_exchange(name)
    return {
        "success": True,
        "message": f"Disconnected from {name}",
    }


@router.get("/exchange", summary="List connected exchanges")
async def list_exchanges():
    exchanges = exchange_manager.list_exchanges()
    return {
        "exchanges": exchanges,
        "count": len(exchanges),
    }


@router.get("/balance", summary="Get account balance")
async def get_balance(exchange_name: str = "default"):
    balance = exchange_manager.get_balance(exchange_name)
    if not balance:
        raise HTTPException(status_code=404, detail=f"Exchange '{exchange_name}' not connected")
    return balance


@router.post("/order", summary="Place a new order")
async def place_order(
    symbol: str,
    side: OrderSide,
    quantity: float,
    order_type: OrderType = OrderType.MARKET,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
    exchange_name: str = "default",
):
    try:
        order_request = OrderRequest(
            exchange=exchange_type,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )
        exchange = exchange_manager.get_exchange(exchange_name)
        if not exchange:
            raise HTTPException(status_code=404, detail=f"Exchange '{exchange_name}' not configured")
        
        order = exchange.create_order(order_request)
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/order/with-protection", summary="Place order with stop loss and take profit")
async def place_order_with_protection(
    symbol: str,
    side: OrderSide,
    quantity: float,
    entry_price: Optional[float] = None,
    stop_loss_pct: float = 0.02,
    take_profit_pct: float = 0.05,
    exchange_name: str = "default",
):
    result = trading_service.place_order_with_protection(
        symbol=symbol,
        side=side,
        quantity=quantity,
        entry_price=entry_price,
        stop_loss_pct=stop_loss_pct,
        take_profit_pct=take_profit_pct,
        exchange_name=exchange_name,
    )
    return result


@router.delete("/order/{order_id}", summary="Cancel an order")
async def cancel_order(
    order_id: str,
    symbol: str,
    exchange_name: str = "default",
):
    exchange = exchange_manager.get_exchange(exchange_name)
    if not exchange:
        raise HTTPException(status_code=404, detail=f"Exchange '{exchange_name}' not configured")
    
    success = exchange.cancel_order(order_id, symbol)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to cancel order")
    return {"success": True, "order_id": order_id}


@router.post("/positions/close", summary="Close a position")
async def close_position(
    symbol: str,
    quantity: Optional[float] = None,
    exchange_name: str = "default",
):
    result = trading_service.close_position(symbol, quantity, exchange_name)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error_message)
    return result


@router.get("/positions", summary="Get open positions")
async def get_positions():
    positions = trading_service.get_open_positions()
    return {
        "positions": positions,
        "count": len(positions),
    }


@router.get("/orders/open", summary="Get open orders")
async def get_open_orders(
    symbol: Optional[str] = None,
    exchange_name: str = "default",
):
    exchange = exchange_manager.get_exchange(exchange_name)
    if not exchange:
        raise HTTPException(status_code=404, detail=f"Exchange '{exchange_name}' not configured")
    
    orders = exchange.fetch_open_orders(symbol)
    return {
        "orders": [o.model_dump() for o in orders],
        "count": len(orders),
    }


@router.get("/ticker/{symbol}", summary="Get ticker information")
async def get_ticker(symbol: str, exchange_name: str = "default"):
    exchange = exchange_manager.get_exchange(exchange_name)
    if not exchange:
        raise HTTPException(status_code=404, detail=f"Exchange '{exchange_name}' not configured")
    
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/trades/history", summary="Get trade history")
async def get_trades(
    symbol: Optional[str] = None,
    limit: int = 50,
    exchange_name: str = "default",
):
    exchange = exchange_manager.get_exchange(exchange_name)
    if not exchange:
        raise HTTPException(status_code=404, detail=f"Exchange '{exchange_name}' not configured")
    
    try:
        trades = exchange.fetch_trades(symbol or "BTC/USDT", limit)
        return {
            "trades": trades,
            "count": len(trades),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/markets/pairs", summary="Get available trading pairs")
async def get_trading_pairs(exchange_name: str = "default"):
    exchange = exchange_manager.get_exchange(exchange_name)
    if not exchange:
        raise HTTPException(status_code=404, detail=f"Exchange '{exchange_name}' not configured")
    
    try:
        pairs = exchange.get_trading_pairs()
        return {
            "pairs": [p.model_dump() for p in pairs[:50]],
            "total": len(pairs),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/execute/from-decision", summary="Execute trade from agent decision")
async def execute_from_decision(
    symbol: str,
    action: str,
    quantity: float,
    price: Optional[float] = None,
    stop_loss_pct: Optional[float] = 0.02,
    take_profit_pct: Optional[float] = 0.05,
    exchange_name: str = "default",
):
    side = OrderSide.BUY if action.lower() in ["buy", "long", "overweight"] else OrderSide.SELL
    
    result = trading_service.place_order_with_protection(
        symbol=symbol,
        side=side,
        quantity=quantity,
        entry_price=price,
        stop_loss_pct=stop_loss_pct,
        take_profit_pct=take_profit_pct,
        exchange_name=exchange_name,
    )
    
    return {
        "success": result["all_success"],
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "details": result,
    }


@router.post("/cancel-all", summary="Cancel all open orders")
async def cancel_all_orders(
    symbol: Optional[str] = None,
    exchange_name: str = "default",
):
    trading_service.cancel_all_orders(symbol, exchange_name)
    return {
        "success": True,
        "message": "All open orders cancelled",
    }
