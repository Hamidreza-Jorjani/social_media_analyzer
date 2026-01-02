from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import random

from app.config import settings
from app.mock_data import (
    generate_sentiment,
    generate_emotions,
    generate_keywords,
    generate_entities,
    generate_topics,
    generate_summary,
    generate_full_analysis
)

router = APIRouter(prefix="/analyze", tags=["Analysis"])


class TextAnalysisRequest(BaseModel):
    texts: List[str]
    text_ids: Optional[List[str]] = None
    analysis_types: List[str] = ["sentiment", "emotion", "keywords"]
    language: str = "fa"
    config: Optional[Dict[str, Any]] = None


class SentimentRequest(BaseModel):
    texts: List[str]
    text_ids: Optional[List[str]] = None
    language: str = "fa"


class SummarizationRequest(BaseModel):
    texts: List[str]
    max_length: int = 150
    min_length: int = 30
    language: str = "fa"


class KeywordRequest(BaseModel):
    texts: List[str]
    max_keywords: int = 10
    language: str = "fa"


class EntityRequest(BaseModel):
    texts: List[str]
    language: str = "fa"


class TopicRequest(BaseModel):
    texts: List[str]
    num_topics: int = 10
    language: str = "fa"


async def simulate_delay():
    """Simulate processing time."""
    delay = random.uniform(settings.MOCK_DELAY_MIN, settings.MOCK_DELAY_MAX)
    await asyncio.sleep(delay)


@router.post("/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment of texts."""
    await simulate_delay()
    
    text_ids = request.text_ids or [str(i) for i in range(len(request.texts))]
    
    results = []
    for i, text in enumerate(request.texts):
        results.append({
            "text_id": text_ids[i],
            "sentiment": generate_sentiment(text)  # Pass text for analysis
        })
    
    return {"results": results}


@router.post("/emotion")
async def analyze_emotions(request: SentimentRequest):
    """Analyze emotions in texts."""
    await simulate_delay()
    
    text_ids = request.text_ids or [str(i) for i in range(len(request.texts))]
    
    results = []
    for i, text in enumerate(request.texts):
        emotions = generate_emotions(text)  # Pass text for analysis
        results.append({
            "text_id": text_ids[i],
            "emotions": emotions,
            "dominant_emotion": max(emotions, key=emotions.get)
        })
    
    return {"results": results}


@router.post("/text")
async def analyze_text(request: TextAnalysisRequest):
    """Full text analysis."""
    await simulate_delay()
    
    text_ids = request.text_ids or [str(i) for i in range(len(request.texts))]
    
    results = []
    for i, text in enumerate(request.texts):
        result = {"text_id": text_ids[i]}
        
        if "sentiment" in request.analysis_types:
            result["sentiment"] = generate_sentiment(text)
        
        if "emotion" in request.analysis_types:
            emotions = generate_emotions(text)
            result["emotions"] = emotions
            result["dominant_emotion"] = max(emotions, key=emotions.get)
        
        if "keywords" in request.analysis_types:
            result["keywords"] = generate_keywords(text)
        
        if "entities" in request.analysis_types:
            result["entities"] = generate_entities(text)
        
        if "topics" in request.analysis_types:
            result["topics"] = generate_topics(text)
        
        if "summary" in request.analysis_types:
            result["summary"] = generate_summary(text)
        
        results.append(result)
    
    return {"results": results}


@router.post("/summarize")
async def summarize_texts(request: SummarizationRequest):
    """Summarize texts."""
    await simulate_delay()
    
    summaries = [generate_summary(text) for text in request.texts]
    
    return {"summaries": summaries}


@router.post("/keywords")
async def extract_keywords(request: KeywordRequest):
    """Extract keywords from texts."""
    await simulate_delay()
    
    keywords = [
        generate_keywords(text, request.max_keywords) 
        for text in request.texts
    ]
    
    return {"keywords": keywords}


@router.post("/entities")
async def extract_entities(request: EntityRequest):
    """Extract named entities from texts."""
    await simulate_delay()
    
    entities = [generate_entities(text) for text in request.texts]
    
    return {"entities": entities}


@router.post("/topics")
async def detect_topics(request: TopicRequest):
    """Detect topics in texts."""
    await simulate_delay()
    
    # Global topics from all texts
    all_text = " ".join(request.texts)
    global_topics = generate_topics(all_text, request.num_topics)
    
    # Topic distribution per document
    doc_topics = [generate_topics(text, 3) for text in request.texts]
    
    return {
        "global_topics": global_topics,
        "document_topics": doc_topics
    }
