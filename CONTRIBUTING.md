# 贡献指南

欢迎贡献！请先阅读本文档。

## 开发环境设置

```bash
# 安装 Python 依赖
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 本地启动 (使用 Docker 数据库)
docker-compose up -d postgres redis
uvicorn main:app --reload
```

## 代码规范

- 使用 `black` 格式化 Python 代码
- 使用 `isort` 整理 import
- 使用 `mypy` 进行类型检查
- 遵循 FastAPI 最佳实践

## 提交规范

使用 conventional commits:

```
<type>(<scope>): <subject>

<type>: feat, fix, docs, style, refactor, test, chore
```

## 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "Add xxx table"

# 执行迁移
alembic upgrade head
```

## 测试

```bash
# 运行测试
pytest tests/
```
