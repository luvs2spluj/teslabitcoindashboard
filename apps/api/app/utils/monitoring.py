"""
Monitoring and observability utilities.
"""
import time
import functools
from typing import Any, Dict, Optional
import structlog
from datetime import datetime
import traceback

logger = structlog.get_logger()

class MetricsCollector:
    """Simple metrics collector."""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
    
    def increment(self, metric_name: str, value: float = 1.0, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric."""
        key = self._make_key(metric_name, tags)
        if key not in self.metrics:
            self.metrics[key] = {"type": "counter", "value": 0.0}
        self.metrics[key]["value"] += value
    
    def gauge(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Set a gauge metric."""
        key = self._make_key(metric_name, tags)
        self.metrics[key] = {"type": "gauge", "value": value}
    
    def histogram(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record a histogram value."""
        key = self._make_key(metric_name, tags)
        if key not in self.metrics:
            self.metrics[key] = {"type": "histogram", "values": []}
        self.metrics[key]["values"].append(value)
    
    def _make_key(self, metric_name: str, tags: Optional[Dict[str, str]]) -> str:
        """Make a unique key for the metric."""
        if not tags:
            return metric_name
        
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric_name}[{tag_str}]"
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        return {
            "metrics": self.metrics,
            "uptime_seconds": time.time() - self.start_time,
            "timestamp": datetime.now().isoformat()
        }

# Global metrics collector
metrics = MetricsCollector()

def monitor_performance(func_name: Optional[str] = None):
    """Decorator to monitor function performance."""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            name = func_name or func.__name__
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Record metrics
                metrics.histogram(f"{name}.duration", duration)
                metrics.increment(f"{name}.success")
                
                logger.info(f"Function {name} completed successfully", duration=duration)
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Record error metrics
                metrics.histogram(f"{name}.duration", duration)
                metrics.increment(f"{name}.error")
                
                logger.error(f"Function {name} failed", error=str(e), duration=duration)
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            name = func_name or func.__name__
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Record metrics
                metrics.histogram(f"{name}.duration", duration)
                metrics.increment(f"{name}.success")
                
                logger.info(f"Function {name} completed successfully", duration=duration)
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Record error metrics
                metrics.histogram(f"{name}.duration", duration)
                metrics.increment(f"{name}.error")
                
                logger.error(f"Function {name} failed", error=str(e), duration=duration)
                raise
        
        # Return appropriate wrapper based on function type
        if hasattr(func, '__code__') and func.__code__.co_flags & 0x80:  # CO_COROUTINE
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

class HealthChecker:
    """Health check utilities."""
    
    def __init__(self):
        self.checks = {}
    
    def add_check(self, name: str, check_func):
        """Add a health check function."""
        self.checks[name] = check_func
    
    async def run_checks(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        overall_healthy = True
        
        for name, check_func in self.checks.items():
            try:
                if hasattr(check_func, '__code__') and check_func.__code__.co_flags & 0x80:
                    # Async function
                    result = await check_func()
                else:
                    # Sync function
                    result = check_func()
                
                results[name] = {
                    "status": "healthy" if result else "unhealthy",
                    "details": result
                }
                
                if not result:
                    overall_healthy = False
                    
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
                overall_healthy = False
        
        return {
            "status": "healthy" if overall_healthy else "unhealthy",
            "checks": results,
            "timestamp": datetime.now().isoformat()
        }

# Global health checker
health_checker = HealthChecker()

def add_health_check(name: str):
    """Decorator to add a health check."""
    def decorator(func):
        health_checker.add_check(name, func)
        return func
    return decorator

