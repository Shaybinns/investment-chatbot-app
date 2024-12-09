# api.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import redis
import json
from typing import Dict

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

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
            except json.JSONDecodeError:
                message = {"text": data}
            
            # Store message in Redis (optional)
            redis_client.lpush(f"chat_history:{user_id}", json.dumps(message))
            
            # Echo back for testing
            response = {
                "message": f"Received: {message.get('text', '')}",
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

# For testing the server is up
@app.get("/health")
async def health_check():
    return {"status": "healthy"}