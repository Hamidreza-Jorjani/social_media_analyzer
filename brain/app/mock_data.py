import random
from typing import List, Dict, Any

# Persian sample keywords
PERSIAN_KEYWORDS = [
    "تهران", "ایران", "سلام", "خوب", "بد", "عالی", "زیبا", "قشنگ",
    "سیاست", "اقتصاد", "ورزش", "فوتبال", "موسیقی", "فیلم", "کتاب",
    "دانشگاه", "کار", "زندگی", "عشق", "دوست", "خانواده", "سفر",
    "غذا", "هنر", "تکنولوژی", "اینترنت", "موبایل", "کامپیوتر"
]

PERSIAN_ENTITIES = [
    {"text": "تهران", "type": "location"},
    {"text": "ایران", "type": "location"},
    {"text": "مشهد", "type": "location"},
    {"text": "اصفهان", "type": "location"},
    {"text": "شیراز", "type": "location"},
    {"text": "علی", "type": "person"},
    {"text": "محمد", "type": "person"},
    {"text": "فاطمه", "type": "person"},
    {"text": "حسین", "type": "person"},
    {"text": "دانشگاه تهران", "type": "organization"},
    {"text": "صدا و سیما", "type": "organization"},
]

TOPICS = [
    "سیاست", "اقتصاد", "ورزش", "فرهنگ", "اجتماعی",
    "تکنولوژی", "سلامت", "محیط زیست", "آموزش", "سرگرمی"
]

EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]

SENTIMENT_LABELS = ["positive", "negative", "neutral"]


def generate_sentiment() -> Dict[str, Any]:
    """Generate mock sentiment result."""
    label = random.choice(SENTIMENT_LABELS)
    
    if label == "positive":
        score = random.uniform(0.3, 1.0)
    elif label == "negative":
        score = random.uniform(-1.0, -0.3)
    else:
        score = random.uniform(-0.3, 0.3)
    
    return {
        "label": label,
        "score": round(score, 4),
        "confidence": round(random.uniform(0.7, 0.99), 4)
    }


def generate_emotions() -> Dict[str, float]:
    """Generate mock emotion scores."""
    emotions = {}
    remaining = 1.0
    
    shuffled = EMOTIONS.copy()
    random.shuffle(shuffled)
    
    for i, emotion in enumerate(shuffled):
        if i == len(shuffled) - 1:
            emotions[emotion] = round(remaining, 4)
        else:
            value = random.uniform(0, remaining * 0.6)
            emotions[emotion] = round(value, 4)
            remaining -= value
    
    return emotions


def generate_keywords(count: int = 5) -> List[str]:
    """Generate mock keywords."""
    return random.sample(PERSIAN_KEYWORDS, min(count, len(PERSIAN_KEYWORDS)))


def generate_entities(text: str = "") -> List[Dict[str, Any]]:
    """Generate mock entities."""
    count = random.randint(0, 4)
    entities = []
    
    for entity_data in random.sample(PERSIAN_ENTITIES, min(count, len(PERSIAN_ENTITIES))):
        entities.append({
            "text": entity_data["text"],
            "type": entity_data["type"],
            "start": random.randint(0, 50),
            "end": random.randint(51, 100),
            "confidence": round(random.uniform(0.75, 0.99), 4)
        })
    
    return entities


def generate_topics(count: int = 3) -> List[Dict[str, Any]]:
    """Generate mock topics."""
    selected = random.sample(TOPICS, min(count, len(TOPICS)))
    topics = []
    
    for topic in selected:
        topics.append({
            "topic": topic,
            "score": round(random.uniform(0.3, 0.95), 4),
            "keywords": random.sample(PERSIAN_KEYWORDS, 3)
        })
    
    return sorted(topics, key=lambda x: x["score"], reverse=True)


def generate_summary(text: str = "") -> str:
    """Generate mock summary."""
    summaries = [
        "این متن درباره موضوعات اجتماعی و فرهنگی صحبت می‌کند.",
        "نویسنده نظر مثبتی درباره این موضوع دارد.",
        "این پست شامل اطلاعاتی درباره رویدادهای اخیر است.",
        "متن حاوی نکات مهمی درباره زندگی روزمره است.",
        "این محتوا به بررسی مسائل جاری می‌پردازد.",
    ]
    return random.choice(summaries)


def generate_full_analysis(text_id: str, text: str = "") -> Dict[str, Any]:
    """Generate complete mock analysis for a text."""
    emotions = generate_emotions()
    
    return {
        "text_id": text_id,
        "sentiment": generate_sentiment(),
        "emotions": emotions,
        "dominant_emotion": max(emotions, key=emotions.get),
        "keywords": generate_keywords(random.randint(3, 8)),
        "entities": generate_entities(text),
        "topics": generate_topics(random.randint(1, 3)),
        "summary": generate_summary(text)
    }


def generate_pagerank_scores(nodes: List[Dict]) -> List[Dict[str, Any]]:
    """Generate mock PageRank scores for nodes."""
    results = []
    
    for node in nodes:
        results.append({
            "id": node.get("id"),
            "type": node.get("type", "unknown"),
            "pagerank": round(random.uniform(0.001, 0.1), 6),
            "degree": random.randint(1, 100),
            "in_degree": random.randint(0, 50),
            "out_degree": random.randint(0, 50)
        })
    
    # Sort by pagerank
    results.sort(key=lambda x: x["pagerank"], reverse=True)
    return results


def generate_communities(nodes: List[Dict]) -> Dict[str, Any]:
    """Generate mock community detection results."""
    num_communities = min(len(nodes) // 3 + 1, 10)
    
    communities = []
    for i in range(num_communities):
        communities.append({
            "community_id": i,
            "size": random.randint(3, len(nodes) // num_communities + 5),
            "density": round(random.uniform(0.1, 0.8), 4),
            "keywords": random.sample(PERSIAN_KEYWORDS, 3)
        })
    
    # Assign communities to nodes
    node_results = []
    for node in nodes:
        node_results.append({
            "id": node.get("id"),
            "community_id": random.randint(0, num_communities - 1)
        })
    
    return {
        "communities": communities,
        "nodes": node_results,
        "modularity": round(random.uniform(0.3, 0.8), 4)
    }


def generate_trend_detection(posts: List[Dict]) -> List[Dict[str, Any]]:
    """Generate mock trend detection results."""
    trends = []
    
    trend_names = [
        "#تهران", "#ایران", "#ورزش", "#سیاست", "#اقتصاد",
        "#فوتبال", "#موسیقی", "#سینما", "#کتاب", "#سفر"
    ]
    
    for i, name in enumerate(random.sample(trend_names, random.randint(3, 7))):
        trends.append({
            "name": name,
            "volume": random.randint(50, 1000),
            "growth_rate": round(random.uniform(-0.5, 2.0), 4),
            "velocity": round(random.uniform(0.1, 1.0), 4),
            "sentiment": generate_sentiment(),
            "keywords": random.sample(PERSIAN_KEYWORDS, 3)
        })
    
    return sorted(trends, key=lambda x: x["volume"], reverse=True)
