from fastapi import APIRouter, HTTPException
from typing import Dict

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Investment Chatbot API"}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
