"""Simple test deployment script."""

import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import vertexai
from dotenv import load_dotenv
from test_agent import test_agent
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

def deploy_test_agent():
    """Deploy a simple test agent."""
    load_dotenv()
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "agent-space-465923-agent-staging")
    
    print(f"PROJECT: {project_id}")
    print(f"LOCATION: {location}")
    print(f"BUCKET: {bucket}")
    
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket}",
    )
    
    adk_app = AdkApp(agent=test_agent, enable_tracing=False)
    
    print("Deploying test agent...")
    remote_agent = agent_engines.create(
        adk_app,
        display_name=test_agent.name,
        description="Simple test agent for deployment verification",
        requirements=[
            "google-adk (>=1.0.0)",
            "google-cloud-aiplatform[agent_engines] (>=1.91.0,<2.0.0)",
            "google-genai (>=1.5.0,<2.0.0)",
        ],
    )
    
    print(f"Created test agent: {remote_agent.resource_name}")
    print(f"Agent Engine ID: {remote_agent.resource_name.split('/')[-1]}")

if __name__ == "__main__":
    deploy_test_agent()
