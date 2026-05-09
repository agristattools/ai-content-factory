"""
🎬 VIDEO CREATOR
Combines: Stock footage (Pexels) + Voiceover + Background music
Output: MP4 video (HD/Full HD/4K)
Supports: Shorts (9:16) and Landscape (16:9)
"""
import os
import requests
import random
from pathlib import Path
from loguru import logger
from moviepy import (
    VideoFileClip, AudioFileClip, ImageClip, 
    CompositeVideoClip, concatenate_videoclips,
    TextClip, ColorClip
)
from moviepy.video.fx import FadeIn, FadeOut
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import numpy as np

load_dotenv()

class VideoCreator:
    """Create professional videos from scripts and voiceovers"""
    
    def __init__(self, resolution: tuple = (1920, 1080), format_type: str = "landscape"):
        self.resolution = resolution
        self.format_type = format_type
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        self.fps = 30
        
    def search_stock_videos(self, query: str, count: int = 5) -> list:
        """Search free stock videos from Pexels"""
        
        if not self.pexels_key:
            logger.warning("⚠️ No Pexels API key, using colored backgrounds instead")
            return []
        
        try:
            url = "https://api.pexels.com/videos/search"
            headers = {"Authorization": self.pexels_key}
            params = {"query": query, "per_page": count, "orientation": "landscape"}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                videos = response.json().get("videos", [])
                logger.info(f"📹 Found {len(videos)} stock videos for: {query}")
                return videos
            else:
                logger.warning(f"Pexels API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Stock video search failed: {e}")
            return []
    
    def download_video(self, video_data: dict, output_path: str) -> str:
        """Download a video from Pexels"""
        
        try:
            # Get the HD or SD video file
            video_files = video_data.get("video_files", [])
            
            # Prefer HD quality
            hd_video = None
            for vf in video_files:
                if vf.get("quality") == "hd" and vf.get("width") >= 1920:
                    hd_video = vf
                    break
            
            if not hd_video:
                # Fallback to any available
                for vf in video_files:
                    if vf.get("width", 0) >= 1280:
                        hd_video = vf
                        break
            
            if not hd_video and video_files:
                hd_video = video_files[0]
            
            if hd_video:
                video_url = hd_video["link"]
                response = requests.get(video_url, timeout=30)
                
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                logger.info(f"📥 Downloaded: {output_path}")
                return output_path
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
        
        return ""
    
    def create_colored_clip(self, duration: float, color: tuple = None) -> ImageClip:
        """Create a colored background clip when no stock video"""
        
        if color is None:
            colors = [
                (25, 25, 50),    # Dark blue
                (50, 25, 25),    # Dark red
                (25, 50, 25),    # Dark green
                (50, 50, 25),    # Dark yellow
                (25, 25, 25),    # Almost black
            ]
            color = random.choice(colors)
        
        clip = ColorClip(size=self.resolution, color=color, duration=duration)
        return clip
    
    def add_text_overlay(self, clip, text: str, duration: float):
        """Add text overlay to video"""
        
        try:
            txt_clip = TextClip(
                text=text,
                font_size=50,
                color='white',
                stroke_color='black',
                stroke_width=2,
                size=(self.resolution[0] - 100, None),
                method='caption'
            )
            txt_clip = txt_clip.with_position(('center', 'center')).with_duration(duration)
            
            return CompositeVideoClip([clip, txt_clip])
        except:
            return clip
    
    def create_video(self, voiceover_path: str, topic: str, duration: float, 
                     output_path: str = "output/final_video.mp4") -> str:
        """Create complete video with stock footage and voiceover"""
        
        logger.info(f"🎬 Creating video: {topic[:60]}...")
        
        # Load voiceover
        try:
            audio = AudioFileClip(voiceover_path)
            actual_duration = min(duration, audio.duration)
            logger.info(f"🔊 Voiceover: {actual_duration:.1f}s")
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            return ""
        
        # Search for stock videos
        search_terms = topic.split()[:3]  # First 3 words
        search_query = " ".join(search_terms)
        stock_videos = self.search_stock_videos(search_query, count=3)
        
        video_clips = []
        
        if stock_videos:
            # Download and use stock videos
            temp_dir = Path("data/temp")
            temp_dir.mkdir(exist_ok=True)
            
            clip_duration = actual_duration / len(stock_videos)
            
            for i, video_data in enumerate(stock_videos):
                temp_path = temp_dir / f"stock_{i}.mp4"
                
                if self.download_video(video_data, str(temp_path)):
                    try:
                        clip = VideoFileClip(str(temp_path))
                        
                        # Resize to our resolution
                        clip = clip.resized(self.resolution)
                        
                        # Trim to needed duration
                        if clip.duration > clip_duration:
                            clip = clip.subclipped(0, clip_duration)
                        
                        # Add fade effects
                        clip = clip.with_effects([FadeIn(0.5), FadeOut(0.5)])
                        
                        video_clips.append(clip)
                    except Exception as e:
                        logger.warning(f"Failed to process video {i}: {e}")
        
        # If no stock videos, create colored slides
        if not video_clips:
            logger.info("🎨 Using colored backgrounds (no stock videos)")
            num_slides = max(3, int(actual_duration / 5))
            slide_duration = actual_duration / num_slides
            
            for i in range(num_slides):
                slide = self.create_colored_clip(slide_duration)
                slide = slide.with_effects([FadeIn(0.3), FadeOut(0.3)])
                
                # Add topic text
                if i == 0:
                    slide = self.add_text_overlay(slide, topic, slide_duration)
                
                video_clips.append(slide)
        
        # Combine all clips
        if video_clips:
            final_video = concatenate_videoclips(video_clips)
            
            # Set audio
            final_video = final_video.with_audio(audio)
            
            # Trim to exact duration
            if final_video.duration > actual_duration:
                final_video = final_video.subclipped(0, actual_duration)
            
            # Write video file
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                bitrate='5000k',
                preset='medium',
                threads=2
            )
            
            # Clean up
            for clip in video_clips:
                clip.close()
            audio.close()
            
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            logger.info(f"✅ Video created: {output_path} ({size_mb:.1f} MB)")
            
            return output_path
        
        audio.close()
        logger.error("❌ No video clips generated")
        return ""


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬  VIDEO CREATOR TEST")
    print("="*60)
    
    creator = VideoCreator(
        resolution=(1920, 1080),
        format_type="landscape"
    )
    
    # Check if voiceover exists
    voiceover_file = "output/test_english.mp3"
    
    if Path(voiceover_file).exists():
        print(f"\n✅ Found voiceover: {voiceover_file}")
        
        result = creator.create_video(
            voiceover_path=voiceover_file,
            topic="Google Pixel Battery Drain Issues and Fixes",
            duration=15,  # Short test
            output_path="output/test_video.mp4"
        )
        
        if result:
            print(f"\n✅ Test video created: {result}")
        else:
            print("\n❌ Video creation failed")
    else:
        print(f"\n⚠️ Voiceover not found: {voiceover_file}")
        print("Run voiceover_gen.py first to create test_english.mp3")
    
    print("\n" + "="*60)