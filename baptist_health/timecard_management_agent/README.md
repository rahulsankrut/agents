# Baptist Health Timecard Management Agent

A sophisticated AI agent built with Google's Agent Development Kit (ADK) to streamline timecard management for healthcare organizations.

## Overview

**Spark_v2** is an intelligent timecard management assistant that helps healthcare managers efficiently review, approve, and manage employee timecards. Built specifically for Baptist Health, it transforms hours of manual review into minutes of intelligent interaction.

## Features

### 🚀 Core Capabilities
- **Quick Summaries**: Get instant overviews of timecard status for any pay period
- **Exception Handling**: Identify and help resolve timecard issues efficiently
- **Bulk Approvals**: Approve standard timecards with a single command
- **Historical Analysis**: Compare periods to identify trends and patterns
- **Reminder Generation**: Draft professional reminder messages for missing submissions

### 🛠️ Tools Available
- `get_summary`: Comprehensive timecard status overview
- `get_exceptions`: Detailed exception analysis and breakdown
- `approve_standard_timecards`: Bulk approval of compliant timecards
- `get_employee_schedule`: Retrieve employee schedules for investigation
- `get_historical_comparison`: Compare pay periods for trend analysis
- `draft_reminder_message`: Generate professional reminder messages

## Demo Scenarios

### Scenario 1: "Happy Path" - Gaining Time Back
**Manager**: "Good morning Spark, let's take a look at the time cards from last week."
**Spark**: Provides summary and offers to approve standard timecards
**Outcome**: 30-second interaction replaces hours of manual review

### Scenario 2: "Exception Handling" - Guided Resolution
**Manager**: "Okay, show me the exceptions."
**Spark**: Provides detailed breakdown and helps investigate issues
**Outcome**: Intelligent problem-solving vs. manual investigation

### Scenario 3: "Historical Lookback" - Simple Analytics
**Manager**: "How does this compare to the first week of August?"
**Spark**: Shows trend analysis and pattern recognition
**Outcome**: Data-driven insights impossible with manual processes

## Setup

### Prerequisites
- Python 3.11+
- Poetry
- Google Cloud Project with Firestore
- Authentication: `gcloud auth application-default login`

### Installation
```bash
cd timecard_management_agent
poetry install
```

### Configuration
1. Copy `.env.example` to `.env`
2. Update with your project settings:
   ```
   PROJECT_ID=your-gcp-project-id
   DATABASE_ID=your-firestore-database-id
   ```

### Running the Agent
```bash
# Using ADK CLI
adk run .

# Using ADK Web UI
adk web
```

## Data Requirements

The agent expects Firestore collections:
- `managers`: Manager information
- `employees`: Employee data with manager relationships
- `timecards`: Timecard entries with status and exceptions
- `schedules`: Employee schedules for investigation

## Demo Data

Use the provided `synthetic_data_generator.py` to create realistic demo data:
```bash
python synthetic_data_generator.py
```

## Reset Between Demos

Reset current week data for fresh demos:
```bash
python reset_demo_data.py
```

## Architecture

```
timecard_management_agent/
├── timecard_management_agent/
│   ├── tools/              # Firestore tools for timecard operations
│   ├── shared_libraries/   # Firestore client utilities
│   ├── agent.py            # Main agent definition
│   ├── config.py           # Configuration settings
│   └── prompts.py          # Agent prompts and instructions
├── deployment/             # Deployment scripts for Agent Engine
├── eval/                   # Evaluation scripts
├── tests/                  # Unit tests
└── pyproject.toml         # Poetry configuration
```

## Deployment

The agent can be deployed to Google Cloud Agent Engine using the deployment scripts in the `../deployment/` directory.

### Quick Deployment

```bash
# Navigate to deployment directory
cd ../deployment

# Test deployment setup
python test_deployment.py

# Deploy the agent (uses current gcloud project)
python deploy.py

# Deploy with custom project and region
python deploy.py --project your-project-id --region us-central1

# Deploy with custom agent name
python deploy.py --agent-name my-timecard-agent --display-name "My Timecard Agent"
```

### Verify Deployment

```bash
# Verify the deployment was successful
python verify_deployment.py --project your-project-id --agent-name baptist-health-timecard-agent
```

### Environment Setup

1. Copy `env.template` to `.env` in the deployment directory
2. Update with your project settings:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_GENAI_USE_VERTEXAI=1
   AGENT_MODEL=gemini-2.5-pro
   AGENT_NAME=Spark_v2
   ```

For detailed deployment instructions, see the [deployment README](../deployment/README.md).

## Contributing

1. Follow the ADK structure and patterns
2. Add tests for new tools
3. Update documentation for new features
4. Ensure proper error handling and logging

## License

Apache License 2.0
