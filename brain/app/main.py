from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.config import settings
from app.routers import analysis_router, graph_router, batch_router


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="DEBUG" if settings.DEBUG else "INFO"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("🧠 BRAIN Mock Service starting...")
    logger.info(f"   Version: {settings.APP_VERSION}")
    logger.info(f"   Debug: {settings.DEBUG}")
    logger.info(f"   GPU Simulation: {settings.SIMULATE_GPU}")
    logger.info("🚀 BRAIN Mock Service ready!")
    
    yield
    
    logger.info("🧠 BRAIN Mock Service shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Mock BRAIN Service for Persian Social Media Analysis (Development)",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "gpu_available": settings.SIMULATE_GPU,
        "gpu_memory_used": 2048 if settings.SIMULATE_GPU else None,
        "gpu_memory_total": 8192 if settings.SIMULATE_GPU else None,
        "mode": "mock"
    }


# Root
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "mode": "mock",
        "message": "This is a MOCK service. Replace with real BRAIN for production."
    }


# Include routers
app.include_router(analysis_router)
app.include_router(graph_router)
app.include_router(batch_router)


# Trend detection endpoint (at root level to match backend expectations)
@app.post("/analyze/trends", tags=["Analysis"])
async def analyze_trends(posts: list, time_window: str = "1h", min_trend_size: int = 10):
    """Detect trends endpoint at root level."""
    from app.mock_data import generate_trend_detection
    trends = generate_trend_detection(posts)
    return {"trends": trends}
