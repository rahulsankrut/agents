# Presentation Chatbot - Agent Engine Deployment

This directory contains the deployment scripts and configuration for deploying the Presentation Chatbot to Google Cloud Vertex AI Agent Engine.

## Prerequisites

1. **Google Cloud Project Setup**:
   - Ensure you have a GCP project with billing enabled
   - Enable the Vertex AI API: `gcloud services enable aiplatform.googleapis.com`
   - Enable the Agent Engine API: `gcloud services enable aiplatformagent.googleapis.com`

2. **Required Permissions**:
   - Vertex AI Agent Engine Admin (`roles/aiplatform.agentEngineAdmin`)
   - Storage Object Admin (`roles/storage.objectAdmin`)
   - Secret Manager Secret Accessor (`roles/secretmanager.secretAccessor`) - if using secrets

3. **Google Cloud Storage Bucket**:
   - Create a GCS bucket for staging deployment artifacts
   - Example: `gsutil mb gs://your-project-agent-engine-bucket`

## Environment Setup

1. **Copy Environment Template**:
   ```bash
   cp env.template .env
   ```

2. **Configure Environment Variables**:
   Edit `.env` and set the following values:
   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
   ```

3. **Install Deployment Dependencies**:
   ```bash
   cd anderson_agent/presentation_chatbot
   poetry install --with deployment
   ```

## Deployment Commands

### Deploy the Agent

```bash
cd anderson_agent/presentation_chatbot
python deployment/deploy.py --create
```

This will:
- Create an AdkApp wrapper around your root_agent
- Deploy to Agent Engine with all required dependencies
- Print the Agent Engine resource ID for future use

### List Deployed Agents

```bash
python deployment/deploy.py --list
```

### Delete a Deployed Agent

```bash
python deployment/deploy.py --delete --resource_id=YOUR_RESOURCE_ID
```

## Testing the Deployed Agent

1. **Get the Resource ID** from the deployment output or list command

2. **Test the Agent**:
   ```bash
   python deployment/test_deployment.py \
     --resource_id=YOUR_RESOURCE_ID \
     --user_id=test_user
   ```

3. **Interactive Testing**:
   - The test script will start an interactive session
   - Type your messages and see the agent's responses
   - Type 'quit' to exit

## Deployment Configuration

The deployment script includes the following configurations:

- **Resource Limits**: 0-10 instances (auto-scaling)
- **Container Concurrency**: 80 concurrent requests
- **Tracing**: Enabled for monitoring and debugging
- **Dependencies**: All required packages with version constraints

## Advanced Configuration

### Custom Resource Limits

You can modify the deployment script to set custom resource limits:

```python
remote_agent = agent_engines.create(
    adk_app,
    # ... other parameters
    min_instances=1,  # Always keep 1 instance running
    max_instances=20,  # Scale up to 20 instances
    resource_limits={
        "cpu": "2",
        "memory": "4Gi"
    }
)
```

### Environment Variables

You can pass environment variables to the deployed agent:

```python
remote_agent = agent_engines.create(
    adk_app,
    # ... other parameters
    env_vars={
        "CUSTOM_VAR": "value",
        "API_KEY": "your-api-key"
    }
)
```

### Private Service Connect (Optional)

For VPC connectivity, you can configure Private Service Connect:

```python
remote_agent = agent_engines.create(
    adk_app,
    # ... other parameters
    psc_interface_config={
        "network_attachment": "NETWORK_ATTACHMENT_NAME",
    }
)
```

## Troubleshooting

### Common Issues

1. **Missing Permissions**: Ensure you have the required IAM roles
2. **Invalid Project ID**: Verify your GCP project ID is correct
3. **Bucket Not Found**: Create the GCS bucket before deployment
4. **API Not Enabled**: Enable the required APIs in your project

### Debugging

- Check the deployment logs in Cloud Console
- Use tracing to monitor agent execution
- Review the Agent Engine logs for errors

## Monitoring and Management

- **Cloud Console**: Monitor your deployed agents in the Vertex AI console
- **Logs**: View logs in Cloud Logging
- **Tracing**: Use the tracing feature to debug agent execution
- **Metrics**: Monitor performance and usage metrics

## Cleanup

To avoid charges, delete your deployed agent when not in use:

```bash
python deployment/deploy.py --delete --resource_id=YOUR_RESOURCE_ID
```
