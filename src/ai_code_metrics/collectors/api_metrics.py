"""API usage tracking for AI coding assistants."""

import json
import time
from functools import wraps
from typing import Any

import tiktoken

from ai_code_metrics.config import config


class APIUsageTracker:
    """Tracks API usage and costs for AI coding assistants."""
    
    def __init__(self):
        self.usage_log = []
        self.metrics_path = config.get_metrics_path()
        self.metrics_path.mkdir(exist_ok=True)
    
    def track_api_call(self, model: str, provider: str = 'anthropic'):
        """Decorator to track API calls, estimate token usage and calculate costs."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                # Estimate input tokens from request
                request_text = str(kwargs.get('messages', []))
                estimated_tokens = self._estimate_tokens(request_text, model)
                
                # Make API call
                response = func(*args, **kwargs)
                
                # Calculate actual usage and cost
                usage_data = self._extract_usage(response, provider)
                cost = self._calculate_cost(model, usage_data)
                
                # Log metrics
                self._log_usage({
                    'timestamp': time.time(),
                    'model': model,
                    'provider': provider,
                    'input_tokens': usage_data.get('input_tokens', estimated_tokens),
                    'output_tokens': usage_data.get('output_tokens', 0),
                    'total_cost': cost,
                    'duration': time.time() - start_time,
                    'function': func.__name__
                })
                
                return response
            return wrapper
        return decorator
    
    def _estimate_tokens(self, text: str, model: str) -> int:
        """Estimate token count for a given text and model."""
        try:
            if model.startswith('claude'):
                encoding = tiktoken.encoding_for_model('cl100k_base')  # Claude models
            else:
                encoding = tiktoken.encoding_for_model(model)  # OpenAI models
                
            return len(encoding.encode(text))
        except Exception:
            # Rough estimate: 4 chars = 1 token
            return len(text) // 4
    
    def _extract_usage(self, response: Any, provider: str) -> dict[str, int]:
        """Extract token usage from API response."""
        if provider == 'anthropic':
            # Extract from Claude response format
            return {
                'input_tokens': getattr(response, 'usage', {}).get('input_tokens', 0),
                'output_tokens': getattr(response, 'usage', {}).get('output_tokens', 0)
            }
        elif provider == 'openai':
            # Extract from OpenAI response format
            usage = response.get('usage', {})
            return {
                'input_tokens': usage.get('prompt_tokens', 0),
                'output_tokens': usage.get('completion_tokens', 0)
            }
        return {}
    
    def _calculate_cost(self, model: str, usage: dict[str, int]) -> float:
        """Calculate cost based on token usage and model pricing."""
        pricing = config.get(f"models.{model}")
        if not pricing:
            return 0.0
        
        input_cost = (usage.get('input_tokens', 0) / 1_000_000) * pricing['input']
        output_cost = (usage.get('output_tokens', 0) / 1_000_000) * pricing['output']
        
        return round(input_cost + output_cost, 4)
    
    def _log_usage(self, data: dict[str, Any]):
        """Log API usage data."""
        self.usage_log.append(data)
        
        # Also persist to file
        date_str = time.strftime('%Y-%m-%d')
        metrics_file = self.metrics_path / f'api_usage_{date_str}.jsonl'
        
        with open(metrics_file, 'a') as f:
            json.dump(data, f)
            f.write('\n')