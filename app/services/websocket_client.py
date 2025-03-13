import json
import logging
import threading
import time
from typing import Callable, Optional, Dict, Any
import websocket
import streamlit as st
from app.utils.logger import get_logger

logger = get_logger(__name__)

class WebSocketClient:
    """WebSocket client for communicating with AWS API Gateway."""
    
    def __init__(self, websocket_url: str, on_message: Callable, on_error: Callable):
        """Initialize WebSocket client.
        
        Args:
            websocket_url: WebSocket endpoint URL
            on_message: Callback function for handling messages
            on_error: Callback function for handling errors
        """
        logger.info("Initializing WebSocket client")
        logger.debug(f"WebSocket URL: {websocket_url}")
        self.websocket_url = websocket_url
        self.on_message = on_message
        self.on_error = on_error
        self.ws = None
        self.thread = None
        self.is_connected = False
        
    def connect(self):
        """Establish WebSocket connection."""
        logger.info("Attempting to establish WebSocket connection")
        try:
            # Create WebSocket connection
            logger.debug(f"Creating WebSocketApp for URL: {self.websocket_url}")
            self.ws = websocket.WebSocketApp(
                self.websocket_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )
            
            # Start WebSocket connection in a separate thread
            logger.debug("Starting WebSocket connection in a separate thread")
            self.thread = threading.Thread(target=self.ws.run_forever)
            self.thread.daemon = True
            self.thread.start()
            
            logger.info("WebSocket connection thread started")
            
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {str(e)}", exc_info=True)
            self.on_error(e)
    
    def disconnect(self):
        """Close WebSocket connection."""
        logger.info("Disconnecting WebSocket")
        if self.ws:
            logger.debug("Closing WebSocket connection")
            self.ws.close()
            self.is_connected = False
            logger.info("WebSocket connection closed")
        else:
            logger.warning("Attempted to disconnect, but no WebSocket connection exists")
    
    def _on_message(self, ws, message):
        """Handle incoming WebSocket messages."""
        logger.info("Received WebSocket message")
        try:
            logger.debug(f"Raw message: {message[:100]}{'...' if len(message) > 100 else ''}")
            data = json.loads(message)
            logger.debug(f"Parsed message: {json.dumps(data)[:100]}...")
            
            # Call the provided message handler
            logger.info("Calling message handler")
            self.on_message(data)
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse WebSocket message: {message}", exc_info=True)
            self.on_error("Invalid message format")
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {str(e)}", exc_info=True)
            self.on_error(str(e))
    
    def _on_error(self, ws, error):
        """Handle WebSocket errors."""
        logger.error(f"WebSocket error: {str(error)}", exc_info=True)
        self.is_connected = False
        self.on_error(error)
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close."""
        logger.info(f"WebSocket connection closed: {close_status_code} - {close_msg}")
        self.is_connected = False
    
    def _on_open(self, ws):
        """Handle WebSocket connection open."""
        logger.info("WebSocket connection established successfully")
        self.is_connected = True
        st.session_state.websocket_connected = True

def handle_websocket_message(data: Dict[str, Any]):
    """Handle incoming WebSocket messages in the Streamlit app.
    
    Args:
        data: The message data received from WebSocket
    """
    logger.info("Processing WebSocket message in Streamlit app")
    try:
        if "search_results" in data:
            logger.info(f"Received search results: {len(data['search_results'])} items")
            
            # Store search results in session state
            st.session_state.search_results = data["search_results"]
            logger.debug(f"Stored {len(data['search_results'])} search results in session state")
            
            # Add assistant message with search results
            if data["search_results"]:
                logger.info("Formatting search results for display")
                result_text = "Here are the search results:\n\n"
                for idx, result in enumerate(data["search_results"], 1):
                    result_text += f"{idx}. {result['title']}: {result['snippet']}\n"
                
                from app.utils.session import add_message
                logger.debug("Adding assistant message with search results")
                add_message("assistant", result_text)
            else:
                logger.info("No search results found")
                from app.utils.session import add_message
                add_message("assistant", "No search results found.")
                
            # Force Streamlit to update the UI
            logger.debug("Triggering Streamlit rerun to update UI")
            st.rerun()
            
        else:
            logger.warning(f"Received WebSocket message without search_results: {data.keys()}")
            
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {str(e)}", exc_info=True)

def handle_websocket_error(error):
    """Handle WebSocket errors in the Streamlit app.
    
    Args:
        error: The error that occurred
    """
    logger.error(f"WebSocket error in Streamlit app: {str(error)}", exc_info=True)
    st.session_state.websocket_connected = False
    st.error(f"WebSocket error: {str(error)}") 