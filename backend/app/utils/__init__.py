"""
Utility functions for Persian Social Analytics.
"""

from app.utils.text import (
    normalize_persian,
    remove_diacritics,
    extract_hashtags,
    extract_mentions,
    extract_urls,
    remove_urls,
    remove_mentions,
    remove_hashtags,
    remove_emojis,
    clean_text,
    remove_stop_words,
    is_persian,
    get_text_language,
    truncate_text,
    word_count,
    char_count,
    PERSIAN_STOP_WORDS,
)

from app.utils.datetime import (
    utc_now,
    to_utc,
    format_datetime,
    parse_datetime,
    parse_iso_datetime,
    datetime_to_iso,
    time_ago,
    get_date_range,
    get_time_buckets,
    parse_duration,
)

from app.utils.pagination import (
    PaginationMeta,
    PaginatedResult,
    paginate,
    get_pagination_params,
    paginate_list,
)

from app.utils.validators import (
    is_valid_email,
    is_valid_username,
    is_valid_password,
    is_valid_url,
    is_valid_platform_id,
    sanitize_string,
    sanitize_filename,
    validate_json_field,
)

from app.utils.security import (
    generate_random_string,
    generate_api_key,
    generate_secret_key,
    hash_string,
    verify_hash,
    mask_email,
    mask_string,
    generate_token,
)

from app.utils.json import (
    json_dumps,
    json_loads,
    orjson_dumps,
    orjson_loads,
    safe_json_loads,
    merge_json,
    flatten_json,
    unflatten_json,
)

__all__ = [
    # Text utilities
    "normalize_persian",
    "remove_diacritics",
    "extract_hashtags",
    "extract_mentions",
    "extract_urls",
    "remove_urls",
    "remove_mentions",
    "remove_hashtags",
    "remove_emojis",
    "clean_text",
    "remove_stop_words",
    "is_persian",
    "get_text_language",
    "truncate_text",
    "word_count",
    "char_count",
    "PERSIAN_STOP_WORDS",
    # DateTime utilities
    "utc_now",
    "to_utc",
    "format_datetime",
    "parse_datetime",
    "parse_iso_datetime",
    "datetime_to_iso",
    "time_ago",
    "get_date_range",
    "get_time_buckets",
    "parse_duration",
    # Pagination utilities
    "PaginationMeta",
    "PaginatedResult",
    "paginate",
    "get_pagination_params",
    "paginate_list",
    # Validators
    "is_valid_email",
    "is_valid_username",
    "is_valid_password",
    "is_valid_url",
    "is_valid_platform_id",
    "sanitize_string",
    "sanitize_filename",
    "validate_json_field",
    # Security
    "generate_random_string",
    "generate_api_key",
    "generate_secret_key",
    "hash_string",
    "verify_hash",
    "mask_email",
    "mask_string",
    "generate_token",
    # JSON
    "json_dumps",
    "json_loads",
    "orjson_dumps",
    "orjson_loads",
    "safe_json_loads",
    "merge_json",
    "flatten_json",
    "unflatten_json",
]
