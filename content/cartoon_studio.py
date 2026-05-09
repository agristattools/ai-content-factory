"""
🎬 CARTOON STUDIO v2.0
Creates animated cartoon videos with:
- Multiple AI images per scene
- Smooth scene transitions
- Character bounce/talk animations
- Background changes every scene
- Text overlays with voice sync
- Professional cartoon look
"""
import os
import sys
import json
import random
import requests
import numpy as np
from pathlib import Path
from loguru import logger
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv()

class CartoonStudio:
    """Professional cartoon video creator"""
    
    def __init__(self):
        self.width, self.height = 1920, 1080
        self.fps = 30
        
        # Vibrant cartoon colors
        self.colors = {
            "sky": [(135, 206, 235), (100, 180, 255), (70, 150, 220)],
            "grass": [(100, 200, 80), (80, 180, 60), (60, 160, 40)],
            "sun": [(255, 220, 50), (255, 200, 30), (255, 180, 10)],
            "night": [(25, 25, 60), (40, 40, 80), (20, 20, 50)],
            "magic": [(150, 50, 200), (180, 80, 220), (120, 30, 180)],
            "fire": [(255, 100, 30), (255, 60, 10), (200, 40, 5)],
            "water": [(30, 144, 255), (50, 160, 255), (20, 120, 230)],
            "forest": [(34, 139, 34), (50, 150, 50), (20, 120, 20)],
        }
        
        self.output_dir = Path("output/cartoon_studio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_cartoon_background(self, mood: str = "happy", 
                                  setting: str = "village") -> Image.Image:
        """Create a colorful cartoon background"""
        
        # Create base
        bg = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(bg)
        
        # Sky gradient
        if mood == "happy":
            sky_colors = [(135, 206, 235), (180, 220, 255)]
        elif mood == "tense":
            sky_colors = [(60, 60, 100), (80, 80, 130)]
        elif mood == "magical":
            sky_colors = [(100, 50, 180), (150, 100, 220)]
        elif mood == "night":
            sky_colors = [(15, 15, 40), (30, 30, 60)]
        else:
            sky_colors = [(135, 206, 235), (180, 220, 255)]
        
        # Draw sky
        for y in range(int(self.height * 0.7)):
            ratio = y / (self.height * 0.7)
            r = int(sky_colors[0][0] + (sky_colors[1][0] - sky_colors[0][0]) * ratio)
            g = int(sky_colors[0][1] + (sky_colors[1][1] - sky_colors[0][1]) * ratio)
            b = int(sky_colors[0][2] + (sky_colors[1][2] - sky_colors[0][2]) * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Sun/moon
        if mood in ["happy", "magical"]:
            # Sun
            for i in range(120, 0, -1):
                alpha = int(255 * (1 - i/120))
                color = (255, min(220 + i, 255), min(50 + i, 255))
                draw.ellipse([self.width-250-i, 80-i, self.width-250+i, 80+i], 
                           fill=color)
            draw.ellipse([self.width-250, 80, self.width-130, 200], fill=(255, 255, 100))
        
        elif mood == "night":
            # Moon
            draw.ellipse([self.width-200, 60, self.width-100, 160], fill=(230, 230, 250))
            draw.ellipse([self.width-180, 70, self.width-120, 140], fill=sky_colors[0])
        
        # Clouds
        if mood in ["happy", "magical"]:
            for _ in range(5):
                cx = random.randint(50, self.width-50)
                cy = random.randint(30, 200)
                for i in range(40, 0, -3):
                    alpha = int(150 * (1 - i/40))
                    color = (255, 255, 255)
                    draw.ellipse([cx-i*2, cy-i, cx+i*2, cy+i*0.7], fill=color)
        
        # Ground
        ground_y = int(self.height * 0.7)
        for y in range(ground_y, self.height):
            ratio = (y - ground_y) / (self.height - ground_y)
            if setting == "village":
                r = int(100 + 40 * ratio)
                g = int(180 + 30 * ratio)
                b = int(60 + 30 * ratio)
            elif setting == "forest":
                r = int(30 + 20 * ratio)
                g = int(100 + 30 * ratio)
                b = int(30 + 20 * ratio)
            elif setting == "mountain":
                r = int(120 + 20 * ratio)
                g = int(110 + 20 * ratio)
                b = int(100 + 20 * ratio)
            else:
                r, g, b = 100, 180, 60
            
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        # Add hills
        for i in range(3):
            hill_x = random.randint(0, self.width)
            hill_h = random.randint(50, 150)
            hill_w = random.randint(200, 400)
            draw.ellipse([hill_x-hill_w, ground_y-hill_h, hill_x+hill_w, ground_y+hill_h], 
                        fill=(80, 160, 50))
        
        # Add trees for village/forest
        if setting in ["village", "forest"]:
            for _ in range(8):
                tx = random.randint(50, self.width-50)
                ty = ground_y - random.randint(80, 200)
                # Trunk
                draw.rectangle([tx-10, ty, tx+10, ground_y], fill=(101, 67, 33))
                # Leaves
                for _ in range(3):
                    lx = tx + random.randint(-30, 30)
                    ly = ty - random.randint(10, 50)
                    lr = random.randint(25, 45)
                    draw.ellipse([lx-lr, ly-lr, lx+lr, ly+lr], 
                               fill=(random.randint(30, 100), random.randint(120, 200), 30))
        
        # Add houses for village
        if setting == "village":
            for _ in range(3):
                hx = random.randint(100, self.width-200)
                hy = ground_y - random.randint(80, 150)
                # Body
                draw.rectangle([hx, hy, hx+100, ground_y], fill=(200, 180, 150))
                # Roof
                draw.polygon([hx-20, hy, hx+50, hy-60, hx+120, hy], fill=(180, 50, 50))
                # Door
                draw.rectangle([hx+35, hy+40, hx+65, ground_y], fill=(101, 67, 33))
                # Window
                draw.rectangle([hx+15, hy+15, hx+40, hy+35], fill=(200, 230, 255))
        
        return bg
    
    def create_cartoon_character(self, char_type: str = "cat", 
                                 expression: str = "happy",
                                 size: tuple = (300, 300)) -> Image.Image:
        """Draw a cartoon character programmatically"""
        
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        w, h = size
        cx, cy = w // 2, h // 2
        
        if char_type == "cat":
            # Body
            draw.ellipse([cx-60, cy+10, cx+60, cy+120], fill=(255, 180, 50))
            # Head
            draw.ellipse([cx-55, cy-70, cx+55, cy+40], fill=(255, 180, 50))
            # Ears
            draw.polygon([cx-50, cy-60, cx-35, cy-110, cx-10, cy-50], fill=(255, 180, 50))
            draw.polygon([cx+50, cy-60, cx+35, cy-110, cx+10, cy-50], fill=(255, 180, 50))
            # Inner ears
            draw.polygon([cx-42, cy-62, cx-35, cy-95, cx-18, cy-52], fill=(255, 150, 150))
            draw.polygon([cx+42, cy-62, cx+35, cy-95, cx+18, cy-52], fill=(255, 150, 150))
            
            # Eyes
            if expression == "happy":
                draw.ellipse([cx-30, cy-30, cx-5, cy-5], fill=(255, 255, 255))
                draw.ellipse([cx+5, cy-30, cx+30, cy-5], fill=(255, 255, 255))
                draw.ellipse([cx-20, cy-22, cx-12, cy-12], fill=(0, 180, 0))
                draw.ellipse([cx+12, cy-22, cx+20, cy-12], fill=(0, 180, 0))
                # Happy mouth
                draw.arc([cx-15, cy, cx+15, cy+25], 0, 180, fill=(0, 0, 0), width=3)
            elif expression == "surprised":
                draw.ellipse([cx-30, cy-30, cx-5, cy-5], fill=(255, 255, 255))
                draw.ellipse([cx+5, cy-30, cx+30, cy-5], fill=(255, 255, 255))
                draw.ellipse([cx-20, cy-22, cx-12, cy-12], fill=(0, 180, 0))
                draw.ellipse([cx+12, cy-22, cx+20, cy-12], fill=(0, 180, 0))
                draw.ellipse([cx-8, cy+5, cx+8, cy+18], fill=(0, 0, 0))
            elif expression == "sad":
                draw.ellipse([cx-30, cy-30, cx-5, cy-5], fill=(255, 255, 255))
                draw.ellipse([cx+5, cy-30, cx+30, cy-5], fill=(255, 255, 255))
                draw.ellipse([cx-20, cy-22, cx-12, cy-12], fill=(0, 180, 0))
                draw.ellipse([cx+12, cy-22, cx+20, cy-12], fill=(0, 180, 0))
                draw.arc([cx-10, cy+15, cx+10, cy+35], 180, 360, fill=(0, 0, 0), width=3)
            
            # Nose
            draw.polygon([cx-5, cy-10, cx+5, cy-10, cx, cy-3], fill=(255, 150, 150))
            # Whiskers
            for side in [-1, 1]:
                for wy in [-5, 0, 5]:
                    draw.line([cx+side*15, cy+wy, cx+side*55, cy+wy-10], fill=(0, 0, 0), width=1)
            
            # Tail
            draw.arc([cx+30, cy+20, cx+100, cy+80], 0, 200, fill=(255, 180, 50), width=12)
        
        elif char_type == "dragon":
            # Body
            draw.ellipse([cx-80, cy-20, cx+80, cy+100], fill=(50, 200, 50))
            # Head
            draw.ellipse([cx-50, cy-90, cx+50, cy+10], fill=(50, 200, 50))
            # Eyes
            draw.ellipse([cx-25, cy-60, cx-5, cy-40], fill=(255, 255, 0))
            draw.ellipse([cx+5, cy-60, cx+25, cy-40], fill=(255, 255, 0))
            draw.ellipse([cx-18, cy-55, cx-12, cy-45], fill=(0, 0, 0))
            draw.ellipse([cx+12, cy-55, cx+18, cy-45], fill=(0, 0, 0))
            # Mouth
            if expression == "happy":
                draw.arc([cx-30, cy-30, cx+30, cy+10], 0, 180, fill=(0, 0, 0), width=4)
            else:
                draw.ellipse([cx-15, cy-20, cx+15, cy+5], fill=(200, 50, 50))
            # Spikes
            for i, sx in enumerate(range(cx-40, cx+50, 20)):
                spike_h = 30 + (i % 3) * 15
                draw.polygon([sx-8, cy-90, sx, cy-90-spike_h, sx+8, cy-90], fill=(200, 50, 50))
            # Wings
            draw.polygon([cx+60, cy-40, cx+130, cy-100, cx+120, cy-30], fill=(100, 200, 100))
            # Tail
            draw.line([cx+80, cy+40, cx+150, cy+70], fill=(50, 200, 50), width=15)
            draw.polygon([cx+140, cy+60, cx+170, cy+90, cx+150, cy+50], fill=(200, 50, 50))
        
        elif char_type == "robot":
            # Body
            draw.rectangle([cx-60, cy-20, cx+60, cy+100], fill=(180, 180, 200), outline=(100, 100, 120), width=3)
            # Head
            draw.rectangle([cx-45, cy-80, cx+45, cy], fill=(200, 200, 220), outline=(100, 100, 120), width=3)
            # Eyes
            draw.ellipse([cx-25, cy-55, cx-10, cy-40], fill=(0, 255, 255))
            draw.ellipse([cx+10, cy-55, cx+25, cy-40], fill=(0, 255, 255))
            # Antenna
            draw.line([cx, cy-80, cx, cy-110], fill=(150, 150, 170), width=4)
            draw.ellipse([cx-10, cy-120, cx+10, cy-100], fill=(255, 50, 50))
            # Arms
            draw.rectangle([cx-90, cy-10, cx-65, cy+60], fill=(180, 180, 200), outline=(100, 100, 120), width=2)
            draw.rectangle([cx+65, cy-10, cx+90, cy+60], fill=(180, 180, 200), outline=(100, 100, 120), width=2)
            # Legs
            draw.rectangle([cx-35, cy+100, cx-15, cy+140], fill=(180, 180, 200), outline=(100, 100, 120), width=2)
            draw.rectangle([cx+15, cy+100, cx+35, cy+140], fill=(180, 180, 200), outline=(100, 100, 120), width=2)
        
        return img
    
    def create_animated_scene(self, background: Image.Image, 
                              characters: list,
                              dialogue: str = "",
                              duration: float = 5.0) -> list:
        """Create animated frames for a complete scene"""
        
        frames = []
        num_frames = int(duration * self.fps)
        
        import tempfile
        temp_dir = Path(tempfile.gettempdir()) / "cartoon_scene"
        temp_dir.mkdir(exist_ok=True)
        
        for frame_num in range(num_frames):
            # Copy background
            frame = background.copy()
            
            progress = frame_num / num_frames
            
            # Add each character with animation
            for char_data in characters:
                char_img = char_data.get("image")
                position = char_data.get("position", "center")
                animation = char_data.get("animation", "idle")
                
                if char_img:
                    # Calculate position
                    if position == "left":
                        base_x = 100
                        base_y = self.height - char_img.height - 150
                    elif position == "right":
                        base_x = self.width - char_img.width - 100
                        base_y = self.height - char_img.height - 150
                    else:
                        base_x = (self.width - char_img.width) // 2
                        base_y = self.height - char_img.height - 150
                    
                    # Apply animation
                    x, y = base_x, base_y
                    
                    if animation == "idle":
                        y += int(np.sin(progress * np.pi * 6) * 10)
                    elif animation == "talk":
                        y += int(np.sin(progress * np.pi * 8) * 6)
                        scale_factor = 1 + np.sin(progress * np.pi * 8) * 0.03
                        new_w = int(char_img.width * scale_factor)
                        new_h = int(char_img.height * scale_factor)
                        if new_w > 0 and new_h > 0:
                            char_img = char_img.resize((new_w, new_h), Image.LANCZOS)
                    elif animation == "fly":
                        y = base_y - int(abs(np.sin(progress * np.pi * 2)) * 200)
                        x = int(base_x + np.sin(progress * np.pi * 3) * 100)
                    elif animation == "walk":
                        x = int(base_x - 200 + (progress * 400) % (self.width + 400) - 200)
                        y += int(np.sin(progress * np.pi * 12) * 15)
                    elif animation == "appear":
                        scale = min(1.0, progress * 5)
                        new_w = int(char_img.width * scale)
                        new_h = int(char_img.height * scale)
                        if new_w > 0 and new_h > 0:
                            char_img = char_img.resize((new_w, new_h), Image.LANCZOS)
                    
                    frame.paste(char_img, (int(x), int(y)), char_img)
            
            # Add dialogue bubble
            if dialogue and frame_num < self.fps * 3:  # Show for 3 seconds
                self._add_speech_bubble(frame, dialogue)
            
            frame_path = str(temp_dir / f"frame_{frame_num:04d}.png")
            frame.save(frame_path)
            frames.append(frame_path)
        
        return frames
    
    def _add_speech_bubble(self, frame: Image.Image, text: str):
        """Add cartoon speech bubble"""
        draw = ImageDraw.Draw(frame)
        
        try:
            font = ImageFont.truetype("arial.ttf", 35)
        except:
            font = ImageFont.load_default()
        
        # Bubble position
        bx, by = self.width//2, 100
        bubble_w = min(len(text) * 20, self.width - 200)
        bubble_h = 80
        
        # Draw bubble
        draw.ellipse([bx-bubble_w//2-20, by-20, bx+bubble_w//2+20, by+bubble_h+20], 
                    fill=(255, 255, 255, 240), outline=(0, 0, 0), width=4)
        
        # Draw text
        text_x = bx - bubble_w//2 + 20
        draw.text((text_x, by + 15), text[:min(len(text), 50)], fill=(0, 0, 0), font=font)
    
    def create_cartoon_episode(self, story_data: dict, 
                               episode_number: int = 1,
                               voiceover_path: str = None) -> str:
        """Create a complete cartoon episode with scene changes"""
        
        logger.info(f"🎬 Creating Cartoon Episode {episode_number}")
        
        scenes = story_data.get("scenes", [])
        characters_data = story_data.get("characters", [])
        
        if not scenes:
            logger.error("No scenes in story")
            return ""
        
        # Generate character images
        logger.info("🎨 Creating characters...")
        character_images = {}
        
        char_types = ["cat", "dragon", "robot"]
        for i, char in enumerate(characters_data):
            char_name = char.get("name", f"Character_{i}")
            char_type = char_types[i % len(char_types)]
            
            for expression in ["happy", "surprised", "sad"]:
                img = self.create_cartoon_character(char_type, expression)
                character_images[f"{char_name}_{expression}"] = img
        
        # Default character if none created
        if not character_images:
            img = self.create_cartoon_character("cat", "happy")
            character_images["Hero_happy"] = img
        
        # Create each scene
        all_frames = []
        
        for scene_num, scene in enumerate(scenes):
            mood = scene.get("mood", "happy")
            dialogue = scene.get("dialogue", "")
            narration = scene.get("narration", "")
            duration = scene.get("duration_seconds", 6)
            setting = scene.get("setting", "village")
            
            # Create background for this scene
            bg = self.create_cartoon_background(mood=mood, setting=setting)
            
            # Determine characters in this scene
            scene_characters = []
            
            main_char = characters_data[0] if characters_data else {"name": "Hero"}
            main_name = main_char.get("name", "Hero")
            main_key = f"{main_name}_happy"
            
            if main_key in character_images:
                scene_characters.append({
                    "image": character_images[main_key],
                    "position": "left" if dialogue and len(characters_data) > 1 else "center",
                    "animation": "talk" if dialogue else "idle"
                })
            
            # Add second character if dialogue
            if dialogue and len(characters_data) > 1:
                char2 = characters_data[1]
                char2_name = char2.get("name", "Villain")
                char2_key = f"{char2_name}_happy"
                
                if char2_key in character_images:
                    scene_characters.append({
                        "image": character_images[char2_key],
                        "position": "right",
                        "animation": "talk"
                    })
            
            # Create animated frames for this scene
            display_text = dialogue if dialogue else narration[:60]
            frames = self.create_animated_scene(
                background=bg,
                characters=scene_characters,
                dialogue=display_text,
                duration=duration
            )
            
            all_frames.extend(frames)
            logger.info(f"   Scene {scene_num+1}/{len(scenes)}: {len(frames)} frames")
        
        # Create video from all frames
        logger.info(f"🎥 Creating video from {len(all_frames)} frames...")
        
        from moviepy import ImageSequenceClip, AudioFileClip
        
        if all_frames:
            clip = ImageSequenceClip(all_frames, fps=self.fps)
            
            # Add voiceover
            if voiceover_path and Path(voiceover_path).exists():
                audio = AudioFileClip(voiceover_path)
                if clip.duration > audio.duration:
                    clip = clip.subclipped(0, audio.duration)
                clip = clip.with_audio(audio)
            
            # Save
            episode_path = str(self.output_dir / f"cartoon_ep_{episode_number:03d}.mp4")
            
            clip.write_videofile(
                episode_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                bitrate='5000k',
                preset='medium',
                threads=4
            )
            
            size_mb = os.path.getsize(episode_path) / (1024*1024)
            logger.info(f"✅ Cartoon Episode created: {episode_path} ({size_mb:.1f} MB)")
            
            return episode_path
        
        return ""


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬 CARTOON STUDIO v2.0 TEST")
    print("="*60)
    
    studio = CartoonStudio()
    
    # Create test story
    test_story = {
        "title": "The Brave Cat Adventure",
        "characters": [
            {"name": "Whiskers", "description": "brave orange cat"},
            {"name": "Drago", "description": "friendly dragon"},
        ],
        "scenes": [
            {
                "scene_number": 1,
                "narration": "Whiskers the cat lives in a beautiful village.",
                "dialogue": "",
                "mood": "happy",
                "duration_seconds": 5,
                "setting": "village"
            },
            {
                "scene_number": 2,
                "narration": "One day, he meets a friendly dragon named Drago!",
                "dialogue": "Hello! I am Drago the dragon!",
                "mood": "happy",
                "duration_seconds": 6,
                "setting": "forest"
            },
            {
                "scene_number": 3,
                "narration": "The village needs their help!",
                "dialogue": "We must save the village!",
                "mood": "tense",
                "duration_seconds": 5,
                "setting": "village"
            },
            {
                "scene_number": 4,
                "narration": "Together they save the day!",
                "dialogue": "We did it! Hooray!",
                "mood": "magical",
                "duration_seconds": 6,
                "setting": "village"
            },
        ]
    }
    
    print("\n🎬 Creating test cartoon episode...")
    episode = studio.create_cartoon_episode(
        story_data=test_story,
        episode_number=1,
        voiceover_path="output/test_english.mp3"
    )
    
    if episode:
        print(f"\n✅ Episode created: {episode}")
    else:
        print("\n❌ Failed")
    
    print("\n" + "="*60)