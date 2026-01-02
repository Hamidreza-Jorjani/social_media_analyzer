"""
Enhanced Persian Mock Data Generator
Generates realistic NLP analysis results for Persian text.
"""

import random
import re
from typing import List, Dict, Any, Optional


# ============================================
# Persian Word Lists
# ============================================

# Positive words for sentiment detection
POSITIVE_WORDS = [
    "عالی", "خوب", "زیبا", "قشنگ", "فوق‌العاده", "عشق", "دوست", "خوشحال",
    "موفق", "بهترین", "شگفت‌انگیز", "لذت", "سپاس", "ممنون", "مثبت",
    "امید", "پیروز", "برنده", "خوش", "مبارک", "تبریک", "افتخار",
    "عالیه", "خوبه", "دوستت", "عاشق", "محشر", "باحال", "توپ"
]

# Negative words for sentiment detection
NEGATIVE_WORDS = [
    "بد", "زشت", "افتضاح", "وحشتناک", "غم", "ناراحت", "شکست",
    "بدترین", "متنفر", "نفرت", "خسته", "گرانی", "مشکل", "سخت",
    "درد", "رنج", "ناامید", "بیچاره", "فقر", "جنگ", "مرگ",
    "بده", "گرون", "داغون", "خراب", "ضعیف", "بیکار", "ترافیک"
]

# Emotion-specific words
EMOTION_WORDS = {
    "joy": ["خوشحال", "شاد", "لذت", "خنده", "جشن", "مبارک", "عید", "خوش"],
    "sadness": ["غم", "ناراحت", "گریه", "اشک", "تنها", "دلتنگ", "افسرده", "غصه"],
    "anger": ["عصبانی", "خشم", "جنگ", "دعوا", "متنفر", "نفرت", "لعنت", "کثیف"],
    "fear": ["ترس", "وحشت", "نگران", "خطر", "تهدید", "فرار", "وحشتناک", "خوف"],
    "surprise": ["عجیب", "شگفت", "باورنکردنی", "ناگهان", "غیرمنتظره", "وای", "چه"],
    "disgust": ["چندش", "نفرت‌انگیز", "زشت", "کثیف", "بد", "متعفن", "حال‌بهم‌زن"]
}

# Common Persian keywords by category
KEYWORDS_BY_CATEGORY = {
    "سیاست": ["سیاست", "دولت", "مجلس", "رئیس‌جمهور", "انتخابات", "قانون", "وزیر"],
    "اقتصاد": ["اقتصاد", "قیمت", "گرانی", "دلار", "بورس", "تورم", "بازار", "کار"],
    "ورزش": ["فوتبال", "ورزش", "تیم", "بازی", "گل", "برد", "باخت", "قهرمان"],
    "تکنولوژی": ["تکنولوژی", "اینترنت", "موبایل", "کامپیوتر", "هوش مصنوعی", "اپلیکیشن"],
    "فرهنگ": ["فرهنگ", "هنر", "موسیقی", "فیلم", "کتاب", "شعر", "سینما", "تئاتر"],
    "اجتماعی": ["مردم", "جامعه", "خانواده", "دوست", "عشق", "زندگی", "روابط"],
    "گردشگری": ["سفر", "گردشگری", "هتل", "پرواز", "تعطیلات", "طبیعت", "دریا", "کوه"],
    "غذا": ["غذا", "رستوران", "آشپزی", "چلوکباب", "پیتزا", "قهوه", "چای"],
    "آموزش": ["دانشگاه", "مدرسه", "درس", "امتحان", "استاد", "دانشجو", "تحصیل"],
    "سلامت": ["سلامت", "بیماری", "دکتر", "بیمارستان", "دارو", "کرونا", "واکسن"]
}

# Persian named entities
ENTITIES_DB = {
    "location": [
        "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "کرج", "قم",
        "ایران", "ترکیه", "دبی", "آلمان", "کانادا", "آمریکا",
        "دربند", "درکه", "کیش", "قشم", "شمال", "جنوب"
    ],
    "person": [
        "علی", "محمد", "حسین", "رضا", "امیر", "فاطمه", "زهرا", "مریم",
        "شجریان", "فردوسی", "حافظ", "سعدی", "مولانا"
    ],
    "organization": [
        "دانشگاه تهران", "دانشگاه شریف", "صدا و سیما", "بانک ملی",
        "ایران خودرو", "سایپا", "دیجی‌کالا", "اسنپ", "تپسی"
    ],
    "event": [
        "نوروز", "عید", "یلدا", "چهارشنبه‌سوری", "سیزده‌بدر",
        "جام جهانی", "المپیک", "لیگ برتر"
    ],
    "product": [
        "آیفون", "سامسونگ", "پراید", "پژو", "تسلا"
    ]
}

