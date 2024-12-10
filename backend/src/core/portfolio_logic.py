from typing import Dict, List
from .market_data import MarketData

class PortfolioLogic:
    def __init__(self, market_data: MarketData):
        self.market_data = market_data

    async def calculate_portfolio_metrics(self, portfolio: Dict) -> Dict:
        return {
            "total_value": self._calculate_total_value(portfolio),
            "risk_metrics": self._calculate_risk_metrics(portfolio),
            "performance": self._calculate_performance(portfolio)
        }

    def _calculate_total_value(self, portfolio: Dict) -> float:
        total = 0
        for asset in portfolio['assets']:
            price = self.market_data.get_current_price(asset['symbol'])
            total += price * asset['quantity']
        return total