from typing import Dict, List

class KnowledgeBase:
    def __init__(self):
        self.investment_rules = self._load_investment_rules()
        self.market_knowledge = self._load_market_knowledge()

    def _load_investment_rules(self) -> Dict:
        return {
            "risk_levels": ["conservative", "moderate", "aggressive"],
            "asset_classes": ["stocks", "bonds", "commodities", "crypto"],
            "investment_principles": ["diversification", "risk_management", "long_term_focus"]
        }

    def _load_market_knowledge(self) -> Dict:
        return {
            "market_indicators": ["PE_ratio", "market_cap", "dividend_yield"],
            "analysis_methods": ["technical", "fundamental", "quantitative"]
        }