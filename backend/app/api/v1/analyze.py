from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.strategy import BacktestResult
from app.schemas.strategy import MetricResult
from app.services import AnalyzeService

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.get("/{result_id}/metrics", response_model=MetricResult)
async def get_metrics(result_id: int, db: AsyncSession = Depends(get_db)):
    """获取性能指标"""
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.calculate_metrics(result)

@router.get("/{result_id}/charts")
async def get_charts(result_id: int, db: AsyncSession = Depends(get_db)):
    """获取图表数据"""
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.generate_charts(result)

@router.get("/{result_id}/risk")
async def get_risk_analysis(result_id: int, db: AsyncSession = Depends(get_db)):
    """获取风险分析"""
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.risk_analysis(result)

@router.get("/{result_id}/summary")
async def get_summary(result_id: int, db: AsyncSession = Depends(get_db)):
    """获取摘要"""
    result = await db.get(BacktestResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    service = AnalyzeService()
    return service.get_summary(result)
