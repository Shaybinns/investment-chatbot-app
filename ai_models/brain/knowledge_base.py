class KnowledgeBase:
    def __init__(self):
        self.base_knowledge = self._load_base_knowledge()
    
    def _load_base_knowledge(self):
        """Load initial financial knowledge"""
        return {
            'investment_principles': [
                'Diversification is key to reducing risk',
                'Long-term investing typically outperforms short-term trading',
                'Risk and return are typically correlated',
                'Market timing is generally ineffective',
                'Regular rebalancing helps maintain desired risk levels'
            ],
            'risk_management': [
                'Never invest more than you can afford to lose',
                'Emergency funds should be kept liquid',
                'Investment horizon affects risk tolerance',
                'Diversification across asset classes reduces risk'
            ],
            'asset_classes': [
                'Stocks: Higher risk, potentially higher returns',
                'Bonds: Lower risk, typically lower returns',
                'Real Estate: Tangible assets, potential income generation',
                'Cash: Lowest risk, lowest potential returns'
            ],
            'market_basics': [
                'Market cycles are normal and expected',
                'Economic indicators affect market performance',
                'Company fundamentals drive long-term stock performance',
                'Global events can impact local markets'
            ]
        }
    
    def get_base_knowledge(self):
        return self.base_knowledge
