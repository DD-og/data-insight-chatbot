import streamlit as st
import requests
import json
from typing import List
from datetime import datetime

# API Configuration
URL = "https://api.langflow.astra.datastax.com/lf/d32df16c-912e-4108-b74a-d1abc775f169/api/v1/run/4c6df195-bf22-4375-94e5-1a6e2f7bb4eb?stream=false"
TOKEN = "AstraCS:qPzaEhMMIdZiHYILkssXxhaC:ab118817d459f9c6d84662f3fd6c7f757cc6108d9c80bb259186fed5a8841f6d"
def get_bot_response(message: str) -> str:
    """Get response from the API"""
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "AstraDBToolComponent-CF8aW": {},
            "ParseData-cwkgx": {},
            "TextInput-OS4Th": {},
            "ChatInput-L0kXb": {},
            "CombineText-JYwrG": {},
            "GroqModel-7sUX4": {},
            "ChatOutput-X19Q2": {},
        },
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }
    
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        
        # Navigate through the nested structure to get the message
        message_text = response_data['outputs'][0]['outputs'][0]['results']['message']['text']
        return message_text
    except (requests.exceptions.RequestException, KeyError) as e:
        return f"Error: {str(e)}"

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Enhanced Custom CSS with improved styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        max-width: 1200px !important;
        padding: 2rem;
        margin: 0 auto;
    }

    /* Header styling */
    .stTitle {
        color: #1E88E5;
        font-size: 2.5rem !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        border-bottom: 2px solid #E3F2FD;
    }

    /* Chat container styling */
    .stChatMessage {
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        margin-left: 2rem;
        margin-right: 1rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #F5F5F5 0%, #E0E0E0 100%);
        margin-right: 2rem;
        margin-left: 1rem;
    }

    /* Chat input styling */
    .stTextInput {
        border-radius: 25px !important;
        padding: 0.75rem 1.5rem !important;
        border: 2px solid #E3F2FD !important;
        transition: all 0.3s ease;
    }

    .stTextInput:focus {
        border-color: #1E88E5 !important;
        box-shadow: 0 0 0 2px rgba(30,136,229,0.2) !important;
    }

    /* Sidebar styling */
    .sidebar .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        background: #1E88E5;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }

    .sidebar .stButton > button:hover {
        background: #1565C0;
        transform: translateY(-2px);
    }

    /* Typing indicator styling */
    .typing-indicator {
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-left: 1rem;
    }

    .typing-indicator span {
        height: 10px;
        width: 10px;
        margin: 0 3px;
        background-color: #1E88E5;
        border-radius: 50%;
        display: inline-block;
        animation: bounce 1.5s infinite;
    }

    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
    }

    /* Dark theme support */
    .dark-theme .stTitle {
        color: #90CAF9;
    }

    .dark-theme .user-message {
        background: linear-gradient(135deg, #1E3C5A 0%, #2C5282 100%);
    }

    .dark-theme .assistant-message {
        background: linear-gradient(135deg, #2D3748 0%, #1A202C 100%);
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #1E88E5;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #1565C0;
    }
    </style>
""", unsafe_allow_html=True)

# Update the title with an icon and better formatting
st.markdown('<h1 class="stTitle">🤖 Data Insights Chatbot</h1>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Initialize waiting state if not exists
if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# Display typing indicator when waiting
if st.session_state.waiting_for_response:
    st.markdown("""
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>
    """, unsafe_allow_html=True)

# Custom chat input
if prompt := st.chat_input("What's on your mind?"):
    # Set waiting state to True
    st.session_state.waiting_for_response = True
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        try:
            response = get_bot_response(prompt)
            st.write(response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Reset waiting state
            st.session_state.waiting_for_response = False

# Enhanced sidebar
with st.sidebar:
    st.markdown("### ⚙️ Chat Settings")
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("### 📊 Chat Statistics")
    st.markdown(f"**Total Messages:** {len(st.session_state.messages)}")
    if len(st.session_state.messages) > 0:
        st.markdown(f"**Last Message:** {st.session_state.messages[-1]['timestamp']}")
