from typing import Dict, List
import json
from datetime import datetime
from pathlib import Path

class MemoryManager:
    def __init__(self):
        self.memory_file = Path('memory_store.json')
        self.short_term_memory = []
        self.load_memory()
    
    def load_memory(self):
        """Load memory from persistent storage"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                self.long_term_memory = json.load(f)
        else:
            self.long_term_memory = []
    
    def save_memory(self):
        """Save memory to persistent storage"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.long_term_memory, f)
    
    def add_to_long_term_memory(self, data: Dict):
        """Add information to long-term memory"""
        self.long_term_memory.append({
            **data,
            'timestamp': datetime.now().isoformat()
        })
        self.save_memory()
    
    def get_relevant_context(self, query: str) -> str:
        """Get relevant context from memory based on query"""
        # Simple relevance scoring based on keyword matching
        relevant_memories = []
        query_words = set(query.lower().split())
        
        for memory in self.long_term_memory:
            memory_words = set(str(memory).lower().split())
            relevance = len(query_words.intersection(memory_words))
            if relevance > 0:
                relevant_memories.append((relevance, memory))
        
        # Sort by relevance and format context
        relevant_memories.sort(reverse=True)
        context = [str(m[1]) for m in relevant_memories[:5]]
        
        return '\n'.join(context)
    
    def store_interaction(self, message: str, response: str):
        """Store interaction in short-term memory and potentially long-term"""
        interaction = {
            'message': message,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        
        self.short_term_memory.append(interaction)
        
        # Keep short-term memory limited
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)
        
        # Store important interactions in long-term memory
        if self._is_important_interaction(interaction):
            self.add_to_long_term_memory(interaction)
    
    def _is_important_interaction(self, interaction: Dict) -> bool:
        """Determine if interaction should be stored in long-term memory"""
        important_keywords = ['portfolio', 'strategy', 'goal', 'risk', 'investment']
        return any(keyword in str(interaction).lower() for keyword in important_keywords)
