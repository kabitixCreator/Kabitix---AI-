
import streamlit as st
import requests
import urllib.parse

# Page Config
st.set_page_config(page_title="Kabitix AI", page_icon="", layout="wide")

# Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "chat" # Default to chat

# Professional CSS (Dark Theme + Custom Chat Bubbles)
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* App Background */
    .stApp {
        background-color: #0f172a; /* Deep professional dark blue/slate */
        color: #f8fafc;
    }
    
    /* Top Navigation Buttons */
    .stButton>button {
        background-color: #1e293b;
        color: #94a3b8;
        border: 1px solid #334155;
        border-radius: 8px;
        font-size: 14px;
    }
    .stButton>button:hover {
        background-color: #334155;
        color: white;
    }
    
    /* Chat Input Box */
    .stChatInput textarea {
        background-color: #1e293b;
        color: white;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION (Sleek & Clean) ---
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 1])
with nav_col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "home"
with nav_col2:
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.current_page = "chat"
with nav_col3:
    if st.button("📸 Images", use_container_width=True):
        st.session_state.current_page = "images"
with nav_col4:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.current_page = "settings"

st.markdown("---")

# ==========================================
# PAGE 1: HOME
# ==========================================
if st.session_state.current_page == "home":
    st.markdown("<h1 style='text-align: center; color: #60a5fa;'>Welcome to Kabitix</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Your intelligent AI assistant is ready.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
            <h3 style="color: #60a5fa; margin-top: 0;">💬 AI Assistant</h3>
            <p style="color: #94a3b8;">Ask questions, get smart answers, and accelerate your learning.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Chat", use_container_width=True):
            st.session_state.current_page = "chat"
            
    with c2:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
            <h3 style="color: #60a5fa; margin-top: 0;">🎨 Image Generator</h3>
            <p style="color: #94a3b8;">Create stunning images from text descriptions instantly.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Images", use_container_width=True):
            st.session_state.current_page = "images"

# ==========================================
# PAGE 2: AI CHAT (With Professional Colors)
# ==========================================
elif st.session_state.current_page == "chat":
    st.markdown("<h2 style='color: #f8fafc;'>💬 AI Chat</h2>", unsafe_allow_html=True)
    
    # CUSTOM CHAT BUBBLES (No more orange/yellow!)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            # Professional Blue for User
            st.markdown(f'''
            <div style="background-color: #1e3a8a; padding: 15px; border-radius: 15px; 
                        margin: 10px 0; margin-left: 20%; color: white; font-size: 16px;">
                {msg["content"]}
            </div>''', unsafe_allow_html=True)
        else:
            # Professional Dark Slate for AI
            st.markdown(f'''
            <div style="background-color: #334155; padding: 15px; border-radius: 15px; 
                        margin: 10px 0; margin-right: 20%; color: #e2e8f0; font-size: 16px;">
                {msg["content"]}
            </div>''', unsafe_allow_html=True)

    # Chat Input
    if prompt := st.chat_input("Ask Kabitix anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # AI Response
        with st.spinner("Kabitix is thinking..."):
            try:
                url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                response = requests.get(url, timeout=15).text
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun() # Refresh to show new messages
            except:
                st.session_state.messages.append({"role": "assistant", "content": "⚠️ Connection error. Please try again."})
                st.rerun()

# ==========================================
# PAGE 3: IMAGE GENERATOR
# ==========================================
elif st.session_state.current_page == "images":
    st.markdown("<h2 style='color: #f8fafc;'>📸 AI Image Generator</h2>", unsafe_allow_html=True)
    
    img_prompt = st.text_input("Describe the image you want:", placeholder="A futuristic city at sunset")
    
    if st.button("🎨 Generate Image", use_container_width=True):
        if img_prompt:
            with st.spinner("Creating masterpiece..."):
                try:
                    safe_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
                    st.image(image_url, caption=img_prompt, use_column_width=True)
                except:
                    st.error("Failed to generate image.")

# ==========================================
# PAGE 4: SETTINGS
# ==========================================
elif st.session_state.current_page == "settings":
    st.markdown("<h2 style='color: #f8fafc;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; color: #94a3b8;">
        <h3 style="color: #60a5fa; margin-top: 0;">About Kabitix</h3>
        <p><strong>Version:</strong> 1.0 Professional</p>
        <p><strong>Engine:</strong> Pollinations.ai (Unlimited)</p>
        <p><strong>Creator:</strong> Kabit Lego</p>
        <p style="margin-bottom: 0;">© 2026 Kabitix. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
