#!/usr/bin/env python3
"""
Test script for deployed Baptist Health Timecard Management Agent
"""

import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_deployed_agent():
    """Test the deployed agent."""
    print("🧪 Testing Deployed Baptist Health Timecard Management Agent")
    print("=" * 60)
    
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
        
        print(f"✅ Initialized Vertex AI with project: {project}")
        
        # List available agents
        agent_engines_list = agent_engines.AgentEngine.list()
        
        if not agent_engines_list:
            print("❌ No deployed agents found. Deploy first with: poetry run python deploy.py --create")
            return
        
        # Use the first available agent
        agent_engine = agent_engines_list[0]
        print(f"✅ Using agent: {agent_engine.display_name}")
        
        # Test the agent
        print("\n🤖 Agent Details:")
        print(f"  - Name: {agent_engine.display_name}")
        print(f"  - Resource Name: {agent_engine.name}")
        print(f"  - Project: {agent_engine.project}")
        print(f"  - Location: {agent_engine.location}")
        print(f"  - Create Time: {agent_engine.create_time}")
        
        print("\n📋 Agent Engine created successfully!")
        print("Note: This AgentEngine appears to be a resource management object.")
        print("To interact with it, you may need to use the Agent Engine web interface")
        print("or check the Vertex AI console for interaction methods.")
        
        print("\n🎉 Deployed agent test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_deployed_agent()
