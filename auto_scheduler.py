"""
⏰ COMPLETE AUTO-SCHEDULER
Fully automated content factory
"""
import sys
import asyncio
import json
import time
import os
from pathlib import Path
from datetime import datetime
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from schedule import every, repeat, run_pending
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

from research.trend_finder import TrendFinder
from content.script_generator import ScriptGenerator
from content.voiceover_gen import VoiceoverGenerator
from content.thumbnail_maker import ThumbnailMaker
from seo.seo_engine import SEOEngine
from platforms.facebook_publisher import FacebookPublisher

# Video creator - try both
try:
    sys.path.insert(0, str(Path(__file__).parent / "content"))
    from video_creator_pro import ProfessionalVideoCreator
except:
    from content.video_creator import VideoCreator as ProfessionalVideoCreator

console = Console()

class AutoScheduler:
    """Complete automated content factory"""
    
    def __init__(self, language="english", niche="tech", 
                 post_to_youtube=False, post_to_facebook=False):
        self.language = language
        self.niche = niche
        self.post_to_youtube = post_to_youtube
        self.post_to_facebook = post_to_facebook
        
        self.trend_finder = TrendFinder(niche=niche, language=language)
        self.script_gen = ScriptGenerator(language=language, niche=niche)
        self.voice_gen = VoiceoverGenerator(language=language, gender="female")
        self.video_creator = ProfessionalVideoCreator()
        self.thumbnail_maker = ThumbnailMaker()
        self.seo_engine = SEOEngine(language=language, niche=niche)
        self.fb_publisher = FacebookPublisher()
        
        self.stats = {
            "videos_created": 0,
            "posts_made": 0,
            "last_run": None,
            "errors": 0
        }
        self._load_stats()
        logger.info(f"🚀 AutoScheduler: {language}/{niche}")
    
    def _load_stats(self):
        stats_path = Path("data/stats.json")
        if stats_path.exists():
            with open(stats_path) as f:
                self.stats = json.load(f)
    
    def _save_stats(self):
        stats_path = Path("data/stats.json")
        stats_path.parent.mkdir(exist_ok=True)
        with open(stats_path, "w") as f:
            json.dump(self.stats, f, indent=2)
    
    async def create_content(self, topic=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        console.print(Panel(f"[bold cyan]🎬 Creating Content: {timestamp}[/bold cyan]"))
        
        try:
            if not topic:
                console.print("[yellow]🔍 Finding trending topic...[/yellow]")
                trends = self.trend_finder.find_trends(1)
                topic = trends[0]['topic'] if trends else f"Latest {self.niche} news"
                console.print(f"[green]✅ Topic: {topic[:80]}[/green]")
            
            console.print("[yellow]✍️ Writing script...[/yellow]")
            script_data = self.script_gen.generate_script({'topic': topic})
            
            console.print("[yellow]🎙️ Creating voiceover...[/yellow]")
            voice_path = f"output/auto_voice_{timestamp}.mp3"
            await self.voice_gen.generate(script_data['script'], voice_path)
            
            console.print("[yellow]🎬 Creating video...[/yellow]")
            video_path = f"output/auto_video_{timestamp}.mp4"
            self.video_creator.create_professional_video(
                voiceover_path=voice_path, topic=topic,
                script_text=script_data['script'], niche=self.niche,
                add_music=True, output_path=video_path
            )
            
            console.print("[yellow]🖼️ Creating thumbnail...[/yellow]")
            thumb_path = self.thumbnail_maker.create_thumbnail(topic, niche=self.niche)
            
            console.print("[yellow]📈 Generating SEO...[/yellow]")
            seo_data = self.seo_engine.generate_all_metadata(topic, script_data['script'])
            
            # Save history
            result = {"timestamp": timestamp, "topic": topic, 
                     "video": video_path, "thumbnail": thumb_path, "seo": seo_data}
            history_dir = Path("data/history")
            history_dir.mkdir(exist_ok=True)
            with open(history_dir / f"content_{timestamp}.json", "w") as f:
                json.dump(result, f, indent=2, default=str)
            
            self.stats["videos_created"] += 1
            self.stats["last_run"] = timestamp
            self._save_stats()
            
            console.print(f"\n[bold green]✅ CONTENT CREATED![/bold green]")
            console.print(f"📁 {video_path}")
            return result
            
        except Exception as e:
            self.stats["errors"] += 1
            self._save_stats()
            console.print(f"[red]❌ Error: {e}[/red]")
            return None
    
    def show_status(self):
        table = Table(title="📊 AUTO-SCHEDULER STATUS")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Language", self.language)
        table.add_row("Niche", self.niche)
        table.add_row("Videos Created", str(self.stats["videos_created"]))
        table.add_row("Last Run", str(self.stats.get("last_run", "Never")))
        table.add_row("Errors", str(self.stats["errors"]))
        console.print(table)
    
    def run_forever(self):
        console.print(Panel.fit("[bold green]🚀 AUTO-SCHEDULER RUNNING[/bold green]"))
        post_time = os.getenv("POSTING_TIME", "10:00")
        
        @repeat(every().day.at(post_time))
        def scheduled_run():
            asyncio.run(self.create_content())
        
        console.print(f"⏰ Daily run at: {post_time}")
        try:
            while True:
                run_pending()
                time.sleep(30)
        except KeyboardInterrupt:
            console.print("\n[green]👋 Stopped[/green]")


async def main():
    console.print("""
    ╔═══════════════════════════════╗
    ║  ⏰ AI CONTENT AUTO-SCHEDULER ║
    ╚═══════════════════════════════╝
    """)
    
    scheduler = AutoScheduler(language="english", niche="tech")
    scheduler.show_status()
    
    while True:
        console.print("\n📋 1. Create NOW | 2. Auto-Schedule | 3. Status | 4. Exit")
        choice = input("👉 ").strip()
        if choice == "1":
            topic = input("Topic (Enter=auto): ").strip()
            await scheduler.create_content(topic if topic else None)
        elif choice == "2":
            scheduler.run_forever()
        elif choice == "3":
            scheduler.show_status()
        elif choice == "4":
            break

if __name__ == "__main__":
    asyncio.run(main())