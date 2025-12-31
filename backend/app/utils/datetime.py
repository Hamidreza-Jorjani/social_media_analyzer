from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import re


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    """Convert datetime to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_datetime(
    dt: Optional[datetime],
    fmt: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[str]:
    """Format datetime to string."""
    if dt is None:
        return None
    return dt.strftime(fmt)


def parse_datetime(
    dt_str: str,
    fmt: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[datetime]:
    """Parse string to datetime."""
    try:
        return datetime.strptime(dt_str, fmt)
    except (ValueError, TypeError):
        return None


def parse_iso_datetime(dt_str: str) -> Optional[datetime]:
    """Parse ISO format datetime string."""
    try:
        # Handle various ISO formats
        dt_str = dt_str.replace('Z', '+00:00')
        return datetime.fromisoformat(dt_str)
    except (ValueError, TypeError):
        return None


def datetime_to_iso(dt: Optional[datetime]) -> Optional[str]:
    """Convert datetime to ISO format string."""
    if dt is None:
        return None
    return dt.isoformat()


def time_ago(dt: datetime) -> str:
    """Get human-readable time ago string."""
    now = utc_now()
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    diff = now - dt
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years > 1 else ''} ago"


def get_date_range(
    range_type: str,
    reference: Optional[datetime] = None
) -> tuple[datetime, datetime]:
    """
    Get date range based on type.
    Types: today, yesterday, this_week, last_week, this_month, last_month, last_7_days, last_30_days
    """
    if reference is None:
        reference = utc_now()
    
    reference = reference.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if range_type == "today":
        start = reference
        end = reference + timedelta(days=1)
    
    elif range_type == "yesterday":
        start = reference - timedelta(days=1)
        end = reference
    
    elif range_type == "this_week":
        start = reference - timedelta(days=reference.weekday())
        end = start + timedelta(days=7)
    
    elif range_type == "last_week":
        end = reference - timedelta(days=reference.weekday())
        start = end - timedelta(days=7)
    
    elif range_type == "this_month":
        start = reference.replace(day=1)
        if reference.month == 12:
            end = reference.replace(year=reference.year + 1, month=1, day=1)
        else:
            end = reference.replace(month=reference.month + 1, day=1)
    
    elif range_type == "last_month":
        end = reference.replace(day=1)
        start = (end - timedelta(days=1)).replace(day=1)
    
    elif range_type == "last_7_days":
        end = utc_now()
        start = end - timedelta(days=7)
    
    elif range_type == "last_30_days":
        end = utc_now()
        start = end - timedelta(days=30)
    
    elif range_type == "last_90_days":
        end = utc_now()
        start = end - timedelta(days=90)
    
    else:
        raise ValueError(f"Unknown range type: {range_type}")
    
    return start, end


def get_time_buckets(
    start: datetime,
    end: datetime,
    interval: str = "1h"
) -> list[datetime]:
    """
    Generate time buckets between start and end.
    Intervals: 1h, 6h, 12h, 1d
    """
    buckets = []
    current = start
    
    interval_map = {
        "1h": timedelta(hours=1),
        "6h": timedelta(hours=6),
        "12h": timedelta(hours=12),
        "1d": timedelta(days=1),
    }
    
    delta = interval_map.get(interval, timedelta(hours=1))
    
    while current < end:
        buckets.append(current)
        current += delta
    
    return buckets


def parse_duration(duration_str: str) -> Optional[timedelta]:
    """
    Parse duration string to timedelta.
    Examples: "1h", "30m", "2d", "1w"
    """
    pattern = r'^(\d+)([mhdw])$'
    match = re.match(pattern, duration_str.lower())
    
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)
    
    unit_map = {
        'm': timedelta(minutes=value),
        'h': timedelta(hours=value),
        'd': timedelta(days=value),
        'w': timedelta(weeks=value),
    }
    
    return unit_map.get(unit)
