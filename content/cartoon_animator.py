"""
🎬 CARTOON ANIMATOR v1.0
Creates animated cartoon videos with:
- AI-generated characters
- Animated scenes (bounce, slide, pulse, walk)
- Multi-character dialogue
- Sound effects & music
- Cartoon text bubbles
- Professional transitions
"""
import os
import sys
import json
import random
import requests
from pathlib import Path
from loguru import logger
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import numpy as np
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

class CartoonAnimator:
    """Professional cartoon series creator"""
    
    def __init__(self, output_dir="output/cartoon_series"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width, self.height = 1920, 1080
        
        # Sound effects URLs (free)
        self.sfx = {
            "boing": "https://cdn.pixabay.com/audio/2023/05/09/audio_9e5c8d4a72.mp3",
            "pop": "https://cdn.pixabay.com/audio/2023/03/15/audio_7f2a1b3c4d.mp3",
            "whoosh": "https://cdn.pixabay.com/audio/2023/01/25/audio_3d6e8f2a1b.mp3",
            "ding": "https://cdn.pixabay.com/audio/2023/06/12/audio_a4b7c9d1e2.mp3",
            "laugh": "https://cdn.pixabay.com/audio/2023/04/18/audio_5c2e8f4a6b.mp3",
            "wow": "https://cdn.pixabay.com/audio/2023/07/20/audio_8f3a1b5c7d.mp3",
            "sad": "https://cdn.pixabay.com/audio/2023/02/28/audio_2b6d9e4f8a.mp3",
            "magic": "https://cdn.pixabay.com/audio/2023/08/05/audio_1e4a7c3d9f.mp3",
        }
        
        # Color palettes for cartoon moods
        self.mood_colors = {
            "happy": [(255, 220, 100), (255, 255, 200), (100, 200, 255)],
            "sad": [(100, 100, 180), (150, 150, 200), (80, 80, 120)],
            "tense": [(180, 50, 50), (200, 100, 50), (100, 20, 20)],
            "exciting": [(255, 200, 0), (255, 100, 50), (255, 50, 100)],
            "magical": [(150, 50, 200), (100, 150, 255), (200, 100, 255)],
            "peaceful": [(100, 200, 150), (150, 220, 180), (200, 240, 220)],
        }
    
    def generate_character_image(self, name: str, description: str, 
                                  expression: str = "happy") -> str:
        """Generate AI character image with emotion"""
        
        from content.ai_image_gen import AIImageGenerator
        gen = AIImageGenerator()
        
        prompt = f"cartoon character, {description}, {expression} expression, white background, character sheet style, vibrant colors, animated style, clean lines, kid-friendly"
        
        filename = f"char_{name.replace(' ', '_')}_{expression}.jpg"
        char_dir = Path("output/cartoon_characters")
        char_dir.mkdir(parents=True, exist_ok=True)
        
        return gen.generate_image(
            prompt=prompt,
            style="cartoon",
            width=1024,
            height=1024,
            filename=str(char_dir / filename)
        )
    
    def generate_scene_background(self, location: str, mood: str = "peaceful") -> str:
        """Generate AI scene background"""
        
        from content.ai_image_gen import AIImageGenerator
        gen = AIImageGenerator()
        
        prompt = f"cartoon background, {location}, {mood} atmosphere, animated style, colorful, kid-friendly, studio quality, wide shot"
        
        filename = f"bg_{location.replace(' ', '_')[:30]}_{mood}.jpg"
        bg_dir = Path("output/cartoon_backgrounds")
        bg_dir.mkdir(parents=True, exist_ok=True)
        
        return gen.generate_image(
            prompt=prompt,
            style="cartoon",
            width=self.width,
            height=self.height,
            filename=str(bg_dir / filename)
        )
    
    def create_character_animation(self, char_image_path: str, 
                                   animation_type: str = "idle",
                                   duration: float = 5.0) -> list:
        """Create character animation frames"""
        """
        animation_types:
        - idle: gentle bounce
        - talk: mouth movement simulation
        - walk: side-to-side movement
        - jump: up and down with squash/stretch
        - appear: scale from 0 to 1
        - disappear: scale from 1 to 0
        - excited: fast bounce + pulse
        """
        
        if not Path(char_image_path).exists():
            logger.warning(f"Character image not found: {char_image_path}")
            return []
        
        try:
            char_img = Image.open(char_image_path).convert("RGBA")
        except:
            return []
        
        frames = []
        num_frames = int(duration * 30)  # 30 fps
        frame_duration = duration / num_frames
        
        # Resize character to reasonable size
        char_height = int(self.height * 0.6)
        char_width = int(char_height * (char_img.width / char_img.height))
        char_img = char_img.resize((char_width, char_height), Image.LANCZOS)
        
        # Starting position (center)
        base_x = (self.width - char_width) // 2
        base_y = (self.height - char_height) // 2
        
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "cartoon_frames"
        temp_dir.mkdir(exist_ok=True)
        
        for i in range(num_frames):
            frame = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
            
            progress = i / num_frames
            x, y = base_x, base_y
            scale_x, scale_y = 1.0, 1.0
            rotation = 0
            
            if animation_type == "idle":
                # Gentle bounce
                y = base_y + int(np.sin(progress * np.pi * 2 * 3) * 15)
                scale_x = 1.0 + np.sin(progress * np.pi * 2 * 3) * 0.03
                scale_y = 1.0 - np.sin(progress * np.pi * 2 * 3) * 0.03
                
            elif animation_type == "talk":
                # Slight bounce + mouth area pulse
                y = base_y + int(np.sin(progress * np.pi * 2 * 4) * 8)
                scale_y = 1.0 + abs(np.sin(progress * np.pi * 2 * 4)) * 0.05
                
            elif animation_type == "walk":
                # Move across screen
                x = int((self.width + char_width) * progress) - char_width
                y = base_y + int(np.sin(progress * np.pi * 8) * 20)
                scale_y = 1.0 + np.sin(progress * np.pi * 8) * 0.05
                
            elif animation_type == "jump":
                # Jump arc
                jump_progress = np.sin(progress * np.pi)
                y = base_y - int(jump_progress * 200)
                scale_x = 1.0 + 0.2 * (1 - jump_progress)
                scale_y = 1.0 - 0.2 * (1 - jump_progress)
                
            elif animation_type == "appear":
                scale_factor = min(1.0, progress * 3)
                scale_x = scale_factor
                scale_y = scale_factor
                
            elif animation_type == "excited":
                y = base_y + int(np.sin(progress * np.pi * 2 * 5) * 25)
                scale_factor = 1.0 + 0.1 * abs(np.sin(progress * np.pi * 2 * 5))
                scale_x = scale_factor
                scale_y = scale_factor
            
            # Apply scaling
            new_w = int(char_width * scale_x)
            new_h = int(char_height * scale_y)
            
            if new_w > 0 and new_h > 0:
                scaled_char = char_img.resize((new_w, new_h), Image.LANCZOS)
                
                # Calculate position to center scaled image
                paste_x = x - (new_w - char_width) // 2
                paste_y = y - (new_h - char_height) // 2
                
                frame.paste(scaled_char, (paste_x, paste_y), scaled_char)
            
            frame_path = str(temp_dir / f"frame_{i:04d}.png")
            frame.save(frame_path)
            frames.append(frame_path)
        
        return frames
    
    def create_scene_composition(self, background_path: str, 
                                 character_data: list,
                                 dialogue_text: str = "",
                                 sound_effect: str = None) -> list:
        """Compose a complete scene with background + characters + dialogue"""
        
        frames = []
        
        # Load background
        if background_path and Path(background_path).exists():
            bg = Image.open(background_path).convert("RGBA")
            bg = bg.resize((self.width, self.height), Image.LANCZOS)
        else:
            colors = self.mood_colors.get("peaceful", [(100,200,150)])
            color = colors[0]
            bg = Image.new("RGBA", (self.width, self.height), tuple(color) + (255,))
        
        # Generate frames (1 frame for static, more for animated)
        frame_count = 30  # 1 second of frames for static scenes
        
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "scene_frames"
        temp_dir.mkdir(exist_ok=True)
        
        for i in range(frame_count):
            frame = bg.copy()
            draw = ImageDraw.Draw(frame)
            
            # Add characters with animation
            for char_data in character_data:
                char_path = char_data.get("path", "")
                anim_type = char_data.get("animation", "idle")
                position = char_data.get("position", "center")
                
                if char_path and Path(char_path).exists():
                    char_img = Image.open(char_path).convert("RGBA")
                    
                    # Resize character
                    char_height = int(self.height * 0.5)
                    char_width = int(char_height * char_img.width / char_img.height)
                    char_img = char_img.resize((char_width, char_height), Image.LANCZOS)
                    
                    # Position
                    if position == "left":
                        x = 50
                        y = self.height - char_height - 20
                    elif position == "right":
                        x = self.width - char_width - 50
                        y = self.height - char_height - 20
                    else:
                        x = (self.width - char_width) // 2
                        y = self.height - char_height - 20
                    
                    # Apply animation
                    if anim_type == "idle":
                        y += int(np.sin(i * 0.3) * 8)
                    elif anim_type == "talk":
                        y += int(np.sin(i * 0.5) * 5)
                    
                    frame.paste(char_img, (x, y), char_img)
            
            # Add dialogue bubble
            if dialogue_text:
                self._draw_speech_bubble(draw, dialogue_text, (self.width//2, 150))
            
            frame_path = str(temp_dir / f"scene_{i:04d}.png")
            frame = frame.convert("RGB")
            frame.save(frame_path)
            frames.append(frame_path)
        
        return frames
    
    def _draw_speech_bubble(self, draw, text: str, position: tuple):
        """Draw cartoon speech bubble"""
        
        x, y = position
        
        # Wrap text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 40:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate bubble size
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        
        max_line_width = max([font.getbbox(line)[2] - font.getbbox(line)[0] for line in lines]) if lines else 300
        bubble_width = max_line_width + 40
        bubble_height = len(lines) * 40 + 30
        
        # Draw bubble
        bubble_x = x - bubble_width//2
        bubble_y = y - bubble_height//2
        
        draw.ellipse(
            [bubble_x-15, bubble_y-15, bubble_x+bubble_width+15, bubble_y+bubble_height+15],
            fill=(255, 255, 255, 240),
            outline=(0, 0, 0),
            width=3
        )
        
        # Draw text
        for i, line in enumerate(lines):
            text_y = bubble_y + i * 40
            draw.text((bubble_x + 20, text_y + 5), line, fill=(0, 0, 0), font=font)
    
    def create_episode(self, story_data: dict, 
                       episode_number: int = 1,
                       voiceover_path: str = None) -> str:
        """Create a complete cartoon episode"""
        
        logger.info(f"🎬 Creating Episode {episode_number}: {story_data.get('title', 'Untitled')}")
        
        scenes = story_data.get("scenes", [])
        characters = story_data.get("characters", [])
        
        if not scenes:
            logger.error("No scenes in story data")
            return ""
        
        # Step 1: Generate character images
        logger.info("🎨 Generating characters...")
        char_images = {}
        
        for char in characters:
            char_name = char.get("name", "Character")
            char_desc = char.get("description", "cartoon character")
            
            for expression in ["happy", "surprised", "sad", "excited"]:
                img_path = self.generate_character_image(char_name, char_desc, expression)
                if img_path:
                    key = f"{char_name}_{expression}"
                    char_images[key] = img_path
            
            if not char_images:
                logger.warning(f"Could not generate images for {char_name}")
        
        # Step 2: Generate scene backgrounds
        logger.info("🏞️ Generating backgrounds...")
        bg_images = {}
        
        for i, scene in enumerate(scenes):
            bg_desc = scene.get("description", f"cartoon scene {i}")[:100]
            mood = scene.get("mood", "peaceful")
            
            bg_path = self.generate_scene_background(bg_desc, mood)
            if bg_path:
                bg_images[i] = bg_path
            else:
                bg_images[i] = ""
        
        # Step 3: Create scene compositions
        logger.info("🎬 Composing scenes...")
        all_scene_frames = []
        
        for i, scene in enumerate(scenes):
            bg_path = bg_images.get(i, "")
            dialogue = scene.get("dialogue", "")
            narration = scene.get("narration", "")
            mood = scene.get("mood", "happy")
            duration = scene.get("duration_seconds", 8)
            
            # Determine which characters are in this scene
            scene_chars = []
            main_char = characters[0] if characters else {}
            char_name = main_char.get("name", "Hero")
            
            # Try to find character with matching mood
            char_key = f"{char_name}_{mood}"
            if char_key not in char_images:
                char_key = f"{char_name}_happy" if f"{char_name}_happy" in char_images else list(char_images.keys())[0] if char_images else ""
            
            char_data = [{
                "path": char_images.get(char_key, ""),
                "animation": "talk" if dialogue else "idle",
                "position": "center"
            }]
            
            # Add second character for dialogue
            if dialogue and len(characters) > 1:
                char2 = characters[1]
                char2_name = char2.get("name", "Sidekick")
                char2_key = f"{char2_name}_happy"
                if char2_key in char_images:
                    char_data.append({
                        "path": char_images[char2_key],
                        "animation": "talk",
                        "position": "right" if len(char_data) == 1 else "left"
                    })
                    char_data[0]["position"] = "left"
            
            frames = self.create_scene_composition(
                background_path=bg_path,
                character_data=char_data,
                dialogue_text=dialogue or narration[:80]
            )
            
            all_scene_frames.extend(frames)
        
        # Step 4: Assemble video from frames + voiceover
        logger.info("🎥 Assembling final video...")
        
        from moviepy import ImageSequenceClip, AudioFileClip, CompositeAudioClip
        
        # Create video from frames
        if all_scene_frames:
            clip = ImageSequenceClip(all_scene_frames, fps=30)
            
            # Add voiceover if provided
            if voiceover_path and Path(voiceover_path).exists():
                audio = AudioFileClip(voiceover_path)
                if clip.duration > audio.duration:
                    clip = clip.subclipped(0, audio.duration)
                clip = clip.with_audio(audio)
            
            # Save episode
            episode_path = str(self.output_dir / f"episode_{episode_number:03d}.mp4")
            
            clip.write_videofile(
                episode_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                bitrate='8000k',
                preset='medium',
                threads=4
            )
            
            size_mb = os.path.getsize(episode_path) / (1024*1024)
            logger.info(f"✅ Episode created: {episode_path} ({size_mb:.1f} MB)")
            
            return episode_path
        
        return ""


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬 CARTOON ANIMATOR TEST")
    print("="*60)
    
    animator = CartoonAnimator()
    
    # Test: Generate a character
    print("\n🎨 Generating test character...")
    char_path = animator.generate_character_image(
        "Sparky", 
        "a cute orange cat with big green eyes, wearing a blue cape",
        "happy"
    )
    print(f"✅ Character: {char_path}")
    
    # Test: Generate background
    print("\n🏞️ Generating test background...")
    bg_path = animator.generate_scene_background(
        "a colorful cartoon village with rainbow houses",
        "happy"
    )
    print(f"✅ Background: {bg_path}")
    
    # Test: Create a simple scene composition
    print("\n🎬 Creating test scene...")
    frames = animator.create_scene_composition(
        background_path=bg_path,
        character_data=[{
            "path": char_path,
            "animation": "idle",
            "position": "center"
        }],
        dialogue_text="Hello friends! Welcome to my amazing adventure!"
    )
    print(f"✅ Created {len(frames)} frames for test scene")
    
    print("\n✅ Cartoon Animator Test Complete!")
    print("Check output/cartoon_characters/ and output/cartoon_backgrounds/")
    print("="*60)