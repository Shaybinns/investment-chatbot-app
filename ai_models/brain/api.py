from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from .core import ChatBrain

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

@app.websocket('/ws/chat/{user_id}')
async def chat_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    try:
        while True:
            # Receive message
            message = await websocket.receive_text()
            
            # Process message
            response, msg_id = await brain.process_message(user_id, message)
            
            # Send response with message ID
            await websocket.send_json({
                'response': response,
                'message_id': msg_id
            })
    except Exception as e:
        print(f'WebSocket error: {str(e)}')
        await websocket.close()

@app.post('/feedback/{message_id}')
async def submit_feedback(message_id: str, rating: int, comment: Optional[str] = None):
    """Submit feedback for a chat interaction."""
    try:
        await brain.store_feedback(message_id, rating, comment)
        return {'status': 'success', 'message': 'Feedback stored successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/chat/history/{user_id}')
async def get_chat_history(user_id: str, limit: int = 10):
    """Get chat history for a user."""
    try:
        history = await brain.get_conversation_history(user_id, limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
