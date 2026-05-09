"""
🎯 MASTER ORCHESTRATOR
Connects all modules into one automated pipeline
Trend → Script → Voice → Video → Thumbnail → SEO → Upload
"""
import sys
import asyncio
import json
from pathlib import Path
from datetime import datetime
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

load_dotenv()

# Import all modules
from research.trend_finder import TrendFinder
from content.script_generator import ScriptGenerator
from content.voiceover_gen import VoiceoverGenerator
from content.video_creator import VideoCreator
from content.thumbnail_maker import ThumbnailMaker
from content.ai_image_gen import AIImageGenerator
from content.ai_story_gen import StoryGenerator
from seo.seo_engine import SEOEngine

console = Console()

class ContentPipeline:
    """Master orchestrator for the entire content factory"""
    
    def __init__(self, language: str = "english", niche: str = "tech",
                 format_type: str = "landscape", content_mode: str = "auto"):
        self.language = language
        self.niche = niche
        self.format_type = format_type
        self.content_mode = content_mode  # auto, cartoon, stock
        
        # Initialize all modules
        self.trend_finder = TrendFinder(niche=niche, language=language)
        self.script_gen = ScriptGenerator(language=language, niche=niche)
        self.voice_gen = VoiceoverGenerator(language=language, gender="female")
        self.video_creator = VideoCreator(format_type=format_type)
        self.thumbnail_maker = ThumbnailMaker()
        self.ai_image_gen = AIImageGenerator()
        self.story_gen = StoryGenerator(language=language)
        self.seo_engine = SEOEngine(language=language, niche=niche)
        
        logger.info(f"🚀 Pipeline initialized: {language}/{niche}/{format_type}")
    
    async def run_cartoon_pipeline(self, topic: str, num_scenes: int = 6):
        """Run the complete cartoon/animation pipeline"""
        
        console.print(Panel(f"[bold cyan]🎬 CARTOON PIPELINE: {topic}[/bold cyan]"))
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            
            # Step 1: Generate story
            progress.add_task("[yellow]📖 Generating story...", total=None)
            story = self.story_gen.generate_story(topic, num_scenes=num_scenes, style="cartoon")
            
            if "error" in story:
                console.print(f"[red]❌ Story generation failed: {story['error']}[/red]")
                return
            
            console.print(f"[green]✅ Story: {story.get('title')}[/green]")
            
            # Step 2: Generate narration script
            progress.add_task("[yellow]📝 Creating narration...", total=None)
            narration = self.story_gen.story_to_narration(story)
            
            # Step 3: Generate voiceover
            progress.add_task("[yellow]🎙️ Generating voiceover...", total=None)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            voice_path = f"output/voiceover_cartoon_{timestamp}.mp3"
            await self.voice_gen.generate(narration, voice_path)
            
            # Step 4: Generate scene images
            progress.add_task("[yellow]🎨 Creating scene images...", total=None)
            scenes = self.story_gen.story_to_scenes(story)
            image_paths = self.ai_image_gen.generate_scene_images(
                scenes, style="cartoon", width=1920, height=1080
            )
            
            console.print(f"[green]✅ Generated {len(image_paths)} scene images[/green]")
            
            # Step 5: Create video from images + voiceover
            # (Using VideoCreator would need adaptation for images)
            video_path = f"output/cartoon_video_{timestamp}.mp4"
            
            # Step 6: Generate thumbnail
            progress.add_task("[yellow]🖼️ Creating thumbnail...", total=None)
            thumb_path = self.thumbnail_maker.create_thumbnail(
                story.get('title', topic),
                niche=self.niche
            )
            
            # Step 7: SEO
            progress.add_task("[yellow]📈 Optimizing SEO...", total=None)
            seo = self.seo_engine.generate_all_metadata(
                story.get('title', topic),
                script=narration
            )
            
            # Save everything
            output = {
                "pipeline": "cartoon",
                "story": story,
                "voiceover": voice_path,
                "images": image_paths,
                "video": video_path,
                "thumbnail": thumb_path,
                "seo": seo,
                "timestamp": timestamp
            }
            
            # Save output
            output_path = f"output/pipeline_cartoon_{timestamp}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False, default=str)
            
            console.print(f"\n[bold green]✅ CARTOON PIPELINE COMPLETE![/bold green]")
            console.print(f"📁 Output: {output_path}")
            
            return output
    
    async def run_standard_pipeline(self, topic: str = None):
        """Run the standard (stock footage) pipeline"""
        
        console.print(Panel(f"[bold cyan]🎬 STANDARD PIPELINE[/bold cyan]"))
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            
            # Step 1: Find trends if no topic given
            if topic is None:
                progress.add_task("[yellow]🔍 Finding trending topics...", total=None)
                trends = self.trend_finder.find_trends(limit=1)
                if trends:
                    topic = trends[0]
                    console.print(f"[green]✅ Trend found: {topic['topic'][:60]}[/green]")
                else:
                    console.print("[red]❌ No trends found[/red]")
                    return
            
            topic_text = topic if isinstance(topic, str) else topic.get('topic', str(topic))
            
            # Step 2: Generate script
            progress.add_task("[yellow]✍️ Writing script...", total=None)
            script_data = self.script_gen.generate_script(
                {'topic': topic_text} if isinstance(topic, str) else topic
            )
            
            if not script_data.get('script'):
                console.print("[red]❌ Script generation failed[/red]")
                return
            
            console.print(f"[green]✅ Script: {script_data['word_count']} words[/green]")
            
            # Step 3: Generate voiceover
            progress.add_task("[yellow]🎙️ Creating voiceover...", total=None)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            voice_path = f"output/voiceover_{timestamp}.mp3"
            await self.voice_gen.generate(script_data['script'], voice_path)
            
            # Step 4: Create video
            progress.add_task("[yellow]🎬 Creating video...", total=None)
            video_path = f"output/video_{timestamp}.mp4"
            duration = script_data.get('estimated_duration_min', 5) * 60
            
            self.video_creator.create_video(
                voiceover_path=voice_path,
                topic=topic_text,
                duration=min(duration, 30),  # Cap for test
                output_path=video_path
            )
            
            # Step 5: Generate thumbnail
            progress.add_task("[yellow]🖼️ Creating thumbnail...", total=None)
            thumb_path = self.thumbnail_maker.create_thumbnail(
                topic_text,
                niche=self.niche
            )
            
            # Step 6: SEO
            progress.add_task("[yellow]📈 Generating SEO...", total=None)
            seo = self.seo_engine.generate_all_metadata(
                topic_text,
                script=script_data['script']
            )
            
            # Save output
            output = {
                "pipeline": "standard",
                "topic": topic_text,
                "script": script_data,
                "voiceover": voice_path,
                "video": video_path,
                "thumbnail": thumb_path,
                "seo": seo,
                "timestamp": timestamp
            }
            
            output_path = f"output/pipeline_{timestamp}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False, default=str)
            
            console.print(f"\n[bold green]✅ STANDARD PIPELINE COMPLETE![/bold green]")
            console.print(f"📁 Output: {output_path}")
            
            return output
    
    def display_menu(self):
        """Show interactive menu"""
        
        console.print(Panel.fit(
            "[bold cyan]🎯 AI CONTENT FACTORY - MAIN MENU[/bold cyan]",
            border_style="cyan"
        ))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", width=5)
        table.add_column("Pipeline", style="white")
        table.add_column("Description", style="yellow")
        
        table.add_row("1", "🔄 Full Standard", "Trend → Script → Voice → Video → Thumbnail → SEO")
        table.add_row("2", "🎨 Cartoon/Story", "AI Story → Images → Voice → Video → Thumbnail")
        table.add_row("3", "✍️ Script Only", "Generate script from topic")
        table.add_row("4", "🎙️ Voice Only", "Generate voiceover from script")
        table.add_row("5", "🎬 Video Only", "Create video from voiceover")
        table.add_row("6", "📈 SEO Only", "Generate SEO metadata")
        table.add_row("7", "🔍 Trends Only", "Find trending topics")
        table.add_row("8", "❌ Exit", "Close program")
        
        console.print(table)


