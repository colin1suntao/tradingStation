from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.schemas.risk import (
    RiskConfig,
    RiskCheckRequest,
    RiskCheckResponse,
    PositionSizeRequest,
    PositionSizeResponse,
    StopLossRequest,
    TakeProfitRequest,
    RiskMetrics,
    RiskLevel,
)
from app.risk.risk_manager import risk_manager, RiskCalculator

router = APIRouter(prefix="/risk", tags=["Risk Management"])


@router.get("/config", summary="Get current risk configuration")
async def get_risk_config():
    return risk_manager.config.model_dump()


@router.post("/config", summary="Update risk configuration")
async def update_risk_config(config: RiskConfig):
    risk_manager.set_config(config)
    return {
        "success": True,
        "message": "Risk configuration updated",
        "config": config.model_dump(),
    }


@router.post("/check", response_model=RiskCheckResponse, summary="Check if trade passes risk rules")
async def check_risk(request: RiskCheckRequest):
    result = risk_manager.check_risk(request)
    return result


@router.post("/position/size", response_model=PositionSizeResponse, summary="Calculate optimal position size")
async def calculate_position_size(request: PositionSizeRequest):
    result = RiskCalculator.calculate_position_size(request)
    return result


@router.post("/stop-loss/calculate", summary="Calculate stop loss price")
async def calculate_stop_loss(
    entry_price: float,
    side: str,
    stop_loss_pct: float
):
    position_side = PositionSide.LONG if side.lower() == "long" else PositionSide.SHORT
    stop_loss_price = RiskCalculator.calculate_stop_loss(entry_price, position_side, stop_loss_pct)
    return {
        "entry_price": entry_price,
        "side": side,
        "stop_loss_pct": stop_loss_pct,
        "stop_loss_price": stop_loss_price,
    }


@router.post("/take-profit/calculate", summary="Calculate take profit price")
async def calculate_take_profit(
    entry_price: float,
    side: str,
    take_profit_pct: float
):
    position_side = PositionSide.LONG if side.lower() == "long" else PositionSide.SHORT
    take_profit_price = RiskCalculator.calculate_take_profit(entry_price, position_side, take_profit_pct)
    return {
        "entry_price": entry_price,
        "side": side,
        "take_profit_pct": take_profit_pct,
        "take_profit_price": take_profit_price,
    }


@router.post("/liquidation/calculate", summary="Calculate liquidation price")
async def calculate_liquidation_price(
    entry_price: float,
    side: str,
    leverage: float
):
    position_side = PositionSide.LONG if side.lower() == "long" else PositionSide.SHORT
    liquidation_price = RiskCalculator.calculate_liquidation_price(entry_price, position_side, leverage)
    return {
        "entry_price": entry_price,
        "side": side,
        "leverage": leverage,
        "liquidation_price": liquidation_price,
    }


@router.get("/metrics", summary="Get current risk metrics")
async def get_risk_metrics(account_balance: float = 100000.0):
    metrics = risk_manager.get_metrics(account_balance)
    return metrics


@router.get("/positions", summary="Get all open positions")
async def get_positions():
    positions = risk_manager.position_manager.get_all_positions()
    return {
        "positions": [p.model_dump() for p in positions],
        "count": len(positions),
    }


@router.post("/positions/update-price", summary="Update position price and check stops")
async def update_position_price(symbol: str, current_price: float):
    try:
        risk_manager.update_position_price(symbol, current_price)
        return {
            "success": True,
            "symbol": symbol,
            "current_price": current_price,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/trades/history", summary="Get trade history")
async def get_trade_history(limit: int = 100):
    history = risk_manager.trade_history[-limit:]
    return {
        "trades": history,
        "count": len(history),
    }


@router.get("/daily-stats", summary="Get daily trading statistics")
async def get_daily_stats():
    return risk_manager.daily_stats


@router.post("/daily-stats/reset", summary="Reset daily statistics")
async def reset_daily_stats():
    risk_manager.reset_daily_stats()
    return {
        "success": True,
        "message": "Daily statistics reset",
    }
