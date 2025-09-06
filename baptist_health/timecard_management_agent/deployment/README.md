# Timecard Management Agent Deployment

This directory contains deployment scripts for the Baptist Health Timecard Management Agent to Google Cloud Agent Engine.

## Prerequisites

1. **Google Cloud Project**: Ensure you have a GCP project with Agent Engine API enabled
2. **Authentication**: Run `gcloud auth application-default login`
3. **Permissions**: Ensure your account has the necessary permissions for Agent Engine
4. **Python Environment**: Use the virtual environment in `../venv/`

## Environment Setup

1. Copy `env.template` to `.env`:
   ```bash
   cp env.template .env
   ```

2. Update `.env` with your project settings:
   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_CLOUD_STORAGE_BUCKET=your-project-id-adk-timecard-staging
   GOOGLE_GENAI_USE_VERTEXAI=1
   AGENT_MODEL=gemini-2.5-pro
   AGENT_NAME=Spark_v2
   ```

## Deployment Commands

### Quick Deployment
```bash
# Activate the virtual environment
source ../venv/bin/activate

# Deploy the agent
python deploy.py --create
```

### Advanced Deployment Options
```bash
# Deploy with custom project and location
python deploy.py --create --project_id your-project-id --location us-central1

# List all deployed agents
python deploy.py --list

# Delete an agent
python deploy.py --delete --resource_id projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ID
```

### Test Deployment
```bash
# Test the deployment setup
python test_deployment.py
```

## Deployment Process

1. **Build Package**: The deployment script builds a wheel package from the agent code
2. **Upload to Cloud Storage**: The package is uploaded to the staging bucket
3. **Create Agent Engine**: The agent is deployed to Agent Engine with all dependencies
4. **Test Connection**: A test session is created to verify the deployment

## Verification

After deployment, you can verify the agent is working:

```bash
# Test the deployed agent
python verify_deployment.py --project your-project-id --agent-name Spark_v2
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure you're authenticated with `gcloud auth application-default login`
2. **Permission Errors**: Check that your account has Agent Engine permissions
3. **Package Build Errors**: Ensure all dependencies are installed in the virtual environment
4. **Storage Bucket Errors**: Create the staging bucket if it doesn't exist

### Logs

Check the deployment logs for detailed error information. The deployment script uses DEBUG level logging.

## Cleanup

To clean up resources:

```bash
# Delete the deployed agent
python deploy.py --delete --resource_id projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ID

# Delete the staging bucket (optional)
gsutil rm -r gs://your-project-id-adk-timecard-staging
```

## Architecture

The deployment creates:
- **Agent Engine**: The main reasoning engine hosting the agent
- **Cloud Storage Bucket**: Staging bucket for deployment artifacts
- **IAM Permissions**: Necessary permissions for the agent to access Firestore

## Security

- All sensitive data is stored in environment variables
- The agent uses service account authentication
- Firestore access is controlled through IAM permissions
