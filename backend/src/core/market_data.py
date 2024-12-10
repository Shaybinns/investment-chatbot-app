import yfinance as yf
from typing import Dict, List

class MarketData:
    def __init__(self):
        pass

    def get_current_price(self, symbol: str) -> float:
        ticker = yf.Ticker(symbol)
        return ticker.info['regularMarketPrice']

    def get_historical_data(self, symbol: str, period: str = '1y') -> Dict:
        ticker = yf.Ticker(symbol)
        return ticker.history(period=period)

    def get_company_info(self, symbol: str) -> Dict:
        ticker = yf.Ticker(symbol)
        return ticker.info