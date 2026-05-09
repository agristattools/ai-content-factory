"""
🎬 PROFESSIONAL VIDEO CREATOR v2.0
- AI images for every scene
- Ken Burns animation (zoom/pan)
- Background music
- Professional transitions
- Text overlays
- Zero blank screens
- Built for maximum retention & CTR
"""
import os
import requests
import random
from pathlib import Path
from loguru import logger
from moviepy import (
    VideoFileClip, AudioFileClip, ImageClip,
    CompositeVideoClip, CompositeAudioClip,
    concatenate_videoclips, TextClip, ColorClip
)
from moviepy.video.fx import FadeIn, FadeOut, Resize
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
import numpy as np
from dotenv import load_dotenv
from content.ai_image_gen import AIImageGenerator

load_dotenv()

class ProfessionalVideoCreator:
    """Create studio-quality videos for maximum engagement"""
    
    def __init__(self, resolution=(1920, 1080), fps=30):
        self.resolution = resolution
        self.fps = fps
        self.width, self.height = resolution
        self.ai_image_gen = AIImageGenerator()
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        
        # Professional color palettes
        self.color_palettes = {
            "tech": [(15, 15, 40), (0, 150, 255), (255, 255, 255)],
            "motivation": [(20, 20, 20), (255, 180, 0), (255, 255, 255)],
            "education": [(10, 30, 60), (80, 220, 100), (255, 255, 255)],
            "cartoon": [(30, 20, 50), (255, 100, 200), (255, 255, 255)],
            "gaming": [(10, 10, 10), (200, 50, 255), (255, 255, 255)],
        }
    
    def _get_bg_music(self, mood="tech") -> str:
        """Get background music path"""
        music_path = Path(f"data/assets/bg_music_{mood}.mp3")
        if music_path.exists():
            return str(music_path)
        return ""
    
    def _generate_scene_image(self, description: str, style: str, index: int) -> str:
        """Generate AI image for a scene"""
        
        output_dir = Path("output/scene_images")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return self.ai_image_gen.generate_image(
            prompt=description,
            style=style,
            width=self.width,
            height=self.height,
            filename=f"scene_{index:03d}.jpg"
        )
    
    def _create_animated_clip(self, image_path: str, duration: float, 
                             text: str = "", style: str = "ken_burns") -> ImageClip:
        """Create animated clip from image with Ken Burns effect"""
        
        if not Path(image_path).exists():
            # Fallback: colored clip with text
            colors = self.color_palettes.get("tech", [(15,15,40), (0,150,255), (255,255,255)])
            clip = ColorClip(size=self.resolution, color=colors[0], duration=duration)
            if text:
                try:
                    txt = TextClip(
                        text=text, font_size=50, color='white',
                        size=(self.width-200, None), method='caption'
                    ).with_position('center').with_duration(duration)
                    clip = CompositeVideoClip([clip, txt])
                except:
                    pass
            return clip
        
        # Load image
        clip = ImageClip(image_path, duration=duration)
        
        # Ken Burns effect: zoom in or out slightly
        if style == "ken_burns":
            zoom_factor = random.uniform(1.05, 1.15)
            
            def ken_burns_effect(get_frame, t):
                progress = t / duration if duration > 0 else 0
                current_zoom = 1.0 + (zoom_factor - 1.0) * progress
                
                frame = get_frame(t)
                h, w = frame.shape[:2]
                
                new_h, new_w = int(h * current_zoom), int(w * current_zoom)
                
                # Resize
                from PIL import Image as PILImage
                pil_img = PILImage.fromarray(frame)
                pil_img = pil_img.resize((new_w, new_h), PILImage.LANCZOS)
                
                # Center crop
                left = (new_w - w) // 2
                top = (new_h - h) // 2
                pil_img = pil_img.crop((left, top, left + w, top + h))
                
                return np.array(pil_img)
            
            clip = clip.transform(ken_burns_effect)
        
        # Add text overlay
        if text:
            try:
                txt_clip = TextClip(
                    text=text, font_size=55, color='white',
                    stroke_color='black', stroke_width=3,
                    size=(self.width - 150, None), method='caption'
                ).with_position(('center', self.height - 150)).with_duration(duration)
                
                clip = CompositeVideoClip([clip, txt_clip])
            except:
                pass
        
        return clip
    
    def _search_stock_videos(self, query: str, count: int = 8) -> list:
        """Search stock videos from Pexels"""
        
        if not self.pexels_key:
            return []
        
        try:
            url = "https://api.pexels.com/videos/search"
            headers = {"Authorization": self.pexels_key}
            params = {"query": query, "per_page": min(count, 15)}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                videos = response.json().get("videos", [])
                logger.info(f"📹 Found {len(videos)} stock videos")
                return videos
        except Exception as e:
            logger.warning(f"Stock search failed: {e}")
        
        return []
    
    def _download_stock_video(self, video_data: dict, path: str) -> bool:
        """Download a stock video"""
        try:
            video_files = video_data.get("video_files", [])
            best = None
            
            for vf in video_files:
                if vf.get("quality") == "hd" and vf.get("width", 0) >= 1920:
                    best = vf
                    break
            
            if not best:
                best = video_files[0] if video_files else None
            
            if best:
                response = requests.get(best["link"], timeout=30)
                with open(path, "wb") as f:
                    f.write(response.content)
                return True
        except:
            pass
        return False
    
    def create_professional_video(self, 
                                  voiceover_path: str,
                                  topic: str,
                                  script_text: str = "",
                                  niche: str = "tech",
                                  style: str = "professional",
                                  add_music: bool = True,
                                  output_path: str = "output/pro_video.mp4") -> str:
        """Create professional video with all features"""
        
        logger.info(f"🎬 Creating PRO video: {topic[:60]}...")
        
        # Load voiceover
        if not Path(voiceover_path).exists():
            logger.error(f"Voiceover not found: {voiceover_path}")
            return ""
        
        audio = AudioFileClip(voiceover_path)
        total_duration = audio.duration
        logger.info(f"⏱️ Total duration: {total_duration:.1f}s")
        
        # Split script into scenes (roughly 5-8 seconds each)
        sentences = script_text.replace('\n', ' ').split('.')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        num_scenes = max(len(sentences), int(total_duration / 7))
        scene_duration = total_duration / num_scenes
        
        logger.info(f"🎬 Creating {num_scenes} scenes ({scene_duration:.1f}s each)")
        
        # Generate AI images for ALL scenes (NO blank screens!)
        logger.info("🎨 Generating scene images...")
        image_paths = []
        
        for i in range(num_scenes):
            scene_text = sentences[i % len(sentences)] if sentences else f"{topic} - Part {i+1}"
            
            img_path = self._generate_scene_image(
                description=f"professional {niche} visual: {scene_text[:100]}",
                style="realistic" if niche in ["tech", "motivation"] else "cartoon",
                index=i
            )
            
            if img_path and Path(img_path).exists():
                image_paths.append(img_path)
        
        # If not enough images, generate more
        while len(image_paths) < num_scenes:
            img_path = self._generate_scene_image(
                description=f"{niche} background visual {len(image_paths)}",
                style="realistic",
                index=len(image_paths)
            )
            if img_path and Path(img_path).exists():
                image_paths.append(img_path)
            else:
                break
        
        logger.info(f"✅ {len(image_paths)} scene images ready")
        
        # Create animated clips from images
        video_clips = []
        
        for i in range(num_scenes):
            img_path = image_paths[i % len(image_paths)] if image_paths else ""
            scene_text = sentences[i % len(sentences)] if sentences else f"{topic}"
            
            clip = self._create_animated_clip(
                image_path=img_path,
                duration=scene_duration,
                text=scene_text[:100] if i % 3 == 0 else "",
                style="ken_burns"
            )
            
            # Add fade transitions
            if i > 0:
                clip = clip.with_effects([FadeIn(0.3), FadeOut(0.3)])
            else:
                clip = clip.with_effects([FadeIn(0.5)])
            
            video_clips.append(clip)
        
        # Combine all clips
        final_video = concatenate_videoclips(video_clips)
        
        # Adjust to exact audio duration
        if final_video.duration > total_duration:
            final_video = final_video.subclipped(0, total_duration)
        
        # Add voiceover
        final_video = final_video.with_audio(audio)
        
        # Add background music (lowered volume)
        if add_music:
            music_path = self._get_bg_music(niche if niche in ["tech", "inspirational"] else "tech")
            
            if music_path and Path(music_path).exists():
                try:
                    music = AudioFileClip(music_path)
                    # Loop music to match video length
                    if music.duration < total_duration:
                        repeats = int(total_duration / music.duration) + 1
                        music = concatenate_videoclips([music] * repeats)
                    
                    music = music.subclipped(0, total_duration)
                    music = music.with_volume(0.08)  # Low background volume
                    
                    # Mix voiceover + music
                    final_audio = CompositeAudioClip([audio, music])
                    final_video = final_video.with_audio(final_audio)
                    
                    logger.info("🎵 Background music added")
                except Exception as e:
                    logger.warning(f"Music addition failed: {e}")
        
        # Add intro hook text (first 3 seconds)
        try:
            hook_text = TextClip(
                text=topic[:80].upper(),
                font_size=70,
                color='white',
                stroke_color='black',
                stroke_width=4,
                size=(self.width - 100, None),
                method='caption'
            ).with_position('center').with_duration(3).with_effects([FadeOut(0.5)])
            
            final_video = CompositeVideoClip([final_video, hook_text])
        except:
            pass
        
        # Write final video
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        final_video.write_videofile(
            output_path,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            bitrate='8000k',  # High quality
            preset='medium',
            threads=4
        )
        
        # Cleanup
        audio.close()
        for clip in video_clips:
            clip.close()
        
        size_mb = os.path.getsize(output_path) / (1024*1024)
        logger.info(f"✅ PRO Video created: {output_path} ({size_mb:.1f} MB)")
        
        return output_path


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬 PROFESSIONAL VIDEO CREATOR TEST")
    print("="*60)
    
    creator = ProfessionalVideoCreator(resolution=(1920, 1080))
    
    # Test script
    test_topic = "The Future of Artificial Intelligence in 2025"
    test_script = """
    Artificial intelligence is changing everything around us.
    From smartphones to self-driving cars, AI is everywhere.
    In 2025, we are seeing incredible breakthroughs.
    Machines can now understand human emotions.
    They can create art, write stories, and even compose music.
    But what does this mean for our future?
    Let us explore the amazing possibilities ahead.
    """
    
    # Check for voiceover file
    voice_file = "output/test_english.mp3"
    if not Path(voice_file).exists():
        voice_file = "output/voiceover_cartoon_20260508_102128.mp3"
    
    for vf in Path("output").glob("voiceover_*.mp3"):
        voice_file = str(vf)
        break
    
    if Path(voice_file).exists():
        result = creator.create_professional_video(
            voiceover_path=str(voice_file),
            topic=test_topic,
            script_text=test_script,
            niche="tech",
            add_music=True,
            output_path="output/pro_test_video.mp4"
        )
        
        if result:
            print(f"\n✅ PRO Video: {result}")
        else:
            print("\n❌ Failed")
    else:
        print("⚠️ No voiceover found - run voiceover_gen first")
    
    print("\n" + "="*60)