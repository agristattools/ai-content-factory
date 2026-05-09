"""
📘 FACEBOOK AUTO-PUBLISHER
Posts videos/text/images to Facebook Pages
Uses Facebook Graph API (Free)
"""
import os
import requests
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class FacebookPublisher:
    """Auto-publish content to Facebook Pages"""
    
    def __init__(self):
        self.access_token = os.getenv("FB_ACCESS_TOKEN", "")
        self.page_id = os.getenv("FB_PAGE_ID", "")
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    def is_configured(self) -> bool:
        """Check if Facebook credentials are set"""
        return bool(self.access_token and "your_" not in self.access_token 
                   and self.page_id and "your_" not in self.page_id)
    
    def post_text(self, message: str) -> dict:
        """Post a text update to Facebook page"""
        
        if not self.is_configured():
            return {"error": "Facebook not configured. Add FB_ACCESS_TOKEN and FB_PAGE_ID to .env"}
        
        url = f"{self.base_url}/{self.page_id}/feed"
        params = {
            "message": message,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, data=params, timeout=15)
            result = response.json()
            
            if "id" in result:
                logger.info(f"✅ Posted to Facebook: {result['id']}")
                return {"success": True, "post_id": result["id"]}
            else:
                logger.error(f"Facebook post failed: {result}")
                return {"error": result}
        except Exception as e:
            logger.error(f"Facebook error: {e}")
            return {"error": str(e)}
    
    def post_video(self, video_path: str, title: str = "", 
                   description: str = "") -> dict:
        """Upload and publish video to Facebook page"""
        
        if not self.is_configured():
            return {"error": "Facebook not configured"}
        
        if not Path(video_path).exists():
            return {"error": f"Video not found: {video_path}"}
        
        url = f"{self.base_url}/{self.page_id}/videos"
        
        try:
            with open(video_path, "rb") as video_file:
                files = {"source": video_file}
                data = {
                    "title": title[:255] if title else "New Video",
                    "description": description[:5000] if description else "",
                    "access_token": self.access_token
                }
                
                response = requests.post(url, files=files, data=data, timeout=120)
                result = response.json()
                
                if "id" in result:
                    logger.info(f"✅ Video posted to Facebook: {result['id']}")
                    return {"success": True, "video_id": result["id"]}
                else:
                    logger.error(f"Facebook video upload failed: {result}")
                    return {"error": result}
        except Exception as e:
            logger.error(f"Facebook video error: {e}")
            return {"error": str(e)}
    
    def post_photo(self, image_path: str, caption: str = "") -> dict:
        """Post a photo to Facebook page"""
        
        if not self.is_configured():
            return {"error": "Facebook not configured"}
        
        url = f"{self.base_url}/{self.page_id}/photos"
        
        try:
            with open(image_path, "rb") as photo:
                files = {"source": photo}
                data = {
                    "caption": caption[:1000] if caption else "",
                    "access_token": self.access_token
                }
                
                response = requests.post(url, files=files, data=data, timeout=60)
                result = response.json()
                
                if "id" in result:
                    logger.info(f"✅ Photo posted: {result['id']}")
                    return {"success": True, "photo_id": result["id"]}
                else:
                    return {"error": result}
        except Exception as e:
            logger.error(f"Facebook photo error: {e}")
            return {"error": str(e)}


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n📘 Facebook Publisher Test")
    
    fb = FacebookPublisher()
    
    if fb.is_configured():
        print("✅ Facebook API configured")
        
        # Test post
        result = fb.post_text("🤖 Testing from AI Content Factory! Automated post.")
        print(f"Result: {result}")
    else:
        print("⚠️ Facebook not configured")
        print("To setup:")
        print("1. Go to https://developers.facebook.com")
        print("2. Create an App")
        print("3. Get Page Access Token")
        print("4. Add FB_ACCESS_TOKEN and FB_PAGE_ID to .env")