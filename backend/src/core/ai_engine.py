from typing import Dict, List
from openai import OpenAI
from .memory_store import MemoryStore

class AIEngine:
    def __init__(self, memory_store: MemoryStore):
        self.client = OpenAI()
        self.memory_store = memory_store

    async def process_message(self, user_id: str, message: str) -> str:
        context = await self.memory_store.get_context(user_id)
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an investment advisor AI."},
                *context,
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content