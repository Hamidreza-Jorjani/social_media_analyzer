import hashlib
import secrets
import string
from typing import Optional


def generate_random_string(length: int = 32) -> str:
    """Generate a random alphanumeric string."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_api_key() -> str:
    """Generate an API key."""
    return f"psa_{generate_random_string(32)}"


def generate_secret_key() -> str:
    """Generate a secret key for JWT or other purposes."""
    return secrets.token_urlsafe(64)


def hash_string(text: str, algorithm: str = 'sha256') -> str:
    """Hash a string using specified algorithm."""
    if algorithm == 'sha256':
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(text.encode()).hexdigest()
    elif algorithm == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def verify_hash(text: str, hash_value: str, algorithm: str = 'sha256') -> bool:
    """Verify a string against its hash."""
    return hash_string(text, algorithm) == hash_value


def mask_email(email: str) -> str:
    """Mask email for privacy."""
    if not email or '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    
    if len(local) <= 2:
        masked_local = '*' * len(local)
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"


def mask_string(text: str, visible_start: int = 2, visible_end: int = 2) -> str:
    """Mask a string showing only start and end characters."""
    if not text:
        return text
    
    if len(text) <= visible_start + visible_end:
        return '*' * len(text)
    
    return text[:visible_start] + '*' * (len(text) - visible_start - visible_end) + text[-visible_end:]


def generate_token(prefix: Optional[str] = None) -> str:
    """Generate a secure token with optional prefix."""
    token = secrets.token_urlsafe(32)
    if prefix:
        return f"{prefix}_{token}"
    return token
