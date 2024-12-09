from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import redis
import json
import os
from typing import Dict
from .openai_handler import OpenAIHandler

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize OpenAI handler
openai_handler = OpenAIHandler(api_key=os.getenv('OPENAI_API_KEY'))

# Store active connections
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Parse the message
            try:
                message = json.loads(data)
                user_message = message.get('text', '')
            except json.JSONDecodeError:
                user_message = data
            
            # Get conversation history from Redis
            history_key = f"chat_history:{user_id}"
            chat_history = [
                json.loads(msg) 
                for msg in redis_client.lrange(history_key, -5, -1)
            ]  # Get last 5 messages
            
            # Get AI response
            ai_response = await openai_handler.get_response(
                user_message,
                context=chat_history
            )
            
            # Store messages in Redis
            redis_client.lpush(
                history_key,
                json.dumps({
                    "text": user_message,
                    "sender": "user"
                })
            )
            redis_client.lpush(
                history_key,
                json.dumps({
                    "text": ai_response,
                    "sender": "assistant"
                })
            )
            
            # Send response back to client
            response = {
                "message": ai_response,
                "user_id": user_id
            }
            
            await websocket.send_json(response)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if user_id in active_connections:
            del active_connections[user_id]

@app.get("/")
async def root():
    return {"message": "Investment Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}