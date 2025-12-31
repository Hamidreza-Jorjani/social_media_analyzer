import re
from typing import List, Optional, Set
import unicodedata


# Persian/Arabic character ranges
PERSIAN_CHARS = r'\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF'
PERSIAN_NUMBERS = '۰۱۲۳۴۵۶۷۸۹'
ENGLISH_NUMBERS = '0123456789'

# Common Persian stop words
PERSIAN_STOP_WORDS: Set[str] = {
    'و', 'در', 'به', 'از', 'که', 'این', 'را', 'با', 'است', 'برای',
    'آن', 'یک', 'خود', 'تا', 'کرد', 'بر', 'هم', 'نیز', 'گفت', 'می',
    'شد', 'او', 'ما', 'اما', 'یا', 'شده', 'باید', 'هر', 'آنها', 'بود',
    'پس', 'اگر', 'همه', 'دارد', 'ها', 'های', 'شود', 'کنند', 'کند',
    'بین', 'بعد', 'چه', 'وی', 'شوند', 'کنید', 'کرده', 'کردن', 'دیگر',
    'اینکه', 'بوده', 'نه', 'چون', 'کردند', 'همین', 'داشت', 'داده',
    'بودن', 'چند', 'جا', 'کجا', 'مگر', 'چرا', 'کی', 'همچنین'
}


def normalize_persian(text: str) -> str:
    """
    Normalize Persian/Arabic text.
    - Normalize Unicode
    - Convert Arabic characters to Persian equivalents
    - Normalize whitespace
    - Convert Persian numbers to English
    """
    if not text:
        return ""
    
    # Unicode normalization
    text = unicodedata.normalize('NFKC', text)
    
    # Arabic to Persian character mapping
    arabic_to_persian = {
        'ك': 'ک',
        'ي': 'ی',
        'ى': 'ی',
        'ة': 'ه',
        'ؤ': 'و',
        'إ': 'ا',
        'أ': 'ا',
        'آ': 'آ',
    }
    
    for arabic, persian in arabic_to_persian.items():
        text = text.replace(arabic, persian)
    
    # Convert Persian numbers to English
    for persian, english in zip(PERSIAN_NUMBERS, ENGLISH_NUMBERS):
        text = text.replace(persian, english)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def remove_diacritics(text: str) -> str:
    """Remove Arabic/Persian diacritics (harakat)."""
    if not text:
        return ""
    
    # Diacritics Unicode range
    diacritics_pattern = r'[\u064B-\u065F\u0670]'
    return re.sub(diacritics_pattern, '', text)


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text."""
    if not text:
        return []
    
    # Match hashtags (supports Persian and English)
    pattern = rf'#([{PERSIAN_CHARS}\w]+)'
    hashtags = re.findall(pattern, text, re.UNICODE)
    
    return list(set(hashtags))


def extract_mentions(text: str) -> List[str]:
    """Extract @mentions from text."""
    if not text:
        return []
    
    # Match mentions
    pattern = r'@(\w+)'
    mentions = re.findall(pattern, text)
    
    return list(set(mentions))


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    if not text:
        return []
    
    # URL pattern
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(pattern, text)
    
    return list(set(urls))


def remove_urls(text: str) -> str:
    """Remove URLs from text."""
    if not text:
        return ""
    
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.sub(pattern, '', text)


def remove_mentions(text: str) -> str:
    """Remove @mentions from text."""
    if not text:
        return ""
    
    return re.sub(r'@\w+', '', text)


def remove_hashtags(text: str) -> str:
    """Remove hashtags from text."""
    if not text:
        return ""
    
    pattern = rf'#[{PERSIAN_CHARS}\w]+'
    return re.sub(pattern, '', text, flags=re.UNICODE)


def remove_emojis(text: str) -> str:
    """Remove emojis from text."""
    if not text:
        return ""
    
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


def clean_text(
    text: str,
    remove_urls_flag: bool = True,
    remove_mentions_flag: bool = True,
    remove_hashtags_flag: bool = False,
    remove_emojis_flag: bool = True,
    normalize: bool = True,
    remove_diacritics_flag: bool = True
) -> str:
    """
    Clean text with various options.
    """
    if not text:
        return ""
    
    if normalize:
        text = normalize_persian(text)
    
    if remove_diacritics_flag:
        text = remove_diacritics(text)
    
    if remove_urls_flag:
        text = remove_urls(text)
    
    if remove_mentions_flag:
        text = remove_mentions(text)
    
    if remove_hashtags_flag:
        text = remove_hashtags(text)
    
    if remove_emojis_flag:
        text = remove_emojis(text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def remove_stop_words(
    words: List[str],
    stop_words: Optional[Set[str]] = None
) -> List[str]:
    """Remove stop words from word list."""
    if stop_words is None:
        stop_words = PERSIAN_STOP_WORDS
    
    return [w for w in words if w not in stop_words]


def is_persian(text: str) -> bool:
    """Check if text contains Persian characters."""
    if not text:
        return False
    
    persian_pattern = rf'[{PERSIAN_CHARS}]'
    return bool(re.search(persian_pattern, text))


def get_text_language(text: str) -> str:
    """
    Simple language detection based on character analysis.
    Returns 'fa' for Persian, 'en' for English, 'mixed' for mixed.
    """
    if not text:
        return 'unknown'
    
    persian_count = len(re.findall(rf'[{PERSIAN_CHARS}]', text))
    english_count = len(re.findall(r'[a-zA-Z]', text))
    
    total = persian_count + english_count
    if total == 0:
        return 'unknown'
    
    persian_ratio = persian_count / total
    
    if persian_ratio > 0.7:
        return 'fa'
    elif persian_ratio < 0.3:
        return 'en'
    else:
        return 'mixed'


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to max length."""
    if not text or len(text) <= max_length:
        return text or ""
    
    return text[:max_length - len(suffix)] + suffix


def word_count(text: str) -> int:
    """Count words in text."""
    if not text:
        return 0
    
    # Split by whitespace and filter empty
    words = [w for w in text.split() if w]
    return len(words)


def char_count(text: str, exclude_spaces: bool = True) -> int:
    """Count characters in text."""
    if not text:
        return 0
    
    if exclude_spaces:
        return len(text.replace(' ', ''))
    return len(text)
