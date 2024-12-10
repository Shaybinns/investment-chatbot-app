import numpy as np
from typing import Dict, List
from .market_data import MarketData

class PortfolioOptimizer:
    def __init__(self, market_data: MarketData):
        self.market_data = market_data

    def optimize_portfolio(self, portfolio: Dict, risk_tolerance: float) -> Dict:
        returns = self._calculate_expected_returns(portfolio)
        risks = self._calculate_risks(portfolio)
        weights = self._optimize_weights(returns, risks, risk_tolerance)
        
        return {
            "optimal_weights": weights,
            "expected_return": np.dot(returns, weights),
            "expected_risk": self._calculate_portfolio_risk(risks, weights)
        }