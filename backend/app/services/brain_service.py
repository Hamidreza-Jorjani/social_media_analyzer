from typing import Optional, Any, Dict, List
import httpx
from app.core.config import settings
from app.services.base import BaseService
from app.schemas.brain import (
    BrainHealthResponse,
    TextAnalysisRequest,
    TextAnalysisResponse,
    BatchAnalysisRequest,
    BatchAnalysisResponse,
    SummarizationRequest,
    TrendDetectionRequest,
)


class BrainServiceError(Exception):
    """Exception for BRAIN service errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BrainService(BaseService):
    """
    Service for communicating with the BRAIN (RAPIDS Docker) container.
    Handles all AI/ML analysis requests.
    """
    
    def __init__(self):
        super().__init__("BrainService")
        self.base_url = settings.BRAIN_SERVICE_URL
        self.timeout = settings.BRAIN_SERVICE_TIMEOUT
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                headers={"Content-Type": "application/json"}
            )
        return self._client
    
    async def close(self) -> None:
        """Close HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to BRAIN service."""
        client = await self._get_client()
        
        try:
            response = await client.request(
                method=method,
                url=endpoint,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            self.log_error(f"BRAIN service timeout: {endpoint}")
            raise BrainServiceError("BRAIN service timeout", status_code=504)
        except httpx.HTTPStatusError as e:
            self.log_error(f"BRAIN service HTTP error: {e.response.status_code}")
            raise BrainServiceError(
                f"BRAIN service error: {e.response.text}",
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            self.log_error(f"BRAIN service connection error: {e}")
            raise BrainServiceError("BRAIN service unavailable", status_code=503)
        except Exception as e:
            self.log_error(f"BRAIN service unexpected error: {e}")
            raise BrainServiceError(str(e))
    
    async def health_check(self) -> BrainHealthResponse:
        """Check BRAIN service health."""
        try:
            result = await self._request("GET", "/health")
            return BrainHealthResponse(**result)
        except BrainServiceError:
            return BrainHealthResponse(
                status="unhealthy",
                gpu_available=False
            )
    
    async def is_available(self) -> bool:
        """Check if BRAIN service is available."""
        try:
            health = await self.health_check()
            return health.status == "healthy"
        except Exception:
            return False
    
    # ==========================================
    # Sentiment Analysis
    # ==========================================
    
    async def analyze_sentiment(
        self,
        texts: List[str],
        text_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment of texts."""
        if text_ids is None:
            text_ids = [str(i) for i in range(len(texts))]
        
        request_data = {
            "texts": texts,
            "text_ids": text_ids,
            "analysis_types": ["sentiment"],
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/sentiment", data=request_data)
        return result.get("results", [])
    
    async def analyze_sentiment_batch(
        self,
        posts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Batch sentiment analysis for posts."""
        texts = [p.get("content", "") for p in posts]
        text_ids = [str(p.get("id", i)) for i, p in enumerate(posts)]
        
        return await self.analyze_sentiment(texts, text_ids)
    
    # ==========================================
    # Emotion Analysis
    # ==========================================
    
    async def analyze_emotions(
        self,
        texts: List[str],
        text_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Analyze emotions in texts."""
        if text_ids is None:
            text_ids = [str(i) for i in range(len(texts))]
        
        request_data = {
            "texts": texts,
            "text_ids": text_ids,
            "analysis_types": ["emotion"],
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/emotion", data=request_data)
        return result.get("results", [])
    
    # ==========================================
    # Full Text Analysis
    # ==========================================
    
    async def analyze_text(
        self,
        texts: List[str],
        text_ids: Optional[List[str]] = None,
        analysis_types: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> List[TextAnalysisResponse]:
        """Full text analysis including sentiment, emotion, keywords, etc."""
        if text_ids is None:
            text_ids = [str(i) for i in range(len(texts))]
        
        if analysis_types is None:
            analysis_types = ["sentiment", "emotion", "keywords", "entities"]
        
        request_data = TextAnalysisRequest(
            texts=texts,
            text_ids=text_ids,
            analysis_types=analysis_types,
            language="fa",
            config=config
        ).model_dump()
        
        result = await self._request("POST", "/analyze/text", data=request_data)
        
        return [TextAnalysisResponse(**r) for r in result.get("results", [])]
    
    # ==========================================
    # Summarization
    # ==========================================
    
    async def summarize_texts(
        self,
        texts: List[str],
        max_length: int = 150,
        min_length: int = 30
    ) -> List[str]:
        """Summarize texts."""
        request_data = SummarizationRequest(
            texts=texts,
            max_length=max_length,
            min_length=min_length,
            language="fa"
        ).model_dump()
        
        result = await self._request("POST", "/analyze/summarize", data=request_data)
        return result.get("summaries", [])
    
    async def summarize_single(
        self,
        text: str,
        max_length: int = 150
    ) -> str:
        """Summarize a single text."""
        summaries = await self.summarize_texts([text], max_length)
        return summaries[0] if summaries else ""
    
    # ==========================================
    # Keyword Extraction
    # ==========================================
    
    async def extract_keywords(
        self,
        texts: List[str],
        max_keywords: int = 10
    ) -> List[List[str]]:
        """Extract keywords from texts."""
        request_data = {
            "texts": texts,
            "max_keywords": max_keywords,
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/keywords", data=request_data)
        return result.get("keywords", [])
    
    # ==========================================
    # Named Entity Recognition
    # ==========================================
    
    async def extract_entities(
        self,
        texts: List[str]
    ) -> List[List[Dict[str, Any]]]:
        """Extract named entities from texts."""
        request_data = {
            "texts": texts,
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/entities", data=request_data)
        return result.get("entities", [])
    
    # ==========================================
    # Topic Modeling
    # ==========================================
    
    async def detect_topics(
        self,
        texts: List[str],
        num_topics: int = 10
    ) -> Dict[str, Any]:
        """Detect topics in texts."""
        request_data = {
            "texts": texts,
            "num_topics": num_topics,
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/topics", data=request_data)
        return result
    
    # ==========================================
    # Trend Detection
    # ==========================================
    
    async def detect_trends(
        self,
        posts: List[Dict[str, Any]],
        time_window: str = "1h",
        min_trend_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Detect trends in posts."""
        request_data = TrendDetectionRequest(
            posts=posts,
            time_field="posted_at",
            content_field="content",
            min_trend_size=min_trend_size,
            time_window=time_window
        ).model_dump()
        
        result = await self._request("POST", "/analyze/trends", data=request_data)
        return result.get("trends", [])
    
    # ==========================================
    # Graph Analysis
    # ==========================================
    
    async def analyze_graph(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        algorithms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze graph structure."""
        if algorithms is None:
            algorithms = ["pagerank", "community_detection", "centrality"]
        
        request_data = {
            "nodes": nodes,
            "edges": edges,
            "algorithms": algorithms
        }
        
        result = await self._request("POST", "/analyze/graph", data=request_data)
        return result
    
    async def calculate_pagerank(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        damping: float = 0.85
    ) -> List[Dict[str, Any]]:
        """Calculate PageRank for nodes."""
        request_data = {
            "nodes": nodes,
            "edges": edges,
            "algorithm": "pagerank",
            "damping": damping
        }
        
        result = await self._request("POST", "/analyze/graph/pagerank", data=request_data)
        return result.get("nodes", [])
    
    async def detect_communities(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect communities in graph."""
        request_data = {
            "nodes": nodes,
            "edges": edges,
            "algorithm": "community_detection"
        }
        
        result = await self._request("POST", "/analyze/graph/communities", data=request_data)
        return result
    
    # ==========================================
    # Batch Analysis
    # ==========================================
    
    async def submit_batch_analysis(
        self,
        analysis_id: int,
        posts: List[Dict[str, Any]],
        config: Dict[str, Any],
        callback_url: Optional[str] = None
    ) -> BatchAnalysisResponse:
        """Submit batch analysis job to BRAIN."""
        request_data = BatchAnalysisRequest(
            analysis_id=analysis_id,
            posts=posts,
            config=config,
            callback_url=callback_url
        ).model_dump()
        
        result = await self._request("POST", "/batch/analyze", data=request_data)
        return BatchAnalysisResponse(**result)
    
    async def get_batch_status(
        self,
        task_id: str
    ) -> Dict[str, Any]:
        """Get batch analysis status."""
        result = await self._request("GET", f"/batch/status/{task_id}")
        return result
    
    async def get_batch_result(
        self,
        task_id: str
    ) -> Dict[str, Any]:
        """Get batch analysis result."""
        result = await self._request("GET", f"/batch/result/{task_id}")
        return result


# Create singleton instance
brain_service = BrainService()
