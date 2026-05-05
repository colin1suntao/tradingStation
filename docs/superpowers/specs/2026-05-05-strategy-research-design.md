# 策略研究环境设计文档

## 1. 概述

策略研究环境是 TradingStation 量化交易平台的核心模块之一，旨在为个人量化团队提供完整的策略开发、回测、分析工作流。本设计采用方案一：轻量级自研引擎 + VectorBT 集成。

## 2. 需求分析

根据用户需求，策略研究环境需要包含以下核心功能：
- ✅ 策略代码编辑器（支持 Python）
- ✅ 策略回测引擎
- ✅ 回测结果可视化（收益率曲线、回撤图、交易量图等）
- ✅ 策略参数优化功能
- ✅ 策略性能分析（胜率、盈亏比、夏普比率、最大回撤等）
- ✅ 策略版本管理
- ✅ 策略风险分析
- ✅ 订单类型支持（市价单、限价单、止损单等）
- ✅ 组合回测（多策略多资产）
- ✅ 策略存储：数据库 + Git 结合

## 3. 架构设计

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    API 层 (FastAPI)                            │
│  - /api/v1/strategies    # 策略管理                          │
│  - /api/v1/backtests     # 回测管理                          │
│  - /api/v1/analyze       # 分析与可视化                      │
└────────────────────┬───────────────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────────────┐
│                    业务逻辑层                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │StrategyService│  │BacktestService│  │AnalyzeService│        │
│  │ - 策略CRUD   │  │ - 回测执行   │  │ - 指标计算   │          │
│  │ - 版本管理   │  │ - 订单处理   │  │ - 可视化    │          │
│  │ - 代码存储   │  │ - 组合回测   │  │ - 风险分析   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└────────────────────┬───────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼─────────┐
│   回测引擎层     │    │   数据存储层     │
│  - VectorBT      │    │  - PostgreSQL   │
│  - 订单系统      │    │  - Git (代码)   │
│  - 组合管理      │    │  - Redis(缓存)  │
└──────────────────┘    └──────────────────┘
```

### 3.2 模块划分

| 模块 | 职责 | 状态 |
|------|------|------|
| `strategies` | 策略定义、版本管理、代码存储 | MVP |
| `backtests` | 回测任务管理、执行引擎 | MVP |
| `analyze` | 性能分析、可视化、风险评估 | MVP |
| `orders` | 订单类型、交易执行模拟 | MVP |
| `portfolio` | 组合管理、多策略配置 | MVP |

## 4. 数据模型设计

### 4.1 策略表 (`strategies`)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | Integer | PRIMARY KEY | 主键 |
| name | String(100) | NOT NULL | 策略名称 |
| code | String(50) | UNIQUE, NOT NULL | 策略唯一标识 |
| description | Text | NULLABLE | 策略描述 |
| code_content | Text | NOT NULL | 策略代码 |
| parameters | JSON | NOT NULL | 参数配置 |
| asset_class | Enum | NOT NULL | 适用资产类别 |
| status | Enum | DEFAULT 'draft' | 状态 |
| created_at | DateTime | DEFAULT now() | 创建时间 |
| updated_at | DateTime | NULLABLE | 更新时间 |
| version | Integer | DEFAULT 1 | 版本号 |

### 4.2 回测任务表 (`backtest_tasks`)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | Integer | PRIMARY KEY | 主键 |
| strategy_id | Integer | FOREIGN KEY | 关联策略 |
| name | String(100) | NOT NULL | 回测名称 |
| instrument_ids | JSON | NOT NULL | 标的列表 |
| timeframe | String(10) | NOT NULL | 时间周期 |
| start_time | DateTime | NOT NULL | 开始时间 |
| end_time | DateTime | NOT NULL | 结束时间 |
| parameters | JSON | NULLABLE | 参数覆盖 |
| status | Enum | DEFAULT 'pending' | 状态 |
| progress | Float | DEFAULT 0 | 进度(0-100) |
| created_at | DateTime | DEFAULT now() | 创建时间 |
| started_at | DateTime | NULLABLE | 开始执行时间 |
| completed_at | DateTime | NULLABLE | 完成时间 |

### 4.3 回测结果表 (`backtest_results`)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | Integer | PRIMARY KEY | 主键 |
| task_id | Integer | FOREIGN KEY | 关联任务 |
| strategy_id | Integer | FOREIGN KEY | 关联策略 |
| equity_curve | JSON | NOT NULL | 权益曲线 |
| stats | JSON | NOT NULL | 性能指标 |
| trades | JSON | NOT NULL | 交易记录 |
| drawdown | JSON | NOT NULL | 回撤数据 |
| summary | JSON | NOT NULL | 摘要信息 |
| created_at | DateTime | DEFAULT now() | 创建时间 |

### 4.4 枚举类型定义

```python
class StrategyStatus(str, Enum):
    DRAFT = "draft"
    TESTING = "testing"
    LIVE = "live"
    ARCHIVED = "archived"

class BacktestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AssetClass(str, Enum):
    EQUITY = "equity"
    FUTURE = "future"
    OPTION = "option"
    FX = "fx"
    BOND = "bond"
    CRYPTO = "crypto"
```

## 5. API 接口设计

### 5.1 策略管理 API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/strategies` | GET | 列出策略 |
| `/api/v1/strategies/{id}` | GET | 获取策略详情 |
| `/api/v1/strategies` | POST | 创建策略 |
| `/api/v1/strategies/{id}` | PUT | 更新策略 |
| `/api/v1/strategies/{id}` | DELETE | 删除策略 |
| `/api/v1/strategies/{id}/versions` | GET | 获取版本历史 |
| `/api/v1/strategies/{id}/validate` | POST | 验证策略代码 |

### 5.2 回测管理 API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/backtests` | POST | 创建回测任务 |
| `/api/v1/backtests` | GET | 列出回测任务 |
| `/api/v1/backtests/{id}` | GET | 获取回测详情 |
| `/api/v1/backtests/{id}` | DELETE | 取消回测 |
| `/api/v1/backtests/{id}/run` | POST | 执行回测 |

### 5.3 分析与可视化 API

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/analyze/{result_id}/metrics` | GET | 获取性能指标 |
| `/api/v1/analyze/{result_id}/charts` | GET | 获取图表数据 |
| `/api/v1/analyze/{result_id}/summary` | GET | 获取摘要 |
| `/api/v1/analyze/{result_id}/risk` | GET | 获取风险分析 |

## 6. 核心服务设计

### 6.1 StrategyService

```python
class StrategyService:
    def create_strategy(self, strategy_in: StrategyCreate) -> Strategy:
        """创建策略"""
    
    def update_strategy(self, strategy_id: int, strategy_in: StrategyUpdate) -> Strategy:
        """更新策略（自动版本递增）"""
    
    def get_strategy(self, strategy_id: int) -> Optional[Strategy]:
        """获取策略"""
    
    def get_strategy_versions(self, strategy_id: int) -> List[Strategy]:
        """获取版本历史"""
    
    def validate_strategy(self, code_content: str) -> ValidationResult:
        """验证策略代码"""
    
    def delete_strategy(self, strategy_id: int) -> bool:
        """删除策略"""
```

### 6.2 BacktestService

```python
class BacktestService:
    def create_backtest(self, backtest_in: BacktestCreate) -> BacktestTask:
        """创建回测任务"""
    
    def run_backtest(self, task_id: int) -> BacktestResult:
        """执行回测"""
    
    def run_portfolio_backtest(self, portfolio_in: PortfolioBacktest) -> BacktestResult:
        """组合回测（多策略多资产）"""
    
    def cancel_backtest(self, task_id: int) -> bool:
        """取消回测"""
    
    def get_backtest_status(self, task_id: int) -> BacktestTask:
        """获取回测状态"""
