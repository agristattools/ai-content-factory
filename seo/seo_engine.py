"""
📈 AI SEO ENGINE
Generates high-ranking YouTube titles, tags, descriptions
Uses Groq (Free Llama 3) for SEO optimization
Supports: English, Urdu, Hindi, Punjabi
"""
import os
import json
from typing import Dict, List, Tuple
from loguru import logger
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class SEOEngine:
    """Generate optimized YouTube metadata for maximum views"""
    
    def __init__(self, language: str = "english", niche: str = "tech"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.language = language
        self.niche = niche
        
        # Power words that increase CTR
        self.power_words = {
            "english": ["Ultimate", "Secret", "Proven", "Shocking", "Must See", 
                       "Game Changer", "You Won't Believe", "Exposed", "Truth"],
            "urdu": ["Haqeeqat", "Raaz", "Kamaal", "Zabardast", "Aakhri", "Bilkul Naya"],
            "hindi": ["Sach", "Raaz", "Dhamaal", "Zabardast", "Aakhri", "Naya"],
            "punjabi": ["Sach", "Raaz", "Kamaal", "Zabardast", "Vadhia"],
        }
    
    def generate_all_metadata(self, topic: str, script: str = "", 
                             keywords: List[str] = None) -> Dict:
        """Generate complete YouTube metadata package"""
        
        logger.info(f"📈 Generating SEO for: {topic[:60]}...")
        
        # Generate each piece
        titles = self.generate_titles(topic)
        tags = self.generate_tags(topic, keywords)
        description = self.generate_description(topic, script)
        hashtags = self.generate_hashtags(topic)
        
        result = {
            "topic": topic,
            "language": self.language,
            "titles": titles,
            "best_title": titles[0] if titles else topic,
            "tags": tags,
            "description": description,
            "hashtags": hashtags,
            "estimated_ctr": self._estimate_ctr(titles[0] if titles else topic)
        }
        
        logger.info(f"✅ SEO package generated: {len(tags)} tags, {len(titles)} titles")
        return result
    
    def generate_titles(self, topic: str, count: int = 5) -> List[str]:
        """Generate high-CTR video titles"""
        
        pw = self.power_words.get(self.language, self.power_words["english"])
        
        prompt = f"""Generate {count} YouTube video titles for: "{topic}"

Rules for HIGH CTR titles:
1. Use power words like: {', '.join(pw[:5])}
2. Include numbers when possible
3. Create curiosity gap (viewer MUST click)
4. Keep under 60 characters
5. Use emotional triggers
6. Add brackets/parentheses for extra info
7. Language: {self.language}

Format as JSON list:
["title 1", "title 2", "title 3", "title 4", "title 5"]"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a YouTube SEO expert. Always return valid JSON lists."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            text = response.choices[0].message.content.strip()
            
            # Clean up
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text.rsplit("\n", 1)[0]
            
            titles = json.loads(text)
            return titles[:count]
            
        except Exception as e:
            logger.error(f"Title generation failed: {e}")
            return [topic]
    
    def generate_tags(self, topic: str, extra_keywords: List[str] = None) -> List[str]:
        """Generate optimized YouTube tags"""
        
        keywords = extra_keywords or []
        
        prompt = f"""Generate 25 YouTube tags for video about: "{topic}"
Additional keywords to include: {', '.join(keywords[:5]) if keywords else 'none'}

Rules:
1. Mix broad and specific tags
2. Include long-tail phrases (3-5 words)
3. Add related search terms
4. Include competitor keywords
5. Language: {self.language}

Format as JSON list of 25 tags."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a YouTube SEO expert. Return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            text = response.choices[0].message.content.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text.rsplit("\n", 1)[0]
            
            tags = json.loads(text)
            
            # Add topic as tag
            if topic.lower() not in [t.lower() for t in tags]:
                tags.insert(0, topic)
            
            return tags[:30]  # YouTube limit ~500 chars total
            
        except Exception as e:
            logger.error(f"Tag generation failed: {e}")
            return [topic]
    
    def generate_description(self, topic: str, script: str = "") -> str:
        """Generate SEO-optimized video description"""
        
        script_excerpt = script[:300] if script else ""
        
        prompt = f"""Write a YouTube video description for: "{topic}"

STRUCTURE:
1. First 2 lines: MOST IMPORTANT (appears above fold)
2. Brief summary (2-3 sentences)
3. Timestamps/chapters (if applicable)
4. Call to action (subscribe, like, comment)
5. Related videos/playlists
6. Social media links
7. Hashtags at bottom

Rules:
- First 2 lines must hook viewers
- Include relevant keywords naturally
- Write in {self.language}
- Keep professional but approachable
- Add emojis sparingly (1-2 max)
- Total: 200-300 words

Script excerpt for reference:
{script_excerpt[:200]}

Write the description now:"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a YouTube SEO expert. Write compelling descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Description generation failed: {e}")
            return f"Watch this video about {topic}! Don't forget to like and subscribe!"
    
    def generate_hashtags(self, topic: str) -> List[str]:
        """Generate trending hashtags"""
        
        prompt = f"""Generate 10 hashtags for YouTube video: "{topic}"
Rules:
- Mix popular and niche hashtags
- Max 3 words per hashtag
- Language: {self.language}
Format as JSON list."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            text = response.choices[0].message.content.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text.rsplit("\n", 1)[0]
            
            hashtags = json.loads(text)
            
            # Add niche tags
            if self.niche:
                hashtags.append(f"#{self.niche.replace('_', '')}")
            
            return hashtags[:15]
            
        except:
            return [f"#{topic.replace(' ', '')}", "#YouTube", "#Viral"]
    
    def _estimate_ctr(self, title: str) -> Dict:
        """Estimate click-through rate potential"""
        
        score = 50  # Base
        
        # Check for power words
        for pw_list in self.power_words.values():
            for word in pw_list:
                if word.lower() in title.lower():
                    score += 10
                    break
        
        # Numbers in title
        if any(char.isdigit() for char in title):
            score += 8
        
        # Curiosity gap indicators
        curiosity_words = ["this", "secret", "why", "how", "what", "shocking", "never"]
        for word in curiosity_words:
            if word.lower() in title.lower():
                score += 5
        
        # Length check
        if 30 <= len(title) <= 60:
            score += 7
        
        score = min(score, 100)
        
        return {
            "score": score,
            "rating": "⭐⭐⭐" if score > 70 else "⭐⭐" if score > 50 else "⭐"
        }
    
    def save_metadata(self, metadata: Dict, filepath: str = None) -> str:
        """Save SEO metadata to file"""
        
        if filepath is None:
            safe_name = metadata.get("topic", "video")[:30].replace(" ", "_")
            filepath = f"output/seo_{safe_name}.json"
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 SEO metadata saved: {filepath}")
        return filepath


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    from pathlib import Path
    
    print("\n" + "="*60)
    print("📈  AI SEO ENGINE TEST")
    print("="*60)
    
    # Test English
    print("\n📊 Testing English SEO...")
    seo_en = SEOEngine(language="english", niche="tech")
    
    test_topic = "Google Pixel Battery Drain Issues - How to Fix"
    result = seo_en.generate_all_metadata(test_topic)
    
    print(f"\n✅ Best Title: {result['best_title']}")
    print(f"📊 CTR Score: {result['estimated_ctr']['score']}/100 {result['estimated_ctr']['rating']}")
    print(f"\n🏷️ Tags ({len(result['tags'])}):")
    for tag in result['tags'][:5]:
        print(f"   - {tag}")
    print(f"   ... and {len(result['tags']) - 5} more")
    
    print(f"\n📝 Description Preview:")
    desc = result['description']
    print(f"   {desc[:200]}...")
    
    print(f"\n#️⃣ Hashtags:")
    for ht in result['hashtags'][:5]:
        print(f"   {ht}")
    
    # Save
    seo_en.save_metadata(result, "output/seo_test.json")
    
    # Test Urdu
    print("\n" + "-"*40)
    print("\n📊 Testing Urdu SEO...")
    seo_ur = SEOEngine(language="urdu", niche="tech")
    
    test_topic_ur = "Pakistan 5G Technology - Latest Updates"
    result_ur = seo_ur.generate_all_metadata(test_topic_ur)
    
    print(f"\n✅ Best Title (UR): {result_ur['best_title']}")
    print(f"📊 CTR Score: {result_ur['estimated_ctr']['score']}/100")
    print(f"\n🏷️ Tags ({len(result_ur['tags'])}):")
    for tag in result_ur['tags'][:5]:
        print(f"   - {tag}")
    
    seo_en.save_metadata(result_ur, "output/seo_test_ur.json")
    
    print("\n" + "="*60)
    print("✅ SEO Engine Test Complete!")
    print("📁 Check output/ folder for JSON files")
    print("="*60)