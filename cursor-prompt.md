# Comprehensive Prompt for Building a Streamlit Chatbot

I need you to help me build a complete Streamlit application for a chatbot that will do messaging with openAI. Depending on the user input the application will also do an http call to an AWS api gateway endpoint for semantic search results. The endpoint does not return the actual results, as this is an asynchronous handling with AWS lambda functions. The results will be delivered over a separate AWS API gateway endpoint via Websockets. The AWS lambda functions and API gateways are already build and in place. There must be a clear separation in logic in handling the openAI LLM calls and the semantic search. The application should follow modern Python practices and be deployable to AWS App Runner via Docker.

## Application Requirements

1. The chatbot should be built with Streamlit using the latest version.
2. Must include openAI messaging.
2. Must include WebSocket connectivity to AWS API Gateway for asynchronous communication with my Lambda function
3. Should handle both direct LLM responses and semantic search results from Lambda
4. Maintain conversation history and context
5. Include proper error handling and loading states
6. Follow a clean, maintainable project structure
7. Include comprehensive testing
8. Be containerized for AWS App Runner deployment
9. Include CI/CD with GitHub Actions

## Project Structure

Please set up a project with the following structure:
- Use pip for dependency management
- Include proper typing with mypy integration
- Implement pytest with fixtures for testing
- Organize code with clear separation of concerns (UI, business logic, API clients)
- Include comprehensive documentation
- Implement logging with proper levels

## Critical Components

1. WebSocket client implementation for real-time communication with AWS
2. Session state management for maintaining conversation context
3. UI components for chat interface
4. Service layer for determining when to use the semantic search.
5. Error handling and retry mechanisms
6. Configuration management using environment variables
7. Dockerfile optimized for Streamlit and deployable in AWS ECR for AWS App runner

## Testing Requirements

1. Unit tests for all core functions
2. Integration tests with mocked AWS services
3. UI testing with Streamlit's testing utilities
4. Test coverage reports

## CI/CD and Deployment

1. GitHub Actions workflow for:
   - Running tests
   - Building Docker image
   - Deploying to AWS App Runner
2. Environment-specific configurations (dev, staging, prod)
3. Secrets management for API keys and AWS credentials

Please generate the foundation for this project with the latest Python libraries, focusing on clean architecture and maintainability. Ensure the WebSocket implementation is robust and can handle the asynchronous nature of the Lambda function.
