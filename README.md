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
- [ ] 策略研究环境 (JupyterLab 集成)
- [ ] 回测引擎
- [ ] 组合管理
- [ ] 风险管理
- [ ] 模拟交易
- [ ] 实盘交易对接
- [ ] 多 Agent 协作框架
- [ ] 监控与复盘
- [ ] 前端界面

## 贡献指南

请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 许可证

MIT License
