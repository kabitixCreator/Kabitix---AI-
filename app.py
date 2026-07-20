l
import streamlit as st
import requests
import urllib.parse

# Page Configuration
st.set_page_config(
    page_title="Kabitix AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Professional Blue Theme (matching your logo)
st.markdown("""
<style>
    /* Hide hamburger menu */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Professional dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }
    
    /* Professional blue gradient buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        border: none;
        padding: 12px 24px;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 30px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2);
    }
    
    /* Welcome text */
    .welcome-title {
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .welcome-subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 18px;
    }
    
    /* Chat styling */
    .chat-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Logo and Branding (Centered)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 42px; font-weight: 700; margin: 0;">🧠 Kabitix</h1>
        <p style="color: #64748b; margin: 5px 0 20px 0;">AI Note-Taking App</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation Buttons (Clean, no sidebar)
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button(" Home", use_container_width=True, type="primary" if st.session_state.current_page == "home" else "secondary"):
        st.session_state.current_page = "home"
with nav_col2:
    if st.button("💬 AI Chat", use_container_width=True, type="primary" if st.session_state.current_page == "chat" else "secondary"):
        st.session_state.current_page = "chat"
with nav_col3:
    if st.button("📸 Images", use_container_width=True, type="primary" if st.session_state.current_page == "images" else "secondary"):
        st.session_state.current_page = "images"
with nav_col4:
    if st.button("⚙️ Settings", use_container_width=True, type="primary" if st.session_state.current_page == "settings" else "secondary"):
        st.session_state.current_page = "settings"

st.markdown("---")

# HOME PAGE
if st.session_state.current_page == "home":
    st.markdown('<p class="welcome-title">Welcome to Kabitix</p>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subtitle">Welcome back, Kabit Lego. Your intelligent AI assistant is ready.</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Cards
    feat_col1, feat_col2 = st.columns(2)
    
    with feat_col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #60a5fa; margin-top: 0;">💬 AI Assistant</h3>
            <p style="color: #94a3b8;">Ask questions, get smart answers, and accelerate your learning.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open AI Chat", key="home_chat", use_container_width=True):
            st.session_state.current_page = "chat"
    
    with feat_col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #60a5fa; margin-top: 0;"> Image Generator</h3>
            <p style="color: #94a3b8;">Create stunning images from text descriptions instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Images", key="home_images", use_container_width=True):
            st.session_state.current_page = "images"
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    feat_col3, feat_col4 = st.columns(2)
    with feat_col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #60a5fa; margin-top: 0;">📝 Smart Notes</h3>
            <p style="color: #94a3b8;">Create, edit, and organize notes with rich text editing.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("My Notes", key="home_notes", use_container_width=True):
            st.info("Notes feature coming soon!")
    
    with feat_col4:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #60a5fa; margin-top: 0;">🔍 Web Search</h3>
            <p style="color: #94a3b8;">Find information from across the web right inside the app.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Search Web", key="home_search", use_container_width=True):
            st.info("Web search coming soon!")

# AI CHAT PAGE
elif st.session_state.current_page == "chat":
    st.title("💬 AI Chat")
    st.caption("Your 100% free, unlimited AI engine")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask Kabitix anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                    response = requests.get(url, timeout=15).text
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.write("⚠️ Error! Try again.")

# IMAGE GENERATOR PAGE
elif st.session_state.current_page == "images":
    st.title("📸 AI Image Generator")
    st.caption("Create stunning images from text - 100% free!")
    
    img_prompt = st.text_input("Describe the image you want:", placeholder="A futuristic city at sunset")
    
    if st.button("🎨 Generate Image", use_container_width=True):
        if img_prompt:
            with st.spinner("Creating masterpiece..."):
                try:
                    safe_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
                    st.image(image_url, caption=img_prompt, use_column_width=True)
                except Exception as e:
                    st.error(f"Failed to generate: {e}")

# SETTINGS PAGE
elif st.session_state.current_page == "settings":
    st.title("⚙️ Settings")
    
    st.subheader("Chat Management")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat cleared!")
    
    st.markdown("---")
    st.subheader("About Kabitix AI")
    st.info("""
    **Version:** 1.0  
    **Engine:** Pollinations.ai (Free & Unlimited)  
    **Creator:** Kabit Lego  
    **Status:** ✅ Active & Ready  
    **© 2026 Kabitix. Founded by Kabit.**
    """)
