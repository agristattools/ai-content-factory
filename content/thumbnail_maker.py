"""
🖼️ AI THUMBNAIL MAKER
Creates click-worthy YouTube thumbnails
Uses: Pillow for design, Pollinations for AI images
Output: 1280x720 HD thumbnails
"""
import os
import requests
from pathlib import Path
from loguru import logger
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
import textwrap
from dotenv import load_dotenv

load_dotenv()

class ThumbnailMaker:
    """Generate professional YouTube thumbnails"""
    
    def __init__(self):
        self.size = (1280, 720)  # YouTube thumbnail size
        self.output_dir = Path("output/thumbnails")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Color schemes for different niches
        self.color_schemes = {
            "tech": {
                "bg": (15, 15, 40),        # Dark blue-black
                "accent": (0, 200, 255),    # Cyan
                "text": (255, 255, 255),    # White
                "highlight": (255, 50, 50), # Red
            },
            "motivation": {
                "bg": (20, 20, 20),         # Dark
                "accent": (255, 180, 0),    # Gold
                "text": (255, 255, 255),    # White
                "highlight": (255, 80, 0),  # Orange
            },
            "educational": {
                "bg": (10, 30, 60),         # Navy blue
                "accent": (80, 220, 100),   # Green
                "text": (255, 255, 255),    # White
                "highlight": (255, 255, 0), # Yellow
            },
            "gaming": {
                "bg": (10, 10, 10),         # Black
                "accent": (200, 50, 255),   # Purple
                "text": (255, 255, 255),    # White
                "highlight": (0, 255, 100), # Neon green
            }
        }
    
    def get_ai_background(self, prompt: str) -> Image.Image:
        """Get AI-generated background from Pollinations (FREE)"""
        
        try:
            # Pollinations.ai - completely free, no API key
            encoded_prompt = requests.utils.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.resize(self.size, Image.LANCZOS)
                logger.info(f"🖼️ AI background generated: {prompt[:50]}...")
                return img
            
        except Exception as e:
            logger.warning(f"AI background failed: {e}, using gradient")
        
        return None
    
    def create_gradient_background(self, color1: tuple, color2: tuple) -> Image.Image:
        """Create gradient background"""
        
        img = Image.new('RGB', self.size, color1)
        draw = ImageDraw.Draw(img)
        
        for i in range(self.size[1]):
            r = int(color1[0] + (color2[0] - color1[0]) * i / self.size[1])
            g = int(color1[1] + (color2[1] - color1[1]) * i / self.size[1])
            b = int(color1[2] + (color2[2] - color1[2]) * i / self.size[1])
            draw.line([(0, i), (self.size[0], i)], fill=(r, g, b))
        
        return img
    
    def add_glow_text(self, draw: ImageDraw, text: str, position: tuple, 
                      font_size: int, color: tuple, glow_color: tuple):
        """Add text with glow effect"""
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        x, y = position
        
        # Draw glow (outline)
        for offset in [(2,2), (-2,-2), (2,-2), (-2,2)]:
            draw.text((x+offset[0], y+offset[1]), text, font=font, fill=glow_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=color)
    
    def create_thumbnail(self, topic: str, niche: str = "tech", 
                         style: str = "modern") -> str:
        """Create a complete thumbnail"""
        
        logger.info(f"🖼️ Creating thumbnail for: {topic[:60]}...")
        
        colors = self.color_schemes.get(niche, self.color_schemes["tech"])
        
        # Try AI background first
        bg_prompt = f"professional youtube thumbnail background {niche} {topic[:80]}"
        background = self.get_ai_background(bg_prompt)
        
        if background is None:
            # Fallback: gradient background
            background = self.create_gradient_background(colors["bg"], 
                                                         (colors["bg"][0]+30, 
                                                          colors["bg"][1]+30, 
                                                          colors["bg"][2]+30))
        
        # Darken background for text visibility
        overlay = Image.new('RGBA', self.size, (0, 0, 0, 100))
        background = background.convert('RGBA')
        background = Image.alpha_composite(background, overlay)
        background = background.convert('RGB')
        
        draw = ImageDraw.Draw(background)
        
        # Add accent bar at bottom
        bar_height = 120
        for i in range(bar_height):
            alpha = int(200 * (1 - i/bar_height))
            draw.line(
                [(0, self.size[1]-bar_height+i), (self.size[0], self.size[1]-bar_height+i)],
                fill=colors["accent"]
            )
        
        # Add main title text
        title_words = topic.split()
        title_lines = textwrap.wrap(topic.upper(), width=20)
        
        y_position = 100
        for line in title_lines[:3]:  # Max 3 lines
            # Center text
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.size[0] - text_width) // 2
            
            self.add_glow_text(
                draw, line, (x_position, y_position),
                60, colors["text"], colors["accent"]
            )
            y_position += 80
        
        # Add highlight circle with "NEW" or emoji
        circle_pos = (self.size[0] - 180, 40)
        draw.ellipse(
            [circle_pos[0], circle_pos[1], circle_pos[0]+140, circle_pos[1]+140],
            fill=colors["highlight"]
        )
        
        try:
            emoji_font = ImageFont.truetype("seguiemj.ttf", 60)
        except:
            emoji_font = ImageFont.load_default()
        
        draw.text((circle_pos[0]+40, circle_pos[1]+35), "🔥", font=emoji_font)
        
        # Add small branding text at bottom
        try:
            small_font = ImageFont.truetype("arial.ttf", 24)
        except:
            small_font = ImageFont.load_default()
        
        draw.text(
            (30, self.size[1] - 50), 
            "📺 SUBSCRIBE FOR MORE",
            font=small_font,
            fill=colors["text"]
        )
        
        # Save thumbnail
        filename = f"thumbnail_{topic[:30].replace(' ', '_')}.jpg"
        output_path = str(self.output_dir / filename)
        
        background.save(output_path, "JPEG", quality=95)
        
        size_kb = os.path.getsize(output_path) / 1024
        logger.info(f"✅ Thumbnail saved: {output_path} ({size_kb:.1f} KB)")
        
        return output_path
    
    def create_multiple(self, topics: list, niche: str = "tech") -> list:
        """Create thumbnails for multiple topics"""
        
        results = []
        for topic in topics:
            path = self.create_thumbnail(
                topic.get('topic', topic) if isinstance(topic, dict) else topic,
                niche=niche
            )
            results.append(path)
        
        return results


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🖼️  THUMBNAIL MAKER TEST")
    print("="*60)
    
    maker = ThumbnailMaker()
    
    # Test 1: Tech thumbnail
    print("\n📸 Creating Tech Thumbnail...")
    path1 = maker.create_thumbnail(
        topic="Google Pixel Battery Drain - FIXED!",
        niche="tech"
    )
    print(f"✅ Saved: {path1}")
    
    # Test 2: Motivation thumbnail
    print("\n📸 Creating Motivation Thumbnail...")
    path2 = maker.create_thumbnail(
        topic="5 Morning Habits That Changed My Life",
        niche="motivation"
    )
    print(f"✅ Saved: {path2}")
    
    print("\n" + "="*60)
    print("✅ THUMBNAIL TEST COMPLETE!")
    print("📁 Check output/thumbnails/ folder")
    print("="*60)