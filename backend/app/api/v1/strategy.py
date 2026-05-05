from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.strategy import Strategy, StrategyCreate, StrategyUpdate, ValidationResult
from app.services import StrategyService

router = APIRouter(prefix="/strategies", tags=["strategies"])

@router.get("/", response_model=List[Strategy])
async def get_strategies(db: AsyncSession = Depends(get_db)):
    """获取所有策略"""
    service = StrategyService(db)
    return await service.get_all_strategies()

@router.get("/{strategy_id}", response_model=Strategy)
async def get_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    """获取策略"""
    service = StrategyService(db)
    strategy = await service.get_strategy(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.post("/", response_model=Strategy)
async def create_strategy(strategy_in: StrategyCreate, db: AsyncSession = Depends(get_db)):
    """创建策略"""
    service = StrategyService(db)
    existing = await service.get_strategy_by_code(strategy_in.code)
    if existing:
        raise HTTPException(status_code=400, detail="Strategy code already exists")
    
    validation = service.validate_strategy(strategy_in.code_content)
    if not validation.valid:
        raise HTTPException(status_code=400, detail=validation.message)
    
    return await service.create_strategy(strategy_in)

@router.put("/{strategy_id}", response_model=Strategy)
async def update_strategy(strategy_id: int, strategy_in: StrategyUpdate, db: AsyncSession = Depends(get_db)):
    """更新策略"""
    service = StrategyService(db)
    
    if strategy_in.code_content:
        validation = service.validate_strategy(strategy_in.code_content)
        if not validation.valid:
            raise HTTPException(status_code=400, detail=validation.message)
    
    try:
        return await service.update_strategy(strategy_id, strategy_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Strategy not found")

@router.delete("/{strategy_id}")
async def delete_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    """删除策略"""
    service = StrategyService(db)
    success = await service.delete_strategy(strategy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return {"message": "Strategy deleted"}

@router.post("/validate", response_model=ValidationResult)
async def validate_strategy(code_content: str):
    """验证策略代码"""
    service = StrategyService(None)
    return service.validate_strategy(code_content)
