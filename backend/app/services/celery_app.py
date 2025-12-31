from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "persian_analytics",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.services.tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution settings
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3300,  # 55 minutes soft limit
    
    # Result settings
    result_expires=86400,  # Results expire after 24 hours
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
    
    # Task routing
    task_routes={
        "app.services.tasks.process_analysis": {"queue": "analysis"},
        "app.services.tasks.detect_trends": {"queue": "trends"},
        "app.services.tasks.build_graph": {"queue": "graph"},
    },
    
    # Beat schedule for periodic tasks
    beat_schedule={
        "detect-trends-hourly": {
            "task": "app.services.tasks.detect_trends_periodic",
            "schedule": 3600.0,  # Every hour
        },
        "update-trend-status": {
            "task": "app.services.tasks.update_trend_status_periodic",
            "schedule": 1800.0,  # Every 30 minutes
        },
        "cleanup-old-results": {
            "task": "app.services.tasks.cleanup_old_results",
            "schedule": 86400.0,  # Every 24 hours
        },
    },
)


# Optional: Configure task queues
celery_app.conf.task_queues = {
    "default": {
        "exchange": "default",
        "routing_key": "default",
    },
    "analysis": {
        "exchange": "analysis",
        "routing_key": "analysis",
    },
    "trends": {
        "exchange": "trends",
        "routing_key": "trends",
    },
    "graph": {
        "exchange": "graph",
        "routing_key": "graph",
    },
}