# Persian topics
TOPICS_LIST = [
    {"name": "سیاست", "keywords": ["دولت", "مجلس", "انتخابات", "قانون"]},
    {"name": "اقتصاد", "keywords": ["قیمت", "دلار", "بورس", "تورم"]},
    {"name": "ورزش", "keywords": ["فوتبال", "تیم", "بازی", "قهرمان"]},
    {"name": "فرهنگ و هنر", "keywords": ["موسیقی", "فیلم", "کتاب", "سینما"]},
    {"name": "اجتماعی", "keywords": ["مردم", "جامعه", "خانواده", "زندگی"]},
    {"name": "تکنولوژی", "keywords": ["اینترنت", "موبایل", "هوش مصنوعی"]},
    {"name": "سلامت", "keywords": ["بیماری", "دکتر", "دارو", "سلامت"]},
    {"name": "آموزش", "keywords": ["دانشگاه", "مدرسه", "درس", "تحصیل"]},
    {"name": "گردشگری", "keywords": ["سفر", "هتل", "گردشگری", "طبیعت"]},
    {"name": "آشپزی", "keywords": ["غذا", "رستوران", "آشپزی", "دستور"]}
]

# Summary templates
SUMMARY_TEMPLATES = {
    "positive": [
        "این متن نگرش مثبتی نسبت به {topic} دارد.",
        "نویسنده رضایت خود را از {topic} ابراز کرده است.",
        "محتوا حاوی دیدگاه مثبت درباره {topic} است.",
        "در این پست، {topic} مورد تحسین قرار گرفته است."
    ],
    "negative": [
        "این متن انتقادی نسبت به {topic} است.",
        "نویسنده نارضایتی خود را از {topic} بیان کرده است.",
        "محتوا حاوی انتقاد از {topic} است.",
        "در این پست، نگرانی درباره {topic} مطرح شده است."
    ],
    "neutral": [
        "این متن اطلاعاتی درباره {topic} ارائه می‌دهد.",
        "محتوا به صورت خنثی درباره {topic} صحبت می‌کند.",
        "نویسنده بدون قضاوت درباره {topic} نوشته است.",
        "این پست شامل اطلاعات عمومی درباره {topic} است."
    ]
}


# ============================================
# Text Analysis Functions
# ============================================

def analyze_text_content(text: str) -> Dict[str, Any]:
    """Analyze Persian text to extract features."""
    text_lower = text.lower() if text else ""
    
    # Count positive/negative words
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text)
    
    # Detect emotions
    emotion_scores = {}
    for emotion, words in EMOTION_WORDS.items():
        score = sum(1 for word in words if word in text)
        emotion_scores[emotion] = score
    
    # Detect category
    category_scores = {}
    for category, keywords in KEYWORDS_BY_CATEGORY.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            category_scores[category] = score
    
    # Find entities in text
    found_entities = []
    for entity_type, entities in ENTITIES_DB.items():
        for entity in entities:
            if entity in text:
                found_entities.append({"text": entity, "type": entity_type})
    
    # Extract hashtags
    hashtags = re.findall(r'#([\u0600-\u06FF\w]+)', text)
    
    return {
        "positive_count": positive_count,
        "negative_count": negative_count,
        "emotion_scores": emotion_scores,
        "category_scores": category_scores,
        "found_entities": found_entities,
        "hashtags": hashtags,
        "text_length": len(text)
    }


def generate_sentiment(text: str = "") -> Dict[str, Any]:
    """Generate sentiment based on text analysis."""
    analysis = analyze_text_content(text)
    
    positive = analysis["positive_count"]
    negative = analysis["negative_count"]
    
    # Determine sentiment
    if positive > negative:
        label = "positive"
        base_score = 0.3 + min(positive * 0.15, 0.6)
    elif negative > positive:
        label = "negative"
        base_score = -0.3 - min(negative * 0.15, 0.6)
    else:
        label = "neutral"
        base_score = random.uniform(-0.2, 0.2)
    
    # Add some randomness
    score = base_score + random.uniform(-0.1, 0.1)
    score = max(-1.0, min(1.0, score))
    
    confidence = 0.7 + min((positive + negative) * 0.05, 0.25)
    confidence += random.uniform(-0.05, 0.05)
    confidence = max(0.5, min(0.99, confidence))
    
    return {
        "label": label,
        "score": round(score, 4),
        "confidence": round(confidence, 4)
    }


