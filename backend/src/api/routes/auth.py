from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login():
    # TODO: Implement login
    pass

@router.post("/register")
def register():
    # TODO: Implement registration
    pass