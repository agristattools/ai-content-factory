"""
🎙️ VOICEOVER GENERATOR
Uses Microsoft Edge TTS (FREE)
Supports: English, Urdu, Hindi, Punjabi
"""
import asyncio
import edge_tts
import os
from pathlib import Path
from loguru import logger
import random
from typing import Dict

class VoiceoverGenerator:
    """Generate human-like voiceovers for free"""
    
    # Only VERIFIED working voices
    VOICES = {
        "english": {
            "male": "en-US-AriaNeural",       # Confirmed ✅
            "female": "en-US-JennyNeural",    # Confirmed ✅
        },
        "urdu": {
            "male": "ur-PK-AsadNeural",       # Confirmed ✅
            "female": "ur-PK-UzmaNeural",     # Confirmed ✅
        },
        "hindi": {
            "male": "hi-IN-MadhurNeural",     # Confirmed ✅
            "female": "hi-IN-SwaraNeural",    # Confirmed ✅
        },
        "punjabi": {
            "male": "hi-IN-MadhurNeural",     # Fallback (similar accent)
            "female": "hi-IN-SwaraNeural",    # Fallback (similar accent)
        }
    }
    
    def __init__(self, language: str = "english", gender: str = "male"):
        self.language = language
        self.gender = gender
        
        lang_voices = self.VOICES.get(language, self.VOICES["english"])
        self.voice = lang_voices.get(gender, lang_voices["male"])
        
        logger.info(f"🎙️ Voice: {self.voice} ({language}/{gender})")
    
    async def generate(self, script: str, output_path: str) -> str:
        """Convert script to speech"""
        
        logger.info(f"🎙️ Generating: {len(script.split())} words → {output_path}")
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        communicate = edge_tts.Communicate(script, self.voice)
        await communicate.save(output_path)
        
        size_kb = os.path.getsize(output_path) / 1024
        logger.info(f"✅ Saved: {size_kb:.1f} KB")
        
        return output_path


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎙️  VOICEOVER GENERATOR TEST")
    print("="*60)
    
    async def test():
        # Test 1: English
        print("\n🔊 English (Female - Jenny)...")
        gen_en = VoiceoverGenerator(language="english", gender="female")
        script_en = "Hey everyone, welcome back to the channel. Today we are talking about Google Pixel battery issues and the simple fixes you can try right now."
        await gen_en.generate(script_en, "output/test_english.mp3")
        
        # Test 2: Urdu
        print("\n🔊 Urdu (Female - Uzma)...")
        gen_ur = VoiceoverGenerator(language="urdu", gender="female")
        script_ur = "Aaj hum baat karenge Pakistan mein 5G technology ke baare mein. Kya ye sach mein aa rahi hai. Chaliye jaante hain."
        await gen_ur.generate(script_ur, "output/test_urdu.mp3")
        
        # Test 3: Hindi
        print("\n🔊 Hindi (Female - Swara)...")
        gen_hi = VoiceoverGenerator(language="hindi", gender="female")
        script_hi = "Namaste dosto, aaj hum baat karenge ek naye smartphone ke baare mein. Is phone mein bahut kuch khaas hai."
        await gen_hi.generate(script_hi, "output/test_hindi.mp3")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETE!")
        print("📁 Check 'output' folder for MP3 files")
        print("="*60)
    
    asyncio.run(test())