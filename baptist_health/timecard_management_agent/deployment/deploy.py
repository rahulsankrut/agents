#!/usr/bin/env python3
"""
Deployment script for Baptist Health Timecard Management Agent
Deploys to Google Cloud Agent Engine
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def deploy_agent():
    """Deploy the agent to Agent Engine."""
    print("🚀 Deploying Baptist Health Timecard Management Agent")
    print("=" * 60)
    
    try:
        # Import required modules
        import vertexai
        from vertexai import agent_engines
        
        # Initialize Vertex AI
        project = os.getenv("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        vertexai.init(
            project=project,
            location=location
        )
        
        print(f"✅ Initialized Vertex AI with project: {project}")
        
        # Create agent engine
        agent_engine = agent_engines.AgentEngine.create(
            display_name="Spark_v2",
            description="Baptist Health Timecard Management Agent using ADK"
        )
        
        print(f"✅ Agent Engine created with ID: {agent_engine.name}")
        print(f"✅ Agent Engine name: {agent_engine.display_name}")
        
        return agent_engine
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def list_agents():
    """List deployed agents."""
    print("📋 Listing deployed agents...")
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        # Initialize Vertex AI
        project = os.getenv("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        vertexai.init(
            project=project,
            location=location
        )
        
        # List agent engines
        agent_engines_list = agent_engines.AgentEngine.list()
        
        if not agent_engines_list:
            print("No deployed agents found.")
            return
        
        print(f"Found {len(agent_engines_list)} deployed agents:")
        for agent in agent_engines_list:
            print(f"  - Name: {agent.display_name}")
            print()
        
    except Exception as e:
        print(f"❌ Failed to list agents: {e}")

def delete_agent(resource_id):
    """Delete a deployed agent."""
    print(f"🗑️  Deleting agent with ID: {resource_id}")
    
    try:
        import vertexai
        from vertexai import agent_engines
        
        # Initialize Vertex AI
        project = os.getenv("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        vertexai.init(
            project=project,
            location=location
        )
        
        # Delete agent engine
        agent_engines.AgentEngine.delete(resource_id)
        print(f"✅ Agent {resource_id} deleted successfully")
        
    except Exception as e:
        print(f"❌ Failed to delete agent: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Deploy Baptist Health Timecard Management Agent")
    parser.add_argument("--create", action="store_true", help="Create and deploy agent")
    parser.add_argument("--list", action="store_true", help="List deployed agents")
    parser.add_argument("--delete", action="store_true", help="Delete agent")
    parser.add_argument("--resource_id", type=str, help="Agent resource ID for deletion")
    
    args = parser.parse_args()
    
    if args.create:
        deploy_agent()
    elif args.list:
        list_agents()
    elif args.delete:
        if not args.resource_id:
            print("❌ --resource_id is required for deletion")
            return
        delete_agent(args.resource_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
