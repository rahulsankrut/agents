# Presentation Chatbot

A conversational AI agent that helps users create PowerPoint presentations using the Agent Development Kit (ADK) and Gemini 2.5 Pro models.

## Features

- 🤖 Conversational interface for collecting presentation information
- 📊 Integrates with the PowerPoint generation cloud function
- 🖼️ Supports logo and image uploads via GCS URLs
- 📝 Collects text content for presentation slides
- ⚙️ Configurable options (EQI inclusion, etc.)
- 🎯 Simple and user-friendly interaction

## Architecture

The chatbot uses:
- **Google ADK**: Agent Development Kit for building conversational AI
- **Gemini 2.5 Pro**: Advanced language model for natural conversations
- **Cloud Function Integration**: Connects to the PowerPoint generation service
- **GCS Support**: Handles image uploads via Google Cloud Storage

## Setup

### Prerequisites

- Python 3.11+
- Google Cloud Project with Vertex AI enabled
- Access to Gemini 2.5 Pro models
- PowerPoint generation cloud function deployed

### Installation

1. Install dependencies:
```bash
pip install poetry
poetry install
```

2. Set up environment variables:
```bash
# Create .env file
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1
```

3. Run the demo:
```bash
python demo.py
```

## Usage

The chatbot will guide you through creating a presentation by asking for:

1. **Presentation Title** (required)
2. **Logo** (optional) - GCS URL
3. **Text Content** - Bullet points for the left box
4. **Images** (optional) - GCS URLs with titles
5. **EQI Inclusion** - Whether to include Execution Quality Index

Example conversation:
```
🤖 Bot: Hello! I'd like to help you create a PowerPoint presentation. 
      Let's start with the title. What would you like to call your presentation?

👤 You: Weekly Project Update

🤖 Bot: Great! "Weekly Project Update" is a good title. 
      Do you have a logo you'd like to include in the presentation? 
      If yes, please provide the GCS URL. If not, just say "no".

👤 You: No, I don't have a logo

🤖 Bot: No problem! Now let's add some content to the left box. 
      What are the key points you'd like to include? 
      You can provide them as bullet points.
```

## Project Structure

```
presentation_chatbot/
├── presentation_chatbot/
│   ├── __init__.py
│   ├── agent.py              # Main agent configuration
│   ├── config.py             # Configuration settings
│   ├── prompts.py            # Agent prompts and instructions
│   ├── entities/             # Data models
│   ├── shared_libraries/     # Shared utilities
│   └── tools/
│       ├── __init__.py
│       └── tools.py          # Tool definitions
├── demo.py                   # Interactive demo script
├── pyproject.toml           # Dependencies and project config
└── README.md               # This file
```

## Tools

### generate_presentation
Generates a PowerPoint presentation using the cloud function.

**Parameters:**
- `title`: Presentation title (required)
- `logo_gcs_url`: GCS URL for logo (optional)
- `text_content`: List of text content
- `image_data`: List of image data with GCS URLs
- `include_eqi`: Whether to include EQI (default: True)

### get_presentation_templates
Retrieves available presentation templates from the cloud function.

## Configuration

The agent is configured to use:
- **Model**: `gemini-2.5-pro`
- **Project**: `agent-space-465923`
- **Location**: `us-central1`
- **Cloud Function**: PowerPoint generation service

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run pyink .
```

### Linting
```bash
poetry run pylint presentation_chatbot/
```

## Deployment

### Agent Engine Deployment

The presentation chatbot can be deployed to Google Cloud Vertex AI Agent Engine for production use.

#### Quick Deploy

1. **Set up environment**:
   ```bash
   cd deployment
   cp env.template .env
   # Edit .env with your GCP project details
   ```

2. **Install deployment dependencies**:
   ```bash
   poetry install --with deployment
   ```

3. **Deploy to Agent Engine**:
   ```bash
   python deployment/deploy.py --create
   ```

4. **Test the deployed agent**:
   ```bash
   python deployment/test_deployment.py \
     --resource_id=YOUR_RESOURCE_ID \
     --user_id=test_user
   ```

For detailed deployment instructions, see [deployment/README.md](deployment/README.md).

## License

Apache License 2.0
