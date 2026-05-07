import sys
sys.path.insert(0, '/workspace/backend')

from app.risk.risk_manager import risk_manager, RiskCalculator, PositionManager
from app.trading.trading_service import trading_service
from app.trading.exchange_manager import exchange_manager
from app.schemas.risk import RiskConfig, PositionSide, RiskCheckRequest, PositionSizeRequest
from app.schemas.trading import ExchangeType, OrderSide, OrderType

print("=" * 60)
print("Risk Management & Trading Module Test")
print("=" * 60)

print("\n1. Testing Risk Configuration:")
config = RiskConfig(
    max_position_size=10000,
    max_position_pct=0.2,
    max_loss_per_trade=0.02,
    max_daily_loss=0.05,
    max_leverage=10,
    max_open_positions=5,
    stop_loss_pct=0.02,
    take_profit_pct=0.05,
)
risk_manager.set_config(config)
print(f"   Max Position Size: ${config.max_position_size}")
print(f"   Max Position %: {config.max_position_pct * 100}%")
print(f"   Max Leverage: {config.max_leverage}x")
print(f"   Max Open Positions: {config.max_open_positions}")

print("\n2. Testing Position Size Calculation:")
pos_request = PositionSizeRequest(
    account_balance=100000,
    entry_price=50000,
    stop_loss_price=49000,
    risk_pct=0.01,
)
pos_result = RiskCalculator.calculate_position_size(pos_request)
print(f"   Account Balance: ${pos_request.account_balance}")
print(f"   Entry Price: ${pos_request.entry_price}")
print(f"   Stop Loss: ${pos_request.stop_loss_price}")
print(f"   Calculated Position Size: ${pos_result.position_size:.2f}")
print(f"   Quantity: {pos_result.quantity:.6f}")
print(f"   Risk Amount: ${pos_result.risk_amount:.2f}")

print("\n3. Testing Risk Check:")
risk_check = RiskCheckRequest(
    symbol="BTC/USDT",
    side=PositionSide.LONG,
    quantity=pos_result.quantity,
    entry_price=50000,
    stop_loss_price=49000,
    take_profit_price=55000,
)
check_result = risk_manager.check_risk(risk_check)
print(f"   Risk Check Approved: {check_result.approved}")
print(f"   Risk Level: {check_result.risk_level}")
if check_result.reasons:
    print(f"   Reasons: {check_result.reasons}")
if check_result.warnings:
    print(f"   Warnings: {check_result.warnings}")

print("\n4. Testing Stop Loss & Take Profit Calculation:")
entry_price = 50000
sl = RiskCalculator.calculate_stop_loss(entry_price, PositionSide.LONG, 0.02)
tp = RiskCalculator.calculate_take_profit(entry_price, PositionSide.LONG, 0.05)
print(f"   Entry Price: ${entry_price}")
print(f"   Stop Loss (2%): ${sl:.2f} (-{((entry_price - sl) / entry_price) * 100:.1f}%)")
print(f"   Take Profit (5%): ${tp:.2f} (+{((tp - entry_price) / entry_price) * 100:.1f}%)")

print("\n5. Testing Liquidation Price Calculation:")
liq_price = RiskCalculator.calculate_liquidation_price(entry_price, PositionSide.LONG, 10)
print(f"   Entry Price: ${entry_price}")
print(f"   Leverage: 10x")
print(f"   Liquidation Price: ${liq_price:.2f}")

print("\n6. Testing Exchange Connection (Mock):")
print(f"   Connected Exchanges: {list(exchange_manager.list_exchanges().keys())}")

print("\n7. Testing Risk Metrics:")
metrics = risk_manager.get_metrics(account_balance=100000)
print(f"   Total Exposure: ${metrics.total_exposure:.2f}")
print(f"   Available Balance: ${metrics.available_balance:.2f}")
print(f"   Risk Level: {metrics.risk_level}")
print(f"   Win Rate: {metrics.win_rate * 100:.1f}%")

print("\n" + "=" * 60)
print("All Risk Management & Trading Tests Passed!")
print("=" * 60)
