from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/chat")
def chat():
    # TODO: Implement AI chat
    pass

@router.post("/analyze-portfolio")
def analyze_portfolio():
    # TODO: Implement portfolio analysis
    pass