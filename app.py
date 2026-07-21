
import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Kabitix AI", page_icon="🧠", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} 
    header {visibility: hidden;}
    .stApp { background-color: #212121; color: #ececf1; }
    .user-msg { background-color: #424242; padding: 12px 18px; border-radius: 20px; margin: 15px 0 15px auto; max-width: 70%; color: #ececf1; font-size: 16px; }
    .ai-msg { padding: 10px 0; margin: 10px 0; max-width: 85%; color: #ececf1; font-size: 16px; line-height: 1.6; }
    .stButton>button { background: none; border: none; color: #8e8e8e; cursor: pointer; padding: 5px 10px; font-size: 16px; }
    .stButton>button:hover { color: #ffffff; background-color: #333; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

# Top Bar (Safe Logo Loading)
col_logo, col_newchat = st.columns([4, 1])
with col_logo:
    try:
        st.image("kabitix.png", width=50)
    except:
        st.markdown("🧠", unsafe_allow_html=True) # Shows emoji if logo missing
    st.markdown('<h1 style="font-size: 24px; margin-left: 10px; display: inline;">Kabitix</h1>', unsafe_allow_html=True)

with col_newchat:
    if st.button("➕ New Chat", use_container_width=False):
        st.session_state.messages = []
        st.session_state.feedback = {}
        st.rerun()

st.markdown("---")

# Welcome Text
if len(st.session_state.messages) == 0:
    st.markdown('<h2 style="text-align: center; color: #ececf1; margin-top: 50px;">How can I help you today?</h2>', unsafe_allow_html=True)

# AI Function
def get_ai_response(prompt):
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        return requests.get(url, timeout=15).text
    except:
        return "⚠️ Connection error. Please try again."

# Chat History
for idx, msg in enumerate(st.session_state.messages):
    msg_id = f"msg_{idx}"
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Action Buttons
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("", key=f"{msg_id}_like"):
                st.session_state.feedback[msg_id] = "liked"
                st.toast("Thanks for the feedback! 👍", icon="✅")
                st.rerun()
        with c2:
            if st.button("👎", key=f"{msg_id}_dislike"):
                st.session_state.feedback[msg_id] = "disliked"
                st.toast("Thanks for the feedback! 👎", icon="✅")
                st.rerun()
        with c3:
            if st.button("📋", key=f"{msg_id}_copy"):
                st.toast("Response copied!", icon="✅")
        with c4:
            if st.button("🔊", key=f"{msg_id}_sound"):
                st.toast("Reading aloud...", icon="🔊")
        with c5:
            if st.button("📤", key=f"{msg_id}_share"):
                st.toast("Share coming soon!", icon="📤")

# Input Area with + Icon
st.markdown("---")
col_plus, col_input = st.columns([1, 10])
with col_plus:
    st.button("➕", help="Upload files or images")
with col_input:
    if prompt := st.chat_input("Message Kabitix..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Kabitix is thinking..."):
            response = get_ai_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
