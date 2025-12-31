import pytest
from datetime import datetime, timedelta, timezone

from app.utils.text import (
    normalize_persian,
    extract_hashtags,
    extract_mentions,
    extract_urls,
    clean_text,
    is_persian,
    get_text_language,
    truncate_text,
    word_count
)
from app.utils.datetime import (
    utc_now,
    format_datetime,
    parse_datetime,
    time_ago,
    get_date_range,
    parse_duration
)
from app.utils.validators import (
    is_valid_email,
    is_valid_username,
    is_valid_password,
    is_valid_url
)
from app.utils.security import (
    generate_random_string,
    generate_api_key,
    hash_string,
    verify_hash,
    mask_email
)
from app.utils.json import (
    json_dumps,
    json_loads,
    safe_json_loads,
    flatten_json,
    unflatten_json
)


class TestTextUtils:
    """Tests for text utilities."""
    
    def test_normalize_persian(self):
        """Test Persian text normalization."""
        # Arabic to Persian conversion
        text = "كتاب"  # Arabic kaf
        normalized = normalize_persian(text)
        assert "ک" in normalized  # Persian kaf
    
    def test_normalize_persian_numbers(self):
        """Test Persian number conversion."""
        text = "۱۲۳۴۵"
        normalized = normalize_persian(text)
        assert normalized == "12345"
    
    def test_extract_hashtags(self):
        """Test hashtag extraction."""
        text = "سلام #تهران و #ایران"
        hashtags = extract_hashtags(text)
        assert "تهران" in hashtags
        assert "ایران" in hashtags
    
    def test_extract_hashtags_english(self):
        """Test English hashtag extraction."""
        text = "Hello #world and #python"
        hashtags = extract_hashtags(text)
        assert "world" in hashtags
        assert "python" in hashtags
    
    def test_extract_mentions(self):
        """Test mention extraction."""
        text = "Hello @user1 and @user2"
        mentions = extract_mentions(text)
        assert "user1" in mentions
        assert "user2" in mentions
    
    def test_extract_urls(self):
        """Test URL extraction."""
        text = "Check https://example.com and http://test.org"
        urls = extract_urls(text)
        assert len(urls) == 2
        assert "https://example.com" in urls
    
    def test_clean_text(self):
        """Test text cleaning."""
        text = "Hello @user https://example.com #tag 😀"
        cleaned = clean_text(text)
        assert "@user" not in cleaned
        assert "https://" not in cleaned
        assert "😀" not in cleaned
        assert "#tag" in cleaned  # hashtags kept by default
    
    def test_is_persian(self):
        """Test Persian detection."""
        assert is_persian("سلام") is True
        assert is_persian("Hello") is False
        assert is_persian("سلام Hello") is True
    
    def test_get_text_language(self):
        """Test language detection."""
        assert get_text_language("سلام دوستان عزیز") == "fa"
        assert get_text_language("Hello world") == "en"
        assert get_text_language("سلام Hello") == "mixed"
    
    def test_truncate_text(self):
        """Test text truncation."""
        text = "This is a long text that should be truncated"
        truncated = truncate_text(text, max_length=20)
        assert len(truncated) == 20
        assert truncated.endswith("...")
    
    def test_word_count(self):
        """Test word counting."""
        assert word_count("Hello world") == 2
        assert word_count("سلام دنیا") == 2
        assert word_count("") == 0


class TestDateTimeUtils:
    """Tests for datetime utilities."""
    
    def test_utc_now(self):
        """Test UTC now."""
        now = utc_now()
        assert now.tzinfo is not None
    
    def test_format_datetime(self):
        """Test datetime formatting."""
        dt = datetime(2024, 1, 15, 10, 30, 0)
        formatted = format_datetime(dt)
        assert "2024-01-15" in formatted
        assert "10:30:00" in formatted
    
    def test_parse_datetime(self):
        """Test datetime parsing."""
        dt_str = "2024-01-15 10:30:00"
        parsed = parse_datetime(dt_str)
        assert parsed.year == 2024
        assert parsed.month == 1
        assert parsed.day == 15
    
    def test_time_ago(self):
        """Test time ago formatting."""
        now = utc_now()
        
        # Just now
        assert time_ago(now - timedelta(seconds=30)) == "just now"
        
        # Minutes ago
        assert "minute" in time_ago(now - timedelta(minutes=5))
        
        # Hours ago
        assert "hour" in time_ago(now - timedelta(hours=3))
        
        # Days ago
        assert "day" in time_ago(now - timedelta(days=2))
    
    def test_get_date_range(self):
        """Test date range calculation."""
        start, end = get_date_range("last_7_days")
        diff = end - start
        assert diff.days == 7 or diff.days == 6  # May vary by hours
    
    def test_parse_duration(self):
        """Test duration parsing."""
        assert parse_duration("1h") == timedelta(hours=1)
        assert parse_duration("30m") == timedelta(minutes=30)
        assert parse_duration("2d") == timedelta(days=2)
        assert parse_duration("1w") == timedelta(weeks=1)
        assert parse_duration("invalid") is None


