from typing import Dict, Optional, Any

from app.trading.exchanges.base import BaseExchange
from app.trading.exchanges.binance import BinanceExchange, BinanceFuturesExchange
from app.schemas.trading import ExchangeType


class ExchangeFactory:
    _exchange_classes = {
        ExchangeType.BINANCE: BinanceExchange,
        'binance': BinanceExchange,
    }

    @classmethod
    def create_exchange(
        cls,
        exchange_type: ExchangeType,
        api_key: str,
        api_secret: str,
        passphrase: Optional[str] = None,
        testnet: bool = False,
    ) -> BaseExchange:
        if exchange_type == ExchangeType.BINANCE:
            return BinanceExchange(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet,
            )
        else:
            raise ValueError(f"Unsupported exchange type: {exchange_type}")

    @classmethod
    def create_futures_exchange(
        cls,
        exchange_type: ExchangeType,
        api_key: str,
        api_secret: str,
        testnet: bool = False,
    ) -> BaseExchange:
        if exchange_type == ExchangeType.BINANCE:
            return BinanceFuturesExchange(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet,
            )
        else:
            raise ValueError(f"Unsupported exchange type for futures: {exchange_type}")

    @classmethod
    def register_exchange(cls, name: str, exchange_class: type):
        cls._exchange_classes[name] = exchange_class


class ExchangeManager:
    _instances: Dict[str, BaseExchange] = {}
    _configs: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def add_exchange(
        cls,
        name: str,
        exchange_type: ExchangeType,
        api_key: str,
        api_secret: str,
        passphrase: Optional[str] = None,
        testnet: bool = False,
        is_futures: bool = False,
    ):
        if is_futures:
            exchange = ExchangeFactory.create_futures_exchange(
                exchange_type=exchange_type,
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet,
            )
        else:
            exchange = ExchangeFactory.create_exchange(
                exchange_type=exchange_type,
                api_key=api_key,
                api_secret=api_secret,
                passphrase=passphrase,
                testnet=testnet,
            )

        cls._instances[name] = exchange
        cls._configs[name] = {
            'exchange_type': exchange_type,
            'api_key': api_key,
            'testnet': testnet,
            'is_futures': is_futures,
        }

    @classmethod
    def get_exchange(cls, name: str = 'default') -> Optional[BaseExchange]:
        return cls._instances.get(name)

    @classmethod
    def remove_exchange(cls, name: str):
        if name in cls._instances:
            del cls._instances[name]
        if name in cls._configs:
            del cls._configs[name]

    @classmethod
    def list_exchanges(cls) -> Dict[str, Dict[str, Any]]:
        return cls._configs.copy()

    @classmethod
    def get_balance(cls, exchange_name: str = 'default') -> Dict[str, Any]:
        exchange = cls.get_exchange(exchange_name)
        if exchange:
            return exchange.fetch_balance().model_dump()
        return None

    @classmethod
    def clear_all(cls):
        cls._instances.clear()
        cls._configs.clear()


exchange_manager = ExchangeManager()
