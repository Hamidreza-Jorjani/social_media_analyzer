from typing import Optional, Dict, Any, List
from celery import current_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import asyncio
import httpx

from app.services.celery_app import celery_app
from app.core.config import settings
from loguru import logger

# Create sync engine for Celery tasks
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL,
    pool_pre_ping=True
)
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


def get_sync_db() -> Session:
    """Get synchronous database session for Celery tasks."""
    db = SyncSessionLocal()
    return db


def run_async(coro):
    """Run async function in sync context - properly handles event loop."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(coro)
    finally:
        # Don't close the loop, just clean up pending tasks
        try:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
        except RuntimeError:
            pass


def call_brain_sync(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous HTTP call to BRAIN service."""
    url = f"{settings.BRAIN_SERVICE_URL}{endpoint}"
    
    try:
        with httpx.Client(timeout=settings.BRAIN_SERVICE_TIMEOUT) as client:
            response = client.post(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        logger.error(f"BRAIN service timeout: {endpoint}")
        raise Exception("BRAIN service timeout")
    except httpx.HTTPStatusError as e:
        logger.error(f"BRAIN service HTTP error: {e.response.status_code}")
        raise Exception(f"BRAIN service error: {e.response.text}")
    except httpx.RequestError as e:
        logger.error(f"BRAIN service connection error: {e}")
        raise Exception("BRAIN service unavailable")


@celery_app.task(bind=True, name="app.services.tasks.process_analysis")
def process_analysis(
    self,
    analysis_id: int,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process an analysis job.
    """
    logger.info(f"Starting analysis task for analysis_id={analysis_id}")
    
    db = get_sync_db()
    
    try:
        from app.models.analysis import Analysis, AnalysisStatus
        from app.models.post import Post
        from app.models.analysis_result import AnalysisResult
        from datetime import datetime
        
        # Get analysis
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return {"status": "error", "message": "Analysis not found"}
        
        # Update status to processing
        analysis.status = AnalysisStatus.PROCESSING
        analysis.started_at = datetime.utcnow()
        analysis.progress = 0.0
        db.commit()
        
        # Get posts based on filters
        query = db.query(Post)
        
        filters = analysis.query_filters or {}
        if filters.get("platform"):
            query = query.filter(Post.platform == filters["platform"])
        if filters.get("language"):
            query = query.filter(Post.language == filters["language"])
        if filters.get("data_source_id"):
            query = query.filter(Post.data_source_id == filters["data_source_id"])
        
        limit = analysis.post_count or 1000
        posts = query.limit(limit).all()
        
        if not posts:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "No posts found matching filters"
            db.commit()
            return {"status": "error", "message": "No posts found"}
        
        # Update progress
        self.update_state(state="PROGRESS", meta={"progress": 10})
        analysis.progress = 10.0
        db.commit()
        
        # Prepare posts data for BRAIN
        texts = [p.content or "" for p in posts]
        text_ids = [str(p.id) for p in posts]
        
        # Call BRAIN service synchronously
        try:
            analysis_config = config or {
                "sentiment_enabled": True,
                "emotion_enabled": True,
                "keyword_extraction_enabled": True,
            }
            
            request_data = {
                "texts": texts,
                "text_ids": text_ids,
                "analysis_types": ["sentiment", "emotion", "keywords"],
                "language": "fa",
                "config": analysis_config
            }
            
            result = call_brain_sync("/analyze/text", request_data)
            results = result.get("results", [])
            
            # Update progress
            self.update_state(state="PROGRESS", meta={"progress": 50})
            analysis.progress = 50.0
            db.commit()
            
            # Store results
            for i, res in enumerate(results):
                post_id = int(res.get("text_id", i))
                
                sentiment = res.get("sentiment", {})
                emotions = res.get("emotions", {})
                
                analysis_result = AnalysisResult(
                    post_id=post_id,
                    analysis_id=analysis_id,
                    sentiment_label=sentiment.get("label"),
                    sentiment_score=sentiment.get("score"),
                    sentiment_confidence=sentiment.get("confidence"),
                    emotions=emotions,
                    dominant_emotion=res.get("dominant_emotion") or (max(emotions, key=emotions.get) if emotions else None),
                    keywords=res.get("keywords"),
                    entities=res.get("entities"),
                    summary=res.get("summary"),
                    raw_results=res
                )
                db.add(analysis_result)
                
                # Mark post as processed
                post = db.query(Post).filter(Post.id == post_id).first()
                if post:
                    post.is_processed = True
                
                # Update progress periodically
                if i % 100 == 0:
                    progress = 50 + (i / len(results)) * 40
                    self.update_state(state="PROGRESS", meta={"progress": progress})
                    analysis.progress = progress
                    db.commit()
            
            db.commit()
            
            # Generate summary
            summary = generate_analysis_summary(db, analysis_id)
            
            # Complete analysis
            analysis.status = AnalysisStatus.COMPLETED
            analysis.progress = 100.0
            analysis.completed_at = datetime.utcnow()
            analysis.summary = summary
            db.commit()
            
            logger.info(f"Analysis {analysis_id} completed successfully")
            return {
                "status": "completed",
                "analysis_id": analysis_id,
                "results_count": len(results)
            }
            
        except Exception as e:
            logger.error(f"BRAIN service error: {str(e)}")
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = f"BRAIN service error: {str(e)}"
            db.commit()
            return {"status": "error", "message": str(e)}
        
    except Exception as e:
        logger.error(f"Analysis task error: {str(e)}")
        try:
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = AnalysisStatus.FAILED
                analysis.error_message = str(e)
                db.commit()
        except Exception:
            pass
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


def generate_analysis_summary(db: Session, analysis_id: int) -> Dict[str, Any]:
    """Generate summary for completed analysis."""
    from app.models.analysis_result import AnalysisResult
    from sqlalchemy import func
    
    # Count results
    total = db.query(func.count(AnalysisResult.id)).filter(
        AnalysisResult.analysis_id == analysis_id
    ).scalar() or 0
    
    # Sentiment distribution
    sentiment_query = db.query(
        AnalysisResult.sentiment_label,
        func.count(AnalysisResult.id)
    ).filter(
        AnalysisResult.analysis_id == analysis_id,
        AnalysisResult.sentiment_label.isnot(None)
    ).group_by(AnalysisResult.sentiment_label).all()
    
    sentiment_dist = {row[0]: row[1] for row in sentiment_query}
    
    # Emotion distribution
    emotion_query = db.query(
        AnalysisResult.dominant_emotion,
        func.count(AnalysisResult.id)
    ).filter(
        AnalysisResult.analysis_id == analysis_id,
        AnalysisResult.dominant_emotion.isnot(None)
    ).group_by(AnalysisResult.dominant_emotion).all()
    
    emotion_dist = {row[0]: row[1] for row in emotion_query}
    
    # Average sentiment
    avg_sentiment = db.query(func.avg(AnalysisResult.sentiment_score)).filter(
        AnalysisResult.analysis_id == analysis_id
    ).scalar()
    
    # Top keywords
    results = db.query(AnalysisResult.keywords).filter(
        AnalysisResult.analysis_id == analysis_id,
        AnalysisResult.keywords.isnot(None)
    ).all()
    
    keyword_counts = {}
    for row in results:
        for kw in (row[0] or []):
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
    
    top_keywords = sorted(
        keyword_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]
    
    return {
        "total_posts": total,
        "sentiment_distribution": sentiment_dist,
        "emotion_distribution": emotion_dist,
        "average_sentiment_score": float(avg_sentiment) if avg_sentiment else None,
        "top_keywords": [{"keyword": k, "count": v} for k, v in top_keywords]
    }


@celery_app.task(bind=True, name="app.services.tasks.detect_trends")
def detect_trends(
    self,
    hours: int = 24,
    min_count: int = 10
) -> Dict[str, Any]:
    """Detect trends from recent posts."""
    logger.info(f"Starting trend detection for last {hours} hours")
    
    db = get_sync_db()
    
    try:
        from app.models.post import Post
        from app.models.trend import Trend
        from datetime import datetime, timedelta
        
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Get recent posts
        posts = db.query(Post).filter(
            Post.posted_at >= since
        ).limit(10000).all()
        
        if not posts:
            return {"status": "no_posts", "trends": 0}
        
        # Count hashtags
        hashtag_counts = {}
        for post in posts:
            if post.hashtags:
                for tag in post.hashtags:
                    hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
        
        # Filter trending
        trending = [
            (tag, count) for tag, count in hashtag_counts.items()
            if count >= min_count
        ]
        trending.sort(key=lambda x: x[1], reverse=True)
        
        # Create trends
        created = 0
        for tag, count in trending[:50]:
            existing = db.query(Trend).filter(
                Trend.name == f"#{tag}",
                Trend.is_active == "active"
            ).first()
            
            if existing:
                existing.volume = count
                existing.updated_at = datetime.utcnow()
            else:
                trend = Trend(
                    name=f"#{tag}",
                    description=f"Trending hashtag with {count} mentions",
                    volume=count,
                    hashtags=[tag],
                    is_active="active"
                )
                db.add(trend)
                created += 1
        
        db.commit()
        
        logger.info(f"Trend detection completed: {created} new trends")
        return {"status": "completed", "new_trends": created}
        
    except Exception as e:
        logger.error(f"Trend detection error: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.detect_trends_periodic")
def detect_trends_periodic():
    """Periodic task to detect trends."""
    return detect_trends.delay(hours=24, min_count=10)


@celery_app.task(name="app.services.tasks.update_trend_status_periodic")
def update_trend_status_periodic():
    """Periodic task to update trend status."""
    logger.info("Updating trend statuses")
    
    db = get_sync_db()
    
    try:
        from app.models.trend import Trend
        from app.models.post import Post
        from datetime import datetime, timedelta
        
        since = datetime.utcnow() - timedelta(hours=6)
        
        active_trends = db.query(Trend).filter(
            Trend.is_active == "active"
        ).all()
        
        updated = 0
        for trend in active_trends:
            if trend.hashtags:
                recent_count = 0
                for hashtag in trend.hashtags:
                    count = db.query(Post).filter(
                        Post.posted_at >= since,
                        Post.hashtags.contains([hashtag])
                    ).count()
                    recent_count += count
                
                if recent_count < trend.volume * 0.1:
                    trend.is_active = "ended"
                    updated += 1
                elif recent_count < trend.volume * 0.3:
                    trend.is_active = "declining"
                    updated += 1
        
        db.commit()
        logger.info(f"Updated {updated} trend statuses")
        return {"updated": updated}
        
    except Exception as e:
        logger.error(f"Trend status update error: {str(e)}")
        return {"error": str(e)}
    
    finally:
        db.close()


@celery_app.task(bind=True, name="app.services.tasks.build_graph")
def build_graph(
    self,
    graph_type: str = "author_network"
) -> Dict[str, Any]:
    """Build graph from posts."""
    logger.info(f"Building {graph_type} graph")
    
    db = get_sync_db()
    
    try:
        from app.models.post import Post
        from app.models.graph import GraphNode, GraphEdge
        
        nodes_created = 0
        edges_created = 0
        
        posts = db.query(Post).filter(
            Post.mentions.isnot(None)
        ).limit(10000).all()
        
        for post in posts:
            if not post.author_id or not post.mentions:
                continue
            
            # Create or get source node
            source_node_id = f"author_{post.author_id}"
            source = db.query(GraphNode).filter(
                GraphNode.node_id == source_node_id
            ).first()
            
            if not source:
                source = GraphNode(
                    node_id=source_node_id,
                    node_type="author",
                    label=str(post.author_id)
                )
                db.add(source)
                db.flush()
                nodes_created += 1
            
            # Process mentions
            for mention in post.mentions:
                target_node_id = f"mention_{mention}"
                target = db.query(GraphNode).filter(
                    GraphNode.node_id == target_node_id
                ).first()
                
                if not target:
                    target = GraphNode(
                        node_id=target_node_id,
                        node_type="mention",
                        label=mention
                    )
                    db.add(target)
                    db.flush()
                    nodes_created += 1
                
                # Create edge
                edge = db.query(GraphEdge).filter(
                    GraphEdge.source_id == source.id,
                    GraphEdge.target_id == target.id,
                    GraphEdge.edge_type == "mentions"
                ).first()
                
                if edge:
                    edge.occurrence_count += 1
                    edge.weight += 1.0
                else:
                    edge = GraphEdge(
                        edge_type="mentions",
                        source_id=source.id,
                        target_id=target.id,
                        weight=1.0,
                        occurrence_count=1
                    )
                    db.add(edge)
                    edges_created += 1
        
        db.commit()
        
        logger.info(f"Graph built: {nodes_created} nodes, {edges_created} edges")
        return {
            "status": "completed",
            "nodes_created": nodes_created,
            "edges_created": edges_created
        }
        
    except Exception as e:
        logger.error(f"Graph building error: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.cleanup_old_results")
def cleanup_old_results():
    """Clean up old analysis results."""
    logger.info("Starting cleanup of old results")
    
    db = get_sync_db()
    
    try:
        from app.models.analysis_result import AnalysisResult
        from datetime import datetime, timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=30)
        
        deleted = db.query(AnalysisResult).filter(
            AnalysisResult.created_at < cutoff
        ).delete()
        
        db.commit()
        
        logger.info(f"Cleaned up {deleted} old results")
        return {"deleted": deleted}
        
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return {"error": str(e)}
    
    finally:
        db.close()


@celery_app.task(bind=True, name="app.services.tasks.calculate_pagerank")
def calculate_pagerank(self) -> Dict[str, Any]:
    """Calculate PageRank for graph nodes."""
    logger.info("Calculating PageRank")
    
    db = get_sync_db()
    
    try:
        from app.models.graph import GraphNode, GraphEdge
        
        nodes = db.query(GraphNode).all()
        edges = db.query(GraphEdge).all()
        
        if not nodes or not edges:
            return {"status": "no_data"}
        
        # Prepare data for BRAIN
        nodes_data = [{"id": n.node_id, "type": n.node_type} for n in nodes]
        edges_data = []
        
        for e in edges:
            source = db.query(GraphNode).get(e.source_id)
            target = db.query(GraphNode).get(e.target_id)
            if source and target:
                edges_data.append({
                    "source": source.node_id,
                    "target": target.node_id,
                    "weight": e.weight
                })
        
        # Call BRAIN service synchronously
        request_data = {
            "nodes": nodes_data,
            "edges": edges_data,
            "damping": 0.85
        }
        
        result = call_brain_sync("/analyze/graph/pagerank", request_data)
        pagerank_results = result.get("nodes", [])
        
        # Update nodes
        updated = 0
        for pr in pagerank_results:
            node = db.query(GraphNode).filter(
                GraphNode.node_id == pr["id"]
            ).first()
            if node:
                node.pagerank = pr.get("pagerank", 0)
                updated += 1
        
        db.commit()
        
        logger.info(f"PageRank calculated for {updated} nodes")
        return {"status": "completed", "updated": updated}
        
    except Exception as e:
        logger.error(f"PageRank calculation error: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