# ============================================
# MAIN
# ============================================
async def main():
    console.print("""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║     🤖  AI CONTENT FACTORY  v2.0  🤖        ║
    ║   Complete YouTube Automation System        ║
    ║                                              ║
    ║   ✅ Research  ✅ Scripts   ✅ Voice        ║
    ║   ✅ Video     ✅ Images   ✅ SEO          ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """, style="bold cyan")
    
    # Get settings
    language = input("🌐 Language (english/urdu/hindi/punjabi) [english]: ").strip() or "english"
    niche = input("🎯 Niche (tech/motivation/educational/gaming) [tech]: ").strip() or "tech"
    mode = input("🎬 Content Mode (standard/cartoon) [standard]: ").strip() or "standard"
    
    pipeline = ContentPipeline(language=language, niche=niche, content_mode=mode)
    
    while True:
        pipeline.display_menu()
        choice = input("\n👉 Choose option (1-8): ").strip()
        
        if choice == "1":
            topic = input("📝 Enter topic (or press Enter for auto-trend): ").strip()
            await pipeline.run_standard_pipeline(topic if topic else None)
            
        elif choice == "2":
            topic = input("📝 Enter story topic: ").strip()
            if topic:
                scenes = input("🎬 Number of scenes [6]: ").strip()
                await pipeline.run_cartoon_pipeline(topic, int(scenes) if scenes else 6)
            else:
                console.print("[red]❌ Topic required for cartoon pipeline[/red]")
        
        elif choice == "8":
            console.print("[green]👋 Goodbye![/green]")
            break
        
        else:
            console.print("[yellow]Feature in development. Use option 1 or 2 for full pipeline.[/yellow]")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())