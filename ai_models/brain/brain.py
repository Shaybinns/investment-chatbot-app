from typing import List, Dict, Optional
from datetime import datetime
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

class Message(BaseModel):
    content: str
    timestamp: datetime
    sender: str

class AIBrain:
    def __init__(self):
        self.app = FastAPI()
        self.messages = []  # Simple in-memory storage for now
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            print("WebSocket connection established")
            while True:
                try:
                    # Receive message from client
                    data = await websocket.receive_text()
                    print(f"Received message: {data}")
                    
                    # Process message
                    response = await self.process_message(data)
                    
                    # Send response back
                    await websocket.send_text(response)
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
