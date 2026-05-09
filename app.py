"""
🌐 AI CONTENT FACTORY - Web Dashboard v2.0
Complete GUI: Standard Video | Cartoon Studio | Auto-Scheduler
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

st.set_page_config(
    page_title="AI Content Factory v2.0",
    page_icon="🤖",
    layout="wide"
)

sys.path.insert(0, str(Path(__file__).parent))

# Custom CSS
st.markdown("""
<style>
.main-header { font-size: 3rem; font-weight: bold; text-align: center;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
.stats-card { padding: 1.5rem; border-radius: 15px; background: linear-gradient(135deg, #1e1e2e, #2d2d44);
    color: white; text-align: center; margin-bottom: 0.5rem; }
.success-box { padding: 1rem; border-radius: 10px; background: #d4edda; border: 2px solid #28a745; }
</style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

def main():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
        st.title("🤖 AI Factory v2.0")
        st.markdown("---")
        
        page = st.radio("📋 Navigation", [
            "🏠 Dashboard",
            "🎬 Standard Video",
            "🎨 Cartoon Studio",
            "⏰ Auto-Scheduler",
            "📊 History",
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        st.markdown("### 📊 API Status")
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
    
    if page == "🏠 Dashboard":
        dashboard_page()
    elif page == "🎬 Standard Video":
        standard_video_page()
    elif page == "🎨 Cartoon Studio":
        cartoon_page()
    elif page == "⏰ Auto-Scheduler":
        scheduler_page()
    elif page == "📊 History":
        history_page()
    elif page == "⚙️ Settings":
        settings_page()

def dashboard_page():
    st.markdown('<p class="main-header">🤖 AI Content Factory v2.0</p>', unsafe_allow_html=True)
    st.markdown("### Complete YouTube & Facebook Automation System")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("📹 Videos", len(st.session_state.history))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        cartoons = len(list(Path("output/cartoon_studio").glob("*.mp4")))
        st.metric("🎨 Cartoons", cartoons)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        thumbs = len(list(Path("output/thumbnails").glob("*.jpg")))
        st.metric("🖼️ Thumbnails", thumbs)
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        seo_count = len(list(Path("output").glob("seo_*.json")))
        st.metric("📈 SEO Packs", seo_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Features")
    st.markdown("""
    - **🎬 Standard Video** - News, Tech Reviews, Tutorials with AI voice & stock footage
    - **🎨 Cartoon Studio** - Animated cartoon series with AI characters & stories
    - **⏰ Auto-Scheduler** - Hands-free daily content creation & posting
    - **📈 SEO Engine** - High-CTR titles, tags & descriptions
    - **🌐 4 Languages** - English, Urdu, Hindi, Punjabi
    """)

def standard_video_page():
    st.markdown("## 🎬 Create Standard Video")
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("🌐 Language", ["english", "urdu", "hindi", "punjabi"])
        niche = st.selectbox("🎯 Niche", ["tech", "motivation", "educational", "gaming"])
    with col2:
        format_type = st.selectbox("📐 Format", ["landscape", "shorts", "square"])
    
    topic = st.text_input("📝 Topic (leave blank for auto-trend)", 
                          placeholder="e.g., Latest AI tools, iPhone review...")
    
    if st.button("🚀 Create Video", type="primary", use_container_width=True):
        from auto_scheduler import AutoScheduler
        scheduler = AutoScheduler(language=language, niche=niche)
        
        with st.spinner("🔍 Researching & Creating..."):
            result = asyncio.run(scheduler.create_content(topic if topic else None))
        
        if result:
            st.success("✅ Video Created Successfully!")
            video_path = result.get("video", "")
            if video_path and Path(video_path).exists():
                st.video(video_path)
            thumb_path = result.get("thumbnail", "")
            if thumb_path and Path(thumb_path).exists():
                st.image(thumb_path, caption="Thumbnail", width=400)
            
            seo = result.get("seo", {})
            if seo:
                st.markdown(f"**📈 Best Title:** {seo.get('best_title', 'N/A')}")
                st.markdown(f"**🎯 CTR Score:** {seo.get('estimated_ctr', {}).get('score', 'N/A')}/100")
            
            st.session_state.history.append(result)

def cartoon_page():
    st.markdown("## 🎨 Cartoon Studio")
    st.markdown("Create animated cartoon episodes with AI characters & stories!")
    
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("📝 Story Topic", "A brave cat who saves the village from a dragon")
        language = st.selectbox("🌐 Language", ["english", "urdu", "hindi"])
    with col2:
        scenes = st.slider("🎬 Number of Scenes", 5, 30, 10)
    
    if st.button("🎬 Create Cartoon Episode", type="primary", use_container_width=True):
        from create_cartoon_episode import create_episode
        
        with st.spinner("🎨 Creating cartoon episode..."):
            result = asyncio.run(create_episode(topic, language, scenes))
        
        if result and Path(result).exists():
            st.success("✅ Cartoon Episode Created!")
            st.video(result)
            size_mb = Path(result).stat().st_size / (1024*1024)
            st.info(f"📦 Size: {size_mb:.1f} MB")
            st.session_state.history.append({"type": "cartoon", "video": result, "topic": topic})

def scheduler_page():
    st.markdown("## ⏰ Auto-Scheduler")
    st.markdown("Hands-free automation - create & post content daily!")
    
    st.markdown("### 📊 Stats")
    stats_path = Path("data/stats.json")
    if stats_path.exists():
        with open(stats_path) as f:
            stats = json.load(f)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Videos Created", stats.get("videos_created", 0))
        c2.metric("Posts Made", stats.get("posts_made", 0))
        c3.metric("Errors", stats.get("errors", 0))
    
    if st.button("▶️ Create Content NOW", use_container_width=True):
        from auto_scheduler import AutoScheduler
        scheduler = AutoScheduler()
        with st.spinner("Creating..."):
            asyncio.run(scheduler.create_content())
        st.success("✅ Done!")

def history_page():
    st.markdown("## 📊 Content History")
    
    history_dir = Path("data/history")
    if history_dir.exists():
        files = sorted(history_dir.glob("*.json"), reverse=True)[:20]
        for f in files:
            with open(f) as fp:
                data = json.load(fp)
            with st.expander(f"📹 {data.get('topic', 'Unknown')[:80]} - {f.stem}"):
                st.json(data)
    else:
        st.info("No content created yet. Create your first video!")

def settings_page():
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### 🔑 API Keys Status")
    keys = {
        "GROQ_API_KEY": "Groq AI (Script Writing)",
        "GEMINI_API_KEY": "Google Gemini (Research)",
        "YOUTUBE_API_KEY": "YouTube Data API",
        "PEXELS_API_KEY": "Pexels (Stock Media)",
    }
    for key, desc in keys.items():
        val = os.getenv(key, "")
        if val and "your_" not in val:
            st.success(f"✅ {desc}")
        else:
            st.warning(f"⚠️ {desc}")
    
    st.markdown("---")
    st.markdown("### 💡 About")
    st.markdown("""
    **AI Content Factory v2.0**
    - 100% FREE APIs
    - 4 Languages supported
    - Standard videos + Cartoon studio
    - Auto-scheduler for hands-free operation
    - Professional web dashboard
    """)

if __name__ == "__main__":
    main()