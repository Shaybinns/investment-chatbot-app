from alpaca.trading.client import TradingClient
from typing import Dict

class AlpacaTrading:
    def __init__(self, api_key: str, api_secret: str):
        self.client = TradingClient(api_key, api_secret)

    async def place_order(self, symbol: str, qty: int, side: str, type: str = 'market') -> Dict:
        order = self.client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type
        )
        return order._raw