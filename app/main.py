import streamlit as st
from app.components.chat_interface import render_chat_interface
from app.components.sidebar import render_sidebar
from app.utils.config import load_config, get_config
from app.utils.logger import setup_logger
from app.utils.session import initialize_session_state

# Setup logger
logger = setup_logger()

def main():
    """Main function to run the Streamlit application."""
    logger.info("=== Application starting ===")
    
    # Load configuration and store in session state
    logger.info("Loading configuration")
    config = load_config()
    st.session_state.config = config
    logger.debug(f"Configuration loaded: OpenAI model={config['openai']['default_model']}, Debug mode={config['app']['debug']}")
    
    # Set page configuration
    logger.info("Setting up Streamlit page configuration")
    st.set_page_config(
        page_title="AI Chatbot",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    logger.info("Initializing session state")
    initialize_session_state()
    logger.debug(f"Session state initialized: conversation_id={st.session_state.get('conversation_id')}, model={st.session_state.get('openai_model')}")
    
    # Render sidebar
    logger.info("Rendering sidebar")
    render_sidebar()
    
    # Render main chat interface
    logger.info("Rendering chat interface")
    render_chat_interface()
    
    logger.info("Application UI fully rendered")

if __name__ == "__main__":
    main() 