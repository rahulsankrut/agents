# Agentic Weekly Project Update PowerPoint Generator

An intelligent AI-powered application that automates the creation of weekly project update PowerPoint presentations for consulting businesses.

## Project Overview

This application acts as an intelligent "Project Manager's Assistant" that:
- Analyzes project images using Google's Gemini 2.5 Pro model
- Generates professional descriptions and content
- Creates polished PowerPoint presentations automatically
- Streamlines the weekly reporting process

## Core Features

- **Image Analysis**: AI-powered analysis of construction/project images
- **Content Generation**: Professional text descriptions and slide titles
- **Presentation Assembly**: Automated PowerPoint creation with proper formatting
- **Cloud Integration**: Google Cloud Functions, Storage, and Vertex AI
- **Modern UI**: React-based web interface with Firebase hosting

## Architecture

- **Frontend**: React.js with Firebase Hosting
- **Backend**: Google Cloud Functions (Python)
- **AI Engine**: Google Vertex AI with Gemini 2.5 Pro
- **Storage**: Google Cloud Storage for images and presentations
- **Presentation**: python-pptx for PowerPoint generation

## Quick Start

1. Set up Google Cloud Project and enable required APIs
2. Configure environment variables
3. Deploy Cloud Functions
4. Deploy React frontend to Firebase
5. Start generating presentations!

## Project Structure

```
weekly-project-update-generator/
├── frontend/                 # React web application
├── functions/                # Google Cloud Functions
├── shared/                   # Shared utilities and types
├── deployment/               # Deployment scripts
└── docs/                     # Documentation
```

## License

MIT License
