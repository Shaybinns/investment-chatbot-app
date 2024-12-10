import redis
from typing import List, Dict
from sqlalchemy.orm import Session

class MemoryStore:
    def __init__(self, redis_client: redis.Redis, db_session: Session):
        self.redis = redis_client
        self.db = db_session

    async def get_context(self, user_id: str) -> List[Dict[str, str]]:
        # Get recent conversation history from Redis
        return self.redis.lrange(f"chat:{user_id}", 0, -1)

    async def store_interaction(self, user_id: str, message: str, response: str):
        # Store in Redis for short-term memory
        self.redis.lpush(f"chat:{user_id}", {"role": "user", "content": message})
        self.redis.lpush(f"chat:{user_id}", {"role": "assistant", "content": response})