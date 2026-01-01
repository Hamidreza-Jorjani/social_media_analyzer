from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import uuid
import random

from app.config import settings
from app.mock_data import generate_full_analysis, generate_trend_detection

router = APIRouter(prefix="/batch", tags=["Batch Processing"])

# In-memory storage for batch jobs (use Redis in production)
batch_jobs: Dict[str, Dict[str, Any]] = {}


class BatchAnalysisRequest(BaseModel):
    analysis_id: int
    posts: List[Dict[str, Any]]
    config: Dict[str, Any]
    callback_url: Optional[str] = None


class TrendDetectionRequest(BaseModel):
    posts: List[Dict[str, Any]]
    time_field: str = "posted_at"
    content_field: str = "content"
    min_trend_size: int = 10
    time_window: str = "1h"


async def process_batch_job(task_id: str, request: BatchAnalysisRequest):
    """Background task to process batch analysis."""
    batch_jobs[task_id]["status"] = "processing"
    batch_jobs[task_id]["progress"] = 0
    
    results = []
    total = len(request.posts)
    
    for i, post in enumerate(request.posts):
        # Simulate processing delay
        await asyncio.sleep(random.uniform(0.01, 0.05))
        
        post_id = str(post.get("id", i))
        content = post.get("content", "")
        
        result = generate_full_analysis(post_id, content)
        results.append(result)
        
        # Update progress
        batch_jobs[task_id]["progress"] = int(((i + 1) / total) * 100)
    
    batch_jobs[task_id]["status"] = "completed"
    batch_jobs[task_id]["progress"] = 100
    batch_jobs[task_id]["results"] = results


@router.post("/analyze")
async def submit_batch_analysis(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Submit batch analysis job."""
    task_id = str(uuid.uuid4())
    
    batch_jobs[task_id] = {
        "task_id": task_id,
        "analysis_id": request.analysis_id,
        "status": "queued",
        "progress": 0,
        "total_posts": len(request.posts),
        "results": None
    }
    
    # Start background processing
    background_tasks.add_task(process_batch_job, task_id, request)
    
    return {
        "analysis_id": request.analysis_id,
        "task_id": task_id,
        "status": "queued",
        "message": f"Batch job queued for {len(request.posts)} posts"
    }


@router.get("/status/{task_id}")
async def get_batch_status(task_id: str):
    """Get batch job status."""
    if task_id not in batch_jobs:
        return {"error": "Task not found", "task_id": task_id}
    
    job = batch_jobs[task_id]
    
    return {
        "task_id": task_id,
        "status": job["status"],
        "progress": job["progress"],
        "total_posts": job["total_posts"]
    }


@router.get("/result/{task_id}")
async def get_batch_result(task_id: str):
    """Get batch job results."""
    if task_id not in batch_jobs:
        return {"error": "Task not found", "task_id": task_id}
    
    job = batch_jobs[task_id]
    
    if job["status"] != "completed":
        return {
            "task_id": task_id,
            "status": job["status"],
            "message": "Job not completed yet"
        }
    
    return {
        "task_id": task_id,
        "status": "completed",
        "results": job["results"]
    }


@router.post("/trends")
async def detect_trends(request: TrendDetectionRequest):
    """Detect trends from posts."""
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    trends = generate_trend_detection(request.posts)
    
    return {"trends": trends}
