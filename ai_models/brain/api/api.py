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

# Debug print the API key (only first 5 chars)
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key starts with: {api_key[:5]}...")

# Initialize Redis connection
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    print("Redis connection successful")
except Exception as e:
    print(f"Redis connection failed: {str(e)}")
    redis_client = None

# Initialize OpenAI handler
try:
    openai_handler = OpenAIHandler(api_key=os.getenv('OPENAI_API_KEY'))
except Exception as e:
    print(f"Failed to initialize OpenAI handler: {str(e)}")
    raise

# Store active connections
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    try:
        await websocket.accept()
        active_connections[user_id] = websocket
        print(f"New connection established for user: {user_id}")
        
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                print(f"Received message: {data}")
                
                # Parse the message
                try:
                    message = json.loads(data)
                    user_message = message.get('text', '')
                except json.JSONDecodeError:
                    user_message = data
                
                print(f"Processing message: {user_message}")
                
                # Get AI response
                try:
                    ai_response = await openai_handler.get_response(
                        user_message,
                        context=[]  # Simplified for testing
                    )
                    print(f"Got AI response: {ai_response[:100]}...")
                except Exception as e:
                    print(f"Error getting AI response: {str(e)}")
                    ai_response = "Error processing request"
                
                # Send response back to client
                response = {
                    "message": ai_response,
                    "user_id": user_id
                }
                
                await websocket.send_json(response)
                
            except Exception as e:
                print(f"Error processing message: {str(e)}")
                try:
                    await websocket.send_json({
                        "message": "Error processing your message",
                        "user_id": user_id
                    })
                except:
                    pass
                
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        if user_id in active_connections:
            del active_connections[user_id]
            print(f"Connection closed for user: {user_id}")

@app.get("/")
async def root():
    return {"message": "Investment Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}