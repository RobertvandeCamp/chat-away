import json
import logging
import requests
from typing import Dict, Any, Optional
import streamlit as st
from app.utils.logger import get_logger

logger = get_logger(__name__)

class SearchService:
    """Service for performing semantic search via AWS API Gateway."""
    
    def __init__(self, api_endpoint: str, api_key: Optional[str] = None):
        """Initialize search service.
        
        Args:
            api_endpoint: AWS API Gateway endpoint for semantic search
            api_key: Optional API key for authentication
        """
        logger.info("Initializing Search Service")
        logger.debug(f"API Endpoint: {api_endpoint}")
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.headers = {}
        
        if api_key:
            logger.debug("API key provided, adding to headers")
            self.headers["x-api-key"] = api_key
        else:
            logger.debug("No API key provided")
    
    def perform_search(self, query: str) -> bool:
        """Perform semantic search by sending request to AWS API Gateway.
        
        Args:
            query: Search query
            
        Returns:
            True if request was successful, False otherwise
        """
        try:
            logger.info(f"Performing semantic search")
            logger.debug(f"Search query: {query}")
            
            # Prepare request payload
            conversation_id = st.session_state.conversation_id or "new_conversation"
            logger.debug(f"Using conversation ID: {conversation_id}")
            
            payload = {
                "query": query,
                "conversation_id": conversation_id
            }
            
            # Send request to API Gateway
            logger.info(f"Sending POST request to {self.api_endpoint}")
            logger.debug(f"Request payload: {json.dumps(payload)}")
            logger.debug(f"Request headers: {json.dumps({k: '***' if k.lower() == 'x-api-key' else v for k, v in self.headers.items()})}")
            
            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                json=payload
            )
            
            # Check response status
            logger.info(f"Received response with status code: {response.status_code}")
            
            if response.status_code == 202:  # Accepted
                logger.info("Search request accepted for processing")
                
                # If this is a new conversation, get the conversation ID from response
                if not st.session_state.conversation_id:
                    try:
                        logger.debug("Attempting to extract conversation ID from response")
                        response_data = response.json()
                        logger.debug(f"Response data: {json.dumps(response_data)}")
                        
                        new_conversation_id = response_data.get("conversation_id")
                        if new_conversation_id:
                            logger.info(f"Extracted new conversation ID: {new_conversation_id}")
                            st.session_state.conversation_id = new_conversation_id
                        else:
                            logger.warning("Response did not contain conversation_id")
                    except Exception as e:
                        logger.warning(f"Could not extract conversation ID from response: {str(e)}")
                
                return True
            else:
                logger.error(f"Search request failed: {response.status_code}")
                logger.debug(f"Response content: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error performing semantic search: {str(e)}", exc_info=True)
            return False 