"""Timing metrics collection for AI coding assistants."""

import json
import threading
import time
from dataclasses import asdict, dataclass
from functools import wraps
from pathlib import Path


@dataclass
class TimingContext:
    """Context for timing a function execution."""
    function_name: str
    start_time: float
    ai_assisted: bool = False
    iterations: int = 0
    success: bool = False


class MetricsCollector:
    """Collects timing metrics for AI-assisted and manual coding tasks."""
    
    def __init__(self, storage_path: Path = None):
        self.storage_path = storage_path or Path.home() / '.ai_metrics'
        self.storage_path.mkdir(exist_ok=True)
        self._local = threading.local()
        
    def track_function(self, ai_assisted: bool = False):
        """Decorator to track function execution time and success."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                context = TimingContext(
                    function_name=func.__name__,
                    start_time=time.perf_counter(),
                    ai_assisted=ai_assisted
                )
                
                try:
                    result = func(*args, **kwargs)
                    context.success = True
                    return result
                except Exception:
                    context.success = False
                    raise
                finally:
                    end_time = time.perf_counter()
                    self._store_timing_metric(context, end_time)
            
            return wrapper
        return decorator
    
    def _store_timing_metric(self, context: TimingContext, end_time: float):
        """Store timing metrics to a file."""
        metric = {
            **asdict(context),
            'duration': end_time - context.start_time,
            'timestamp': time.time()
        }
        
        # Append to daily file
        date_str = time.strftime('%Y-%m-%d')
        metrics_file = self.storage_path / f'timing_{date_str}.jsonl'
        
        with open(metrics_file, 'a') as f:
            json.dump(metric, f)
            f.write('\n')