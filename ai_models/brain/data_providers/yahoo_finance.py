import yfinance as yf
from typing import Dict, List
import re

class YahooFinanceProvider:
    def __init__(self):
        pass
    
    def get_relevant_data(self, message: str) -> Dict:
        """Extract and return relevant financial data based on message"""
        # Extract stock symbols from message
        symbols = self._extract_symbols(message)
        
        if not symbols:
            return {}
        
        data = {}
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                data[symbol] = {
                    'info': stock.info,
                    'history': stock.history(period='1d').to_dict('records')[0],
                    'recommendations': stock.recommendations.to_dict('records')[-5:] if stock.recommendations is not None else None
                }
            except Exception as e:
                data[symbol] = {'error': str(e)}
        
        return data
    
    def _extract_symbols(self, message: str) -> List[str]:
        """Extract stock symbols from message"""
        # Look for common stock symbol patterns
        pattern = r'\$([A-Z]{1,5})\b|\b([A-Z]{1,5})(?=\s+stock)'
        matches = re.findall(pattern, message.upper())
        
        # Flatten and clean matches
        symbols = [match[0] or match[1] for match in matches]
        return list(set(symbols))  # Remove duplicates