"""
✍️ AI SCRIPT GENERATOR
Uses Groq (Free Llama 3.3 70B) to write human-like scripts
Supports: English, Urdu, Hindi, Punjabi
Built-in humanization to bypass AI detection
"""
import os
import json
from typing import Dict, List
from loguru import logger
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ScriptGenerator:
    """Generate natural, human-style video scripts"""
    
    def __init__(self, language: str = "english", niche: str = "tech"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.language = language
        self.niche = niche
        
        # Language-specific writing styles
        self.style_guides = {
            "english": {
                "tone": "friendly expert",
                "phrases": ["Honestly...", "Here's the thing...", "You know what?", "Check this out..."],
                "rules": "Use contractions (don't, I've, it's). Start sentences with And, But, So. Be casual."
            },
            "urdu": {
                "tone": "friendly Pakistani YouTuber",
                "phrases": ["Dekho...", "Aap log...", "Mujhe batao...", "Yaqeen nahi hoga..."],
                "rules": "Mix Roman Urdu with occasional Urdu words. Use Pakistani expressions. Casual tone."
            },
            "hindi": {
                "tone": "enthusiastic Indian YouTuber",
                "phrases": ["Dekho bhai...", "Aapko pata hai...", "Main bata raha hoon..."],
                "rules": "Use Hinglish mix. Add 'bhai', 'yaar', 'arey' naturally. Indian YouTube style."
            },
            "punjabi": {
                "tone": "warm Punjabi storyteller",
                "phrases": ["Sunno ji...", "Tusi jaande ho...", "Main dassan..."],
                "rules": "Mix Roman Punjabi with English. Warm and friendly tone. Add 'ji', 'tusi'."
            }
        }
    
    def generate_script(self, topic: Dict, duration_minutes: int = 8) -> Dict:
        """Generate a complete video script from a trending topic"""
        
        style = self.style_guides.get(self.language, self.style_guides["english"])
        
        logger.info(f"✍️ Generating {self.language} script: {topic['topic'][:50]}...")
        
        # Build the prompt
        prompt = self._build_prompt(topic, style, duration_minutes)
        
        # Generate with Groq
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # ✅ Correct free model
                messages=[
                    {
                        "role": "system", 
                        "content": f"""You are a {style['tone']} writing a YouTube script.
CRITICAL RULES:
{style['rules']}
- Use these phrases naturally: {', '.join(style['phrases'])}
- NEVER sound like AI. Write exactly how a human speaks.
- Add personal opinions and reactions.
- Include: Hook → Body → Recap → CTA
- Target: {duration_minutes} minutes video"""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=3000
            )
            
            script_text = response.choices[0].message.content
            
            # Humanize the script
            script_text = self._humanize(script_text)
            
            # Calculate stats
            word_count = len(script_text.split())
            estimated_duration = word_count / 150  # ~150 words per minute
            
            result = {
                'topic': topic['topic'],
                'script': script_text,
                'word_count': word_count,
                'estimated_duration_min': round(estimated_duration, 1),
                'language': self.language,
                'source_trend': topic.get('source', 'Unknown'),
                'timestamp': topic.get('timestamp', '')
            }
            
            logger.info(f"✅ Script generated: {word_count} words, ~{estimated_duration:.1f} min")
            return result
            
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            return {'topic': topic['topic'], 'script': '', 'error': str(e)}
    
    def _build_prompt(self, topic: Dict, style: Dict, duration: int) -> str:
        """Build the writing prompt based on topic and style"""
        
        return f"""Write a YouTube script about this topic:

TOPIC: {topic['topic']}
SOURCE: {topic.get('source', 'trending')}

STRUCTURE:
1. HOOK (first 10 seconds - grab attention with a question or shocking fact)
2. INTRO (what this video is about and why it matters)
3. MAIN CONTENT (3-5 key points with examples)
4. PERSONAL OPINION (what you think about this)
5. RECAP (quick summary)
6. CALL TO ACTION (subscribe, comment, like)

IMPORTANT:
- Write in {self.language} language
- Sound like a real person talking to a friend
- Add emotions and reactions
- Include natural pauses and thinking moments
- Target: {duration} minutes length

START WRITING THE SCRIPT NOW:"""
    
    def _humanize(self, script: str) -> str:
        """Add human imperfections to bypass AI detection"""
        
        import random
        
        # Add natural fillers
        fillers = [
            "\n\n[chuckles] ",
            "\n\nWait, let me explain... ",
            "\n\nYou know what I mean? ",
            "\n\nHere's what's crazy... ",
            "\n\n[pause] ",
        ]
        
        lines = script.split('\n')
        humanized = []
        
        for i, line in enumerate(lines):
            humanized.append(line)
            # Add a filler every 3-5 paragraphs
            if i > 2 and i % random.randint(3, 5) == 0 and len(line) > 40:
                humanized.append(random.choice(fillers))
        
        return '\n'.join(humanized)
    
    def generate_multiple(self, topics: List[Dict], count: int = 3) -> List[Dict]:
        """Generate scripts for multiple topics"""
        scripts = []
        
        for topic in topics[:count]:
            script = self.generate_script(topic)
            if script and not script.get('error'):
                scripts.append(script)
        
        return scripts


# ============================================
# TEST THE MODULE
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("✍️  AI SCRIPT GENERATOR TEST")
    print("="*60)
    
    # Test 1: English Script
    print("\n📝 Generating English Script...")
    print("-"*60)
    
    gen = ScriptGenerator(language="english", niche="tech")
    
    test_topic = {
        'topic': 'Google Pixel battery drain issues and how to fix them',
        'source': 'Reddit Trending',
        'score': 95
    }
    
    result = gen.generate_script(test_topic, duration_minutes=5)
    
    if result.get('script'):
        # Show first 500 characters
        preview = result['script'][:500]
        print(preview)
        print(f"\n... (Total: {result['word_count']} words, ~{result['estimated_duration_min']} min)")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print("\n" + "="*60)
    
    # Test 2: Urdu Script (Quick)
    print("\n📝 Testing Urdu Script Generation...")
    print("-"*60)
    
    gen_ur = ScriptGenerator(language="urdu", niche="tech")
    
    test_topic_ur = {
        'topic': 'Pakistan main 5G technology ka aaghaz',
        'source': 'Google Trends PK',
        'score': 90
    }
    
    result_ur = gen_ur.generate_script(test_topic_ur, duration_minutes=3)
    
    if result_ur.get('script'):
        preview_ur = result_ur['script'][:300]
        print(preview_ur)
        print(f"\n... (Total: {result_ur['word_count']} words)")
    else:
        print(f"❌ Error: {result_ur.get('error')}")
    
    print("\n✅ Test Complete!")