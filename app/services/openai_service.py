import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
import streamlit as st
from app.utils.logger import get_logger
from app.utils.session import get_messages_for_openai, add_message
from app.utils.config import get_config

logger = get_logger(__name__)

class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key
        """
        logger.info("Initializing OpenAI service")
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        logger.debug("OpenAI API key configured")
    
    def generate_response(self, messages: List[Dict[str, str]], model: str = "gpt-4") -> str:
        """Generate a response using OpenAI API.
        
        Args:
            messages: List of message dictionaries with role and content
            model: OpenAI model to use
            
        Returns:
            Generated response text
        """
        try:
            logger.info(f"Generating response with OpenAI model: {model}")
            logger.debug(f"Using {len(messages)} messages as context")
            
            logger.debug("Sending request to OpenAI API")
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            response_text = response.choices[0].message.content.strip()
            logger.info("Successfully received response from OpenAI")
            logger.debug(f"Response preview: {response_text[:50]}{'...' if len(response_text) > 50 else ''}")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}", exc_info=True)
            raise

def process_user_input(user_input: str, search_service) -> str:
    """Process user input and determine whether to use OpenAI or semantic search.
    
    Args:
        user_input: User's input text
        search_service: Service for semantic search
        
    Returns:
        Assistant's response
    """
    logger.info("Processing user input")
    logger.debug(f"User input: {user_input[:50]}{'...' if len(user_input) > 50 else ''}")
    
    # Add user message to history
    logger.debug("Adding user message to conversation history")
    add_message("user", user_input)
    
    # Determine if the input requires semantic search
    use_search = should_use_semantic_search(user_input)
    logger.info(f"Decision: {'Use semantic search' if use_search else 'Use OpenAI directly'}")
    
    if use_search:
        # Trigger semantic search
        logger.info("Triggering semantic search")
        search_service.perform_search(user_input)
        return "Searching for relevant information..."
    else:
        # Use OpenAI for direct response
        try:
            logger.info("Getting conversation history for OpenAI")
            messages = get_messages_for_openai()
            
            # Get configuration
            logger.info("Getting OpenAI API key from config")
            config = get_config()
            api_key = config["openai"]["api_key"]
            
            logger.info("Initializing OpenAI service")
            openai_service = OpenAIService(api_key)
            
            logger.info(f"Generating response with model: {st.session_state.openai_model}")
            response = openai_service.generate_response(
                messages, 
                model=st.session_state.openai_model
            )
            
            # Add assistant response to history
            logger.info("Adding assistant response to conversation history")
            add_message("assistant", response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing user input: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"

def should_use_semantic_search(user_input: str) -> bool:
    """Determine if the user input should trigger semantic search.
    
    Args:
        user_input: User's input text
        
    Returns:
        True if semantic search should be used, False otherwise
    """
    logger.info("Evaluating if input should use semantic search")
    
    # Simple heuristic: check if the input contains search-related keywords
    search_keywords = [
        "search", "find", "look up", "lookup", "search for", 
        "find information", "get information", "retrieve"
    ]
    
    # Check if any search keyword is in the user input
    should_search = any(keyword in user_input.lower() for keyword in search_keywords)
    
    logger.debug(f"Search decision: {should_search} (based on keywords in input)")
    return should_search 