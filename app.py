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
    
    /* White outline icons for actions */
    .action-icon {
        color: #ffffff;
        opacity: 0.7;
        cursor: pointer;
        font-size: 20px;
    }
    .action-icon:hover {
        opacity: 1;
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
    
    /* Plus button styling */
    .plus-btn {
        background-color: #424242;
        border: 2px solid #666;
        border-radius: 12px;
        padding: 10px 15px;
        color: white;
        font-size: 24px;
        cursor: pointer;
    }
    .plus-btn:hover {
        background-color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar
col_logo, col_newchat = st.columns([4, 1])
with col_logo:
    try:
        st.image("kabitix.png", width=50)
    except:
        st.markdown('<span style="font-size:30px;"></span>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 24px; margin-left: 10px; display: inline;">Kabitix</h1>', unsafe_allow_html=True)

with col_newchat:
    if st.button(" New Chat", use_container_width=False):
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
        
        # Action Buttons with WHITE ICONS
        st.markdown(f'''
        <div style="display: flex; gap: 15px; margin-top: 10px;">
            <span class="action-icon" onclick="handleFeedback('{msg_id}', 'like')" title="Good response"></span>
            <span class="action-icon" onclick="handleFeedback('{msg_id}', 'dislike')" title="Bad response">👎</span>
            <span class="action-icon" onclick="copyText('{msg_id}')" title="Copy">📋</span>
            <span class="action-icon" onclick="speakText('{msg_id}')" title="Read aloud"></span>
            <span class="action-icon" onclick="shareText('{msg_id}')" title="Share">📤</span>
        </div>
        <div id="feedback-{msg_id}" style="color: #888; font-size: 12px; margin-top: 5px;"></div>
        ''', unsafe_allow_html=True)

# JavaScript for button actions
st.markdown("""
<script>
function handleFeedback(msgId, type) {
    const feedbackDiv = document.getElementById(`feedback-${msgId}`);
    if (type === 'like') {
        feedbackDiv.innerHTML = '✅ Thanks for the feedback!';
    } else {
        feedbackDiv.innerHTML = '👎 Thanks for the feedback!';
    }
}

function copyText(msgId) {
    navigator.clipboard.writeText('Response copied!');
    alert('Response copied to clipboard!');
}

function speakText(msgId) {
    alert('Reading aloud... (feature coming soon)');
}

function shareText(msgId) {
    alert('Share feature coming soon!');
}
</script>
""", unsafe_allow_html=True)

# Input Area with WORKING + Icon
st.markdown("---")

# Show upload options if + is clicked
if st.button("➕", key="plus_icon", help="Upload files or images"):
    st.session_state.show_upload_menu = not st.session_state.show_upload_menu

if st.session_state.show_upload_menu:
    st.markdown("""
    <div style="background-color: #2f2f2f; padding: 15px; border-radius: 12px; margin-bottom: 10px;">
        <p style="margin: 0 0 10px 0; color: #ececf1;">What would you like to upload?</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Upload Document", use_container_width=True):
            st.info("Document upload feature coming soon!")
    with col2:
        if st.button("🖼️ Upload Image", use_container_width=True):
            st.info("Image upload feature coming soon!")
    
    if st.button("️ Close"):
        st.session_state.show_upload_menu = False
        st.rerun()

# Chat Input
if prompt := st.chat_input("Message Kabitix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Kabitix is thinking..."):
        response = get_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
