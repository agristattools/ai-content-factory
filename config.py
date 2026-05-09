"""
AI CONTENT FACTORY - Master Configuration
Multi-Language | Multi-Format | HD Quality
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = DATA_DIR / "assets"
TEMP_DIR = DATA_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

# Create all directories
for d in [DATA_DIR, ASSETS_DIR, TEMP_DIR, LOGS_DIR, OUTPUT_DIR]:
    d.mkdir(exist_ok=True)

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")

# Languages Supported
LANGUAGES = {
    "english": {
        "code": "en",
        "tts_voice": "en-US-JennyNeural",
        "tts_male": "en-US-DavisNeural",
    },
    "urdu": {
        "code": "ur",
        "tts_voice": "ur-PK-UzmaNeural",
        "tts_male": "ur-PK-AsadNeural",
    },
    "hindi": {
        "code": "hi",
        "tts_voice": "hi-IN-SwaraNeural",
        "tts_male": "hi-IN-MadhurNeural",
    },
    "punjabi": {
        "code": "pa",
        "tts_voice": "pa-IN-GurleenNeural",
        "tts_male": "pa-IN-GurleenNeural",
    }
}

# Video Formats
VIDEO_FORMATS = {
    "shorts": {"ratio": (9,16), "size": (1080,1920), "max_sec": 60},
    "landscape": {"ratio": (16,9), "size": (1920,1080), "max_sec": 600},
    "square": {"ratio": (1,1), "size": (1080,1080), "max_sec": 120},
}

# Quality Settings
QUALITY = {
    "hd": {"bitrate": "5M", "fps": 30},
    "full_hd": {"bitrate": "8M", "fps": 30},
    "4k": {"bitrate": "20M", "fps": 60},
}

# Default user settings
DEFAULT_LANGUAGE = "english"
DEFAULT_FORMAT = "landscape"
DEFAULT_QUALITY = "hd"
DEFAULT_NICHE = "tech_reviews"

print("✅ Config loaded successfully!")