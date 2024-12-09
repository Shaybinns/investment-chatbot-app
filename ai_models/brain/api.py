from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
from .core import ChatBrain
import json

app = FastAPI(title='Investment Chatbot API')

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Initialize chat brain
brain = ChatBrain(redis_url='redis://localhost:6379')

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)

    async def send_message(self, client_id: str, data: Any):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(data)

manager = ConnectionManager()

@app.websocket('/ws/chat/{user_id}')
async def chat_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Receive message
            message = await websocket.receive_text()
            
            # Process message
            response, msg_id = await brain.process_message(user_id, message)
            
            # Send response with message ID
            await manager.send_message(
                user_id,
                {
                    'response': response,
                    'message_id': msg_id
                }
            )
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f'WebSocket error: {str(e)}')
        manager.disconnect(user_id)

@app.post('/feedback/{message_id}')
async def submit_feedback(message_id: str, rating: int, comment: Optional[str] = None):
    try:
        await brain.store_feedback(message_id, rating, comment)
        return {'status': 'success', 'message': 'Feedback stored successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/chat/history/{user_id}')
async def get_chat_history(user_id: str, limit: int = 10):
    try:
        history = await brain.get_conversation_history(user_id, limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
