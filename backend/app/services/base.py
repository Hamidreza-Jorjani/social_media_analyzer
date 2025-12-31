from typing import Optional, Any, Dict
from loguru import logger


class BaseService:
    """Base service class with common functionality."""
    
    def __init__(self, name: str = "BaseService"):
        self.name = name
        self.logger = logger.bind(service=name)
    
    def log_info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def log_error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def log_warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def log_debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
