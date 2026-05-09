"""
🎨 AI IMAGE GENERATOR
Uses FREE Pollinations.ai (no API key needed)
Generates custom images for any content type
Supports: Cartoon, Realistic, Anime, 3D, Sketch styles
"""
import requests
from pathlib import Path
from loguru import logger
from PIL import Image
from io import BytesIO
from typing import List, Dict
import time
import os

class AIImageGenerator:
    """Generate AI images for free using Pollinations.ai"""
    
    STYLES = {
        "cartoon": "cartoon style, vibrant colors, animated, pixar style",
        "realistic": "photorealistic, 8k, detailed, professional photography",
        "anime": "anime style, manga, studio ghibli, japanese animation",
        "3d": "3d render, blender, octane render, cinematic lighting",
        "sketch": "pencil sketch, hand drawn, artistic, black and white",
        "watercolor": "watercolor painting, artistic, soft colors",
        "minimal": "minimalist, clean, simple, flat design",
        "cyberpunk": "cyberpunk, neon lights, futuristic, dark",
    }
    
    def __init__(self, output_dir: str = "output/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://image.pollinations.ai/prompt"
    
    def generate_image(self, prompt: str, style: str = "realistic", 
                       width: int = 1280, height: int = 720, 
                       filename: str = None) -> str:
        """Generate a single AI image"""
        
        style_prompt = self.STYLES.get(style, "")
        full_prompt = f"{prompt}, {style_prompt}"
        
        encoded = requests.utils.quote(full_prompt)
        url = f"{self.base_url}/{encoded}?width={width}&height={height}&nologo=true"
        
        logger.info(f"🎨 Generating: {prompt[:60]}... [{style}]")
        
        try:
            response = requests.get(url, timeout=60)
            
            if response.status_code == 200:
                if filename is None:
                    safe_name = prompt[:40].replace(' ', '_').replace('/', '_')
                    filename = f"{safe_name}_{style}.jpg"
                
                output_path = self.output_dir / filename
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                img = Image.open(BytesIO(response.content))
                img.save(str(output_path), "JPEG", quality=95)
                
                size_kb = os.path.getsize(str(output_path)) / 1024
                logger.info(f"✅ Saved: {output_path} ({size_kb:.1f} KB)")
                
                return str(output_path)
            else:
                logger.error(f"❌ Failed: HTTP {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return ""
    
    def generate_scene_images(self, scenes: List[Dict], style: str = "cartoon",
                             width: int = 1920, height: int = 1080) -> List[str]:
        """Generate images for multiple story scenes"""
        
        logger.info(f"🎬 Generating {len(scenes)} scene images in {style} style...")
        
        image_paths = []
        
        for i, scene in enumerate(scenes):
            scene_desc = scene.get('description', scene.get('text', f'scene {i+1}'))
            
            path = self.generate_image(
                prompt=scene_desc,
                style=style,
                width=width,
                height=height,
                filename=f"scene_{i+1:02d}.jpg"
            )
            
            if path:
                image_paths.append(path)
            
            if i < len(scenes) - 1:
                time.sleep(1)
        
        logger.info(f"✅ Generated {len(image_paths)}/{len(scenes)} scene images")
        return image_paths
    
    def generate_character(self, character_desc: str, style: str = "cartoon",
                          filename: str = "character.jpg") -> str:
        """Generate a consistent character image"""
        
        prompt = f"character design sheet, {character_desc}, full body, white background, consistent character"
        
        return self.generate_image(
            prompt=prompt,
            style=style,
            width=1024,
            height=1024,
            filename=filename
        )
    
    def generate_thumbnail_bg(self, topic: str, niche: str = "tech") -> str:
        """Generate thumbnail background"""
        
        prompts = {
            "tech": f"technology background, {topic}, dark blue, circuit board, futuristic, professional",
            "motivation": f"inspirational background, {topic}, sunrise, golden light, success",
            "gaming": f"gaming background, {topic}, neon, epic, action",
            "education": f"educational background, {topic}, books, knowledge, clean",
            "cartoon": f"cartoon background, {topic}, colorful, fun, animated world",
        }
        
        prompt = prompts.get(niche, prompts["tech"])
        
        return self.generate_image(
            prompt=prompt,
            style="realistic" if niche in ["tech", "motivation"] else "cartoon",
            width=1280,
            height=720,
            filename=f"bg_{topic[:30].replace(' ', '_')}.jpg"
        )


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎨  AI IMAGE GENERATOR TEST")
    print("="*60)
    
    gen = AIImageGenerator()
    
    print("\n🖼️ Test 1: Cartoon Style")
    path1 = gen.generate_image(
        prompt="a brave orange cat wearing a superhero cape, flying over a city",
        style="cartoon",
        filename="super_cat.jpg"
    )
    print(f"   Result: {path1}")
    
    print("\n🖼️ Test 2: Realistic Style")
    path2 = gen.generate_image(
        prompt="futuristic smartphone with holographic display, dark background",
        style="realistic",
        filename="futuristic_phone.jpg"
    )
    print(f"   Result: {path2}")
    
    print("\n" + "="*60)
    print("✅ Image Generator Test Complete!")
    print("="*60)