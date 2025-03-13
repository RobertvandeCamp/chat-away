import streamlit as st
from typing import List, Dict, Any
from app.services.openai_service import process_user_input
from app.services.search_service import SearchService
from app.utils.config import get_config
from app.utils.logger import get_logger

logger = get_logger(__name__)

def render_chat_interface():
    """Render the main chat interface."""
    logger.info("Rendering chat interface")
    st.header("AI Chatbot")
    
    # Initialize services
    logger.debug("Getting configuration for services")
    config = get_config()
    
    logger.info("Initializing search service")
    search_service = SearchService(
        api_endpoint=config["aws"]["api_endpoint"],
        api_key=config["aws"]["api_key"]
    )
    
    # Display chat messages
    logger.debug("Displaying chat messages")
    display_chat_messages()
    
    # Chat input
    logger.debug("Rendering chat input")
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        logger.info("User submitted new input")
        logger.debug(f"User input: {user_input[:50]}{'...' if len(user_input) > 50 else ''}")
        
        # Process user input
        logger.info("Processing user input")
        with st.spinner("Thinking..."):
            response = process_user_input(user_input, search_service)
            logger.debug(f"Response: {response[:50]}{'...' if len(response) > 50 else ''}")
        
        # Force UI update
        logger.info("Triggering Streamlit rerun to update UI")
        st.rerun()

def display_chat_messages():
    """Display chat message history."""
    logger.debug("Displaying chat messages from session state")
    
    if not st.session_state.messages:
        logger.debug("No messages to display, showing info message")
        st.info("Send a message to start the conversation!")
        return
    
    # Display all messages
    logger.debug(f"Displaying {len(st.session_state.messages)} messages")
    for idx, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message["content"]
        
        logger.debug(f"Displaying message {idx+1}: role={role}, content preview={content[:30]}...")
        
        if role == "user":
            st.chat_message("user").write(content)
        elif role == "assistant":
            st.chat_message("assistant").write(content)
        elif role == "system":
            # Optionally display system messages differently
            st.chat_message("assistant").write(f"System: {content}") 