import streamlit as st
from typing import List, Dict, Any, Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    logger.info("Initializing session state variables")
    
    if "messages" not in st.session_state:
        logger.debug("Creating empty messages list in session state")
        st.session_state.messages = []
    else:
        logger.debug(f"Messages already in session state: {len(st.session_state.messages)} messages")
    
    if "conversation_id" not in st.session_state:
        logger.debug("Setting conversation_id to None in session state")
        st.session_state.conversation_id = None
    else:
        logger.debug(f"Conversation ID already in session state: {st.session_state.conversation_id}")
    
    if "websocket_connected" not in st.session_state:
        logger.debug("Setting websocket_connected to False in session state")
        st.session_state.websocket_connected = False
    
    if "search_results" not in st.session_state:
        logger.debug("Creating empty search_results list in session state")
        st.session_state.search_results = []
    
    if "openai_model" not in st.session_state:
        logger.debug("Setting default OpenAI model in session state")
        st.session_state.openai_model = "gpt-4"
    
    logger.info("Session state initialization complete")

def add_message(role: str, content: str, search_query: Optional[str] = None):
    """Add a message to the conversation history.
    
    Args:
        role: The role of the message sender (user, assistant, system)
        content: The content of the message
        search_query: Optional search query associated with the message
    """
    logger.info(f"Adding {role} message to conversation history")
    logger.debug(f"Message content: {content[:50]}{'...' if len(content) > 50 else ''}")
    
    message = {
        "role": role,
        "content": content,
        "timestamp": st.session_state.get("_timestamp", 0),
    }
    
    if search_query:
        message["search_query"] = search_query
        logger.debug(f"Message includes search query: {search_query}")
    
    st.session_state.messages.append(message)
    logger.debug(f"Conversation history now has {len(st.session_state.messages)} messages")

def get_messages_for_openai() -> List[Dict[str, str]]:
    """Get messages formatted for OpenAI API."""
    logger.debug("Formatting messages for OpenAI API")
    messages = [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in st.session_state.messages
    ]
    logger.debug(f"Formatted {len(messages)} messages for OpenAI API")
    return messages

def clear_conversation():
    """Clear the conversation history."""
    logger.info("Clearing conversation history")
    st.session_state.messages = []
    st.session_state.conversation_id = None
    st.session_state.search_results = []
    logger.debug("Conversation history, ID, and search results cleared") 