from typing import List, Dict, Optional
from datetime import datetime
import aioredis
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
import json

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.utcnow()

class Feedback(BaseModel):
    message_id: str
    rating: int  # 1-5
    comment: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

class ChatBrain:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
        self.feedback_threshold = 4.0  # Minimum average rating to consider successful
        
    async def process_message(self, user_id: str, message: str) -> str:
        """Process an incoming message and generate a response."""
        # Get conversation history
        history = await self.get_conversation_history(user_id)
        
        # Generate response based on history and message
        response = await self.generate_response(history, message)
        
        # Store the interaction
        msg_id = await self.store_interaction(user_id, message, response)
        
        return response, msg_id
    
    async def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve recent conversation history."""
        history_key = f'chat_history:{user_id}'
        raw_history = await self.redis.lrange(history_key, -limit, -1)
        return [json.loads(h) for h in raw_history]
    
    async def store_interaction(self, user_id: str, message: str, response: str) -> str:
        """Store the interaction in Redis."""
        msg_id = f'{user_id}:{datetime.utcnow().timestamp()}'
        interaction = {
            'id': msg_id,
            'message': message,
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Store in history
        history_key = f'chat_history:{user_id}'
        await self.redis.rpush(history_key, json.dumps(interaction))
        
        return msg_id
    
    async def store_feedback(self, message_id: str, rating: int, comment: Optional[str] = None):
        """Store user feedback and update learning metrics."""
        feedback = Feedback(
            message_id=message_id,
            rating=rating,
            comment=comment
        )
        
        # Store feedback
        feedback_key = f'feedback:{message_id}'
        await self.redis.set(feedback_key, feedback.json())
        
        # Update feedback metrics
        await self.update_feedback_metrics(feedback)
    
    async def update_feedback_metrics(self, feedback: Feedback):
        """Update feedback metrics for learning."""
        metrics_key = 'feedback_metrics'
        
        # Get current metrics
        metrics = await self.redis.get(metrics_key)
        if metrics:
            metrics = json.loads(metrics)
        else:
            metrics = {'total_ratings': 0, 'avg_rating': 0.0}
        
        # Update metrics
        total = metrics['total_ratings']
        current_avg = metrics['avg_rating']
        
        # Calculate new average
        new_total = total + 1
        new_avg = ((current_avg * total) + feedback.rating) / new_total
        
        # Store updated metrics
        metrics.update({
            'total_ratings': new_total,
            'avg_rating': new_avg,
            'last_updated': datetime.utcnow().isoformat()
        })
        
        await self.redis.set(metrics_key, json.dumps(metrics))
    
    async def generate_response(self, history: List[Dict], message: str) -> str:
        """Generate a response based on conversation history and current message."""
        # For now, return a simple response
        # This will be replaced with actual AI model integration
        return f'I understand you said: {message}. How can I help with your investment needs?'
