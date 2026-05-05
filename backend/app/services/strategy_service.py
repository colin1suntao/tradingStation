from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.strategy import Strategy, StrategyStatus
from app.schemas.strategy import StrategyCreate, StrategyUpdate, ValidationResult
import ast

class StrategyService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_strategy(self, strategy_in: StrategyCreate) -> Strategy:
        """创建策略"""
        strategy = Strategy(
            name=strategy_in.name,
            code=strategy_in.code,
            description=strategy_in.description,
            code_content=strategy_in.code_content,
            parameters=strategy_in.parameters,
            asset_class=strategy_in.asset_class,
            status=StrategyStatus.DRAFT,
            version=1
        )
        self.db.add(strategy)
        await self.db.commit()
        await self.db.refresh(strategy)
        return strategy
    
    async def get_strategy(self, strategy_id: int) -> Optional[Strategy]:
        """获取策略"""
        result = await self.db.execute(select(Strategy).where(Strategy.id == strategy_id))
        return result.scalar_one_or_none()
    
    async def get_strategy_by_code(self, code: str) -> Optional[Strategy]:
        """通过 code 获取策略"""
        result = await self.db.execute(select(Strategy).where(Strategy.code == code))
        return result.scalar_one_or_none()
    
    async def get_all_strategies(self) -> List[Strategy]:
        """获取所有策略"""
        result = await self.db.execute(select(Strategy))
        return list(result.scalars().all())
    
    async def update_strategy(self, strategy_id: int, strategy_in: StrategyUpdate) -> Strategy:
        """更新策略"""
        strategy = await self.get_strategy(strategy_id)
        if not strategy:
            raise ValueError("Strategy not found")
        
        update_data = strategy_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(strategy, key, value)
        
        strategy.version += 1
        await self.db.commit()
        await self.db.refresh(strategy)
        return strategy
    
    async def delete_strategy(self, strategy_id: int) -> bool:
        """删除策略"""
        strategy = await self.get_strategy(strategy_id)
        if not strategy:
            return False
        
        await self.db.delete(strategy)
        await self.db.commit()
        return True
    
    def validate_strategy(self, code_content: str) -> ValidationResult:
        """验证策略代码"""
        errors = []
        try:
            ast.parse(code_content)
        except SyntaxError as e:
            errors.append(f"Syntax error: {e.msg}")
        
        if 'class Strategy' not in code_content:
            errors.append("Strategy class not found")
        
        if 'def on_bar' not in code_content:
            errors.append("on_bar method not found")
        
        return ValidationResult(
            valid=len(errors) == 0,
            message="Valid" if len(errors) == 0 else "Invalid",
            errors=errors
        )
