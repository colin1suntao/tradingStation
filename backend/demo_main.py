from fastapi import FastAPI
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# 创建简化版 FastAPI 应用
app = FastAPI(title="TradingStation Demo", version="0.1.0")

# 简单的数据模型
class TimeFrame(str):
    MIN_1 = "1m"
    MIN_5 = "5m"
    HOUR_1 = "1h"
    DAY_1 = "1d"

# 模拟数据
MOCK_EXCHANGES = [
    {"id": 1, "name": "Binance", "code": "binance", "country": "Global"},
    {"id": 2, "name": "NYSE", "code": "nyse", "country": "USA"},
    {"id": 3, "name": "NASDAQ", "code": "nasdaq", "country": "USA"}
]

MOCK_INSTRUMENTS = [
    {"id": 1, "symbol": "BTC/USDT", "name": "Bitcoin", "exchange_id": 1, "asset_class": "crypto", "instrument_type": "spot"},
    {"id": 2, "symbol": "ETH/USDT", "name": "Ethereum", "exchange_id": 1, "asset_class": "crypto", "instrument_type": "spot"},
    {"id": 3, "symbol": "AAPL", "name": "Apple", "exchange_id": 3, "asset_class": "equity", "instrument_type": "spot"},
    {"id": 4, "symbol": "MSFT", "name": "Microsoft", "exchange_id": 3, "asset_class": "equity", "instrument_type": "spot"}
]

MOCK_DATASOURCES = [
    {"id": 1, "name": "Binance", "code": "binance", "type": "crypto"},
    {"id": 2, "name": "Yahoo Finance", "code": "yahoo", "type": "equity"}
]

# 简单的 API 端点
@app.get("/")
async def root():
    return {
        "message": "Welcome to TradingStation Demo!",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/v1/master/exchanges", response_model=List[Dict[str, Any]])
async def list_exchanges():
    return MOCK_EXCHANGES

@app.get("/api/v1/master/instruments", response_model=List[Dict[str, Any]])
async def list_instruments(
    exchange_id: int = None,
    asset_class: str = None
):
    result = MOCK_INSTRUMENTS
    if exchange_id:
        result = [i for i in result if i["exchange_id"] == exchange_id]
    if asset_class:
        result = [i for i in result if i["asset_class"] == asset_class]
    return result

@app.get("/api/v1/datasources")
async def list_datasources():
    return MOCK_DATASOURCES

@app.get("/api/v1/datasources/sync-instruments")
async def sync_instruments(datasource_code: str):
    return {"message": f"Simulated sync for {datasource_code}", "status": "success"}

@app.post("/api/v1/datasources/sync")
async def sync_data(datasource_code: str, instrument_id: int = None, timeframe: str = "1d"):
    return {
        "task_id": 1,
        "status": "pending",
        "message": f"Simulated sync task created for {datasource_code}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