def generate_emotions(text: str = "") -> Dict[str, float]:
    """Generate emotion scores based on text analysis."""
    analysis = analyze_text_content(text)
    emotion_hints = analysis["emotion_scores"]
    
    emotions = {}
    total_hints = sum(emotion_hints.values()) or 1
    remaining = 1.0
    
    # Base emotions on detected words
    emotion_names = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
    
    for i, emotion in enumerate(emotion_names):
        if i == len(emotion_names) - 1:
            emotions[emotion] = round(remaining, 4)
        else:
            hint_weight = emotion_hints.get(emotion, 0) / total_hints
            base = 0.1 + hint_weight * 0.4
            value = base + random.uniform(0, 0.15)
            value = min(value, remaining - 0.05 * (len(emotion_names) - i - 1))
            emotions[emotion] = round(value, 4)
            remaining -= value
    
    return emotions


def generate_keywords(text: str = "", count: int = 5) -> List[str]:
    """Extract keywords based on text content."""
    analysis = analyze_text_content(text)
    keywords = []
    
    # Add hashtags as keywords
    keywords.extend(analysis["hashtags"][:3])
    
    # Add keywords from detected categories
    for category, score in sorted(analysis["category_scores"].items(), key=lambda x: -x[1]):
        if len(keywords) >= count:
            break
        for kw in KEYWORDS_BY_CATEGORY[category]:
            if kw in text and kw not in keywords:
                keywords.append(kw)
                if len(keywords) >= count:
                    break
    
    # Fill with random keywords if needed
    if len(keywords) < count:
        all_keywords = [kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws]
        remaining = count - len(keywords)
        keywords.extend(random.sample(all_keywords, min(remaining, len(all_keywords))))
    
    return keywords[:count]


def generate_entities(text: str = "") -> List[Dict[str, Any]]:
    """Extract named entities from text."""
    analysis = analyze_text_content(text)
    entities = []
    
    for entity_info in analysis["found_entities"]:
        entity_text = entity_info["text"]
        start_pos = text.find(entity_text) if text else 0
        
        entities.append({
            "text": entity_text,
            "type": entity_info["type"],
            "start": start_pos,
            "end": start_pos + len(entity_text),
            "confidence": round(random.uniform(0.85, 0.99), 4)
        })
    
    # Add some random entities if none found
    if not entities and random.random() > 0.3:
        entity_type = random.choice(list(ENTITIES_DB.keys()))
        entity_text = random.choice(ENTITIES_DB[entity_type])
        entities.append({
            "text": entity_text,
            "type": entity_type,
            "start": 0,
            "end": len(entity_text),
            "confidence": round(random.uniform(0.75, 0.95), 4)
        })
    
    return entities


def generate_topics(text: str = "", count: int = 3) -> List[Dict[str, Any]]:
    """Detect topics in text."""
    analysis = analyze_text_content(text)
    topics = []
    
    # Score topics based on keyword matches
    topic_scores = []
    for topic in TOPICS_LIST:
        score = sum(1 for kw in topic["keywords"] if kw in text)
        if score > 0:
            topic_scores.append((topic, score))
    
    # Sort by score
    topic_scores.sort(key=lambda x: -x[1])
    
    # Add matched topics
    for topic, score in topic_scores[:count]:
        topics.append({
            "topic": topic["name"],
            "score": round(0.5 + score * 0.15 + random.uniform(0, 0.2), 4),
            "keywords": topic["keywords"][:3]
        })
    
    # Fill with random topics if needed
    if len(topics) < count:
        remaining_topics = [t for t in TOPICS_LIST if t["name"] not in [x["topic"] for x in topics]]
        for topic in random.sample(remaining_topics, min(count - len(topics), len(remaining_topics))):
            topics.append({
                "topic": topic["name"],
                "score": round(random.uniform(0.3, 0.6), 4),
                "keywords": topic["keywords"][:3]
            })
    
    return sorted(topics, key=lambda x: -x["score"])


def generate_summary(text: str = "") -> str:
    """Generate a summary based on text content."""
    sentiment = generate_sentiment(text)
    analysis = analyze_text_content(text)
    
    # Find main topic
    topic = "این موضوع"
    if analysis["category_scores"]:
        main_category = max(analysis["category_scores"], key=analysis["category_scores"].get)
        topic = main_category
    elif analysis["hashtags"]:
        topic = analysis["hashtags"][0]
    
    # Select template based on sentiment
    templates = SUMMARY_TEMPLATES.get(sentiment["label"], SUMMARY_TEMPLATES["neutral"])
    template = random.choice(templates)
    
    return template.format(topic=topic)


