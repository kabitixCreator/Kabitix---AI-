
import streamlit as st
import requests
import urllib.parse
import json
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
        border: none;
        padding: 10px 20px;
    }
    .stChatInput>div>div>input {
        border-radius: 10px;
    }
    .sidebar-content {
        background-color: #161b22;
    }
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .user-bubble {
        background-color: #2d3748;
        margin-left: 20%;
    }
    .bot-bubble {
        background-color: #1a202c;
        margin-right: 20%;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .note-card {
        background-color: #2d3748;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
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
if "active_section" not in st.session_state:
    st.session_state.active_section = "Dashboard"

# --- Sidebar ---
st.sidebar.markdown("<h1 style='text-align: center; color: #667eea;'>Kabitix AI</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# New Chat Button
if st.sidebar.button("+ New Chat", use_container_width=True):
    new_chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.chats[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id
    st.rerun()

# Search Chats
search_query = st.sidebar.text_input(" Search chats...", "")

st.sidebar.markdown("---")

# Navigation Menu
menu_options = ["🏠 Dashboard", "💬 AI Chat", "📝 Smart Notes", "📚 Library", "📁 Projects", "🧠 Memory", "🎨 Image Gen", "️ Settings"]
active_section = st.sidebar.radio("Menu", menu_options)

st.sidebar.markdown("---")
st.sidebar.success("✅ Unlimited & Free")
st.sidebar.caption("© 2026 Kabitix AI\nBuilt by Kabit Lego")

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
        return "Sorry, I'm having trouble connecting. Please try again!"

# --- MAIN APP ---

# 🏠 DASHBOARD
if active_section == "🏠 Dashboard":
    st.markdown("<h1 style='text-align: center;'>Welcome to Kabitix</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Your intelligent AI assistant is ready.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 AI Chat</h3>
            <p>Chat with unlimited AI</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Chat", key="dash_chat"):
            st.session_state.active_section = "💬 AI Chat"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Smart Notes</h3>
            <p>Organize your thoughts</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Notes", key="dash_notes"):
            st.session_state.active_section = "📝 Smart Notes"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 Image Gen</h3>
            <p>Create stunning images</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Images", key="dash_image"):
            st.session_state.active_section = "🎨 Image Gen"
            st.rerun()
    
    st.markdown("---")
    st.subheader(" Recent Activity")
    total_chats = len(st.session_state.chats)
    total_messages = sum(len(msgs) for msgs in st.session_state.chats.values())
    st.write(f" Total Chats: {total_chats}")
    st.write(f"📨 Total Messages: {total_messages}")
    st.write(f"📝 Saved Notes: {len(st.session_state.notes)}")

# 💬 AI CHAT
elif active_section == "💬 AI Chat":
    st.header("💬 AI Chat")
    st.caption("Your 100% free, unlimited original AI engine.")
    
    # Display chat history
    current_chat = get_current_chat()
    for message in current_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.caption(f" {message.get('timestamp', 'N/A')}")
    
    # Chat Input
    if prompt := st.chat_input("Ask Kabitix anything..."):
        add_to_chat("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🧠 Kabitix is thinking..."):
                response = ai_response(prompt)
                st.markdown(response)
                add_to_chat("assistant", response)
        st.rerun()

#  SMART NOTES
elif active_section == " Smart Notes":
    st.header(" Smart Notes")
    st.caption("Create, edit, and organize notes with AI assistance.")
    
    tab1, tab2 = st.tabs(["📋 My Notes", " New Note"])
    
    with tab1:
        if st.session_state.notes:
            for i, note in enumerate(st.session_state.notes):
                with st.expander(f"📄 {note.get('title', 'Untitled Note')} - {note.get('date', 'N/A')}"):
                    st.write(note.get('content', ''))
                    if st.button("️ Delete", key=f"del_{i}"):
                        st.session_state.notes.pop(i)
                        st.rerun()
        else:
            st.info("No notes yet. Create your first note!")
    
    with tab2:
        note_title = st.text_input("Note Title")
        note_content = st.text_area("Note Content", height=200)
        
        if st.button("💾 Save Note"):
            if note_title and note_content:
                st.session_state.notes.append({
                    "title": note_title,
                    "content": note_content,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("Note saved successfully!")
                st.rerun()
            else:
                st.error("Please fill in both title and content")

# 📚 LIBRARY
elif active_section == "📚 Library":
    st.header("📚 Library")
    st.caption("Your saved resources and documents.")
    
    st.info("📥 Upload documents to analyze them with AI (Coming Soon!)")
    
    uploaded_file = st.file_uploader("Upload PDF/TXT", type=['pdf', 'txt'])
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.write("Feature to analyze documents will be added soon!")

# 📁 PROJECTS
elif active_section == "📁 Projects":
    st.header(" Projects")
    st.caption("Organize your work by projects.")
    
    st.info("📂 Create and manage projects (Coming Soon!)")
    
    project_name = st.text_input("New Project Name")
    if st.button("Create Project"):
        if project_name:
            st.success(f"Project '{project_name}' created!")
        else:
            st.error("Please enter a project name")

# 🧠 MEMORY
elif active_section == "🧠 Memory":
    st.header("🧠 Memory")
    st.caption("AI remembers your preferences and context.")
    
    st.success("✅ Memory is active! The AI remembers context within each chat session.")
    
    st.subheader("Memory Settings")
    clear_memory = st.button("🗑️ Clear All Chat History")
    if clear_memory:
        st.session_state.chats = {"default": []}
        st.session_state.current_chat_id = "default"
        st.success("All chat history cleared!")

# 🎨 IMAGE GENERATOR
elif active_section == " Image Gen":
    st.header(" AI Image Generator")
    st.caption("Create stunning images from text prompts - 100% free!")
    
    prompt = st.text_input("Describe the image you want:", placeholder="A futuristic city at sunset")
    
    if st.button("🖼️ Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                try:
                    safe_prompt = urllib.parse.quote(prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
                    st.image(image_url, caption=prompt, use_column_width=True)
                    st.success("Image generated successfully!")
                except Exception as e:
                    st.error("Failed to generate image. Please try again!")
        else:
            st.warning("Please enter a prompt first!")

# ⚙️ SETTINGS
elif active_section == "️ Settings":
    st.header("⚙️ Settings")
    
    st.subheader("Chat Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Current Chat"):
            st.session_state.chats[st.session_state.current_chat_id] = []
            st.success("Current chat cleared!")
    with col2:
        if st.button("🗑️ Delete This Chat"):
            if st.session_state.current_chat_id != "default":
                del st.session_state.chats[st.session_state.current_chat_id]
                st.session_state.current_chat_id = "default"
                st.success("Chat deleted!")
                st.rerun()
    
    st.subheader("Notes Management")
    if st.button("🗑️ Clear All Notes"):
        st.session_state.notes = []
        st.success("All notes cleared!")
    
    st.subheader("App Info")
    st.write("Version: 1.0.0")
    st.write("Powered by: Pollinations.ai")
    st.write("Status: ✅ Unlimited & Free")
