"""
🎵 FREE BACKGROUND MUSIC
Downloads from Pixabay (100% free, no copyright)
"""
import requests
import os
from pathlib import Path
from loguru import logger

class MusicDownloader:
    """Download free background music"""
    
    MUSIC_URLS = {
    "upbeat": "https://cdn.pixabay.com/audio/2024/01/16/audio_7e3c5a8b12.mp3",
    "inspirational": "https://cdn.pixabay.com/audio/2024/02/19/audio_a2d4f9c3e1.mp3",
    "tech": "https://cdn.pixabay.com/audio/2024/03/21/audio_5b8c2d4a67.mp3",
    "calm": "https://cdn.pixabay.com/audio/2024/01/28/audio_3f6a1e9d45.mp3",
     }
    
    def __init__(self, output_dir: str = "data/assets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download(self, mood: str = "tech") -> str:
        """Download background music by mood"""
        
        url = self.MUSIC_URLS.get(mood, self.MUSIC_URLS["tech"])
        filename = f"bg_music_{mood}.mp3"
        output_path = self.output_dir / filename
        
        if output_path.exists():
            logger.info(f"🎵 Music already exists: {output_path}")
            return str(output_path)
        
        try:
            response = requests.get(url, timeout=30)
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"🎵 Downloaded: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Music download failed: {e}")
            return ""

if __name__ == "__main__":
    dl = MusicDownloader()
    for mood in ["tech", "inspirational", "calm"]:
        dl.download(mood)
    print("✅ Music downloaded!")