"""
Caching utilities using Redis.
"""
import json
import pickle
from typing import Any, Optional, Union
import redis
import structlog
from datetime import timedelta
from app.config import settings

logger = structlog.get_logger()

class CacheManager:
    """Redis-based cache manager."""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=False)
        self.default_ttl = 3600  # 1 hour default TTL
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            
            # Try to deserialize as JSON first, then pickle
            try:
                return json.loads(value.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return pickle.loads(value)
                
        except Exception as e:
            logger.error(f"Cache get failed for key {key}: {e}")
            return None
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None,
        serialize_json: bool = True
    ) -> bool:
        """Set value in cache."""
        try:
            ttl = ttl or self.default_ttl
            
            if serialize_json:
                try:
                    serialized_value = json.dumps(value).encode('utf-8')
                except (TypeError, ValueError):
                    # Fall back to pickle for non-JSON serializable objects
                    serialized_value = pickle.dumps(value)
                    serialize_json = False
            else:
                serialized_value = pickle.dumps(value)
            
            return self.redis_client.setex(key, ttl, serialized_value)
            
        except Exception as e:
            logger.error(f"Cache set failed for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Cache delete failed for key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Cache exists check failed for key {key}: {e}")
            return False
    
    def get_or_set(
        self, 
        key: str, 
        func, 
        ttl: Optional[int] = None,
        *args, 
        **kwargs
    ) -> Any:
        """Get value from cache or set it using function."""
        value = self.get(key)
        if value is not None:
            return value
        
        # Generate new value
        new_value = func(*args, **kwargs)
        self.set(key, new_value, ttl)
        return new_value
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache pattern invalidation failed for {pattern}: {e}")
            return 0
    
    def get_ttl(self, key: str) -> int:
        """Get TTL for key."""
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            logger.error(f"Cache TTL check failed for key {key}: {e}")
            return -1

# Global cache manager instance
cache_manager = CacheManager()

def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments."""
    key_parts = []
    
    for arg in args:
        if isinstance(arg, (str, int, float)):
            key_parts.append(str(arg))
        else:
            key_parts.append(str(hash(str(arg))))
    
    for k, v in sorted(kwargs.items()):
        if isinstance(v, (str, int, float)):
            key_parts.append(f"{k}={v}")
        else:
            key_parts.append(f"{k}={hash(str(v))}")
    
    return ":".join(key_parts)

def cached(ttl: int = 3600, key_func: Optional[callable] = None):
    """Decorator for caching function results."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key_str = key_func(*args, **kwargs)
            else:
                cache_key_str = cache_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key_str)
            if cached_result is not None:
                logger.debug(f"Cache hit for {cache_key_str}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for {cache_key_str}")
            result = func(*args, **kwargs)
            cache_manager.set(cache_key_str, result, ttl)
            
            return result
        
        return wrapper
    return decorator

