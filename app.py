import streamlit as st
import requests
import urllib.parse

# Page Config
st.set_page_config(page_title="Kabitix AI", page_icon="🧠", layout="wide")

# Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "chat"

# Clean ChatGPT-style CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* App Background */
    .stApp {
        background-color: #212121;
        color: #ececf1;
    }
    
    /* Clean top bar - just logo and new chat */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 30px;
        border-bottom: 1px solid #424242;
        margin-bottom: 20px;
    }
    
    /* User message */
    .user-msg {
        background-color: #424242;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 15px 0 15px auto;
        max-width: 70%;
        color: #ececf1;
        font-size: 16px;
    }
    
    /* AI message */
    .ai-msg {
        padding: 10px 0;
        margin: 10px 0;
        max-width: 85%;
        color: #ececf1;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Action buttons */
    .action-buttons {
        display: flex;
        gap: 8px;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #424242;
    }
    
    .action-btn {
        background: none;
        border: none;
        color: #b4b4b4;
        cursor: pointer;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 16px;
    }
    
    .action-btn:hover {
        background-color: #424242;
        color: #ececf1;
    }
    
    /* Chat input area */
    .stChatInput textarea {
        background-color: #2f2f2f;
        color: white;
        border-radius: 24px;
        border: 1px solid #424242;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CLEAN TOP BAR (Like ChatGPT)
# ==========================================
col_logo, col_newchat = st.columns([3, 1])

with col_logo:
    st.markdown('<h1 style="font-size: 24px; margin: 0; color: #ececf1;">🧠 Kabitix</h1>', unsafe_allow_html=True)

with col_newchat:
    if st.button("➕ New Chat", use_container_width=False):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")

# ==========================================
# CHAT INTERFACE (Main Focus)
# ==========================================
st.markdown('<h2 style="text-align: center; color: #ececf1; margin-bottom: 30px;">How can I help you today?</h2>', unsafe_allow_html=True)

# Display messages
for idx, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Action buttons for AI messages
        st.markdown('''
        <div class="action-buttons">
            <button class="action-btn" title="Like">👍</button>
            <button class="action-btn" title="Dislike">👎</button>
            <button class="action-btn" title="Copy">📋</button>
            <button class="action-btn" title="Read aloud">🔊</button>
            <button class="action-btn" title="Share">📤</button>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Message Kabitix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Thinking..."):
        try:
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            response = requests.get(url, timeout=15).text
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except:
            st.session_state.messages.append({"role": "assistant", "content": "⚠️ Connection error. Try again."})
            st.rerun()

# ==========================================
# SIDEBAR (Hidden by default, accessible via menu)
# ==========================================
with st.sidebar:
    st.title(" Kabitix Menu")
    st.markdown("---")
    
    if st.button("💬 AI Chat", use_container_width=True):
        st.session_state.current_page = "chat"
        st.rerun()
    
    if st.button("📸 Image Generator", use_container_width=True):
        st.session_state.current_page = "images"
        st.rerun()
    
    st.markdown("---")
    
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.current_page = "settings"
        st.rerun()
    
    st.markdown("---")
    st.caption("© 2026 Kabitix AI\nBuilt by Kabit Lego")
