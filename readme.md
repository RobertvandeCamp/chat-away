# Streamlit Chatbot with OpenAI and AWS Integration

A powerful chatbot application built with Streamlit that integrates OpenAI's language models and AWS semantic search capabilities. The application provides a clean, intuitive interface for users to interact with AI, with support for both direct LLM responses and semantic search results delivered asynchronously via WebSockets.

![Streamlit Chatbot](https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png)

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [Local Development](#local-development)
  - [Using Docker](#using-docker)
- [Application Flow](#application-flow)
- [Project Structure](#project-structure)
- [Development Guidelines](#development-guidelines)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **OpenAI Integration**: Leverages OpenAI's powerful language models for natural conversation
- **Semantic Search**: Connects to AWS API Gateway for semantic search capabilities
- **Real-time Updates**: WebSocket integration for asynchronous communication with AWS Lambda
- **Conversation History**: Maintains context throughout the conversation
- **Configurable Models**: Select different OpenAI models through the UI
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Docker Support**: Containerized for easy deployment and scaling
- **Clean Architecture**: Separation of concerns for maintainability

## Architecture

The application follows a clean architecture with distinct layers:

- **UI Layer**: Streamlit components for user interaction
- **Service Layer**: Business logic for OpenAI and semantic search
- **API Layer**: Clients for OpenAI API and AWS services
- **Utility Layer**: Configuration, logging, and session management

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker and Docker Compose (for containerized deployment)
- OpenAI API key
- AWS API Gateway endpoints (for semantic search and WebSocket)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/streamlit-chatbot.git
cd streamlit-chatbot
```

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your API keys and endpoints:

```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# AWS Configuration
AWS_API_ENDPOINT=https://your-api-gateway-endpoint.amazonaws.com/stage/search
AWS_WEBSOCKET_URL=wss://your-websocket-endpoint.amazonaws.com/stage
AWS_API_KEY=your_aws_api_key_here

# Application Configuration
DEBUG=false
```

## Running the Application

### Local Development

To run the application locally:

```bash
# Make sure your virtual environment is activated
# Set the Python path to include the current directory
PYTHONPATH=. streamlit run app/main.py
```

For Windows:

```bash
# PowerShell
$env:PYTHONPATH="."
streamlit run app/main.py

# Command Prompt
set PYTHONPATH=.
streamlit run app/main.py
```

The application will be available at http://localhost:8501

### Using Docker

1. Build and start the containers:

```bash
docker-compose up
```

2. For background mode:

```bash
docker-compose up -d
```

3. To stop the application:

```bash
docker-compose down
```

The application will be available at http://localhost:8501

## Application Flow

1. **Initialization**:
   - The application loads configuration from environment variables and Streamlit secrets
   - Session state is initialized to store conversation history and settings
   - UI components (sidebar and chat interface) are rendered

2. **User Interaction**:
   - User enters a message in the chat input
   - The message is processed to determine whether to use OpenAI or semantic search
   - The message is added to the conversation history

3. **OpenAI Flow** (for direct responses):
   - The OpenAI service generates a response using the conversation history
   - The response is added to the message history and displayed in the UI

4. **Semantic Search Flow** (for information retrieval):
   - The search service sends a request to the AWS API Gateway
   - A loading message is displayed while waiting for results
   - The WebSocket client listens for search results from AWS
   - When results are received, they're added to the conversation history and displayed

5. **WebSocket Communication**:
   - The WebSocket connection can be manually established/disconnected via the sidebar
   - Incoming messages are processed and displayed in the chat interface
   - Error handling ensures robustness in case of connection issues

## Project Structure

```
streamlit-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main Streamlit application entry point
│   ├── components/             # UI components
│   │   ├── __init__.py
│   │   ├── chat_interface.py   # Chat UI components
│   │   └── sidebar.py          # Sidebar configuration
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── openai_service.py   # OpenAI integration
│   │   ├── search_service.py   # Semantic search integration
│   │   └── websocket_client.py # WebSocket client for AWS
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   ├── logger.py           # Logging setup
│   │   └── session.py          # Session state management
│   └── api/                    # API clients
│       ├── __init__.py
│       ├── openai_client.py    # OpenAI API client
│       └── aws_client.py       # AWS API Gateway client
├── tests/                      # Test directory
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # This file
```

## Development Guidelines

### Adding New Features

1. **Follow the existing architecture**: Keep UI, business logic, and API clients separate
2. **Add comprehensive logging**: Use the logger utility for all new code
3. **Update configuration**: Add new configuration options to both `.env.example` and `config.py`
4. **Write tests**: Add tests for new functionality in the `tests` directory

### Code Style

- Follow PEP 8 guidelines for Python code
- Use type hints for function parameters and return values
- Add docstrings to all functions and classes
- Keep functions small and focused on a single responsibility

### Debugging

- Set `DEBUG=true` in your `.env` file for detailed logging
- Check the console output for log messages
- Use the Streamlit UI for interactive debugging

## Troubleshooting

### Common Issues

1. **Module not found errors**:
   - Ensure you're running with `PYTHONPATH=.`
   - Check that your virtual environment is activated

2. **OpenAI API errors**:
   - Verify your API key is correct in the `.env` file
   - Check for rate limiting or quota issues
   - Make sure you're using the correct OpenAI client version (v1.0.0+)
   - If you see errors about `openai.ChatCompletion`, update your code to use the new client-based approach

3. **WebSocket connection issues**:
   - Ensure your AWS WebSocket URL is correct
   - Check network connectivity and firewall settings

4. **Docker issues**:
   - Ensure Docker and Docker Compose are installed and running
   - Check that ports are not already in use

5. **Streamlit errors**:
   - If you see errors about `st.experimental_rerun()`, update to use `st.rerun()` instead
   - Make sure you're using a recent version of Streamlit

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing framework
- [OpenAI](https://openai.com/) for the powerful language models
- [AWS](https://aws.amazon.com/) for the cloud infrastructure

---

*This README was generated for the Streamlit Chatbot application.*
