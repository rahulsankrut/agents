# Holland Knight Legal Multi-Agent System

A simple multi-agent system for legal services, built using Google's Agent Development Kit (ADK). This system provides two main agents:

1. **Legal Q&A Agent** - Answers legal questions using Court Listener data
2. **Document Generation Agent** - Creates basic legal documents

## Architecture

This system follows the multi-agent pattern similar to the travel concierge example, with:
- A root agent that coordinates between sub-agents
- Specialized sub-agents for different legal tasks
- Integration with Court Listener API for legal data
- Google Cloud services for deployment and storage

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables in `.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
COURT_LISTENER_API_KEY=your-api-key
```

3. Run the agent:
```bash
adk run holland_knight
```

## Usage

The system can handle queries like:
- "What are the requirements for filing a patent?"
- "Generate a basic non-disclosure agreement"
- "Find recent cases related to intellectual property"

## Deployment

Deploy to Google Cloud using:
```bash
python deployment/deploy.py
```
