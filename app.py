"""
🌐 AI CONTENT FACTORY - Web Dashboard
Streamlit-based GUI for the entire automation system
Run: streamlit run app.py
"""
import streamlit as st
import sys
import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Page config MUST be first
st.set_page_config(
    page_title="AI Content Factory",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
sys.path.insert(0, str(Path(__file__).parent))

from research.trend_finder import TrendFinder
from content.script_generator import ScriptGenerator
from content.voiceover_gen import VoiceoverGenerator
from content.video_creator import VideoCreator
from content.thumbnail_maker import ThumbnailMaker
from content.ai_image_gen import AIImageGenerator
from seo.seo_engine import SEOEngine

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background: #d4edda;
        border: 2px solid #28a745;
    }
    .stats-card {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        border: 1px solid #444;
        text-align: center;
        color: white;
    }
    .step-complete {
        color: #28a745;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline_data' not in st.session_state:
    st.session_state.pipeline_data = {}
if 'history' not in st.session_state:
    st.session_state.history = []

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
        st.title("🤖 AI Factory")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "📋 Navigation",
            ["🏠 Dashboard", "🎬 Create Content", "📊 History", "⚙️ Settings"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 System Status")
        
        # API Status
        apis = {
            "Groq AI": os.getenv("GROQ_API_KEY", ""),
            "Gemini": os.getenv("GEMINI_API_KEY", ""),
            "YouTube": os.getenv("YOUTUBE_API_KEY", ""),
            "Pexels": os.getenv("PEXELS_API_KEY", ""),
        }
        
        for name, key in apis.items():
            if key and "your_" not in key:
                st.success(f"✅ {name}")
            else:
                st.warning(f"⚠️ {name}")
    
    # Main content
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "🎬 Create Content":
        create_content_page()
    elif page == "📊 History":
        history_page()
    elif page == "⚙️ Settings":
        settings_page()

def dashboard_page():
    st.markdown('<p class="main-header">🤖 AI Content Factory</p>', unsafe_allow_html=True)
    st.markdown("### Your All-in-One YouTube & Facebook Automation System")
    
    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("📹 Videos Created", len(st.session_state.history))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("✍️ Scripts Written", sum(1 for h in st.session_state.history if h.get('type') == 'script'))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("🎨 Images Generated", len(list(Path("output/images").glob("*.jpg"))))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("📈 SEO Packages", len(list(Path("output").glob("seo_*.json"))))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Find Trending Topics", use_container_width=True):
            with st.spinner("Searching trends..."):
                finder = TrendFinder(niche="tech", language="english")
                trends = finder.find_trends(5)
                st.session_state.trends = trends
                st.success(f"Found {len(trends)} trending topics!")
    
    with col2:
        if st.button("🎬 Create Full Video", use_container_width=True):
            st.info("Go to 'Create Content' page for full pipeline!")
    
    # Show trends if available
    if 'trends' in st.session_state and st.session_state.trends:
        st.markdown("### 🔥 Trending Topics")
        for i, trend in enumerate(st.session_state.trends[:5], 1):
            st.markdown(f"**{i}.** {trend.get('topic', 'N/A')[:100]}")
            st.caption(f"Source: {trend.get('source', 'Unknown')} | Score: {trend.get('score', 'N/A')}")

def create_content_page():
    st.markdown("## 🎬 Create New Content")
    
    # Content type selection
    content_type = st.radio(
        "Select Content Type",
        ["📹 Standard Video (Stock Footage)", "🎨 Cartoon/Animated Story", "✍️ Script Only", "🎙️ Voiceover Only"],
        horizontal=True
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        language = st.selectbox("🌐 Language", ["english", "urdu", "hindi", "punjabi"])
    
    with col2:
        niche = st.selectbox("🎯 Niche", ["tech", "motivation", "educational", "gaming", "cartoon"])
    
    with col3:
        format_type = st.selectbox("📐 Format", ["landscape (16:9)", "shorts (9:16)", "square (1:1)"])
    
    topic = st.text_input("📝 Topic (leave blank for auto-trend)", placeholder="e.g., Latest AI tools, Cartoon cat story...")
    
    if st.button("🚀 Generate Content", type="primary", use_container_width=True):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Research
        status_text.text("🔍 Finding trends...")
        progress_bar.progress(10)
        
        if not topic:
            finder = TrendFinder(niche=niche, language=language)
            trends = finder.find_trends(1)
            topic = trends[0]['topic'] if trends else "Latest technology trends"
        
        # Step 2: Script
        status_text.text("✍️ Writing script...")
        progress_bar.progress(25)
        
        script_gen = ScriptGenerator(language=language, niche=niche)
        script_data = script_gen.generate_script({'topic': topic})
        
        st.text_area("📝 Generated Script", script_data.get('script', '')[:500], height=200)
        
        # Step 3: Voiceover
        status_text.text("🎙️ Generating voiceover...")
        progress_bar.progress(50)
        
        voice_gen = VoiceoverGenerator(language=language)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        voice_path = f"output/voiceover_{timestamp}.mp3"
        
        async def gen_voice():
            await voice_gen.generate(script_data['script'], voice_path)
        asyncio.run(gen_voice())
        
        if Path(voice_path).exists():
            st.audio(voice_path)
        
        # Step 4: Video
        status_text.text("🎬 Creating video...")
        progress_bar.progress(70)
        
        video_creator = VideoCreator(format_type=format_type.split()[0])
        video_path = f"output/video_{timestamp}.mp4"
        
        video_creator.create_video(voice_path, topic, 30, video_path)
        
        if Path(video_path).exists():
            st.video(video_path)
        
        # Step 5: Thumbnail
        status_text.text("🖼️ Creating thumbnail...")
        progress_bar.progress(85)
        
        thumb_maker = ThumbnailMaker()
        thumb_path = thumb_maker.create_thumbnail(topic, niche=niche)
        
        if Path(thumb_path).exists():
            st.image(thumb_path, caption="Generated Thumbnail", width=400)
        
        # Step 6: SEO
        status_text.text("📈 Generating SEO...")
        progress_bar.progress(100)
        
        seo_engine = SEOEngine(language=language, niche=niche)
        seo_data = seo_engine.generate_all_metadata(topic, script_data['script'])
        
        st.markdown("### 📈 SEO Metadata")
        st.markdown(f"**Title:** {seo_data.get('best_title', 'N/A')}")
        st.markdown(f"**CTR Score:** {seo_data.get('estimated_ctr', {}).get('score', 'N/A')}/100")
        
        tags = seo_data.get('tags', [])
        st.markdown(f"**Tags:** {', '.join(tags[:10])}")
        
        # Save to history
        st.session_state.history.append({
            'type': 'full_pipeline',
            'topic': topic,
            'timestamp': timestamp,
            'files': {
                'voiceover': voice_path,
                'video': video_path,
                'thumbnail': thumb_path,
                'seo': f"output/seo_{timestamp}.json"
            }
        })
        
        status_text.text("")
        st.success("✅ Content Creation Complete!")
        st.balloons()

def history_page():
    st.markdown("## 📊 Content History")
    
    if not st.session_state.history:
        st.info("No content created yet. Go to 'Create Content' to get started!")
        return
    
    for i, entry in enumerate(reversed(st.session_state.history)):
        with st.expander(f"📹 {entry.get('topic', 'Untitled')[:80]} - {entry.get('timestamp', 'N/A')}"):
            st.json(entry)

def settings_page():
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### 🔑 API Keys Status")
    
    api_keys = {
        "GROQ_API_KEY": "Groq AI (Script Writing)",
        "GEMINI_API_KEY": "Google Gemini (Research)",
        "YOUTUBE_API_KEY": "YouTube Data API",
        "PEXELS_API_KEY": "Pexels (Stock Footage)",
        "FB_ACCESS_TOKEN": "Facebook Graph API",
    }
    
    for key, description in api_keys.items():
        value = os.getenv(key, "")
        if value and "your_" not in value:
            st.success(f"✅ {description}")
        else:
            st.warning(f"⚠️ {description} - Not Configured")
    
    st.markdown("---")
    st.markdown("### 💡 Default Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_language = st.selectbox("Default Language", ["english", "urdu", "hindi", "punjabi"])
        default_niche = st.selectbox("Default Niche", ["tech", "motivation", "educational", "gaming"])
    
    with col2:
        default_format = st.selectbox("Default Format", ["landscape", "shorts", "square"])
        default_quality = st.selectbox("Video Quality", ["HD", "Full HD", "4K"])
    
    if st.button("💾 Save Settings"):
        # Update .env
        with open(".env", "r") as f:
            lines = f.readlines()
        
        with open(".env", "w") as f:
            for line in lines:
                if line.startswith("CHANNEL_NICHE="):
                    f.write(f"CHANNEL_NICHE={default_niche}\n")
                elif line.startswith("CONTENT_LANGUAGE="):
                    f.write(f"CONTENT_LANGUAGE={default_language}\n")
                else:
                    f.write(line)
        
        st.success("✅ Settings saved!")

if __name__ == "__main__":
    main()