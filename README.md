# TradingStation

面向个人量化团队的全球多资产、多 Agent 协作量化交易平台。

## 架构设计

- **后端**: Python 3.11+ / FastAPI / SQLAlchemy 2.0
- **数据库**: PostgreSQL + TimescaleDB (时序数据优化)
- **前端**: React + TypeScript (待开发)
- **部署**: Docker + Docker Compose

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 启动开发环境

```bash
# 克隆项目
git clone https://github.com/your-org/tradingstation.git
cd tradingstation

# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

### 访问服务

- API 文档: http://localhost:8000/docs
- API 健康检查: http://localhost:8000/health
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 初始化数据

```bash
# 进入 backend 容器
docker-compose exec backend bash

# 同步标的数据 (Binance)
curl -X POST "http://localhost:8000/api/v1/datasources/sync-instruments?datasource_code=binance"

# 同步标的数据 (Yahoo Finance)
curl -X POST "http://localhost:8000/api/v1/datasources/sync-instruments?datasource_code=yahoo"
```

## API 文档

### 主数据 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/master/exchanges` | GET | 获取交易所列表 |
| `/api/v1/master/exchanges/{code}` | GET | 获取指定交易所 |
| `/api/v1/master/instruments` | GET | 获取标的列表 |
| `/api/v1/master/instruments/{id}` | GET | 获取指定标的 |

### 数据查询 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/data/klines` | GET | 获取K线数据 |
| `/api/v1/data/quote` | GET | 获取实时行情 |

### 数据源管理 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/datasources` | GET | 列出可用数据源 |
| `/api/v1/datasources/sync-instruments` | POST | 同步标的数据 |
| `/api/v1/datasources/sync` | POST | 同步K线数据 |
| `/api/v1/datasources/sync-tasks` | GET | 查看同步任务 |

### 策略研究 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/strategies` | GET | 列出所有策略 |
| `/api/v1/strategies/{id}` | GET | 获取策略详情 |
| `/api/v1/strategies` | POST | 创建策略 |
| `/api/v1/strategies/{id}` | PUT | 更新策略 |
| `/api/v1/strategies/{id}` | DELETE | 删除策略 |
| `/api/v1/strategies/validate` | POST | 验证策略代码 |

### 回测 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/backtests` | GET | 列出所有回测任务 |
| `/api/v1/backtests/{id}` | GET | 获取回测任务详情 |
| `/api/v1/backtests` | POST | 创建回测任务 |
| `/api/v1/backtests/{id}/run` | POST | 运行回测 |
| `/api/v1/backtests/{id}` | DELETE | 取消回测 |

### 分析与可视化 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/analyze/{result_id}/metrics` | GET | 获取性能指标 |
| `/api/v1/analyze/{result_id}/charts` | GET | 获取图表数据 |
| `/api/v1/analyze/{result_id}/risk` | GET | 获取风险分析 |
| `/api/v1/analyze/{result_id}/summary` | GET | 获取摘要 |

## 项目结构

```
tradingstation/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic 模型
│   │   ├── services/    # 业务逻辑
│   │   └── datasources/ # 数据源插件
│   ├── alembic/         # 数据库迁移
│   └── main.py
├── frontend/            # 前端代码 (待开发)
├── docker/              # Docker 配置
├── docker-compose.yml
└── README.md
```

## 支持的数据源

- **Binance**: 加密货币现货、合约
- **Yahoo Finance**: 美股、ETF
- 更多数据源可以通过插件扩展

## 支持的资产类型

- ✅ 股票 / ETF
- ✅ 期货 / 期权
- ✅ 外汇 / 债券
- ✅ 加密货币

## 开发计划

- [x] 统一数据与主数据系统
- [x] 策略研究环境 (策略管理 + 回测引擎 + 分析可视化)
- [ ] 组合管理
- [ ] 风险管理
- [ ] 模拟交易
- [ ] 实盘交易对接
- [ ] 多 Agent 协作框架
- [ ] 监控与复盘
- [ ] 前端界面

## 策略使用示例

### 创建策略

```python
import requests
from datetime import datetime

# 策略代码
strategy_code = """
class Strategy:
    name = "Moving Average Crossover"
    params = {"short_window": 20, "long_window": 50}
    
    def __init__(self, params=None):
        self.params = params or self.params
    
    def initialize(self, context):
        self.context = context
    
    def on_bar(self, data):
        # 简单示例逻辑
        return {"signal": "hold"}
"""

# 创建策略
response = requests.post("http://localhost:8000/api/v1/strategies", json={
    "name": "MA Crossover",
    "code": "ma_crossover",
    "description": "双均线策略",
    "code_content": strategy_code,
    "parameters": {"short_window": 20, "long_window": 50},
    "asset_class": "crypto"
})

print(response.json())
```

### 创建回测

```python
# 创建回测任务
response = requests.post("http://localhost:8000/api/v1/backtests", json={
    "name": "测试回测",
    "strategy_id": 1,
    "instrument_ids": [1],
    "timeframe": "1d",
    "start_time": "2024-01-01T00:00:00",
    "end_time": "2024-12-31T23:59:59",
    "parameters": {"short_window": 20, "long_window": 50}
})

task_id = response.json()["id"]
print(f"回测任务创建: {task_id}")

# 运行回测
response = requests.post(f"http://localhost:8000/api/v1/backtests/{task_id}/run")
print("回测结果:", response.json())
```

### 查看分析结果

```python
# 获取性能指标
result_id = 1  # 从回测结果获取
response = requests.get(f"http://localhost:8000/api/v1/analyze/{result_id}/metrics")
metrics = response.json()

print(f"总收益率: {metrics['total_return']:.2%}")
print(f"夏普比率: {metrics['sharpe_ratio']:.2f}")
print(f"最大回撤: {metrics['max_drawdown']:.2%}")
print(f"胜率: {metrics['win_rate']:.2%}")
```

## 贡献指南

请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 许可证

MIT License
