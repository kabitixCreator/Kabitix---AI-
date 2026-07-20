
import streamlit as st
import requests
import urllib.parse

# Page Config
st.set_page_config(page_title="Kabitix AI", page_icon="🧠", layout="wide")

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Hide Streamlit branding
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #0f172a;}
</style>
""", unsafe_allow_html=True)

# Logo/Header
st.markdown("<h1 style='text-align: center; color: #60a5fa;'> Kabitix</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 30px;'>AI Note-Taking App</p>", unsafe_allow_html=True)

# Navigation
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button(" Home", use_container_width=True):
        st.session_state.current_page = "home"
with col2:
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.current_page = "chat"
with col3:
    if st.button("📸 Images", use_container_width=True):
        st.session_state.current_page = "images"
with col4:
    if st.button("️ Settings", use_container_width=True):
        st.session_state.current_page = "settings"

st.markdown("---")

# HOME PAGE
if st.session_state.current_page == "home":
    st.markdown("## Welcome to Kabitix")
    st.markdown("Welcome back, Kabit Lego. Your intelligent AI assistant is ready.")
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("**💬 AI Assistant**\n\nAsk questions, get smart answers, and accelerate your learning.")
        if st.button("Open AI Chat", use_container_width=True):
            st.session_state.current_page = "chat"
    
    with c2:
        st.success("**🎨 Image Generator**\n\nCreate stunning images from text descriptions instantly.")
        if st.button("Create Images", use_container_width=True):
            st.session_state.current_page = "images"
    
    c3, c4 = st.columns(2)
    with c3:
        st.warning("**📝 Smart Notes**\n\nCreate, edit, and organize notes with rich text editing.")
        if st.button("My Notes", use_container_width=True):
            st.info("Coming soon!")
    
    with c4:
        st.error("**🔍 Web Search**\n\nFind information from across the web right inside the app.")
        if st.button("Search Web", use_container_width=True):
            st.info("Coming soon!")

# CHAT PAGE
elif st.session_state.current_page == "chat":
    st.title("💬 AI Chat")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
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
                except:
                    st.write("⚠️ Error! Try again.")

# IMAGES PAGE
elif st.session_state.current_page == "images":
    st.title(" AI Image Generator")
    
    img_prompt = st.text_input("Describe the image:", placeholder="A futuristic city")
    
    if st.button(" Generate"):
        if img_prompt:
            with st.spinner("Creating..."):
                try:
                    safe_prompt = urllib.parse.quote(img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
                    st.image(image_url, caption=img_prompt)
                except:
                    st.error("Failed!")

# SETTINGS PAGE
elif st.session_state.current_page == "settings":
    st.title("⚙️ Settings")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.success("Cleared!")
    
    st.markdown("---")
    st.info("**About Kabitix**\n\nVersion: 1.0\nEngine: Pollinations.ai\nCreator: Kabit Lego\n© 2026 Kabitix")
