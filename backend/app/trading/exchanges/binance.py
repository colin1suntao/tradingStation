from typing import Optional
import ccxt

from app.trading.exchanges.base import BaseExchange


class BinanceExchange(BaseExchange):
    def _initialize_client(self):
        config = {
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'sandbox': self.testnet,
            'options': {
                'defaultType': 'spot',
            },
        }
        if self.passphrase:
            config['password'] = self.passphrase
        
        self._client = ccxt.binance(config)

    def get_exchange_name(self) -> str:
        return 'binance'

    def set_leverage(self, symbol: str, leverage: int):
        self._client.set_leverage(leverage, symbol)

    def set_position_mode(self, hedge_mode: bool = False):
        self._client.options['defaultType'] = 'swap' if hedge_mode else 'spot'


class BinanceFuturesExchange(BaseExchange):
    def _initialize_client(self):
        config = {
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'sandbox': self.testnet,
            'options': {
                'defaultType': 'future',
            },
        }
        if self.passphrase:
            config['password'] = self.passphrase
        
        self._client = ccxt.binance(config)

    def get_exchange_name(self) -> str:
        return 'binance_futures'

    def set_leverage(self, symbol: str, leverage: int):
        self._client.set_leverage(leverage, symbol)

    def set_hedge_mode(self, symbol: Optional[str] = None, enabled: bool = True):
        if symbol:
            self._client.set_position_mode(hedge_mode=enabled, symbol=symbol)

    def fetch_funding_rate(self, symbol: str):
        funding = self._client.fetch_funding_rate(symbol)
        return {
            'symbol': symbol,
            'funding_rate': funding.get('fundingRate'),
            'next_funding_time': funding.get('nextFundingTime'),
        }
