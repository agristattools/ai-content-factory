"""
🔍 AI TREND FINDER
Finds trending topics from:
- Google Trends (RSS - Free)
- Reddit Hot Posts (Free API)
- YouTube Trending (Free scrape)

Works in: English, Urdu, Hindi, Punjabi
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
from datetime import datetime
import random
from loguru import logger

class TrendFinder:
    """Discover what's trending right now"""
    
    def __init__(self, niche: str = "tech", language: str = "english"):
        self.niche = niche
        self.language = language
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Niche keywords per language
        self.niche_keywords = {
            "tech": {
                "english": ["iPhone", "AI", "Samsung", "Google", "review", "vs", "new", "2024", "2025"],
                "urdu": ["mobil", "review", "price", "Pakistan", "latest", "camera"],
                "hindi": ["mobile", "review", "price", "India", "latest", "camera"],
                "punjabi": ["mobile", "review", "price", "latest", "new", "tech"],
            },
            "motivation": {
                "english": ["success", "mindset", "discipline", "habits", "millionaire"],
                "urdu": ["kamyabi", "success", "motivation", "Pakistan", "story"],
                "hindi": ["safalta", "success", "motivation", "India", "story"],
                "punjabi": ["kamyabi", "success", "motivation", "story"],
            }
        }
    
    def find_trends(self, limit: int = 10) -> List[Dict]:
        """Main method - find trending topics from all sources"""
        logger.info(f"🔍 Finding trends for: {self.niche} in {self.language}")
        
        trends = []
        
        # Try Google Trends RSS
        google_trends = self._from_google_trends()
        if google_trends:
            trends.extend(google_trends)
        
        # Try Reddit
        reddit_trends = self._from_reddit()
        if reddit_trends:
            trends.extend(reddit_trends)
        
        # Score and sort
        trends = self._score_and_sort(trends)
        
        logger.info(f"✅ Found {len(trends[:limit])} trending topics")
        return trends[:limit]
    
    def _from_google_trends(self) -> List[Dict]:
        """Google Trends RSS - 100% Free, no API key needed"""
        try:
            geo_map = {
                "english": "US",
                "urdu": "PK",
                "hindi": "IN",
                "punjabi": "IN"
            }
            geo = geo_map.get(self.language, "US")
            
            url = f"https://trends.google.com/trending/rss?geo={geo}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                logger.warning(f"Google Trends returned {response.status_code}")
                return []
            
            root = ET.fromstring(response.content)
            
            trends = []
            for item in root.findall('.//item'):
                title = item.find('title')
                if title is not None and title.text:
                    trends.append({
                        'topic': title.text.strip(),
                        'source': 'Google Trends',
                        'score': random.randint(60, 95),  # Trends are already hot
                        'timestamp': datetime.now().isoformat()
                    })
            
            logger.info(f"📊 Google Trends: {len(trends)} topics from {geo}")
            return trends
            
        except Exception as e:
            logger.warning(f"Google Trends error: {e}")
            return []
    
    def _from_reddit(self) -> List[Dict]:
        """Reddit JSON API - Free, no auth needed"""
        subreddits_map = {
            "tech": {
                "english": ["technology", "gadgets", "Android", "apple"],
                "urdu": ["Pakistan", "PakistanTech"],
                "hindi": ["India", "IndiaTech", "IndianGaming"],
                "punjabi": ["India", "punjabi"],
            },
            "motivation": {
                "english": ["GetMotivated", "selfimprovement", "productivity"],
                "urdu": ["Pakistan", "islamabad"],
                "hindi": ["India", "delhi"],
                "punjabi": ["punjabi", "India"],
            }
        }
        
        subs = subreddits_map.get(self.niche, {}).get(self.language, ["technology"])
        sub = random.choice(subs)
        
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=15"
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                logger.warning(f"Reddit returned {response.status_code}")
                return []
            
            data = response.json()
            
            trends = []
            for post in data.get('data', {}).get('children', []):
                post_data = post['data']
                
                # Filter: only text posts with good engagement
                score = post_data.get('score', 0)
                comments = post_data.get('num_comments', 0)
                
                if score > 10:  # Minimum engagement threshold
                    trends.append({
                        'topic': post_data['title'],
                        'source': f'Reddit r/{sub}',
                        'score': min(score, 100),
                        'comments': comments,
                        'url': f"https://reddit.com{post_data['permalink']}",
                        'timestamp': datetime.fromtimestamp(post_data['created_utc']).isoformat()
                    })
            
            logger.info(f"📱 Reddit r/{sub}: {len(trends)} hot posts")
            return trends
            
        except Exception as e:
            logger.warning(f"Reddit error: {e}")
            return []
    
    def _score_and_sort(self, trends: List[Dict]) -> List[Dict]:
        """Score topics by relevance to niche and language"""
        
        keywords = self.niche_keywords.get(self.niche, {}).get(self.language, [])
        
        for trend in trends:
            topic_lower = trend['topic'].lower()
            
            # Boost score if contains niche keywords
            keyword_matches = sum(1 for kw in keywords if kw.lower() in topic_lower)
            trend['score'] = trend.get('score', 50) + (keyword_matches * 15)
            
            # Cap at 100
            trend['score'] = min(trend['score'], 100)
        
        # Remove duplicates
        seen = set()
        unique = []
        for trend in sorted(trends, key=lambda x: x['score'], reverse=True):
            topic_key = trend['topic'].lower()[:80]
            if topic_key not in seen:
                seen.add(topic_key)
                unique.append(trend)
        
        return unique


# ============================================
# TEST THE MODULE
# ============================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔍 TREND FINDER TEST")
    print("="*50 + "\n")
    
    # Test English Tech
    print("📊 Testing: English | Tech Niche")
    finder = TrendFinder(niche="tech", language="english")
    trends = finder.find_trends(5)
    
    for i, t in enumerate(trends, 1):
        print(f"  {i}. {t['topic'][:80]}")
        print(f"     Source: {t['source']} | Score: {t['score']}\n")
    
    print("-"*50)
    
    # Test Urdu
    print("\n📊 Testing: Urdu | Tech Niche")
    finder_ur = TrendFinder(niche="tech", language="urdu")
    trends_ur = finder_ur.find_trends(5)
    
    for i, t in enumerate(trends_ur, 1):
        print(f"  {i}. {t['topic'][:80]}")
        print(f"     Source: {t['source']} | Score: {t['score']}\n")