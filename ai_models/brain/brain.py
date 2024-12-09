from typing import Dict, List, Optional
from datetime import datetime
import openai
from .memory_manager import MemoryManager
from .knowledge_base import KnowledgeBase
from .data_providers import YahooFinanceProvider, PerplexityProvider, PortfolioOptimizer
from .response_generator import ResponseGenerator

class Brain:
    """
    Core class that manages the AI chatbot's cognitive functions.
    Handles message processing, memory management, and data integration.
    """
    
    def __init__(self, openai_api_key: str):
        """Initialize the brain with necessary components and API keys."""
        # API Configuration
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        
        # Core Components
        self.memory = MemoryManager()
        self.knowledge_base = KnowledgeBase()
        self.response_generator = ResponseGenerator()
        
        # Data Providers
        self.data_providers = {
            'finance': YahooFinanceProvider(),
            'research': PerplexityProvider(),
            'portfolio': PortfolioOptimizer()
        }
        
        # Load initial knowledge
        self.load_base_knowledge()
        
        # Configuration
        self.config = {
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 1000
        }
    
    def load_base_knowledge(self) -> None:
        """Load initial financial knowledge and rules into memory."""
        try:
            base_knowledge = self.knowledge_base.get_base_knowledge()
            self.memory.add_to_long_term_memory(base_knowledge)
        except Exception as e:
            print(f"Error loading base knowledge: {str(e)}")
    
    def process_message(self, user_message: str, user_id: Optional[str] = None) -> str:
        """
        Process incoming user messages and generate appropriate responses.
        
        Args:
            user_message: The input message from the user
            user_id: Optional identifier for user-specific context
            
        Returns:
            str: Generated response for the user
        """
        try:
            # Get conversation context
            context = self.memory.get_relevant_context(user_message, user_id)
            
            # Get real-time financial data
            financial_data = self.get_relevant_financial_data(user_message)
            
            # Prepare conversation history
            messages = self._prepare_messages(context, user_message, financial_data)
            
            # Generate response
            response = self._generate_response(messages)
            
            # Store interaction
            self.memory.store_interaction(
                user_message, 
                response,
                user_id=user_id,
                metadata={'financial_data': financial_data}
            )
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            print(error_msg)
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    def _prepare_messages(self, context: str, user_message: str, financial_data: Dict) -> List[Dict]:
        """Prepare the message list for the OpenAI API call."""
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": user_message}
        ]
        
        if financial_data:
            data_context = self._format_financial_data(financial_data)
            messages.append({"role": "system", "content": data_context})
            
        return messages
    
    def _generate_response(self, messages: List[Dict]) -> str:
        """Generate response using OpenAI's API."""
        response = openai.ChatCompletion.create(
            model=self.config['model'],
            messages=messages,
            temperature=self.config['temperature'],
            max_tokens=self.config['max_tokens']
        )
        return response.choices[0].message['content']
    
    def get_relevant_financial_data(self, message: str) -> Dict:
        """
        Fetch relevant financial data based on message content.
        
        Args:
            message: User message to analyze
            
        Returns:
            Dict containing relevant financial data
        """
        data = {}
        
        # Keywords for different types of data
        data_keywords = {
            'finance': ['stock', 'price', 'market', 'ticker', 'shares'],
            'research': ['research', 'analysis', 'news', 'report'],
            'portfolio': ['portfolio', 'optimize', 'allocation', 'diversify']
        }
        
        # Check each category and fetch relevant data
        message_lower = message.lower()
        for category, keywords in data_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                try:
                    provider = self.data_providers[category]
                    data[category] = provider.get_relevant_data(message)
                except Exception as e:
                    print(f"Error fetching {category} data: {str(e)}")
        
        return data
    
    def _format_financial_data(self, data: Dict) -> str:
        """Format financial data into a readable string for the AI model."""
        formatted_parts = []
        
        for category, content in data.items():
            formatted_parts.append(f"{category.upper()} DATA:")
            formatted_parts.append(str(content))
        
        return "\n".join(formatted_parts)
    
    def learn_from_feedback(self, message: str, feedback: str, user_id: Optional[str] = None) -> None:
        """
        Update knowledge base based on user feedback.
        
        Args:
            message: Original message
            feedback: User feedback
            user_id: Optional user identifier
        """
        feedback_data = {
            'interaction': message,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        try:
            self.memory.add_to_long_term_memory(feedback_data)
            # Update response generation parameters based on feedback
            self.response_generator.update_parameters(feedback_data)
        except Exception as e:
            print(f"Error processing feedback: {str(e)}")