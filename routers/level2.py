from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/v2", tags=["v2"])

@router.get("/")
async def root_v2():
    """Root route for v2"""
    return {
        "message": "Welcome to InsightBoard AI API (Gemini) v2",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/health")
async def health_check_v2():
    """ Health check for v2 """
    return {
        "status": "healthy",
        "version": "v2",
        "service": "InsightBoard Gemini API",
        "timestamp": datetime.now().isoformat()
    }
