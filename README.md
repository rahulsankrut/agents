# Anderson Agent - Presentation Chatbot & Cloud Function

A comprehensive solution for creating PowerPoint presentations using AI agents and Google Cloud Functions.

## 🚀 Overview

This project consists of two main components:

1. **Presentation Chatbot** - An AI agent built with Google ADK that helps users create PowerPoint presentations
2. **Cloud Function Deployment** - A serverless function that generates PowerPoint files with images and content

## 📁 Project Structure

```
anderson_agent/
├── cloud_function_deployment/     # Cloud Function for PowerPoint generation
│   ├── main.py                   # Cloud Function entry point
│   ├── deploy.py                  # Deployment script
│   ├── test_cloud_function.py    # Test suite
│   ├── requirements.txt          # Dependencies
│   └── ppt_creator_tool/         # PowerPoint generation logic
│       └── simple_presentation.py
├── presentation_chatbot/          # AI Agent for user interaction
│   ├── agent.py                  # Main agent definition
│   ├── config.py                 # Configuration settings
│   ├── prompts.py                # Agent instructions
│   ├── tools/                    # Agent tools
│   │   └── tools.py              # Presentation generation tools
│   ├── demo.py                   # Local testing script
│   ├── pyproject.toml            # Poetry configuration
│   ├── README.md                 # Agent documentation
│   └── tests/                    # Unit tests
└── venv/                         # Virtual environment
```

## 🛠️ Features

### Presentation Chatbot
- **AI-Powered Interface**: Uses Google ADK with Gemini 2.5 Pro
- **Interactive Conversation**: Collects presentation requirements through natural language
- **Image Support**: Handles GCS URLs for logos and content images
- **Template System**: Supports multiple presentation templates
- **Local & Web Interface**: Works with ADK web interface

### Cloud Function
- **Serverless PowerPoint Generation**: Creates .pptx files using python-pptx
- **Image Processing**: Downloads and processes images from GCS
- **Template Support**: Multiple slide layouts and designs
- **Error Handling**: Robust error handling and logging
- **Scalable**: Auto-scales based on demand

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Cloud SDK
- Poetry (for presentation_chatbot)
- Access to Google Cloud project

### 1. Cloud Function Deployment

```bash
cd cloud_function_deployment
pip install -r requirements.txt
python deploy.py
```

### 2. Presentation Chatbot Setup

```bash
cd presentation_chatbot
poetry install
cp env.example env
# Edit env file with your configuration
python demo.py
```

### 3. Web Interface

```bash
cd presentation_chatbot
adk web
# Open http://127.0.0.1:8000
```

## ⚙️ Configuration

### Environment Variables

Create an `env` file in the `presentation_chatbot` directory:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1
CLOUD_FUNCTION_URL=https://us-central1-your-project.cloudfunctions.net/ppt-generator
```

### Google Cloud Setup

1. Enable required APIs:
   - Cloud Functions API
   - Cloud Storage API
   - Vertex AI API

2. Set up authentication:
   ```bash
   gcloud auth application-default login
   ```

## 📖 Usage

### Creating a Presentation

1. **Start the chatbot**:
   ```bash
   cd presentation_chatbot
   python demo.py
   ```

2. **Provide information**:
   - Presentation title
   - Text content (bullet points)
   - Logo image (GCS URL)
   - Additional images (GCS URLs with titles)
   - EQI inclusion preference

3. **Generate presentation**:
   The agent will create a PowerPoint file with your content.

### Example Conversation

```
User: I want to create a presentation about our quarterly results
Agent: Great! I'll help you create a presentation about quarterly results. 
      Let me start by collecting some information...

User: The title is "Q4 2024 Results"
Agent: Perfect! The title is "Q4 2024 Results". 
      Now, what content would you like in the left box? 
      You can provide bullet points or paragraphs.

User: Revenue increased 15%, Customer satisfaction 95%, New features launched
Agent: Excellent content! I have:
      - Revenue increased 15%
      - Customer satisfaction 95% 
      - New features launched
      
      Would you like to include a logo? If so, please provide a GCS URL.
```

## 🧪 Testing

### Cloud Function Tests

```bash
cd cloud_function_deployment
python test_cloud_function.py
```

### Agent Tests

```bash
cd presentation_chatbot
poetry run pytest tests/
```

## 🔧 Development

### Adding New Features

1. **Cloud Function**: Modify `ppt_creator_tool/simple_presentation.py`
2. **Agent Tools**: Update `presentation_chatbot/tools/tools.py`
3. **Agent Behavior**: Modify `presentation_chatbot/prompts.py`

### Deployment

```bash
# Deploy cloud function
cd cloud_function_deployment
python deploy.py

# Test deployment
python test_cloud_function.py
```

## 📊 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  ADK Agent       │───▶│ Cloud Function  │
│   (Web/Local)   │    │  (Gemini 2.5)    │    │  (PowerPoint)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                           │
                              ▼                           ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  GCS Images      │    │  .pptx File     │
                       │  (Logos/Content)  │    │  (Download)     │
                       └──────────────────┘    └─────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the troubleshooting guides in each component
- Review Google Cloud logs for deployment issues
- Ensure all environment variables are properly set

## 🔗 Links

- [Google ADK Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/develop/adk)
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
