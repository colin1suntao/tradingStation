from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.services.execution_service import agent_execution_service

router = APIRouter(prefix="/execution", tags=["Agent Execution"])


class AnalyzeAndExecuteRequest(BaseModel):
    ticker: str
    trade_date: str
    action: str
    llm_provider: str = "openai"
    deep_think_model: str = "gpt-4o"
    quick_think_model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    risk_check: bool = True
    auto_trade: bool = False
    exchange_name: str = "default"


@router.post("/analyze-and-execute", summary="Analyze and optionally execute trade")
async def analyze_and_execute(request: AnalyzeAndExecuteRequest):
    result = agent_execution_service.analyze_and_execute(
        ticker=request.ticker,
        trade_date=request.trade_date,
        action=request.action,
        llm_provider=request.llm_provider,
        deep_think_model=request.deep_think_model,
        quick_think_model=request.quick_think_model,
        api_key=request.api_key,
        risk_check=request.risk_check,
        auto_trade=request.auto_trade,
        exchange_name=request.exchange_name,
    )
    return result


@router.get("/history", summary="Get execution history")
async def get_history(limit: int = 100):
    history = agent_execution_service.get_execution_history(limit)
    return {
        "executions": history,
        "count": len(history),
    }


@router.get("/performance", summary="Get performance summary")
async def get_performance():
    summary = agent_execution_service.get_performance_summary()
    return summary


@router.get("/{execution_id}", summary="Get specific execution details")
async def get_execution(execution_id: str):
    history = agent_execution_service.get_execution_history(limit=1000)
    for exec in history:
        if exec.get("execution_id") == execution_id:
            return exec
    raise HTTPException(status_code=404, detail="Execution not found")