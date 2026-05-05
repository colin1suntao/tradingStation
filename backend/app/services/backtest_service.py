from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.strategy import BacktestTask, BacktestResult, BacktestStatus
from app.schemas.strategy import BacktestTaskCreate, BacktestResultBase
from app.engine.backtest_engine import BacktestEngine
from app.services.data_service import DataService
import pandas as pd

class BacktestService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.engine = BacktestEngine()
    
    async def create_backtest(self, backtest_in: BacktestTaskCreate) -> BacktestTask:
        """创建回测任务"""
        task = BacktestTask(
            strategy_id=backtest_in.strategy_id,
            name=backtest_in.name,
            instrument_ids=backtest_in.instrument_ids,
            timeframe=backtest_in.timeframe,
            start_time=backtest_in.start_time,
            end_time=backtest_in.end_time,
            parameters=backtest_in.parameters,
            status=BacktestStatus.PENDING,
            progress=0
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def get_backtest(self, task_id: int) -> Optional[BacktestTask]:
        """获取回测任务"""
        result = await self.db.execute(select(BacktestTask).where(BacktestTask.id == task_id))
        return result.scalar_one_or_none()
    
    async def get_all_backtests(self) -> List[BacktestTask]:
        """获取所有回测任务"""
        result = await self.db.execute(select(BacktestTask))
        return list(result.scalars().all())
    
    async def run_backtest(self, task_id: int) -> BacktestResult:
        """运行回测"""
        task = await self.get_backtest(task_id)
        if not task:
            raise ValueError("Backtest task not found")
        
        task.status = BacktestStatus.RUNNING
        task.started_at = datetime.now()
        await self.db.commit()
        
        try:
            # 获取数据（模拟）
            strategy = await self.db.get(Strategy, task.strategy_id)
            if not strategy:
                raise ValueError("Strategy not found")
            
            # 生成模拟数据
            dates = pd.date_range(task.start_time, task.end_time, freq='D')
            data = pd.DataFrame({
                'open': pd.Series([100 + i * 0.1 for i in range(len(dates))], index=dates),
                'high': pd.Series([100 + i * 0.1 + 1 for i in range(len(dates))], index=dates),
                'low': pd.Series([100 + i * 0.1 - 1 for i in range(len(dates))], index=dates),
                'close': pd.Series([100 + i * 0.1 for i in range(len(dates))], index=dates),
                'volume': pd.Series([10000 for _ in range(len(dates))], index=dates)
            })
            
            params = task.parameters or {}
            result_data = self.engine.run_strategy(data, strategy.code_content, params)
            
            if not result_data.get('success'):
                raise ValueError(result_data.get('error', 'Backtest failed'))
            
            result = BacktestResult(
                task_id=task.id,
                strategy_id=strategy.id,
                equity_curve=result_data['equity_curve'],
                stats=result_data['stats'],
                trades=result_data['trades'],
                drawdown=result_data['drawdown'],
                summary=result_data['summary']
            )
            self.db.add(result)
            
            task.status = BacktestStatus.COMPLETED
            task.progress = 100
            task.completed_at = datetime.now()
            
            await self.db.commit()
            await self.db.refresh(result)
            return result
        
        except Exception as e:
            task.status = BacktestStatus.FAILED
            task.completed_at = datetime.now()
            await self.db.commit()
            raise
    
    async def cancel_backtest(self, task_id: int) -> bool:
        """取消回测"""
        task = await self.get_backtest(task_id)
        if not task:
            return False
        
        if task.status == BacktestStatus.PENDING:
            task.status = BacktestStatus.CANCELLED
            task.completed_at = datetime.now()
            await self.db.commit()
            return True
        
        return False

# 避免循环导入问题
from app.models.strategy import Strategy
