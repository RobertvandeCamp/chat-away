import streamlit as st
from app.services.websocket_client import WebSocketClient, handle_websocket_message, handle_websocket_error
from app.utils.config import get_config
from app.utils.session import clear_conversation
from app.utils.logger import get_logger

logger = get_logger(__name__)

def render_sidebar():
    """Render the sidebar with settings and controls."""
    logger.info("Rendering sidebar")
    
    with st.sidebar:
        st.title("Chatbot Settings")
        
        # Get configuration
        config = get_config()
        
        # Model selection
        logger.debug("Rendering model selection")
        st.subheader("Model Settings")
        model_options = ["gpt-3.5-turbo", "gpt-4"]
        
        # Use default model from config if not set in session state
        if "openai_model" not in st.session_state:
            st.session_state.openai_model = config["openai"]["default_model"]
        
        current_model = st.session_state.openai_model
        logger.debug(f"Current model: {current_model}")
        
        selected_model = st.selectbox(
            "Select OpenAI Model",
            options=model_options,
            index=model_options.index(current_model) if current_model in model_options else 0
        )
        
        if selected_model != current_model:
            logger.info(f"Model changed from {current_model} to {selected_model}")
            st.session_state.openai_model = selected_model
        
        # WebSocket connection
        logger.debug("Rendering WebSocket connection section")
        st.subheader("WebSocket Connection")
        websocket_status = "Connected" if st.session_state.websocket_connected else "Disconnected"
        logger.debug(f"WebSocket status: {websocket_status}")
        st.write(f"Status: {websocket_status}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Connect WebSocket"):
                logger.info("Connect WebSocket button clicked")
                connect_websocket()
        
        with col2:
            if st.button("Disconnect WebSocket"):
                logger.info("Disconnect WebSocket button clicked")
                disconnect_websocket()
        
        # Conversation controls
        logger.debug("Rendering conversation controls")
        st.subheader("Conversation")
        if st.button("Clear Conversation"):
            logger.info("Clear Conversation button clicked")
            clear_conversation()
            logger.debug("Triggering Streamlit rerun after clearing conversation")
            st.rerun()
        
        # Debug mode toggle
        st.subheader("Debug Settings")
        debug_mode = st.checkbox("Debug Mode", value=config["app"]["debug"])
        if debug_mode != config["app"]["debug"]:
            logger.info(f"Debug mode changed to: {debug_mode}")
            config["app"]["debug"] = debug_mode
            st.session_state.config = config
        
        # About section
        logger.debug("Rendering about section")
        st.subheader("About")
        st.markdown("""
        This chatbot uses OpenAI's models for direct responses and 
        semantic search via AWS for information retrieval.
        """)

def connect_websocket():
    """Connect to WebSocket endpoint."""
    logger.info("Attempting to connect to WebSocket")
    
    if st.session_state.websocket_connected:
        logger.warning("WebSocket already connected, skipping connection")
        st.sidebar.warning("WebSocket already connected")
        return
    
    try:
        logger.debug("Getting WebSocket configuration")
        config = get_config()
        websocket_url = config["aws"]["websocket_url"]
        logger.debug(f"WebSocket URL: {websocket_url}")
        
        # Initialize WebSocket client
        logger.info("Initializing WebSocket client")
        client = WebSocketClient(
            websocket_url=websocket_url,
            on_message=handle_websocket_message,
            on_error=handle_websocket_error
        )
        
        # Connect to WebSocket
        logger.info("Connecting to WebSocket")
        client.connect()
        
        # Store client in session state
        logger.debug("Storing WebSocket client in session state")
        st.session_state.websocket_client = client
        
        logger.info("WebSocket connection initiated successfully")
        st.sidebar.success("WebSocket connection initiated")
        
    except Exception as e:
        logger.error(f"Failed to connect to WebSocket: {str(e)}", exc_info=True)
        st.sidebar.error(f"Failed to connect to WebSocket: {str(e)}")

def disconnect_websocket():
    """Disconnect from WebSocket endpoint."""
    logger.info("Attempting to disconnect from WebSocket")
    
    if not st.session_state.websocket_connected:
        logger.warning("WebSocket not connected, nothing to disconnect")
        st.sidebar.warning("WebSocket not connected")
        return
    
    try:
        if "websocket_client" in st.session_state:
            logger.info("Disconnecting WebSocket client")
            st.session_state.websocket_client.disconnect()
            st.session_state.websocket_connected = False
            logger.info("WebSocket disconnected successfully")
            st.sidebar.success("WebSocket disconnected")
        else:
            logger.warning("No active WebSocket client found in session state")
            st.sidebar.warning("No active WebSocket connection found")
            
    except Exception as e:
        logger.error(f"Error disconnecting WebSocket: {str(e)}", exc_info=True)
        st.sidebar.error(f"Error disconnecting WebSocket: {str(e)}") 