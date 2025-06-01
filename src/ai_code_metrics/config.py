"""Configuration handling for AI Code Metrics."""

import json
from pathlib import Path
from typing import Any


class Config:
    """Configuration manager for AI Code Metrics."""
    
    DEFAULT_CONFIG = {
        "metrics_storage_path": str(Path.home() / ".ai_metrics"),
        "prometheus": {
            "host": "0.0.0.0",
            "port": 8080
        },
        "models": {
            # Current pricing as of May 2024 - per 1M tokens
            "claude-4-sonnet": {"input": 3.0, "output": 15.0},
            "claude-3-opus": {"input": 15.0, "output": 75.0},
            "claude-3-sonnet": {"input": 3.0, "output": 15.0},
            "claude-3-haiku": {"input": 0.25, "output": 1.25},
            "gpt-4": {"input": 30.0, "output": 60.0},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5}
        },
        "roi": {
            "hourly_rate": 75.0,
            "improvement_factor": 0.3  # 30% improvement with AI
        },
        "security": {
            "anonymize": False,
            "salt": "change-this-salt"
        }
    }
    
    def __init__(self, config_path: Path | None = None):
        """Initialize configuration with optional custom path."""
        self.config_path = config_path or Path.home() / ".ai_metrics" / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> dict[str, Any]:
        """Load configuration from file or use defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    return self._merge_configs(self.DEFAULT_CONFIG, user_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: dict[str, Any], user: dict[str, Any]) -> dict[str, Any]:
        """Recursively merge user config with default config."""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
                
        return result
    
    def save_config(self, config: dict[str, Any]) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        # Support nested keys like "prometheus.port"
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save."""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the right nesting level
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated config
        self.save_config(self.config)
        
    def get_metrics_path(self) -> Path:
        """Get the metrics storage path."""
        return Path(self.get("metrics_storage_path", str(Path.home() / ".ai_metrics")))
    
    def update_model_pricing(self, model_data: dict[str, dict[str, float]]) -> None:
        """Update model pricing information."""
        current_models = self.get("models", {})
        current_models.update(model_data)
        self.set("models", current_models)


# Global config instance
config = Config()