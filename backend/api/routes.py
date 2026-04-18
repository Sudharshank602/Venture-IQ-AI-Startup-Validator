"""
Startup Analysis API Router
RESTful endpoints for startup validation and business intelligence.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import time

from backend.models.schemas import (
    StartupIdeaRequest, StartupValidationResponse, HealthResponse
)
from backend.services.analysis_service import orchestrator
from backend.services.vector_store import vector_store
from backend.core.config import settings
from backend.core.logger import logger

router = APIRouter(prefix="/api/v1", tags=["Startup Intelligence"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """API health check endpoint."""
    return HealthResponse(
        status="operational",
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    )


@router.post("/analyze", response_model=StartupValidationResponse)
async def analyze_startup(request: StartupIdeaRequest):
    """
    🚀 Full Startup Analysis Endpoint

    Performs comprehensive AI-powered analysis including:
    - Market demand & sizing
    - Competitor analysis
    - SWOT analysis
    - Business moat evaluation
    - Revenue model suggestions
    - Growth strategy roadmap
    - Go-to-market strategy
    - Risk analysis
    - AI-generated pitch
    - Startup success probability score
    """
    try:
        logger.info(f"Analysis request received: {request.idea[:60]}...")
        result = await orchestrator.run_full_analysis(request)
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed. Please try again. Error: {str(e)[:100]}"
        )


@router.get("/vector-store/status")
async def vector_store_status():
    """Get RAG vector store status."""
    return vector_store.get_status()


@router.get("/models/info")
async def model_info():
    """Get configured AI model information."""
    return {
        "llm_model": settings.OPENAI_MODEL,
        "embedding_model": settings.OPENAI_EMBEDDING_MODEL,
        "vector_store": vector_store.get_status(),
    }
