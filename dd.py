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

# Enhanced Custom CSS
st.markdown("""
    <style>
    .stChat {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 15px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #E3F2FD;
    }
    .assistant-message {
        background-color: #F5F5F5;
    }
    .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
    }
    .sidebar .stButton > button {
        width: 100%;
        margin-bottom: 10px;
    }

    /* Typing indicator animation */
    .typing-indicator {
        padding: 10px;
        display: flex;
        align-items: center;
    }
    .typing-indicator span {
        height: 8px;
        width: 8px;
        margin: 0 2px;
        background-color: #9E9EA1;
        border-radius: 50%;
        display: inline-block;
        animation: blink 1.5s infinite;
    }
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes blink {
        0% { opacity: 0.1; }
        20% { opacity: 1; }
        100% { opacity: 0.1; }
    }

    /* Custom input styling */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 20px;
        background: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    .dark-theme .chat-input-container {
        background: #262730;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("Data Insights Chatbot 📊")

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

# Enhanced sidebar with more options
with st.sidebar:
    st.header("Chat Settings")
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("### Chat Information")
    st.write(f"Messages: {len(st.session_state.messages)}")
