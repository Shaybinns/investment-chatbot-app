import os
from typing import Dict, List
from datetime import datetime
import openai
from .memory_manager import MemoryManager
from .knowledge_base import KnowledgeBase
from .data_providers import YahooFinanceProvider, PerplexityProvider, PortfolioOptimizer

class Brain:
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.memory = MemoryManager()
        self.knowledge_base = KnowledgeBase()
        
        # Initialize data providers
        self.yahoo_finance = YahooFinanceProvider()
        self.perplexity = PerplexityProvider()
        self.portfolio_optimizer = PortfolioOptimizer()
        
        # Load initial financial knowledge
        self.load_base_knowledge()
    
    def load_base_knowledge(self):
        """Load initial financial knowledge into memory"""
        base_knowledge = self.knowledge_base.get_base_knowledge()
        self.memory.add_to_long_term_memory(base_knowledge)
    
    def process_message(self, user_message: str) -> str:
        # Get relevant context from memory
        context = self.memory.get_relevant_context(user_message)
        
        # Get real-time data if needed
        financial_data = self.get_relevant_financial_data(user_message)
        
        # Prepare messages for ChatGPT
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": user_message}
        ]
        
        if financial_data:
            messages.append({"role": "system", "content": f"Current financial data: {financial_data}"})
        
        # Get response from ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        
        # Store interaction in memory
        self.memory.store_interaction(user_message, response.choices[0].message['content'])
        
        return response.choices[0].message['content']
    
    def get_relevant_financial_data(self, message: str) -> Dict:
        """Get relevant financial data from various providers based on message content"""
        data = {}
        
        # Get stock data if needed
        if any(keyword in message.lower() for keyword in ['stock', 'price', 'market']):
            data['market_data'] = self.yahoo_finance.get_relevant_data(message)
        
        # Get research if needed
        if any(keyword in message.lower() for keyword in ['research', 'analysis', 'news']):
            data['research'] = self.perplexity.get_research(message)
        
        # Get portfolio optimization if needed
        if any(keyword in message.lower() for keyword in ['portfolio', 'optimize', 'allocation']):
            data['portfolio'] = self.portfolio_optimizer.get_optimization(message)
        
        return data
    
    def learn_from_feedback(self, message: str, feedback: str):
        """Update knowledge base based on user feedback"""
        self.memory.add_to_long_term_memory({
            'interaction': message,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        })
