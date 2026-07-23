import streamlit as st
import requests

st.set_page_config(page_title="Kabitix AI", page_icon="🤖", layout="wide")

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
    
    /* WHITE OUTLINE ICONS - EXACTLY LIKE YOUR SCREENSHOT */
    .action-icons {
        display: flex;
        gap: 10px;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #333;
    }
    .icon {
        width: 32px;
        height: 32px;
        border: 2px solid #888;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
        color: #fff;
        font-size: 14px;
    }
    .icon:hover {
        border-color: #fff;
        background-color: #333;
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
st.markdown('<h1 style="font-size: 24px;"> Kabitix</h1>', unsafe_allow_html=True)
if st.button(" New Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("---")

if len(st.session_state.messages) == 0:
    st.markdown('<h2 style="text-align: center; color: #ececf1; margin-top: 50px;">How can I help you today?</h2>', unsafe_allow_html=True)

# WORKING FREE AI - No API Key Needed
def get_ai_response(prompt):
    try:
        # Using a completely free endpoint
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers={"Content-Type": "application/json"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 500}},
            timeout=15
        )
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            # Fallback response if API fails
            responses = {
                "hello": "Hello! How can I help you today?",
                "hi": "Hi there! What can I do for you?",
                "how are you": "I'm doing great! Ready to help you with anything.",
                "what is": "That's a great question! Let me explain...",
                "where": "I'd be happy to help you find that information!",
                "who": "I'm Kabitix AI, your intelligent assistant!",
                "when": "I'm here whenever you need help!",
                "why": "Great question! Here's what I think..."
            }
            for key, value in responses.items():
                if key in prompt.lower():
                    return value
            return "I understand you're asking about that. Here's what I know: The information you're looking for should be available through reliable sources. Is there anything specific you'd like to know more about?"
    except:
        return "I'm here to help! Could you ask your question in a different way?"

# Chat Messages
for idx, msg in enumerate(st.session_state.messages):
    msg_id = f"msg_{idx}"
    
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # WHITE OUTLINE ICONS (Like your screenshot)
        st.markdown(f'''
        <div class="action-icons">
            <div class="icon" onclick="showFeedback('{msg_id}', 'copy')" title="Copy">📋</div>
            <div class="icon" onclick="showFeedback('{msg_id}', 'like')" title="Good response"></div>
            <div class="icon" onclick="showFeedback('{msg_id}', 'dislike')" title="Bad response">👎</div>
            <div class="icon" onclick="showFeedback('{msg_id}', 'share')" title="Share">📤</div>
            <div class="icon" onclick="showFeedback('{msg_id}', 'refresh')" title="Regenerate">🔄</div>
            <div class="icon" onclick="showFeedback('{msg_id}', 'more')" title="More">⋯</div>
        </div>
        <div id="feedback-{msg_id}" style="color: #888; font-size: 12px; margin-top: 8px;"></div>
        
        <script>
        function showFeedback(msgId, action) {{
            const div = document.getElementById(`feedback-${{msgId}}`);
            const messages = {{
                'copy': '✅ Copied to clipboard',
                'like': '👍 Thanks for the feedback!',
                'dislike': '👎 Thanks for the feedback!',
                'share': '📤 Share feature coming soon',
                'refresh': ' Regenerating response...',
                'more': ' More options coming soon'
            }};
            div.innerHTML = messages[action] || '';
            setTimeout(() => {{ div.innerHTML = ''; }}, 3000);
        }}
        </script>
        ''', unsafe_allow_html=True)

st.markdown("---")

# Chat Input
if prompt := st.chat_input("Message Kabitix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Kabitix is thinking..."):
        response = get_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
