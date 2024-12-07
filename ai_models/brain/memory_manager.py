from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class MemoryManager:
    def __init__(self):
        # Initialize memory storage
        self.user_contexts: Dict[str, Dict] = {}  # Stores user-specific data
        self.conversation_history: Dict[str, List[Dict]] = {}  # Stores chat history
        self.portfolio_memory: Dict[str, Dict] = {}  # Stores portfolio insights
        self.retention_period = timedelta(days=30)  # How long to keep memory

    def store_user_context(self, user_id: str, context_data: Dict) -> None:
        """Store user-specific context like knowledge level, preferences"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {}
        
        self.user_contexts[user_id].update({
            **context_data,
            'last_updated': datetime.now().isoformat()
        })

    def get_user_context(self, user_id: str) -> Optional[Dict]:
        """Retrieve user context"""
        return self.user_contexts.get(user_id)

    def add_to_conversation(self, user_id: str, message: Dict) -> None:
        """Add new message to conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            **message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Trim history if too long (keep last 50 messages)
        if len(self.conversation_history[user_id]) > 50:
            self.conversation_history[user_id] = self.conversation_history[user_id][-50:]

    def get_recent_conversation(self, user_id: str, message_count: int = 5) -> List[Dict]:
        """Get recent conversation history"""
        history = self.conversation_history.get(user_id, [])
        return history[-message_count:]

    def store_portfolio_insight(self, user_id: str, portfolio_id: str, insight: Dict) -> None:
        """Store insights about user's portfolio"""
        if user_id not in self.portfolio_memory:
            self.portfolio_memory[user_id] = {}
        
        self.portfolio_memory[user_id][portfolio_id] = {
            **insight,
            'last_updated': datetime.now().isoformat()
        }

    def get_portfolio_insights(self, user_id: str, portfolio_id: str) -> Optional[Dict]:
        """Retrieve portfolio insights"""
        return self.portfolio_memory.get(user_id, {}).get(portfolio_id)

    def cleanup_old_data(self) -> None:
        """Remove old data beyond retention period"""
        current_time = datetime.now()
        
        # Clean up user contexts
        for user_id in list(self.user_contexts.keys()):
            last_updated = datetime.fromisoformat(self.user_contexts[user_id]['last_updated'])
            if current_time - last_updated > self.retention_period:
                del self.user_contexts[user_id]

        # Clean up conversation history
        for user_id in list(self.conversation_history.keys()):
            self.conversation_history[user_id] = [
                msg for msg in self.conversation_history[user_id]
                if current_time - datetime.fromisoformat(msg['timestamp']) <= self.retention_period
            ]

        # Clean up portfolio insights
        for user_id in list(self.portfolio_memory.keys()):
            for portfolio_id in list(self.portfolio_memory[user_id].keys()):
                last_updated = datetime.fromisoformat(
                    self.portfolio_memory[user_id][portfolio_id]['last_updated']
                )
                if current_time - last_updated > self.retention_period:
                    del self.portfolio_memory[user_id][portfolio_id]

    def export_user_data(self, user_id: str) -> Dict:
        """Export all user data (for GDPR compliance)"""
        return {
            'context': self.user_contexts.get(user_id, {}),
            'conversations': self.conversation_history.get(user_id, []),
            'portfolio_insights': self.portfolio_memory.get(user_id, {})
        }

    def delete_user_data(self, user_id: str) -> None:
        """Delete all user data (for GDPR compliance)"""
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        if user_id in self.portfolio_memory:
            del self.portfolio_memory[user_id]