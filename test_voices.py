import asyncio
import edge_tts

async def test_voice(voice_name, text):
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(f"test_{voice_name}.mp3")
        print(f"✅ {voice_name} - WORKS")
        return True
    except Exception as e:
        print(f"❌ {voice_name} - FAILED: {str(e)[:80]}")
        return False

async def main():
    voices_to_test = [
        "en-US-JennyNeural",
        "en-US-DavisNeural", 
        "en-US-AriaNeural",
        "en-GB-SoniaNeural",
        "ur-PK-UzmaNeural",
        "ur-PK-AsadNeural",
        "hi-IN-SwaraNeural",
        "hi-IN-MadhurNeural",
        "pa-IN-GurleenNeural",
    ]
    
    text = "Hello, this is a short test."
    
    print("🔍 Testing available voices...\n")
    
    working = []
    for voice in voices_to_test:
        await test_voice(voice, text)
    
    print(f"\n✅ Working: {len(working)} voices")

asyncio.run(main())