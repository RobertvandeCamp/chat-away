import os
from typing import Dict, Any
import streamlit as st
from dotenv import load_dotenv
from app.utils.logger import get_logger

logger = get_logger(__name__)

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables and Streamlit secrets.
    
    Returns:
        Dictionary containing configuration values
    """
    logger.info("Loading application configuration")
    
    # Load environment variables from .env file
    logger.info("Loading environment variables from .env file")
    load_dotenv()
    logger.debug("Environment variables loaded from .env file")
    
    # Default configuration
    logger.debug("Setting up default configuration")
    config = {
        "openai": {
            "api_key": os.environ.get("OPENAI_API_KEY", ""),
            "default_model": "gpt-4"
        },
        "aws": {
            "api_endpoint": os.environ.get("AWS_API_ENDPOINT", ""),
            "websocket_url": os.environ.get("AWS_WEBSOCKET_URL", ""),
            "api_key": os.environ.get("AWS_API_KEY", "")
        },
        "app": {
            "debug": os.environ.get("DEBUG", "false").lower() == "true"
        }
    }
    
    # Log environment variables (without sensitive values)
    logger.debug("Environment variables loaded:")
    logger.debug(f"OPENAI_API_KEY: {'[SET]' if os.environ.get('OPENAI_API_KEY') else '[NOT SET]'}")
    logger.debug(f"AWS_API_ENDPOINT: {os.environ.get('AWS_API_ENDPOINT', '[NOT SET]')}")
    logger.debug(f"AWS_WEBSOCKET_URL: {os.environ.get('AWS_WEBSOCKET_URL', '[NOT SET]')}")
    logger.debug(f"AWS_API_KEY: {'[SET]' if os.environ.get('AWS_API_KEY') else '[NOT SET]'}")
    logger.debug(f"DEBUG: {os.environ.get('DEBUG', 'false')}")
        
    # Validate configuration
    logger.info("Validating configuration")
    _validate_config(config)
    
    return config

def _validate_config(config: Dict[str, Any]) -> None:
    """Validate the configuration and log warnings for missing values.
    
    Args:
        config: Configuration dictionary to validate
    """
    # Check for required OpenAI configuration
    if not config["openai"]["api_key"]:
        logger.error("OpenAI API key is not set. OpenAI features will not work.")
    
    # Check for required AWS configuration
    if not config["aws"]["api_endpoint"]:
        logger.warning("AWS API endpoint is not set. Semantic search will not work.")
    
    if not config["aws"]["websocket_url"]:
        logger.warning("AWS WebSocket URL is not set. Real-time updates will not work.")

def get_config() -> Dict[str, Any]:
    """Get configuration.
    
    Returns:
        Dictionary containing configuration values
    """
    return st.session_state.config 