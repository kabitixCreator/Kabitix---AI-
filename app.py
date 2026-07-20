
import streamlit as st
import requests
import urllib.parse

# --- Page Configuration ---
st.set_page_config(
    page_title="Kabitix AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a Modern, Professional Look ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .stChatInput>div>div>input {
        border-radius: 10px;
    }
    /* Make the sidebar look clean */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🤖 Kabitix AI")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Menu", 
    ["💬 AI Chat", "✨ Features", "⚙️ Settings", "ℹ️ About"]
)

st.sidebar.markdown("---")
st.sidebar.success("✅ Status: Unlimited & Free")
st.sidebar.caption("© 2026 Kabitix AI. Built by Kabit Lego.")

# --- Initialize Session State for Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Main App Pages ---

# 1. AI CHAT PAGE (Your working AI logic + Better UI)
if menu == "💬 AI Chat":
    st.header("💬 Chat with Kabitix")
    st.caption("Your 100% free, unlimited original AI engine.")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask Kabitix anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Kabitix is thinking..."):
                try:
                    # Your brilliant free AI connection node!
                    safe_prompt = urllib.parse.quote(prompt)
                    url = f"https://text.pollinations.ai/{safe_prompt}"
                    res = requests.get(url, timeout=15)
                    
                    response = res.text
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error("⚠️ Connection glitch. Please try sending your message again!")

# 2. FEATURES PAGE (Makes the app look FULL)
elif menu == "✨ Features":
    st.header("✨ Why Choose Kabitix AI?")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🚀 100% Free & Unlimited**\n\nNo premium paywalls. No daily limits. No waiting for resets. Just pure AI power.")
        st.success("**🔒 Private & Secure**\n\nYour conversations are processed securely. We value your privacy.")
    with col2:
        st.warning("**⚡ Lightning Fast**\n\nPowered by optimized connection nodes for instant responses.")
        st.error("**🎨 Constantly Evolving**\n\nBuilt by Kabit Lego, continuously updated with new capabilities.")

# 3. SETTINGS PAGE
elif menu == "⚙️ Settings":
    st.header("⚙️ App Settings")
    st.subheader("Chat Management")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared successfully!")
    
    st.subheader("About the Engine")
    st.write("Currently running on: **Pollinations.ai Free Node**")
    st.write("Timeout limit: **15 seconds**")

# 4. ABOUT PAGE
elif menu == "ℹ️ About":
    st.header("ℹ️ About Kabitix AI")
    st.markdown("""
    **Kabitix AI** is an independent AI platform built to provide a seamless, unlimited, and completely free artificial intelligence experience. 
    
    Unlike traditional platforms that restrict you with premium subscriptions and daily usage resets, Kabitix AI is designed for **everyone**.
    
    👨‍💻 **Creator:** Kabit Lego  
    🏢 **Company:** Kabitix AI  
    🌐 **Mission:** Making advanced AI accessible to all, without limits.
    """)
