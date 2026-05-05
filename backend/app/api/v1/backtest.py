from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.strategy import BacktestTask, BacktestTaskCreate, BacktestResult
from app.services import BacktestService

router = APIRouter(prefix="/backtests", tags=["backtests"])

@router.get("/", response_model=List[BacktestTask])
async def get_backtests(db: AsyncSession = Depends(get_db)):
    """获取所有回测任务"""
    service = BacktestService(db)
    return await service.get_all_backtests()

@router.get("/{task_id}", response_model=BacktestTask)
async def get_backtest(task_id: int, db: AsyncSession = Depends(get_db)):
    """获取回测任务"""
    service = BacktestService(db)
    task = await service.get_backtest(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return task

@router.post("/", response_model=BacktestTask)
async def create_backtest(backtest_in: BacktestTaskCreate, db: AsyncSession = Depends(get_db)):
    """创建回测任务"""
    service = BacktestService(db)
    return await service.create_backtest(backtest_in)

@router.post("/{task_id}/run", response_model=BacktestResult)
async def run_backtest(task_id: int, db: AsyncSession = Depends(get_db)):
    """运行回测"""
    service = BacktestService(db)
    try:
        return await service.run_backtest(task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}")
async def cancel_backtest(task_id: int, db: AsyncSession = Depends(get_db)):
    """取消回测"""
    service = BacktestService(db)
    success = await service.cancel_backtest(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel backtest")
    return {"message": "Backtest cancelled"}
