import os
import streamlit as st
from vapi_python import Vapi
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Vapi Voice Assistant",
    page_icon="🎤",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-title {
        font-size: 24px;
        color: #424242;
        text-align: center;
        margin-bottom: 20px;
    }
    .status-active {
        color: #4CAF50;
        font-weight: bold;
    }
    .status-inactive {
        color: #F44336;
        font-weight: bold;
    }
    .container {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'call_active' not in st.session_state:
    st.session_state.call_active = False
if 'vapi_instance' not in st.session_state:
    st.session_state.vapi_instance = None

# Title and description
st.markdown('<div class="main-title">Vapi Voice Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Talk to an AI assistant using your voice</div>', unsafe_allow_html=True)

# API Key input
api_key = os.getenv("VAPI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your Vapi API Key:", type="password", 
                           help="Get your API key from the Vapi dashboard")

# Assistant configuration section
st.markdown('<div class="container">', unsafe_allow_html=True)
st.subheader("Assistant Configuration")

col1, col2 = st.columns(2)

with col1:
    assistant_id = st.text_input("Assistant ID (Optional):", 
                                help="Leave empty to create a custom assistant")
    first_message = st.text_input("First Message:", 
                                 value="Hello! How can I help you today?")
    context = st.text_area("Assistant Context:", 
                          value="You are a helpful AI assistant that responds to user queries in a friendly manner.")

with col2:
    model = st.selectbox("Model:", 
                        options=["gpt-4o"],
                        index=0)
    voice = st.selectbox("Voice:", 
                        options=["jennifer-playht"],
                        index=0)
    recording_enabled = st.checkbox("Enable Recording", value=True)
    interruptions_enabled = st.checkbox("Enable Interruptions", value=False)

st.markdown('</div>', unsafe_allow_html=True)

# Call control section
st.markdown('<div class="container">', unsafe_allow_html=True)
st.subheader("Voice Call Control")

# Display call status
status_text = "ACTIVE" if st.session_state.call_active else "INACTIVE"
status_class = "status-active" if st.session_state.call_active else "status-inactive"
st.markdown(f"Call Status: <span class='{status_class}'>{status_text}</span>", unsafe_allow_html=True)

# Start/Stop call buttons
col1, col2 = st.columns(2)

def start_call():
    if not api_key:
        st.error("Please enter your Vapi API Key")
        return
    
    try:
        # Initialize Vapi instance
        vapi = Vapi(api_key=api_key)
        st.session_state.vapi_instance = vapi
        
        # Prepare assistant configuration
        if assistant_id:
            # Start call with existing assistant ID
            st.session_state.vapi_instance.start(assistant_id=assistant_id)
        else:
            # Create custom assistant
            assistant = {
                "firstMessage": first_message,
                "context": context,
                "model": model,
                "voice": voice,
                "recordingEnabled": recording_enabled,
                "interruptionsEnabled": interruptions_enabled
            }
            st.session_state.vapi_instance.start(assistant=assistant)
        
        st.session_state.call_active = True
        st.success("Call started successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Error starting call: {str(e)}")

def stop_call():
    if st.session_state.vapi_instance:
        try:
            st.session_state.vapi_instance.stop()
            st.session_state.call_active = False
            st.session_state.vapi_instance = None
            st.success("Call stopped successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error stopping call: {str(e)}")

with col1:
    if not st.session_state.call_active:
        st.button("Start Call", on_click=start_call, type="primary", use_container_width=True)

with col2:
    if st.session_state.call_active:
        st.button("Stop Call", on_click=stop_call, type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Instructions section
if not st.session_state.call_active:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("How to Use")
    st.markdown("""
    1. Enter your Vapi API Key (get it from the [Vapi Dashboard](https://dashboard.vapi.ai/))
    2. Configure your assistant or use an existing assistant ID
    3. Click "Start Call" to begin the voice conversation
    4. Speak into your microphone to interact with the assistant
    5. Click "Stop Call" when you're done
    
    **Note:** Make sure your browser has permission to access your microphone.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("Conversation in Progress")
    st.markdown("""
    Your voice conversation is active. Speak into your microphone to interact with the assistant.
    
    Click "Stop Call" when you're finished with the conversation.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Vapi AI")
