from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
import ccxt

from app.schemas.trading import (
    OrderRequest,
    OrderResponse,
    AccountBalance,
    TradingPair,
    ExchangeType,
)


class BaseExchange(ABC):
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        passphrase: Optional[str] = None,
        testnet: bool = False,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.testnet = testnet
        self._client: Optional[ccxt.Exchange] = None
        self._initialize_client()

    @abstractmethod
    def _initialize_client(self):
        pass

    @abstractmethod
    def get_exchange_name(self) -> str:
        pass

    def fetch_balance(self) -> AccountBalance:
        balance = self._client.fetch_balance()
        total = sum(balance.get('total', {}).values())
        free = sum(balance.get('free', {}).values())
        locked = sum(balance.get('used', {}).values())

        positions = []
        if 'positions' in balance:
            for pos in balance['positions']:
                if pos.get('total', 0) != 0:
                    positions.append({
                        'symbol': pos.get('symbol'),
                        'quantity': pos.get('total'),
                        'entry_price': pos.get('entryPrice'),
                        'unrealized_pnl': pos.get('unrealizedPnl'),
                    })

        return AccountBalance(
            exchange=self.get_exchange_name(),
            total_balance=total,
            available_balance=free,
            locked_balance=locked,
            positions=positions,
        )

    def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        ticker = self._client.fetch_ticker(symbol)
        return {
            'symbol': symbol,
            'last': ticker['last'],
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'volume': ticker['volume'],
            'timestamp': datetime.fromtimestamp(ticker['timestamp'] / 1000),
        }

    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List:
        ohlcv = self._client.fetch_ohlcv(symbol, timeframe, limit=limit)
        return [
            {
                'timestamp': datetime.fromtimestamp(k[0] / 1000),
                'open': k[1],
                'high': k[2],
                'low': k[3],
                'close': k[4],
                'volume': k[5],
            }
            for k in ohlcv
        ]

    def create_order(self, request: OrderRequest) -> OrderResponse:
        params = {}
        if request.reduce_only:
            params['reduceOnly'] = True
        if request.position_side:
            params['positionSide'] = request.position_side

        order = self._client.create_order(
            symbol=request.symbol,
            type=request.order_type.value,
            side=request.side.value,
            amount=request.quantity,
            price=request.price,
            params=params,
        )

        return OrderResponse(
            order_id=str(order['id']),
            exchange=self.get_exchange_name(),
            symbol=order['symbol'],
            side=order['side'],
            order_type=order['type'],
            quantity=order['amount'],
            price=order.get('price'),
            status=order['status'],
            filled_quantity=order.get('filled', 0),
            average_price=order.get('average'),
            created_at=datetime.fromtimestamp(order['timestamp'] / 1000),
            updated_at=datetime.now(),
        )

    def cancel_order(self, order_id: str, symbol: str) -> bool:
        try:
            self._client.cancel_order(order_id, symbol)
            return True
        except Exception:
            return False

    def fetch_order(self, order_id: str, symbol: str) -> OrderResponse:
        order = self._client.fetch_order(order_id, symbol)
        return OrderResponse(
            order_id=str(order['id']),
            exchange=self.get_exchange_name(),
            symbol=order['symbol'],
            side=order['side'],
            order_type=order['type'],
            quantity=order['amount'],
            price=order.get('price'),
            status=order['status'],
            filled_quantity=order.get('filled', 0),
            average_price=order.get('average'),
            created_at=datetime.fromtimestamp(order['timestamp'] / 1000),
            updated_at=datetime.now(),
        )

    def fetch_open_orders(self, symbol: Optional[str] = None) -> List[OrderResponse]:
        orders = self._client.fetch_open_orders(symbol)
        return [
            OrderResponse(
                order_id=str(o['id']),
                exchange=self.get_exchange_name(),
                symbol=o['symbol'],
                side=o['side'],
                order_type=o['type'],
                quantity=o['amount'],
                price=o.get('price'),
                status=o['status'],
                filled_quantity=o.get('filled', 0),
                average_price=o.get('average'),
                created_at=datetime.fromtimestamp(o['timestamp'] / 1000),
                updated_at=datetime.now(),
            )
            for o in orders
        ]

    def fetch_trades(self, symbol: str, limit: int = 50) -> List[Dict]:
        trades = self._client.fetch_my_trades(symbol, limit=limit)
        return [
            {
                'id': t['id'],
                'symbol': t['symbol'],
                'side': t['side'],
                'price': t['price'],
                'quantity': t['amount'],
                'cost': t['cost'],
                'fee': t.get('fee'),
                'timestamp': datetime.fromtimestamp(t['timestamp'] / 1000),
            }
            for t in trades
        ]

    def get_trading_pairs(self) -> List[TradingPair]:
        markets = self._client.load_markets()
        pairs = []
        for symbol, market in markets.items():
            if market.get('active', False):
                pairs.append(TradingPair(
                    symbol=symbol,
                    base_currency=market['base'],
                    quote_currency=market['quote'],
                    price_precision=market.get('precision', {}).get('price', 8),
                    quantity_precision=market.get('precision', {}).get('amount', 8),
                    min_quantity=market.get('limits', {}).get('amount', {}).get('min', 0),
                    max_quantity=market.get('limits', {}).get('amount', {}).get('max', float('inf')),
                    min_notional=market.get('limits', {}).get('cost', {}).get('min', 0),
                    is_trading=market.get('active', False),
                ))
        return pairs
