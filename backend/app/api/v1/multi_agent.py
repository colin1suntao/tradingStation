from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.services.trading_agents_service import TradingAgentsGraph

router = APIRouter(prefix="/multi-agent", tags=["Multi-Agent Trading"])


class MultiAgentAnalysisRequest(BaseModel):
    ticker: str
    trade_date: str
    llm_provider: str = "openai"
    deep_think_model: str = "gpt-4o"
    quick_think_model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    max_debate_rounds: int = 1
    max_risk_discuss_rounds: int = 1
    selected_analysts: List[str] = ["market", "news", "fundamentals"]
    debug: bool = False


class MultiAgentAnalysisResponse(BaseModel):
    success: bool
    ticker: str
    trade_date: str
    final_decision: str
    market_report: Optional[str] = None
    news_report: Optional[str] = None
    fundamentals_report: Optional[str] = None
    sentiment_report: Optional[str] = None
    investment_plan: Optional[str] = None
    trader_plan: Optional[str] = None
    bull_history: Optional[str] = None
    bear_history: Optional[str] = None
    risk_debate_history: Optional[str] = None
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None


@router.post("/analyze", response_model=MultiAgentAnalysisResponse)
async def analyze_stock(request: MultiAgentAnalysisRequest):
    try:
        start_time = datetime.now()
        
        config = {
            "max_debate_rounds": request.max_debate_rounds,
            "max_risk_discuss_rounds": request.max_risk_discuss_rounds,
        }
        
        ta = TradingAgentsGraph(
            selected_analysts=request.selected_analysts,
            debug=request.debug,
            config=config,
            llm_provider=request.llm_provider,
            deep_think_model=request.deep_think_model,
            quick_think_model=request.quick_think_model,
            api_key=request.api_key,
        )
        
        final_state, decision = ta.propagate(request.ticker, request.trade_date)
        
        end_time = datetime.now()
        execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return MultiAgentAnalysisResponse(
            success=True,
            ticker=request.ticker,
            trade_date=request.trade_date,
            final_decision=decision,
            market_report=final_state.get("market_report", ""),
            news_report=final_state.get("news_report", ""),
            fundamentals_report=final_state.get("fundamentals_report", ""),
            sentiment_report=final_state.get("sentiment_report", ""),
            investment_plan=final_state.get("investment_plan", ""),
            trader_plan=final_state.get("trader_investment_plan", ""),
            bull_history=final_state.get("investment_debate_state", {}).get("bull_history", ""),
            bear_history=final_state.get("investment_debate_state", {}).get("bear_history", ""),
            risk_debate_history=final_state.get("risk_debate_state", {}).get("history", ""),
            execution_time_ms=round(execution_time_ms, 2),
        )
    except Exception as e:
        return MultiAgentAnalysisResponse(
            success=False,
            ticker=request.ticker,
            trade_date=request.trade_date,
            final_decision="",
            error=str(e)
        )


@router.post("/analyze/quick")
async def quick_analyze(
    ticker: str,
    trade_date: str,
    llm_provider: str = "openai",
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None
):
    try:
        ta = TradingAgentsGraph(
            selected_analysts=["market"],
            llm_provider=llm_provider,
            deep_think_model=model,
            quick_think_model=model,
            api_key=api_key,
            config={"max_debate_rounds": 1, "max_risk_discuss_rounds": 1},
        )
        
        final_state, decision = ta.propagate(ticker, trade_date)
        
        return {
            "success": True,
            "ticker": ticker,
            "trade_date": trade_date,
            "decision": decision,
            "market_report": final_state.get("market_report", ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysts")
async def list_analysts():
    return {
        "analysts": [
            {
                "id": "market",
                "name": "Market Analyst",
                "description": "Analyzes technical indicators and price trends",
                "tools": ["get_stock_data", "get_indicators"]
            },
            {
                "id": "news",
                "name": "News Analyst",
                "description": "Monitors news and macroeconomic events",
                "tools": ["get_news", "get_global_news", "get_insider_transactions"]
            },
            {
                "id": "social",
                "name": "Social Media Analyst",
                "description": "Analyzes social media sentiment",
                "tools": ["get_news"]
            },
            {
                "id": "fundamentals",
                "name": "Fundamentals Analyst",
                "description": "Evaluates company financial health",
                "tools": ["get_fundamentals", "get_balance_sheet", "get_cashflow", "get_income_statement"]
            }
        ]
    }