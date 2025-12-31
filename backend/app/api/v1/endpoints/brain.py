from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst
from app.models.user import User
from app.services.brain_service import brain_service, BrainServiceError
from app.schemas.brain import (
    BrainHealthResponse,
    TextAnalysisRequest,
    TextAnalysisResponse,
    SummarizationRequest
)

router = APIRouter()


@router.get("/health", response_model=BrainHealthResponse)
async def check_brain_health(
    current_user: User = Depends(get_current_user)
):
    """
    Check BRAIN service health status.
    """
    health = await brain_service.health_check()
    return health


@router.get("/available")
async def check_brain_available(
    current_user: User = Depends(get_current_user)
):
    """
    Check if BRAIN service is available.
    """
    available = await brain_service.is_available()
    return {"available": available}


@router.post("/analyze/sentiment")
async def analyze_sentiment(
    texts: List[str],
    current_user: User = Depends(get_current_analyst)
):
    """
    Analyze sentiment of texts.
    """
    try:
        results = await brain_service.analyze_sentiment(texts)
        return {"results": results}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/analyze/emotions")
async def analyze_emotions(
    texts: List[str],
    current_user: User = Depends(get_current_analyst)
):
    """
    Analyze emotions in texts.
    """
    try:
        results = await brain_service.analyze_emotions(texts)
        return {"results": results}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/analyze/text", response_model=List[TextAnalysisResponse])
async def analyze_text(
    request: TextAnalysisRequest,
    current_user: User = Depends(get_current_analyst)
):
    """
    Full text analysis including sentiment, emotion, keywords.
    """
    try:
        results = await brain_service.analyze_text(
            texts=request.texts,
            text_ids=request.text_ids,
            analysis_types=request.analysis_types,
            config=request.config
        )
        return results
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/summarize")
async def summarize_texts(
    request: SummarizationRequest,
    current_user: User = Depends(get_current_analyst)
):
    """
    Summarize texts.
    """
    try:
        summaries = await brain_service.summarize_texts(
            texts=request.texts,
            max_length=request.max_length,
            min_length=request.min_length
        )
        return {"summaries": summaries}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/extract/keywords")
async def extract_keywords(
    texts: List[str],
    max_keywords: int = 10,
    current_user: User = Depends(get_current_analyst)
):
    """
    Extract keywords from texts.
    """
    try:
        keywords = await brain_service.extract_keywords(
            texts=texts,
            max_keywords=max_keywords
        )
        return {"keywords": keywords}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/extract/entities")
async def extract_entities(
    texts: List[str],
    current_user: User = Depends(get_current_analyst)
):
    """
    Extract named entities from texts.
    """
    try:
        entities = await brain_service.extract_entities(texts)
        return {"entities": entities}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/detect/topics")
async def detect_topics(
    texts: List[str],
    num_topics: int = 10,
    current_user: User = Depends(get_current_analyst)
):
    """
    Detect topics in texts.
    """
    try:
        result = await brain_service.detect_topics(
            texts=texts,
            num_topics=num_topics
        )
        return result
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )
