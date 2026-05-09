from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1 import data, master, datasource, strategy, backtest, analyze, llm, multi_agent, risk, trading, execution, portfolio_backtest

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(data.router, prefix="/api/v1/data", tags=["data"])
app.include_router(master.router, prefix="/api/v1/master", tags=["master"])
app.include_router(datasource.router, prefix="/api/v1/datasources", tags=["datasources"])
app.include_router(strategy.router, prefix="/api/v1", tags=["strategies"])
app.include_router(backtest.router, prefix="/api/v1", tags=["backtests"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["LLM Configuration"])
app.include_router(multi_agent.router, prefix="/api/v1/multi-agent", tags=["Multi-Agent Trading"])
app.include_router(risk.router, prefix="/api/v1/risk", tags=["Risk Management"])
app.include_router(trading.router, prefix="/api/v1/trading", tags=["Trading"])
app.include_router(execution.router, prefix="/api/v1/execution", tags=["Agent Execution"])
app.include_router(portfolio_backtest.router, prefix="/api/v1/portfolio", tags=["Portfolio Backtest"])

@app.get("/")
async def root():
    return {"message": "TradingStation API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
