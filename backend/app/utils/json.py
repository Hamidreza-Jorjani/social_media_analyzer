import json
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Optional
from enum import Enum
import orjson


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for special types."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)


def json_dumps(obj: Any, pretty: bool = False) -> str:
    """Serialize object to JSON string."""
    if pretty:
        return json.dumps(obj, cls=CustomJSONEncoder, indent=2, ensure_ascii=False)
    return json.dumps(obj, cls=CustomJSONEncoder, ensure_ascii=False)


def json_loads(text: str) -> Any:
    """Deserialize JSON string to object."""
    return json.loads(text)


def orjson_dumps(obj: Any) -> bytes:
    """Fast JSON serialization using orjson."""
    return orjson.dumps(
        obj,
        option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_UTC_Z
    )


def orjson_loads(data: bytes | str) -> Any:
    """Fast JSON deserialization using orjson."""
    return orjson.loads(data)


def safe_json_loads(text: str, default: Any = None) -> Any:
    """Safely parse JSON, returning default on error."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def merge_json(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries."""
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_json(result[key], value)
        else:
            result[key] = value
    
    return result


def flatten_json(nested: dict, separator: str = '.') -> dict:
    """Flatten nested dictionary."""
    result = {}
    
    def _flatten(obj: Any, prefix: str = ''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{prefix}{separator}{key}" if prefix else key
                _flatten(value, new_key)
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                new_key = f"{prefix}{separator}{i}" if prefix else str(i)
                _flatten(value, new_key)
        else:
            result[prefix] = obj
    
    _flatten(nested)
    return result


def unflatten_json(flat: dict, separator: str = '.') -> dict:
    """Unflatten dictionary back to nested structure."""
    result = {}
    
    for key, value in flat.items():
        keys = key.split(separator)
        current = result
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    return result
