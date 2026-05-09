from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.schemas.backtest import (
    BacktestConfig,
    BacktestMode,
    AllocationMethod,
)
from app.backtest.backtest_service import backtest_service

router = APIRouter(prefix="/backtest", tags=["Multi-Strategy Backtesting"])


class RunBacktestRequest(BaseModel):
    symbols: List[str] = ["BTC/USDT"]
    start_date: str = "2023-01-01"
    end_date: str = "2023-12-31"
    initial_capital: float = 100000.0
    commission: float = 0.001
    slippage: float = 0.0005
    allocation_method: str = "equal_weight"
    max_positions: int = 5
    strategy_ids: Optional[List[str]] = None
    tool_ids: Optional[List[str]] = None
    strategy_weights: Optional[Dict[str, float]] = None


class CompareStrategiesRequest(BaseModel):
    symbols: List[str] = ["BTC/USDT"]
    start_date: str = "2023-01-01"
    end_date: str = "2023-12-31"
    strategy_ids: List[str] = ["breakout", "mean_reversion", "trend_following", "rsi"]
    initial_capital: float = 100000.0


@router.get("/strategies", summary="List available strategies")
async def list_strategies():
    strategies = backtest_service.get_available_strategies()
    return {
        "strategies": strategies,
        "count": len(strategies),
    }


@router.get("/tools", summary="List available tools")
async def list_tools():
    tools = backtest_service.get_available_tools()
    return {
        "tools": tools,
        "count": len(tools),
    }


@router.post("/run", summary="Run multi-strategy backtest")
async def run_backtest(request: RunBacktestRequest):
    try:
        allocation = AllocationMethod.EQUAL_WEIGHT
        if request.allocation_method == "risk_parity":
            allocation = AllocationMethod.RISK_PARITY
        elif request.allocation_method == "mean_variance":
            allocation = AllocationMethod.MEAN_VARIANCE

        config = BacktestConfig(
            mode=BacktestMode.MULTI_STRATEGY,
            symbols=request.symbols,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            commission=request.commission,
            slippage=request.slippage,
            allocation_method=allocation,
            max_positions=request.max_positions,
        )

        result = backtest_service.run_backtest(
            config=config,
            market_data={},
            strategy_ids=request.strategy_ids,
            tool_ids=request.tool_ids,
            strategy_weights=request.strategy_weights,
        )

        return {
            "backtest_id": id(result),
            "config": result.config,
            "initial_capital": result.initial_capital,
            "final_capital": result.final_capital,
            "total_return": result.total_return,
            "total_return_pct": result.total_return_pct,
            "portfolio_performance": result.portfolio_performance.model_dump(),
            "trades_count": len(result.trades),
            "execution_time_ms": result.execution_time_ms,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compare", summary="Compare multiple strategies")
async def compare_strategies(request: CompareStrategiesRequest):
    try:
        results = backtest_service.compare_strategies(
            symbols=request.symbols,
            start_date=request.start_date,
            end_date=request.end_date,
            strategy_ids=request.strategy_ids,
            initial_capital=request.initial_capital,
        )

        comparison = {}
        for sid, result in results.items():
            comparison[sid] = {
                "strategy_id": sid,
                "initial_capital": result.initial_capital,
                "final_capital": result.final_capital,
                "total_return_pct": result.total_return_pct,
                "sharpe_ratio": result.portfolio_performance.sharpe_ratio,
                "max_drawdown_pct": result.portfolio_performance.max_drawdown_pct,
                "win_rate": result.portfolio_performance.win_rate,
                "total_trades": result.portfolio_performance.total_trades,
            }

        sorted_comparison = sorted(
            comparison.items(),
            key=lambda x: x[1]["sharpe_ratio"],
            reverse=True
        )

        return {
            "comparison": dict(sorted_comparison),
            "best_strategy": sorted_comparison[0][0] if sorted_comparison else None,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", summary="Get backtest history")
async def get_history():
    history = backtest_service.get_backtest_history()
    return {
        "history": history,
        "count": len(history),
    }


@router.get("/{backtest_id}", summary="Get backtest result")
async def get_backtest(backtest_id: str):
    result = backtest_service.get_backtest_result(backtest_id)
    if not result:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return result


@router.get("/{backtest_id}/equity-curve", summary="Get equity curve data")
async def get_equity_curve(backtest_id: str):
    result = backtest_service.get_backtest_result(backtest_id)
    if not result:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return {
        "equity_curve": result.portfolio_performance.equity_curve,
        "daily_returns": result.portfolio_performance.daily_returns,
        "monthly_returns": result.portfolio_performance.monthly_returns,
    }


@router.get("/{backtest_id}/trades", summary="Get trade history")
async def get_trades(backtest_id: str):
    result = backtest_service.get_backtest_result(backtest_id)
    if not result:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return {
        "trades": [t.model_dump() for t in result.trades],
        "count": len(result.trades),
    }


@router.get("/{backtest_id}/performance", summary="Get detailed performance metrics")
async def get_performance(backtest_id: str):
    result = backtest_service.get_backtest_result(backtest_id)
    if not result:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return {
        "portfolio_performance": result.portfolio_performance.model_dump(),
        "strategy_performances": {
            sid: sp.model_dump() for sid, sp in result.strategy_performances.items()
        },
    }


@router.get("/{backtest_id}/summary", summary="Get backtest summary")
async def get_summary(backtest_id: str):
    result = backtest_service.get_backtest_result(backtest_id)
    if not result:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return {
        "backtest_id": backtest_id,
        "start_date": result.start_date,
        "end_date": result.end_date,
        "initial_capital": result.initial_capital,
        "final_capital": result.final_capital,
        "total_return": result.total_return,
        "total_return_pct": result.total_return_pct,
        "sharpe_ratio": result.portfolio_performance.sharpe_ratio,
        "max_drawdown_pct": result.portfolio_performance.max_drawdown_pct,
        "win_rate": result.portfolio_performance.win_rate,
        "total_trades": result.portfolio_performance.total_trades,
        "execution_time_ms": result.execution_time_ms,
    }
