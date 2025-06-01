"""Code anonymization utilities for privacy protection."""

import hashlib
import re


class CodeAnonymizer:
    """Anonymizes code snippets for privacy protection."""
    
    def __init__(self, salt: str = "your-secret-salt"):
        self.salt = salt
        self.replacements = {}
        
    def anonymize_code_snippet(self, code: str) -> str:
        """Anonymize variable and function names in code."""
        # Replace variable names
        code = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', 
                     lambda m: self._get_replacement(m.group(1)), 
                     code)
        return code
    
    def _get_replacement(self, identifier: str) -> str:
        """Get consistent replacement for an identifier."""
        # Keep common keywords
        if identifier in ['def', 'class', 'import', 'from', 'return', 
                         'if', 'else', 'for', 'while', 'try', 'except',
                         'and', 'or', 'not', 'is', 'in', 'as', 'with',
                         'True', 'False', 'None', 'self', 'super', 'pass',
                         'break', 'continue', 'raise', 'assert', 'lambda']:
            return identifier
        
        # Get consistent hash-based replacement
        if identifier not in self.replacements:
            hash_val = hashlib.sha256(
                f"{identifier}{self.salt}".encode()
            ).hexdigest()[:8]
            self.replacements[identifier] = f"var_{hash_val}"
        
        return self.replacements[identifier]
        
    def anonymize_file_path(self, path: str) -> str:
        """Anonymize a file path."""
        parts = path.split('/')
        anonymized_parts = []
        
        for part in parts:
            if part and part[0] not in ('/', '.', '_'):
                anonymized_parts.append(self._get_replacement(part))
            else:
                anonymized_parts.append(part)
                
        return '/'.join(anonymized_parts)