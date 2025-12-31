import re
from typing import Optional


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_username(username: str) -> bool:
    """
    Validate username format.
    - 3-50 characters
    - Letters, numbers, underscore, hyphen
    - Must start with letter
    """
    if not username:
        return False
    
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]{2,49}$'
    return bool(re.match(pattern, username))


def is_valid_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    Returns (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 100:
        return False, "Password must be at most 100 characters"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, None


def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    if not url:
        return False
    
    pattern = r'^https?://[^\s<>"{}|\\^`\[\]]+'
    return bool(re.match(pattern, url))


def is_valid_platform_id(platform_id: str) -> bool:
    """Validate platform ID format."""
    if not platform_id:
        return False
    
    # Most platform IDs are alphanumeric with some special chars
    pattern = r'^[a-zA-Z0-9_-]{1,255}$'
    return bool(re.match(pattern, platform_id))


def sanitize_string(
    text: str,
    max_length: Optional[int] = None,
    strip: bool = True
) -> str:
    """Sanitize string input."""
    if not text:
        return ""
    
    if strip:
        text = text.strip()
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    if max_length:
        text = text[:max_length]
    
    return text


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    if not filename:
        return ""
    
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # Remove other dangerous characters
    filename = re.sub(r'[<>:"|?*]', '_', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    return filename[:255] if filename else "unnamed"


def validate_json_field(
    data: dict,
    required_fields: list,
    optional_fields: Optional[list] = None
) -> tuple[bool, Optional[str]]:
    """
    Validate JSON/dict has required fields.
    Returns (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    return True, None
