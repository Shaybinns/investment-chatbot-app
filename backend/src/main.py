# src/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Investment Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes after FastAPI initialization
from src.api.routes.api import router
app.include_router(router, prefix="/api")

# Remove the uvicorn.run() call since we're using the CMD in Dockerfile