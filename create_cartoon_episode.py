"""
🎬 CARTOON EPISODE CREATOR
Creates complete cartoon episodes with:
- AI Story & Characters
- Animated Scenes
- Voiceover & Music
- Professional Output
"""
import sys
import asyncio
import json
from pathlib import Path
from loguru import logger
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent))

from content.ai_story_gen import StoryGenerator
from content.cartoon_animator import CartoonAnimator
from content.voiceover_gen import VoiceoverGenerator

console = Console()

async def create_episode(topic: str, language: str = "english", 
                         num_scenes: int = 10):
    """Create a complete cartoon episode"""
    
    console.print(Panel(f"[bold cyan]🎬 Creating Cartoon: {topic}[/bold cyan]"))
    
    # Step 1: Generate Story
    console.print("\n📖 [yellow]Generating story...[/yellow]")
    story_gen = StoryGenerator(language=language)
    story = story_gen.generate_story(topic, num_scenes=num_scenes, style="cartoon")
    
    if "error" in story:
        console.print(f"[red]❌ Story failed: {story['error']}[/red]")
        return
    
    console.print(f"[green]✅ Story: {story.get('title')}[/green]")
    console.print(f"   Characters: {len(story.get('characters', []))}")
    console.print(f"   Scenes: {len(story.get('scenes', []))}")
    
    # Save story
    with open("output/cartoon_story.json", "w", encoding="utf-8") as f:
        json.dump(story, f, indent=2, ensure_ascii=False)
    
    # Step 2: Generate Narration & Voiceover
    console.print("\n🎙️ [yellow]Generating voiceover...[/yellow]")
    narration = story_gen.story_to_narration(story)
    
    voice_gen = VoiceoverGenerator(language=language, gender="female")
    voice_path = "output/cartoon_voiceover.mp3"
    await voice_gen.generate(narration, voice_path)
    
    console.print(f"[green]✅ Voiceover: {voice_path}[/green]")
    
    # Step 3: Create Animated Episode
    console.print("\n🎬 [yellow]Creating animated episode...[/yellow]")
    animator = CartoonAnimator()
    episode_path = animator.create_episode(
        story_data=story,
        episode_number=1,
        voiceover_path=voice_path
    )
    
    if episode_path:
        console.print(f"\n[bold green]✅ EPISODE CREATED![/bold green]")
        console.print(f"📁 {episode_path}")
        
        size_mb = Path(episode_path).stat().st_size / (1024*1024)
        console.print(f"📦 Size: {size_mb:.1f} MB")
    else:
        console.print("[red]❌ Episode creation failed[/red]")
    
    return episode_path

if __name__ == "__main__":
    console.print("""
    ╔══════════════════════════════════════╗
    ║  🎬 CARTOON EPISODE CREATOR 🎬     ║
    ║  Create Animated Cartoon Series     ║
    ╚══════════════════════════════════════╝
    """)
    
    topic = input("📝 Cartoon story topic: ").strip()
    if not topic:
        topic = "A brave little cat who discovers a magical world"
    
    language = input("🌐 Language (english/urdu/hindi) [english]: ").strip() or "english"
    scenes = input("🎬 Number of scenes [10]: ").strip()
    
    asyncio.run(create_episode(
        topic=topic,
        language=language,
        num_scenes=int(scenes) if scenes else 10
    ))