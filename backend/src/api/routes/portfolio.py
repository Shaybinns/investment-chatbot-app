from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.get("/")
def get_portfolios():
    # TODO: Implement portfolio listing
    pass

@router.post("/")
def create_portfolio():
    # TODO: Implement portfolio creation
    pass