"""
📖 AI STORY GENERATOR
Creates complete cartoon/animated stories with scenes
Uses Groq (Free Llama 3) for story creation
Output: Story with scene descriptions ready for image generation
"""
import os
import json
from typing import List, Dict
from loguru import logger
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:
    """Generate complete stories for cartoon/animated content"""
    
    def __init__(self, language: str = "english"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.language = language
    
    def generate_story(self, topic: str, num_scenes: int = 8, 
                       style: str = "cartoon") -> Dict:
        """Generate a complete story with scene descriptions"""
        
        logger.info(f"📖 Generating {style} story: {topic[:60]}...")
        
        prompt = f"""Create a complete {style} story about: {topic}

OUTPUT MUST BE VALID JSON with this exact structure:
{{{{
    "title": "Story Title",
    "genre": "{style}",
    "moral": "The moral of the story",
    "characters": [
        {{{{"name": "Character 1", "description": "visual description for AI image generation", "voice_type": "young/friendly/deep/etc"}}}}
    ],
    "scenes": [
        {{{{
            "scene_number": 1,
            "description": "Detailed visual scene description for AI image generation. Include colors, setting, characters, actions, mood. Be very specific and visual.",
            "narration": "The narration text for this scene (2-3 sentences)",
            "dialogue": "Character dialogue if any",
            "mood": "happy/sad/tense/exciting",
            "duration_seconds": 8
        }}}}
    ]
}}}}

Story Requirements:
- Number of scenes: {num_scenes}
- Make it engaging for YouTube audience
- Include a clear beginning, middle, and end
- Add emotional moments
- Make scene descriptions VERY VISUAL and DETAILED for AI image generation
- Language: {self.language}

IMPORTANT: Return ONLY valid JSON, no other text."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a professional story writer for animated YouTube content. You always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=4000
            )
            
            story_text = response.choices[0].message.content
            
            # Clean up JSON
            story_text = story_text.strip()
            if story_text.startswith("```json"):
                story_text = story_text[7:]
            if story_text.startswith("```"):
                story_text = story_text[3:]
            if story_text.endswith("```"):
                story_text = story_text[:-3]
            
            story = json.loads(story_text.strip())
            
            logger.info(f"✅ Story created: {story.get('title', 'Untitled')}")
            logger.info(f"   Scenes: {len(story.get('scenes', []))}")
            logger.info(f"   Characters: {len(story.get('characters', []))}")
            
            return story
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return {"error": "Failed to parse story JSON", "raw": story_text if 'story_text' in locals() else ""}
        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            return {"error": str(e)}
    
    def story_to_scenes(self, story: Dict) -> List[Dict]:
        """Extract scene descriptions for image generation"""
        
        scenes = []
        for scene in story.get("scenes", []):
            scenes.append({
                "scene_number": scene.get("scene_number", 0),
                "description": scene.get("description", ""),
                "narration": scene.get("narration", ""),
                "dialogue": scene.get("dialogue", ""),
                "mood": scene.get("mood", "neutral"),
                "duration": scene.get("duration_seconds", 8)
            })
        
        return scenes
    
    def story_to_narration(self, story: Dict) -> str:
        """Combine all narrations into a single voiceover script"""
        
        parts = []
        
        # Title intro
        parts.append(f"{story.get('title', 'A Story')}")
        parts.append("")
        
        # Each scene
        for scene in story.get("scenes", []):
            narration = scene.get("narration", "")
            dialogue = scene.get("dialogue", "")
            
            if narration:
                parts.append(narration)
            if dialogue:
                parts.append(dialogue)
            parts.append("")  # Pause between scenes
        
        full_script = " ".join(parts)
        
        logger.info(f"📝 Narration script: {len(full_script.split())} words")
        return full_script


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("📖  AI STORY GENERATOR TEST")
    print("="*60)
    
    gen = StoryGenerator(language="english")
    
    # Test story
    print("\n📝 Generating cartoon story...")
    story = gen.generate_story(
        topic="a brave little cat who saves his village from a storm",
        num_scenes=6,
        style="cartoon"
    )
    
    if story and "error" not in story:
        print(f"\n📚 Title: {story.get('title')}")
        print(f"🎭 Genre: {story.get('genre')}")
        print(f"💡 Moral: {story.get('moral')}")
        print(f"\n👥 Characters:")
        for char in story.get('characters', []):
            print(f"   - {char.get('name')}: {char.get('description', '')[:80]}...")
        
        print(f"\n🎬 Scenes ({len(story.get('scenes', []))}):")
        for scene in story.get('scenes', []):
            print(f"   Scene {scene.get('scene_number')}: {scene.get('description', '')[:100]}...")
            print(f"   Mood: {scene.get('mood')} | Duration: {scene.get('duration_seconds')}s")
        
        # Get narration
        print("\n📝 Generating narration script...")
        narration = gen.story_to_narration(story)
        print(f"   Narration words: {len(narration.split())}")
        print(f"   Preview: {narration[:200]}...")
        
        # Save story
        with open("output/story_test.json", "w", encoding="utf-8") as f:
            json.dump(story, f, indent=2, ensure_ascii=False)
        print("\n✅ Story saved: output/story_test.json")
    else:
        print(f"\n❌ Error: {story.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)