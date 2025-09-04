adk w# Deployment Guide: Baptist Health Timecard Management Agent

This guide explains how to deploy the timecard management agent to Google Cloud Agent Engine.

## Prerequisites

1. **Google Cloud CLI**: Install and authenticate with gcloud
   ```bash
   # Install gcloud CLI (if not already installed)
   # Follow: https://cloud.google.com/sdk/docs/install
   
   # Authenticate
   gcloud auth login
   gcloud config set project agent-space-465923
   ```

2. **Required APIs**: The deployment script will enable these automatically:
   - `aiplatform.googleapis.com` - Vertex AI
   - `agentengine.googleapis.com` - Agent Engine
   - `firestore.googleapis.com` - Firestore

3. **Permissions**: Ensure your account has the following roles:
   - `roles/aiplatform.admin`
   - `roles/firestore.admin`
   - `roles/serviceusage.serviceUsageAdmin`

## Deployment

### Option 1: Automated Deployment (Recommended)

```bash
cd timecard_management_agent/deployment
python deploy.py
```

This script will:
- ✅ Check prerequisites
- ✅ Enable required APIs
- ✅ Deploy the agent to Agent Engine
- ✅ Verify deployment status

### Option 2: Manual Deployment

```bash
# Enable required APIs
gcloud services enable aiplatform.googleapis.com --project=agent-space-465923
gcloud services enable agentengine.googleapis.com --project=agent-space-465923
gcloud services enable firestore.googleapis.com --project=agent-space-465923

# Deploy the agent
gcloud ai agents deploy timecard_management_agent \
    --project=agent-space-465923 \
    --location=us-central1 \
    --display-name="Baptist Health Timecard Management Agent" \
    --description="AI agent for Baptist Health timecard management. Helps managers efficiently review, approve, and manage employee timecards." \
    --agent-uri=./timecard_management_agent \
    --async
```

## Agent Configuration

The deployed agent will have:
- **Agent ID**: `timecard_management_agent`
- **Display Name**: "Baptist Health Timecard Management Agent"
- **Project**: `agent-space-465923`
- **Location**: `us-central1`
- **Model**: Gemini 2.5 Pro
- **Tools**: 6 core timecard management tools

## Verification

Check deployment status:
```bash
gcloud ai agents describe timecard_management_agent \
    --project=agent-space-465923 \
    --location=us-central1
```

## Accessing the Agent

Once deployed, you can access the agent through:
1. **Google Cloud Console**: Vertex AI > Agent Engine
2. **Agent Engine API**: Direct API calls
3. **Custom UI**: Integrate into your applications

## Demo Setup

Before running demos:
1. **Generate Data**: Run `python synthetic_data_generator.py`
2. **Reset Between Demos**: Run `python reset_demo_data.py`
3. **Test Agent**: Use the demo scenarios in the README

## Troubleshooting

### Common Issues:

1. **Authentication Error**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Permission Denied**:
   - Ensure you have the required IAM roles
   - Contact your Google Cloud admin

3. **API Not Enabled**:
   - The deployment script should handle this automatically
   - Manual: `gcloud services enable [api-name]`

4. **Agent Not Found**:
   - Check the agent name: `timecard_management_agent`
   - Verify project and location settings

### Logs and Monitoring:

```bash
# View agent logs
gcloud ai agents logs timecard_management_agent \
    --project=agent-space-465923 \
    --location=us-central1

# Monitor agent status
gcloud ai agents list --project=agent-space-465923 --location=us-central1
```

## Support

For issues with:
- **Deployment**: Check the troubleshooting section above
- **Agent Functionality**: Review the main README.md
- **Google Cloud**: Contact Google Cloud Support
