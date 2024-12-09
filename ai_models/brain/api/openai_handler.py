from openai import AsyncOpenAI
import json
from typing import Dict, Optional

class OpenAIHandler:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.default_system_message = """You are an AI investment advisor with expertise in:
- Portfolio management
- Market analysis
- Risk assessment
- Financial planning
- Stock and cryptocurrency trading

Provide clear, well-reasoned investment advice while always considering:
1. Risk management
2. Diversification
3. Long-term strategy
4. Market conditions
5. Individual investor needs

Always remind users that this is educational content and not financial advice."""

    async def get_response(
        self, 
        user_message: str, 
        context: Optional[list] = None,
        system_message: Optional[str] = None
    ) -> str:
        messages = [
            {"role": "system", "content": system_message or self.default_system_message}
        ]
        
        # Add context if provided
        if context:
            for msg in context:
                messages.append({
                    "role": "user" if msg["sender"] == "user" else "assistant",
                    "content": msg["text"]
                })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-1106-preview",  # Using the latest GPT-4 model
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."