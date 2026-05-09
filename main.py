#!/usr/bin/env python3
"""
🤖 AI CONTENT FACTORY v2.0
Complete YouTube & Facebook Automation
🌐 EN | UR | HI | PA
🎬 Standard Videos | 🎨 Cartoon Studio | ⏰ Auto-Scheduler
"""
import sys
import asyncio
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()
import config

console = Console()

def show_banner():
    console.print("""
    ╔══════════════════════════════════════════════╗
    ║   🤖  AI CONTENT FACTORY  v2.0  🤖         ║
    ║   YouTube & Facebook Automation            ║
    ║   🌐 EN | UR | HI | PA                    ║
    ║   🎬 Videos | 🎨 Cartoons | ⏰ Auto       ║
    ╚══════════════════════════════════════════════╝
    """, style="bold cyan")

def check_system():
    console.print(Panel("[bold yellow]🔍 System Check[/bold yellow]"))
    
    table = Table(title="Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    
    py = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python Version", py)
    table.add_row("Config File", "✅ Loaded")
    
    dirs = ["data", "logs", "output", "research", "content", "seo", "platforms"]
    for d in dirs:
        exists = (config.BASE_DIR / d).exists()
        table.add_row(f"Directory: {d}/", "✅" if exists else "❌")
    
    keys = [
        ("GROQ_API_KEY", config.GROQ_API_KEY),
        ("GEMINI_API_KEY", config.GEMINI_API_KEY),
        ("YOUTUBE_API_KEY", config.YOUTUBE_API_KEY),
        ("PEXELS_API_KEY", config.PEXELS_API_KEY),
    ]
    for name, value in keys:
        if value and "your_" not in str(value):
            table.add_row(f"API: {name}", "✅ Configured")
        else:
            table.add_row(f"API: {name}", "⚠️ Not Set")
    
    console.print(table)

async def create_standard_video():
    """Create standard video with full pipeline"""
    from auto_scheduler import AutoScheduler
    scheduler = AutoScheduler(language="english", niche="tech")
    topic = input("\n📝 Topic (Enter for auto-trend): ").strip()
    await scheduler.create_content(topic if topic else None)

async def create_cartoon_episode():
    """Create animated cartoon episode"""
    from create_cartoon_episode import create_episode
    topic = input("\n📝 Cartoon story topic: ").strip()
    if not topic:
        topic = "A brave little cat who discovers a magical world"
    lang = input("🌐 Language (english/urdu/hindi) [english]: ").strip() or "english"
    scenes = input("🎬 Number of scenes [10]: ").strip() or "10"
    await create_episode(topic, lang, int(scenes))

def start_scheduler():
    """Start auto-scheduler"""
    from auto_scheduler import AutoScheduler
    scheduler = AutoScheduler()
    scheduler.show_status()
    
    console.print("\n1. Create Content NOW")
    console.print("2. Run Daily Auto-Schedule")
    choice = input("👉 ").strip()
    
    if choice == "1":
        topic = input("Topic (Enter=auto): ").strip()
        asyncio.run(scheduler.create_content(topic if topic else None))
    elif choice == "2":
        scheduler.run_forever()

def launch_dashboard():
    """Launch web dashboard"""
    console.print("[green]🚀 Launching Web Dashboard...[/green]")
    os.system("streamlit run app.py")

def show_menu():
    console.print("\n[bold cyan]📋 MAIN MENU[/bold cyan]")
    console.print("1.  🎬 Create Standard Video (News/Tech/Reviews)")
    console.print("2.  🎨 Create Cartoon Episode (Animated Series)")
    console.print("3.  ⏰ Auto-Scheduler (Daily Hands-Free)")
    console.print("4.  🔍 Find Trending Topics")
    console.print("5.  ✍️  Generate Script Only")
    console.print("6.  🎙️  Generate Voiceover Only")
    console.print("7.  🖼️  Generate Thumbnail Only")
    console.print("8.  📈 Generate SEO Package Only")
    console.print("9.  🌐 Launch Web Dashboard")
    console.print("10. ❌ Exit")

async def main():
    show_banner()
    check_system()
    
    while True:
        show_menu()
        choice = input("\n👉 Choice (1-10): ").strip()
        
        if choice == "1":
            await create_standard_video()
        elif choice == "2":
            await create_cartoon_episode()
        elif choice == "3":
            start_scheduler()
        elif choice == "4":
            from research.trend_finder import TrendFinder
            finder = TrendFinder(niche="tech", language="english")
            trends = finder.find_trends(10)
            console.print("\n🔥 TRENDING TOPICS:")
            for i, t in enumerate(trends, 1):
                console.print(f"  {i}. {t['topic'][:80]} (Score: {t.get('score', 'N/A')})")
        elif choice == "5":
            from content.script_generator import ScriptGenerator
            gen = ScriptGenerator()
            topic = input("📝 Topic: ").strip()
            result = gen.generate_script({'topic': topic})
            console.print(f"\n[green]✅ Script ({result['word_count']} words):[/green]")
            console.print(result['script'][:800])
        elif choice == "6":
            from content.voiceover_gen import VoiceoverGenerator
            gen = VoiceoverGenerator()
            text = input("🎙️ Text to speak: ").strip()
            await gen.generate(text, "output/manual_voice.mp3")
            console.print("[green]✅ Voiceover saved to output/manual_voice.mp3[/green]")
        elif choice == "7":
            from content.thumbnail_maker import ThumbnailMaker
            maker = ThumbnailMaker()
            topic = input("🖼️ Topic: ").strip()
            path = maker.create_thumbnail(topic)
            console.print(f"[green]✅ Thumbnail: {path}[/green]")
        elif choice == "8":
            from seo.seo_engine import SEOEngine
            seo = SEOEngine()
            topic = input("📈 Topic: ").strip()
            result = seo.generate_all_metadata(topic)
            console.print(f"\n[green]Title: {result.get('best_title')}[/green]")
            console.print(f"Tags: {', '.join(result.get('tags', [])[:15])}")
            console.print(f"CTR Score: {result.get('estimated_ctr', {}).get('score', 'N/A')}/100")
        elif choice == "9":
            launch_dashboard()
            break
        elif choice == "10":
            console.print("[green]👋 Goodbye![/green]")
            break
        else:
            console.print("[red]Invalid choice![/red]")

if __name__ == "__main__":
    asyncio.run(main())