def generate_full_analysis(text_id: str, text: str = "") -> Dict[str, Any]:
    """Generate complete analysis for a text."""
    emotions = generate_emotions(text)
    
    return {
        "text_id": text_id,
        "sentiment": generate_sentiment(text),
        "emotions": emotions,
        "dominant_emotion": max(emotions, key=emotions.get),
        "keywords": generate_keywords(text, random.randint(4, 8)),
        "entities": generate_entities(text),
        "topics": generate_topics(text, random.randint(1, 3)),
        "summary": generate_summary(text)
    }


# ============================================
# Graph Analysis Functions
# ============================================

def generate_pagerank_scores(nodes: List[Dict]) -> List[Dict[str, Any]]:
    """Generate PageRank scores for nodes."""
    results = []
    total_nodes = len(nodes)
    
    for i, node in enumerate(nodes):
        # Higher scores for earlier nodes (simulating importance)
        base_rank = 1.0 / total_nodes
        variance = random.uniform(0.5, 2.0)
        pagerank = base_rank * variance
        
        results.append({
            "id": node.get("id"),
            "type": node.get("type", "unknown"),
            "pagerank": round(pagerank, 6),
            "degree": random.randint(1, min(50, total_nodes)),
            "in_degree": random.randint(0, 30),
            "out_degree": random.randint(0, 30)
        })
    
    # Normalize PageRank
    total = sum(r["pagerank"] for r in results)
    for r in results:
        r["pagerank"] = round(r["pagerank"] / total, 6)
    
    # Sort by pagerank
    results.sort(key=lambda x: x["pagerank"], reverse=True)
    return results


def generate_communities(nodes: List[Dict]) -> Dict[str, Any]:
    """Generate community detection results."""
    num_nodes = len(nodes)
    num_communities = max(1, min(num_nodes // 5, 10))
    
    communities = []
    for i in range(num_communities):
        size = random.randint(max(1, num_nodes // num_communities - 2), 
                             num_nodes // num_communities + 3)
        communities.append({
            "community_id": i,
            "size": size,
            "density": round(random.uniform(0.2, 0.8), 4),
            "keywords": random.sample(
                [kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws], 
                min(3, len([kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws]))
            )
        })
    
    # Assign nodes to communities
    node_results = []
    for node in nodes:
        node_results.append({
            "id": node.get("id"),
            "community_id": random.randint(0, num_communities - 1)
        })
    
    return {
        "communities": communities,
        "nodes": node_results,
        "modularity": round(random.uniform(0.3, 0.8), 4),
        "num_communities": num_communities
    }


def generate_trend_detection(posts: List[Dict]) -> List[Dict[str, Any]]:
    """Generate trend detection results."""
    # Collect all hashtags from posts
    hashtag_counts = {}
    for post in posts:
        content = post.get("content", "")
        hashtags = re.findall(r'#([\u0600-\u06FF\w]+)', content)
        for tag in hashtags:
            hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
    
    # Also add hashtags from hashtags field
    for post in posts:
        for tag in post.get("hashtags", []):
            hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
    
    # Generate trends
    trends = []
    sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: -x[1])
    
    for tag, count in sorted_hashtags[:10]:
        trends.append({
            "name": f"#{tag}",
            "volume": count * random.randint(5, 20),
            "growth_rate": round(random.uniform(-0.3, 2.5), 4),
            "velocity": round(random.uniform(0.1, 1.0), 4),
            "sentiment": generate_sentiment(tag),
            "keywords": [tag] + random.sample(
                [kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws],
                min(2, 5)
            )
        })
    
    # Add some predefined trends if none found
    if not trends:
        predefined = ["تهران", "ایران", "فوتبال", "سیاست", "اقتصاد"]
        for tag in random.sample(predefined, 3):
            trends.append({
                "name": f"#{tag}",
                "volume": random.randint(50, 500),
                "growth_rate": round(random.uniform(0.5, 2.0), 4),
                "velocity": round(random.uniform(0.3, 0.9), 4),
                "sentiment": generate_sentiment(tag),
                "keywords": [tag]
            })
    
    return sorted(trends, key=lambda x: x["volume"], reverse=True)
