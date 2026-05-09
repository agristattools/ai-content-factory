"""
🤖 AI CONTENT FACTORY v1.0
Automated YouTube & Facebook Content Manager
Languages: English | Urdu | Hindi | Punjabi
Formats: Shorts | Landscape | Square
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()
import config

console = Console()

def show_banner():
    banner = """
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║     🤖  AI CONTENT FACTORY  v1.0  🤖        ║
    ║   YouTube & Facebook Automation System      ║
    ║                                              ║
    ║   🌐 EN | UR | HI | PA                     ║
    ║   📐 Shorts | Landscape | Square           ║
    ║   📺 HD | Full HD | 4K                     ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")

def check_system():
    """Verify everything is working"""
    console.print(Panel("[bold yellow]🔍 System Check[/bold yellow]"))
    
    table = Table(title="Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    
    # Python
    py = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python Version", py)
    
    # Config
    table.add_row("Config File", "✅ Loaded")
    
    # Directories
    dirs = ["data", "logs", "output", "research", "content", "seo", "platforms"]
    for d in dirs:
        exists = (config.BASE_DIR / d).exists()
        table.add_row(f"Directory: {d}/", "✅" if exists else "❌")
    
    # API Keys
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

def main():
    show_banner()
    check_system()
    
    console.print("\n[bold]📋 MENU[/bold]")
    console.print("1. Check System Status")
    console.print("2. Setup Wizard (Coming Next)")
    console.print("3. Exit")
    
    choice = input("\n👉 Enter choice (1-3): ").strip()
    
    if choice == "1":
        check_system()
    elif choice == "3":
        console.print("[green]Goodbye! 👋[/green]")
    else:
        console.print("[yellow]Coming soon![/yellow]")

if __name__ == "__main__":
    main()