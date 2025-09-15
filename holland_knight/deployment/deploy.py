#!/usr/bin/env python3
"""Deployment script for Holland Knight Legal Multi-Agent System"""

import os
import subprocess
import sys


def deploy():
    """Deploy Holland Knight agent to Google Cloud Agent Engine"""
    
    # Get configuration from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Create a staging bucket name (you may need to create this bucket first)
    staging_bucket = f"gs://{project_id}-holland-knight-staging"
    
    print(f"🚀 Deploying Holland Knight Legal Multi-Agent System...")
    print(f"Project: {project_id}")
    print(f"Region: {location}")
    print(f"Staging Bucket: {staging_bucket}")
    
    # Build the ADK deploy command with environment file
    cmd = [
        "adk", "deploy", "agent_engine",
        "--project", project_id,
        "--region", location,
        "--staging_bucket", staging_bucket,
        "--display_name", "Holland Knight Legal Multi-Agent System",
        "--description", "Multi-agent legal system for Q&A and document generation",
        "--env_file", ".env",  # Include environment variables
        "holland_knight"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Run the deployment command with more verbose output
        result = subprocess.run(cmd, check=True, text=True)
        print("✅ Deployment successful!")
        print("Check the output above for the Agent Engine resource ID")
        print("\nTo find your agent:")
        print("1. Go to: https://console.cloud.google.com/")
        print(f"2. Select project: {project_id}")
        print("3. Navigate to: Vertex AI → Agent Engine")
        print("4. Look for: 'Holland Knight Legal Multi-Agent System'")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Deployment failed!")
        print(f"Error: {e.stderr}")
        return False


if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
