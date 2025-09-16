# UPS Developer Assistant

A multi-agent application built with Google's Agent Development Kit (ADK) to help developers with UPS-related questions and tasks.

## Overview

This application consists of:
- **Root Agent**: Main UPS Developer Assistant that coordinates between sub-agents
- **Legacy API Documentation Agent**: Specialized agent for retrieving and answering questions from UPS legacy API documentation and resources
- **Code Generation Agent**: Specialized agent for generating code examples, SDK implementations, and integration samples based on UPS API documentation
- **Search Agent**: Specialized agent for finding current UPS information, news, updates, and real-time data using Google Search

## Features

- Intelligent routing of developer questions to appropriate sub-agents
- RAG-powered documentation search and retrieval
- Code generation based on UPS API documentation
- Google Search integration for current information and real-time data
- Professional developer-focused responses
- Integration with UPS APIs and development resources

## Architecture

```
Root Agent (UPS Developer Assistant)
├── Legacy API Documentation Agent (Legacy Documentation & Knowledge Retrieval)
├── Code Generation Agent (Code Examples & SDK Implementation)
└── Search Agent Tool (Current Information & Real-time Data)
```

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your RAG_CORPUS configuration
```

3. Run the application:
```bash
poetry run python -m ups_developer_assistant
```

## Configuration

The Legacy API Documentation agent requires a Vertex AI RAG corpus to be configured. Set the `RAG_CORPUS` environment variable with your corpus ID.

## Development

Run tests:
```bash
poetry run pytest
```

Format code:
```bash
poetry run black .
```

## Deployment

Deploy using the deployment script:
```bash
poetry run python deployment/deploy.py
```