class TestValidators:
    """Tests for validators."""
    
    def test_is_valid_email(self):
        """Test email validation."""
        assert is_valid_email("test@example.com") is True
        assert is_valid_email("user.name@domain.co") is True
        assert is_valid_email("invalid") is False
        assert is_valid_email("@domain.com") is False
    
    def test_is_valid_username(self):
        """Test username validation."""
        assert is_valid_username("john_doe") is True
        assert is_valid_username("user123") is True
        assert is_valid_username("ab") is False  # Too short
        assert is_valid_username("123user") is False  # Starts with number
    
    def test_is_valid_password(self):
        """Test password validation."""
        valid, _ = is_valid_password("Password123")
        assert valid is True
        
        valid, error = is_valid_password("weak")
        assert valid is False
        assert error is not None
        
        valid, _ = is_valid_password("nouppercase123")
        assert valid is False
    
    def test_is_valid_url(self):
        """Test URL validation."""
        assert is_valid_url("https://example.com") is True
        assert is_valid_url("http://localhost:8000") is True
        assert is_valid_url("not-a-url") is False


class TestSecurityUtils:
    """Tests for security utilities."""
    
    def test_generate_random_string(self):
        """Test random string generation."""
        s1 = generate_random_string(32)
        s2 = generate_random_string(32)
        
        assert len(s1) == 32
        assert len(s2) == 32
        assert s1 != s2
    
    def test_generate_api_key(self):
        """Test API key generation."""
        key = generate_api_key()
        assert key.startswith("psa_")
        assert len(key) > 10
    
    def test_hash_string(self):
        """Test string hashing."""
        hash1 = hash_string("password")
        hash2 = hash_string("password")
        
        assert hash1 == hash2
        assert hash1 != "password"
    
    def test_verify_hash(self):
        """Test hash verification."""
        text = "secret"
        hash_value = hash_string(text)
        
        assert verify_hash(text, hash_value) is True
        assert verify_hash("wrong", hash_value) is False
    
    def test_mask_email(self):
        """Test email masking."""
        masked = mask_email("john.doe@example.com")
        assert "@example.com" in masked
        assert "john.doe" not in masked


class TestJsonUtils:
    """Tests for JSON utilities."""
    
    def test_json_dumps_loads(self):
        """Test JSON serialization/deserialization."""
        data = {"key": "value", "number": 123}
        json_str = json_dumps(data)
        loaded = json_loads(json_str)
        
        assert loaded == data
    
    def test_json_dumps_datetime(self):
        """Test JSON serialization with datetime."""
        data = {"time": datetime(2024, 1, 15, 10, 30, 0)}
        json_str = json_dumps(data)
        
        assert "2024-01-15" in json_str
    
    def test_safe_json_loads(self):
        """Test safe JSON loading."""
        valid = safe_json_loads('{"key": "value"}')
        assert valid == {"key": "value"}
        
        invalid = safe_json_loads("not json", default={})
        assert invalid == {}
    
    def test_flatten_json(self):
        """Test JSON flattening."""
        nested = {
            "a": 1,
            "b": {
                "c": 2,
                "d": {"e": 3}
            }
        }
        flat = flatten_json(nested)
        
        assert flat["a"] == 1
        assert flat["b.c"] == 2
        assert flat["b.d.e"] == 3
    
    def test_unflatten_json(self):
        """Test JSON unflattening."""
        flat = {"a": 1, "b.c": 2, "b.d.e": 3}
        nested = unflatten_json(flat)
        
        assert nested["a"] == 1
        assert nested["b"]["c"] == 2
        assert nested["b"]["d"]["e"] == 3
