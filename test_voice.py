import asyncio
import edge_tts

async def test():
    text = "Hello, this is a test of the voice system."
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    await communicate.save("test_output.mp3")
    print("✅ Success! Check test_output.mp3")

asyncio.run(test())