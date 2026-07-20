
import streamlit as st
import requests
import urllib.parse
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Kabitix AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "default"
if "chats" not in st.session_state:
    st.session_state.chats = {"default": []}
if "notes" not in st.session_state:
    st.session_state.notes = []

# --- Sidebar ---
st.sidebar.markdown("<h1 style='text-align: center; color: #667eea;'>Kabitix AI</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# New Chat Button
if st.sidebar.button("+ New Chat", use_container_width=True):
    new_chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.chats[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id
    st.rerun()

st.sidebar.markdown("---")

# Navigation Menu
menu_options = [" Dashboard", "💬 AI Chat", "📝 Smart Notes", "🎨 Image Gen", "⚙️ Settings"]
active_section = st.sidebar.radio("Menu", menu_options)

st.sidebar.markdown("---")
st.sidebar.success("✅ Unlimited & Free")
st.sidebar.caption("© 2026 Kabitix AI")

# --- Helper Functions ---
def get_current_chat():
    return st.session_state.chats.get(st.session_state.current_chat_id, [])

def add_to_chat(role, content):
    st.session_state.chats[st.session_state.current_chat_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    })

def ai_response(prompt):
    try:
        safe_prompt = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{safe_prompt}"
        res = requests.get(url, timeout=15)
        return res.text
    except:
        return "Sorry, having trouble connecting. Try again!"

# --- MAIN APP ---

# 🏠 DASHBOARD
if active_section == "🏠 Dashboard":
    st.markdown("<h1 style='text-align: center;'>Welcome to Kabitix</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Your intelligent AI assistant is ready.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💬 AI Chat")
        st.write("Chat with unlimited AI")
        if st.button("Open Chat"):
            st.session_state.active_section = "💬 AI Chat"
    
    with col2:
        st.markdown("### 📝 Smart Notes")
        st.write("Organize your thoughts")
        if st.button("Open Notes"):
            st.session_state.active_section = "📝 Smart Notes"

# 💬 AI CHAT
elif active_section == "💬 AI Chat":
    st.header("💬 AI Chat")
    
    current_chat = get_current_chat()
    for message in current_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask Kabitix anything..."):
        add_to_chat("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ai_response(prompt)
                st.markdown(response)
                add_to_chat("assistant", response)

# 📝 SMART NOTES
elif active_section == "📝 Smart Notes":
    st.header("📝 Smart Notes")
    
    tab1, tab2 = st.tabs(["My Notes", "New Note"])
    
    with tab1:
        if st.session_state.notes:
            for i, note in enumerate(st.session_state.notes):
                with st.expander(f" {note.get('title', 'Untitled')} - {note.get('date', 'N/A')}"):
                    st.write(note.get('content', ''))
                    if st.button("Delete", key=f"del_{i}"):
                        st.session_state.notes.pop(i)
                        st.rerun()
        else:
            st.info("No notes yet. Create your first note!")
    
    with tab2:
        note_title = st.text_input("Note Title")
        note_content = st.text_area("Note Content", height=200)
        
        if st.button("Save Note"):
            if note_title and note_content:
                st.session_state.notes.append({
                    "title": note_title,
                    "content": note_content,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("Note saved!")
                st.rerun()

# 🎨 IMAGE GENERATOR
elif active_section == "🎨 Image Gen":
    st.header("🎨 AI Image Generator")
    
    prompt = st.text_input("Describe the image:", placeholder="A cute robot in space")
    
    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating..."):
                try:
                    safe_prompt = urllib.parse.quote(prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
                    st.image(image_url, caption=prompt, use_column_width=True)
                except:
                    st.error("Failed to generate image")

# ⚙️ SETTINGS
elif active_section == "⚙️ Settings":
    st.header("⚙️ Settings")
    
    if st.button("Clear All Chats"):
        st.session_state.chats = {"default": []}
        st.session_state.current_chat_id = "default"
        st.success("Chats cleared!")
    
    if st.button("Clear All Notes"):
        st.session_state.notes = []
        st.success("Notes cleared!")
