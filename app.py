
import streamlit as st
import requests
import urllib.parse

# Page Config
st.set_page_config(page_title="Kabitix AI", page_icon="🧠", layout="wide")

# Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    
    /* Top Bar */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        border-bottom: 1px solid #333;
        margin-bottom: 20px;
    }
    
    /* User message bubble */
    .user-msg {
        background-color: #424242;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 15px 0 15px auto;
        max-width: 70%;
        color: #ececf1;
        font-size: 16px;
    }
    
    /* AI message text (no bubble, just clean text) */
    .ai-msg {
        padding: 10px 0;
        margin: 10px 0;
        max-width: 85%;
        color: #ececf1;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Small, clean action buttons (like ChatGPT) */
    .action-row {
        display: flex;
        gap: 12px;
        margin-top: 5px;
        opacity: 0.5; /* Make them subtle */
    }
    
    .action-icon {
        cursor: pointer;
        font-size: 14px;
        color: #b4b4b4;
        transition: opacity 0.2s;
    }
    
    .action-icon:hover {
        opacity: 1;
        color: white;
    }
    
    /* Chat Input */
    .stChatInput textarea {
        background-color: #2f2f2f;
        color: white;
        border-radius: 24px;
        border: 1px solid #424242;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# TOP BAR (Logo + New Chat)
# ==========================================
col_logo, col_newchat = st.columns([3, 1])

with col_logo:
    st.markdown('<h1 style="font-size: 22px; margin: 0; color: #ececf1;">🧠 Kabitix</h1>', unsafe_allow_html=True)

with col_newchat:
    if st.button(" New Chat", use_container_width=False):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")

# ==========================================
# WELCOME MESSAGE (Only shows if chat is empty)
# ==========================================
if len(st.session_state.messages) == 0:
    st.markdown('<h2 style="text-align: center; color: #ececf1; margin-top: 50px;">How can I help you today?</h2>', unsafe_allow_html=True)

# ==========================================
# CHAT MESSAGES
# ==========================================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        # AI Message
        st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Small, clean action buttons (No big yellow emojis!)
        st.markdown('''
        <div class="action-row">
            <span class="action-icon" title="Good response">👍</span>
            <span class="action-icon" title="Bad response">👎</span>
            <span class="action-icon" title="Copy">📋</span>
            <span class="action-icon" title="Read aloud">🔊</span>
            <span class="action-icon" title="Share"></span>
        </div>
        ''', unsafe_allow_html=True)

# ==========================================
# CHAT INPUT & LOGIC
# ==========================================
if prompt := st.chat_input("Message Kabitix..."):
    # 1. Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Get AI response
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        response = requests.get(url, timeout=15).text
        
        # 3. Add AI message ONLY if successful
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun() # Refresh to show new messages
        
    except Exception as e:
        # If error, just show a temporary red box (DO NOT add to chat history)
        st.error("⚠️ Connection error. Please try again.")
