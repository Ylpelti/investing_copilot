from fastapi import APIRouter


router = APIRouter(prefix="/analysis", tags=["AI analysis"] )

@router.post("")
def explain_portfolio()