import logging
import sys
from typing import Optional
import streamlit as st

def setup_logger(level: Optional[int] = None) -> logging.Logger:
    """Set up and configure the application logger.
    
    Args:
        level: Optional logging level (defaults to INFO or DEBUG based on config)
        
    Returns:
        Configured logger instance
    """
    # Determine log level
    if level is None:
        # Check if debug mode is enabled in config or session state
        debug_mode = False
        if "config" in st.session_state and "app" in st.session_state.config:
            debug_mode = st.session_state.config["app"].get("debug", False)
        level = logging.DEBUG if debug_mode else logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Get the root logger
    logger = logging.getLogger()
    
    # Set specific module log levels if needed
    logging.getLogger("websocket").setLevel(logging.WARNING)  # Reduce noise from websocket library
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module.
    
    Args:
        name: Name of the module (typically __name__)
        
    Returns:
        Logger instance for the module
    """
    return logging.getLogger(name) 