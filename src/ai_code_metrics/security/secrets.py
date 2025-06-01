"""Secure configuration handling for API keys and sensitive data."""

import json
import os
from pathlib import Path

from cryptography.fernet import Fernet


class SecureConfig:
    """Securely manage API keys and configuration data."""
    
    def __init__(self):
        self.key_file = Path.home() / '.ai_metrics' / '.key'
        self.config_file = Path.home() / '.ai_metrics' / '.config'
        self._ensure_key()
        
    def _ensure_key(self):
        """Ensure encryption key exists."""
        if not self.key_file.exists():
            self.key_file.parent.mkdir(exist_ok=True)
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            self.key_file.chmod(0o600)  # Read/write for owner only
    
    def _load_config(self):
        """Load configuration from file."""
        if not self.config_file.exists():
            return {}
            
        try:
            return json.loads(self.config_file.read_text())
        except Exception:
            return {}
    
    def _save_config(self, config):
        """Save configuration to file."""
        self.config_file.write_text(json.dumps(config, indent=2))
        self.config_file.chmod(0o600)  # Read/write for owner only
        
    def set_api_key(self, provider: str, key: str):
        """Securely store API key."""
        cipher = Fernet(self.key_file.read_bytes())
        encrypted = cipher.encrypt(key.encode())
        
        # Store in environment variable as backup
        os.environ[f"{provider.upper()}_API_KEY"] = key
        
        # Store encrypted version
        config = self._load_config()
        config[provider] = encrypted.decode()
        self._save_config(config)
    
    def get_api_key(self, provider: str) -> str:
        """Retrieve API key securely."""
        # Try environment variable first
        env_key = os.environ.get(f"{provider.upper()}_API_KEY")
        if env_key:
            return env_key
        
        # Fall back to encrypted storage
        config = self._load_config()
        if provider in config:
            cipher = Fernet(self.key_file.read_bytes())
            return cipher.decrypt(config[provider].encode()).decode()
        
        raise ValueError(f"No API key found for {provider}")