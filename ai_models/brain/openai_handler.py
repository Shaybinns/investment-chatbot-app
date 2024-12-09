from typing import Dict, List, Any, Optional
from openai import OpenAI
import logging
from datetime import datetime

class OpenAIHandler:
    def __init__(self, api_key: str, model: str = 'gpt-4-turbo-preview'):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)
        
        # Investment-specific system prompts
        self.BASE_SYSTEM_PROMPT = """
        You are an advanced investment AI assistant with deep expertise in:
        1. Financial markets and investment strategies
        2. Portfolio management and optimization
        3. Risk assessment and management
        4. Market analysis and research
        5. Investment regulations and compliance
        
        Guidelines:
        - Provide well-reasoned investment analysis backed by data when available
        - Always consider risk management and diversification
        - Be clear about uncertainties and potential risks
        - Maintain compliance with investment regulations
        - Avoid making specific investment recommendations
        - Focus on educational and analytical insights
        """
        
    async def generate_response(
        self,
        message: str,
        context: List[Dict[str, Any]],
        financial_data: Optional[Dict[str, Any]] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            # Construct the full context message
            context_message = self._build_context_message(context, financial_data, additional_context)
            
            # Prepare the messages for the API call
            messages = [
                {"role": "system", "content": self.BASE_SYSTEM_PROMPT},
                {"role": "system", "content": context_message},
                {"role": "user", "content": message}
            ]
            
            # Make the API call
            response = await self._make_api_call(messages)
            
            return {
                'response': response,
                'timestamp': datetime.now().isoformat(),
                'model_used': self.model,
                'context_used': context
            }
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise
    
    def _build_context_message(self, 
                              context: List[Dict[str, Any]], 
                              financial_data: Optional[Dict[str, Any]] = None,
                              additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        context_parts = []
        
        # Add conversation history context
        if context:
            context_parts.append("Previous relevant conversations:")
            for ctx in context:
                context_parts.append(f"- Q: {ctx.get('input', '')}\n  A: {ctx.get('response', '')}")
        
        # Add financial data context
        if financial_data:
            context_parts.append("\nRelevant financial data:")
            for key, value in financial_data.items():
                context_parts.append(f"- {key}: {value}")
        
        # Add additional context
        if additional_context:
            context_parts.append("\nAdditional context:")
            for key, value in additional_context.items():
                context_parts.append(f"- {key}: {value}")
        
        return "\n".join(context_parts)
    
    async def _make_api_call(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {str(e)}")
            raise
    
    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze the sentiment of investment-related text."""
        try:
            messages = [
                {"role": "system", "content": "Analyze the sentiment of the following investment-related text. Return a JSON object with scores for: bullish (0-1), bearish (0-1), and confidence (0-1)."},
                {"role": "user", "content": text}
            ]
            
            response = await self._make_api_call(messages)
            
            # TODO: Parse the response into sentiment scores
            # This is a placeholder implementation
            return {
                'bullish': 0.5,
                'bearish': 0.5,
                'confidence': 0.5
            }
            
        except Exception as e:
            self.logger.error(f"Sentiment analysis failed: {str(e)}")
            raise
    
    async def extract_investment_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract investment-related entities from text."""
        try:
            messages = [
                {"role": "system", "content": "Extract investment-related entities from the text. Categories: stocks, indices, commodities, currencies, companies, sectors. Return as JSON."},
                {"role": "user", "content": text}
            ]
            
            response = await self._make_api_call(messages)
            
            # TODO: Parse the response into entity categories
            # This is a placeholder implementation
            return {
                'stocks': [],
                'indices': [],
                'commodities': [],
                'currencies': [],
                'companies': [],
                'sectors': []
            }
            
        except Exception as e:
            self.logger.error(f"Entity extraction failed: {str(e)}")
            raise
