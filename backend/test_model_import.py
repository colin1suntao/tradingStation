#!/usr/bin/env python3
# 测试模型导入
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from app.models import Strategy, BacktestTask, BacktestResult
    from app.models import StrategyStatus, BacktestStatus
    
    print("✅ 模型导入成功！")
    print(f"StrategyStatus: {list(StrategyStatus)}")
    print(f"BacktestStatus: {list(BacktestStatus)}")
    print("Task 1 完成！")
    
except Exception as e:
    print(f"❌ 模型导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
