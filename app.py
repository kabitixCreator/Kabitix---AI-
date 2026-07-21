
import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Kabitix AI", page_icon="", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}
if "show_upload_menu" not in st.session_state:
    st.session_state.show_upload_menu = False

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} 
    header {visibility: hidden;}
    .stApp { background-color: #212121; color: #ececf1; }
    .user-msg { background-color: #424242; padding: 12px 18px; border-radius: 20px; margin: 15px 0 15px auto; max-width: 70%; color: #ececf1; font-size: 16px; }
    .ai-msg { padding: 10px 0; margin: 10px 0; max-width: 85%; color: #ececf1; font-size: 16px; line-height: 1.6; }
    
    /* WHITE OUTLINE ICONS */
    .icon-row {
        display: flex;
        gap: 12px;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #333;
    }
    .icon-btn {
        background: none;
        border: 1.5px solid #888;
        border-radius: 6px;
        padding: 6px 12px;
        color: #fff;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.2s;
    }
    .icon-btn:hover {
        background-color: #444;
        border-color: #fff;
    }
    
    .stButton>button { 
        background: none; 
        border: none; 
        color: #8e8e8e; 
        cursor: pointer; 
        padding: 5px 10px; 
        font-size: 20px; 
    }
    .stButton>button:hover { 
        color: #ffffff; 
        background-color: #333; 
        border-radius: 6px; 
    }
</style>
""", unsafe_allow_html=True)

# Top Bar
col_logo, col_newchat = st.columns([4, 1])
with col_logo:
    st.markdown('<h1 style="font-size: 24px;"> Kabitix</h1>', unsafe_allow_html=True)
with col_newchat:
    if st.button(" New Chat", use_container_width=False):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")

if len(st.session_state.messages) == 0:
    st.markdown('<h2 style="text-align: center; color: #ececf1; margin-top: 50px;">How can I help you today?</h2>', unsafe_allow_html=True)

def get_ai_response(prompt):
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        res = requests.get(url, timeout=15)
        return res.text
    except:
        return "Hello! I'm Kabitix AI. How can I help you?"

# Chat Messages with WHITE OUTLINE ICONS
for idx, msg in enumerate(st.session_state.messages):
    msg_id = f"msg_{idx}"
    
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # WHITE OUTLINE ACTION BUTTONS
        st.markdown(f'''
        <div class="icon-row">
            <button class="icon-btn" onclick="handleAction('{msg_id}', 'copy')" title="Copy"> Copy</button>
            <button class="icon-btn" onclick="handleAction('{msg_id}', 'like')" title="Good response"> Like</button>
            <button class="icon-btn" onclick="handleAction('{msg_id}', 'dislike')" title="Bad response">👎 Dislike</button>
            <button class="icon-btn" onclick="handleAction('{msg_id}', 'share')" title="Share">📤 Share</button>
        </div>
        <div id="status-{msg_id}" style="color: #888; font-size: 12px; margin-top: 5px;"></div>
        
        <script>
        function handleAction(msgId, action) {{
            const statusDiv = document.getElementById(`status-${{msgId}}`);
            if (action === 'copy') {{
                statusDiv.innerHTML = '✅ Copied to clipboard!';
            }} else if (action === 'like') {{
                statusDiv.innerHTML = '👍 Thanks for the feedback!';
            }} else if (action === 'dislike') {{
                statusDiv.innerHTML = '👎 Thanks for the feedback!';
            }} else if (action === 'share') {{
                statusDiv.innerHTML = '📤 Share feature coming soon!';
            }}
        }}
        </script>
        ''', unsafe_allow_html=True)

# + Button
if st.button("", key="plus_icon"):
    st.session_state.show_upload_menu = not st.session_state.show_upload_menu

if st.session_state.show_upload_menu:
    st.markdown("### What would you like to upload?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Document", use_container_width=True):
            st.info("Coming soon!")
    with col2:
        if st.button("️ Image", use_container_width=True):
            st.info("Coming soon!")

# Chat Input
if prompt := st.chat_input("Message Kabitix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        response = get_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
