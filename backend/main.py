from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1 import data, master, datasource

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(data.router, prefix="/api/v1/data", tags=["data"])
app.include_router(master.router, prefix="/api/v1/master", tags=["master"])
app.include_router(datasource.router, prefix="/api/v1/datasources", tags=["datasources"])

@app.get("/")
async def root():
    return {"message": "TradingStation API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
