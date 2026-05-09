"""
📤 YOUTUBE UPLOADER
Auto-upload videos with SEO metadata
Uses YouTube Data API v3 (Free: 10,000 units/day)
"""
import os
import pickle
from pathlib import Path
from loguru import logger
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

class YouTubeUploader:
    """Upload videos to YouTube with full metadata"""
    
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    
    def __init__(self):
        self.youtube = None
        self.authenticated = False
    
    def authenticate(self, client_secrets_file: str = None) -> bool:
        """Authenticate with YouTube API"""
        
        logger.info("🔐 Authenticating with YouTube...")
        
        # Check for API key (simple uploads) vs OAuth (advanced)
        api_key = os.getenv("YOUTUBE_API_KEY")
        
        if api_key and "your_" not in api_key:
            # Use API key for public data
            self.youtube = build(
                self.API_SERVICE_NAME,
                self.API_VERSION,
                developerKey=api_key
            )
            logger.info("✅ Authenticated with API Key (Read-only + Upload)")
            self.authenticated = True
            return True
        
        logger.warning("⚠️ No valid YouTube API key found")
        return False
    
    def upload_video(self, video_path: str, metadata: Dict, 
                    privacy: str = "private") -> Dict:
        """Upload a video to YouTube"""
        
        if not self.authenticated:
            self.authenticate()
        
        if not self.youtube:
            logger.error("❌ Not authenticated")
            return {"error": "Not authenticated"}
        
        if not Path(video_path).exists():
            logger.error(f"❌ Video not found: {video_path}")
            return {"error": "Video file not found"}
        
        logger.info(f"📤 Uploading: {Path(video_path).name}...")
        
        # Prepare metadata
        body = {
            "snippet": {
                "title": metadata.get("best_title", metadata.get("topic", "Video"))[:100],
                "description": metadata.get("description", "")[:5000],
                "tags": metadata.get("tags", [])[:30],
                "categoryId": "28",  # Science & Technology
                "defaultLanguage": metadata.get("language", "en"),
            },
            "status": {
                "privacyStatus": privacy,  # private, unlisted, public
                "selfDeclaredMadeForKids": False,
            }
        }
        
        try:
            # Create media upload
            media = MediaFileUpload(
                video_path,
                mimetype="video/mp4",
                resumable=True
            )
            
            # Insert video
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            
            logger.info("⏳ Uploading (this may take several minutes)...")
            
            # Execute upload with progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"   Upload progress: {progress}%")
            
            video_id = response.get("id")
            video_url = f"https://youtube.com/watch?v={video_id}"
            
            logger.info(f"✅ Upload complete!")
            logger.info(f"   Video ID: {video_id}")
            logger.info(f"   URL: {video_url}")
            
            return {
                "success": True,
                "video_id": video_id,
                "url": video_url,
                "title": body["snippet"]["title"]
            }
            
        except Exception as e:
            logger.error(f"❌ Upload failed: {e}")
            return {"error": str(e)}
    
    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """Set custom thumbnail for video"""
        
        if not self.youtube:
            logger.error("❌ Not authenticated")
            return False
        
        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            
            logger.info(f"🖼️ Thumbnail set for video: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Thumbnail upload failed: {e}")
            return False
    
    def get_channel_info(self) -> Dict:
        """Get channel statistics"""
        
        if not self.authenticated:
            self.authenticate()
        
        try:
            request = self.youtube.channels().list(
                part="snippet,statistics",
                mine=True
            )
            response = request.execute()
            
            if response.get("items"):
                channel = response["items"][0]
                return {
                    "title": channel["snippet"]["title"],
                    "subscribers": channel["statistics"].get("subscriberCount", "Hidden"),
                    "views": channel["statistics"].get("viewCount", "0"),
                    "videos": channel["statistics"].get("videoCount", "0"),
                }
        except:
            pass
        
        return {"title": "Unknown", "subscribers": "N/A"}


# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("📤  YOUTUBE UPLOADER TEST")
    print("="*60)
    
    uploader = YouTubeUploader()
    
    # Test authentication
    print("\n🔐 Testing authentication...")
    if uploader.authenticate():
        print("✅ Authentication successful!")
        
        # Test if test video exists
        test_video = "output/test_video.mp4"
        test_metadata_path = "output/seo_test.json"
        
        if Path(test_video).exists():
            print(f"\n✅ Found test video: {test_video}")
            print(f"   Size: {Path(test_video).stat().st_size / (1024*1024):.1f} MB")
            
            # Load metadata
            import json
            metadata = {
                "topic": "Google Pixel Battery Drain Fix",
                "best_title": "Shocking Pixel Battery Drain Fix (2024)",
                "description": "Is your Pixel battery draining fast? Here's the ultimate fix!",
                "tags": ["Google Pixel", "Battery Fix", "Android", "Pixel Tips"],
                "language": "english"
            }
            
            if Path(test_metadata_path).exists():
                with open(test_metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
            
            print(f"\n📋 Ready to upload:")
            print(f"   Title: {metadata.get('best_title', 'N/A')[:80]}")
            print(f"   Tags: {len(metadata.get('tags', []))} tags")
            
            # Ask before uploading
            print("\n⚠️ This will upload to your YouTube channel!")
            choice = input("Continue? (y/n): ").strip().lower()
            
            if choice == 'y':
                result = uploader.upload_video(
                    video_path=test_video,
                    metadata=metadata,
                    privacy="private"  # Upload as private for safety
                )
                
                if result.get("success"):
                    print(f"\n🎉 Video uploaded successfully!")
                    print(f"   URL: {result.get('url')}")
                    
                    # Try to set thumbnail
                    thumb_path = "output/thumbnails"
                    if Path(thumb_path).exists():
                        thumbs = list(Path(thumb_path).glob("*.jpg"))
                        if thumbs:
                            print(f"\n🖼️ Setting thumbnail...")
                            uploader.set_thumbnail(result['video_id'], str(thumbs[0]))
                else:
                    print(f"\n❌ Upload failed: {result.get('error')}")
            else:
                print("\n❌ Upload cancelled")
        else:
            print(f"\n⚠️ Test video not found: {test_video}")
            print("Run video_creator.py first")
    else:
        print("❌ Authentication failed")
        print("\n💡 To fix: Add your YouTube API key to .env file")
    
    print("\n" + "="*60)