
import streamlit as st
import requests
import urllib.parse

# Page Config
st.set_page_config(page_title="Kabitix AI", page_icon="🧠", layout="wide")

# Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Professional CSS - Clean gray icons
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
    
    /* AI message text */
    .ai-msg {
        padding: 10px 0;
        margin: 10px 0;
        max-width: 85%;
        color: #ececf1;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Clean action buttons - WHITE/GRAY only! */
    .action-row {
        display: flex;
        gap: 15px;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid #333;
    }
    
    .action-icon {
        cursor: pointer;
        font-size: 16px;
        color: #8e8e8e; /* GRAY color - not yellow! */
        transition: all 0.2s;
        filter: grayscale(100%); /* Force grayscale */
    }
    
    .action-icon:hover {
        color: #ffffff; /* White on hover */
        transform: scale(1.1);
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
        
        # Clean GRAY action buttons (no yellow emojis!)
        st.markdown('''
        <div class="action-row">
            <span class="action-icon" title="Good response">&#128077;</span>
            <span class="action-icon" title="Bad response">&#128078;</span>
            <span class="action-icon" title="Copy">&#128203;</span>
            <span class="action-icon" title="Read aloud">&#128266;</span>
            <span class="action-icon" title="Share">&#128230;</span>
        </div>
        ''', unsafe_allow_html=True)

# ==========================================
# CHAT INPUT & LOGIC
# ==========================================
if prompt := st.chat_input("Message Kabitix..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        response = requests.get(url, timeout=15).text
        
        # Add AI message
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
        
    except Exception as e:
        st.error("⚠️ Connection error. Please try again.")
