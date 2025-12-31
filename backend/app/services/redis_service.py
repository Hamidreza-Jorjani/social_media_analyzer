from typing import Optional, Any, List
import json
import redis.asyncio as redis
from app.core.config import settings
from app.services.base import BaseService


class RedisService(BaseService):
    """Service for Redis cache operations."""
    
    def __init__(self):
        super().__init__("RedisService")
        self._client: Optional[redis.Redis] = None
    
    async def connect(self) -> None:
        """Connect to Redis."""
        if not self._client:
            self._client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self._client.ping()
            self.log_info("Connected to Redis")
    
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()
            self._client = None
            self.log_info("Disconnected from Redis")
    
    @property
    def client(self) -> redis.Redis:
        """Get Redis client."""
        if not self._client:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._client
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        try:
            return await self.client.get(key)
        except Exception as e:
            self.log_error(f"Redis GET error: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: str,
        expire: Optional[int] = None
    ) -> bool:
        """Set value with optional expiration (seconds)."""
        try:
            if expire:
                await self.client.setex(key, expire, value)
            else:
                await self.client.set(key, value)
            return True
        except Exception as e:
            self.log_error(f"Redis SET error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key."""
        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            self.log_error(f"Redis DELETE error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            self.log_error(f"Redis EXISTS error: {e}")
            return False
    
    async def get_json(self, key: str) -> Optional[Any]:
        """Get JSON value by key."""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None
    
    async def set_json(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """Set JSON value."""
        try:
            json_str = json.dumps(value, default=str)
            return await self.set(key, json_str, expire)
        except Exception as e:
            self.log_error(f"Redis SET JSON error: {e}")
            return False
    
    async def incr(self, key: str) -> int:
        """Increment integer value."""
        try:
            return await self.client.incr(key)
        except Exception as e:
            self.log_error(f"Redis INCR error: {e}")
            return 0
    
    async def lpush(self, key: str, *values: str) -> int:
        """Push values to list."""
        try:
            return await self.client.lpush(key, *values)
        except Exception as e:
            self.log_error(f"Redis LPUSH error: {e}")
            return 0
    
    async def lrange(
        self,
        key: str,
        start: int = 0,
        end: int = -1
    ) -> List[str]:
        """Get list range."""
        try:
            return await self.client.lrange(key, start, end)
        except Exception as e:
            self.log_error(f"Redis LRANGE error: {e}")
            return []
    
    async def publish(self, channel: str, message: str) -> int:
        """Publish message to channel."""
        try:
            return await self.client.publish(channel, message)
        except Exception as e:
            self.log_error(f"Redis PUBLISH error: {e}")
            return 0
    
    async def cache_analysis_result(
        self,
        analysis_id: int,
        result: dict,
        expire: int = 3600
    ) -> bool:
        """Cache analysis result."""
        key = f"analysis:{analysis_id}:result"
        return await self.set_json(key, result, expire)
    
    async def get_cached_analysis_result(
        self,
        analysis_id: int
    ) -> Optional[dict]:
        """Get cached analysis result."""
        key = f"analysis:{analysis_id}:result"
        return await self.get_json(key)
    
    async def set_analysis_progress(
        self,
        analysis_id: int,
        progress: float,
        status: str
    ) -> bool:
        """Set analysis progress in cache."""
        key = f"analysis:{analysis_id}:progress"
        data = {"progress": progress, "status": status}
        return await self.set_json(key, data, expire=3600)
    
    async def get_analysis_progress(
        self,
        analysis_id: int
    ) -> Optional[dict]:
        """Get analysis progress from cache."""
        key = f"analysis:{analysis_id}:progress"
        return await self.get_json(key)


# Create singleton instance
redis_service = RedisService()
