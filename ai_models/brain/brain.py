from typing import List, Dict, Optional
from datetime import datetime
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

class Message(BaseModel):
    content: str
    timestamp: datetime
    sender: str

class AIBrain:
    def __init__(self):
        self.app = FastAPI()
        self.messages = []  # Simple in-memory storage for now
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
        @self.app.websocket("/ws/chat/{user_id}")
        async def websocket_endpoint(websocket: WebSocket, user_id: str):
            await websocket.accept()
            print(f"WebSocket connection established for user: {user_id}")
            while True:
                try:
                    # Receive message from client
                    data = await websocket.receive_text()
                    print(f"Received message: {data}")
                    
                    # Parse the JSON message
                    message_data = json.loads(data)
                    message_text = message_data.get('text', '')
                    
                    # Process message
                    response = await self.process_message(message_text)
                    
                    # Send response back in the expected format
                    await websocket.send_text(json.dumps({
                        "message": response
                    }))
                    print(f"Sent response: {response}")
                except Exception as e:
                    print(f"Error in websocket: {e}")
                    break

    async def process_message(self, message: str) -> str:
        # Store message
        self.store_message(message)
        
        # Generate simple response for now
        response = self.generate_response(message)
        
        # Store response
        self.store_message(response, is_response=True)
        
        return response

    def store_message(self, content: str, is_response: bool = False):
        message = Message(
            content=content,
            timestamp=datetime.now(),
            sender="bot" if is_response else "user"
        )
        self.messages.append(message)

    def generate_response(self, message: str) -> str:
        # Simple response generation for testing
        if "hello" in message.lower():
            return "Hello! How can I help you with your investments today?"
        elif "invest" in message.lower():
            return "I can help you understand various investment options. What specific information are you looking for?"
        elif "market" in message.lower():
            return "The market analysis feature will be available soon. Is there anything else you'd like to know?"
        else:
            return "I understand you're interested in investments. Could you please be more specific about what you'd like to know?"

# Create FastAPI app instance
app = AIBrain().app

# Add a simple root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Investment Chatbot Brain is running"}