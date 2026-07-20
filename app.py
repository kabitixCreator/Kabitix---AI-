import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Kabitix AI", page_icon="🤖", layout="wide")

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_sidebar_menu" not in st.session_state:
    st.session_state.show_sidebar_menu = False

# Sidebar (always accessible)
with st.sidebar:
    st.title("🤖 Kabitix AI")
    st.success("✅ Unlimited & Free")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
    
    st.markdown("---")
    menu = st.radio("Navigation", ["💬 Chat", " Camera/Images", "⚙️ Settings"])

# Main Interface
st.title("💬 AI Chat")
st.caption("Your 100% free, unlimited AI engine")

# Quick action buttons at the top
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➕ New", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("📸 Images", use_container_width=True):
        st.session_state.show_images = True
with col3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.show_settings = True

# Show Chat or Images based on state
if not st.session_state.get('show_images', False) and not st.session_state.get('show_settings', False):
    # CHAT INTERFACE
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner(" Thinking..."):
                try:
                    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                    response = requests.get(url, timeout=10).text
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except:
                    st.write("️ Error! Try again.")

elif st.session_state.get('show_images', False):
    # IMAGE GENERATOR
    st.title("📸 Image Generator")
    prompt = st.text_input("Describe the image you want:")
    if st.button("🎨 Generate Image"):
        if prompt:
            with st.spinner("Creating image..."):
                try:
                    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
                    st.image(url, caption=prompt, use_column_width=True)
                except:
                    st.error("Failed to generate image")
    
    if st.button("️ Back to Chat"):
        st.session_state.show_images = False

elif st.session_state.get('show_settings', False):
    # SETTINGS
    st.title("⚙️ Settings")
    if st.button("🗑️ Clear All Chats"):
        st.session_state.messages = []
        st.success("Chat cleared!")
    
    st.markdown("---")
    st.write("**About Kabitix AI**")
    st.write("✅ 100% Free & Unlimited")
    st.write("🤖 Powered by Pollinations.ai")
    st.write("© 2026 Built by Kabit Lego")
    
    if st.button("⬅️ Back to Chat"):
        st.session_state.show_settings = False
