#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8001"

# 策略代码
strategy_code = """
class Strategy:
    name = "Simple Moving Average"
    params = {"ma_window": 20}
    
    def __init__(self, params=None):
        self.params = params or self.params
    
    def initialize(self, context):
        self.context = context
    
    def on_bar(self, data):
        close = data["close"]
        if close > 100:
            return {"signal": "buy"}
        elif close < 95:
            return {"signal": "sell"}
        return {"signal": "hold"}
"""

print("=== 测试策略验证 ===")
response = requests.post(f"{BASE_URL}/api/v1/strategies/validate", params={"code_content": strategy_code})
print("Status:", response.status_code)
print("Response:", response.text)

print("\n=== 创建策略 ===")
response = requests.post(f"{BASE_URL}/api/v1/strategies", json={
    "name": "MA Strategy",
    "code": "ma_strategy_test",
    "description": "Simple Moving Average Strategy",
    "code_content": strategy_code,
    "parameters": {"ma_window": 20},
    "asset_class": "crypto"
})
print("Status:", response.status_code)
if response.status_code == 200:
    strategy = response.json()
    strategy_id = strategy["id"]
    print("策略创建成功:", json.dumps(strategy, indent=2, ensure_ascii=False))
else:
    print("Error:", response.text)
    exit(1)

print("\n=== 获取所有策略 ===")
response = requests.get(f"{BASE_URL}/api/v1/strategies")
print("Status:", response.status_code)
print("策略列表:", json.dumps(response.json(), indent=2, ensure_ascii=False))

print("\n=== 创建回测任务 ===")
response = requests.post(f"{BASE_URL}/api/v1/backtests", json={
    "name": "Test Backtest",
    "strategy_id": strategy_id,
    "instrument_ids": [1],
    "timeframe": "1d",
    "start_time": "2024-01-01T00:00:00",
    "end_time": "2024-06-30T23:59:59",
    "parameters": {"ma_window": 20}
})
print("Status:", response.status_code)
if response.status_code == 200:
    backtest = response.json()
    backtest_id = backtest["id"]
    print("回测任务创建成功:", json.dumps(backtest, indent=2, ensure_ascii=False))
else:
    print("Error:", response.text)
    exit(1)

print("\n=== 运行回测 ===")
response = requests.post(f"{BASE_URL}/api/v1/backtests/{backtest_id}/run")
print("Status:", response.status_code)
if response.status_code == 200:
    result = response.json()
    result_id = result["id"]
    print("回测执行成功!")
    print("\n=== 回测摘要 ===")
    print(f"总收益率: {result['summary']['total_return_pct']:.2f}%")
    print(f"年化收益率: {result['summary']['cagr']:.2f}%")
    print(f"夏普比率: {result['summary']['sharpe_ratio']:.2f}")
    print(f"最大回撤: {result['summary']['max_drawdown_pct']:.2f}%")
    print(f"交易次数: {result['summary']['total_trades']}")
    print(f"胜率: {result['summary']['win_rate_pct']:.2f}%")
else:
    print("Error:", response.text)

print("\n=== 获取性能指标 ===")
response = requests.get(f"{BASE_URL}/api/v1/analyze/{result_id}/metrics")
print("Status:", response.status_code)
if response.status_code == 200:
    metrics = response.json()
    print(json.dumps(metrics, indent=2))

print("\n=== 获取风险分析 ===")
response = requests.get(f"{BASE_URL}/api/v1/analyze/{result_id}/risk")
print("Status:", response.status_code)
if response.status_code == 200:
    risk = response.json()
    print(json.dumps(risk, indent=2))

print("\n=== 获取图表数据 ===")
response = requests.get(f"{BASE_URL}/api/v1/analyze/{result_id}/charts")
print("Status:", response.status_code)
if response.status_code == 200:
    charts = response.json()
    print("Equity curve points:", len(charts['equity_curve']))
    print("Trades count:", len(charts['trades']))

print("\n✅ 所有测试完成!")