```

### 6.3 AnalyzeService

```python
class AnalyzeService:
    def calculate_metrics(self, result: BacktestResult) -> Dict[str, float]:
        """计算性能指标"""
    
    def generate_charts(self, result: BacktestResult) -> Dict[str, Any]:
        """生成图表数据"""
    
    def risk_analysis(self, result: BacktestResult) -> Dict[str, Any]:
        """风险分析"""
```

## 7. 策略代码规范

### 7.1 策略类模板

```python
from typing import Dict, Any

class Strategy:
    """策略基类"""
    
    name: str = "Strategy"
    description: str = ""
    params: Dict[str, Any] = {}
    
    def __init__(self, params: Dict[str, Any] = None):
        self.params = params or self.params
    
    def initialize(self, context: Any):
        """初始化方法"""
        pass
    
    def on_bar(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """每根K线触发"""
        return {}
    
    def on_order_fill(self, order: Dict[str, Any]):
        """订单成交回调"""
        pass
```

### 7.2 策略示例

```python
class MACrossStrategy(Strategy):
    name = "MA Cross Strategy"
    description = "Simple Moving Average Crossover"
    
    params = {
        "short_window": 20,
        "long_window": 50,
        "risk_per_trade": 0.01
    }
    
    def initialize(self, context):
        self.context = context
        self.short_ma = None
        self.long_ma = None
    
    def on_bar(self, data):
        close = data["close"]
        
        if len(close) >= self.params["long_window"]:
            self.short_ma = close[-self.params["short_window"]:].mean()
            self.long_ma = close[-self.params["long_window"]:].mean()
            
            if self.short_ma > self.long_ma:
                return {"signal": "buy"}
            elif self.short_ma < self.long_ma:
                return {"signal": "sell"}
        
        return {"signal": "hold"}
```

## 8. 性能指标列表

| 指标名称 | 计算公式 | 说明 |
|----------|----------|------|
| 总收益率 | (最终权益 - 初始权益) / 初始权益 | 策略期间总收益 |
| 年化收益率 | (1 + 总收益率) ^ (365 / 天数) - 1 | 年化收益 |
| 夏普比率 | 超额收益 / 收益标准差 | 风险调整收益 |
| 最大回撤 | max(1 - 权益 / 之前最高权益) | 最大亏损幅度 |
| 胜率 | 盈利交易数 / 总交易数 | 盈利交易占比 |
| 盈亏比 | 平均盈利 / 平均亏损 | 风险回报比 |
| 收益波动率 | 每日收益标准差 | 收益稳定性 |
| 最大连续亏损 | 连续亏损交易次数 | 策略韧性 |

## 9. 技术栈

| 分类 | 技术 | 版本 |
|------|------|------|
| 语言 | Python | 3.11+ |
| 框架 | FastAPI | 0.115+ |
| 回测引擎 | VectorBT | 0.25+ |
| 数据库 | PostgreSQL | 16+ |
| ORM | SQLAlchemy | 2.0+ |
| 缓存 | Redis | 7+ |
| 可视化 | Plotly | 5+ |
| 异步任务 | Celery | 5.4+ |

## 10. 安全性考虑

1. **代码执行安全**：策略代码使用沙箱环境执行，限制危险操作
2. **参数验证**：严格验证输入参数，防止注入攻击
3. **权限控制**：策略和回测结果需要权限管理
4. **日志审计**：记录所有策略执行和回测操作
5. **资源限制**：限制回测执行时间和内存使用

## 11. 扩展性设计

1. **策略模板库**：支持策略模板的共享和复用
2. **策略市场**：未来可扩展为策略交易市场
3. **多引擎支持**：预留其他回测引擎的接口
4. **分布式回测**：支持大规模并行回测
5. **实时回测**：支持实时数据流回测

---

**文档版本**: v1.0  
**创建日期**: 2026-05-05  
**作者**: TradingStation Team
