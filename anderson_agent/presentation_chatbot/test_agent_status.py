#!/usr/bin/env python3
"""
Simple test to check Agent Engine status and get basic info
"""

import vertexai
from vertexai import agent_engines
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_agent_status():
    """Test the deployed Agent Engine status"""
    
    # Initialize Vertex AI
    project_id = "agent-space-465923"
    location = "us-central1"
    
    print(f"🚀 Agent Engine Status Check")
    print(f"Project: {project_id}")
    print(f"Location: {location}")
    print("=" * 50)
    
    try:
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        
        # Get the deployed agent
        agent_engine_id = "1510891704285134848"
        print(f"📋 Agent Engine ID: {agent_engine_id}")
        
        agent_engine = vertexai.agent_engines.get(agent_engine_id)
        print(f"✅ Successfully connected to Agent Engine")
        print(f"Agent Name: {agent_engine.display_name}")
        print(f"Agent Resource Name: {agent_engine.resource_name}")
        print(f"Agent Create Time: {agent_engine.create_time}")
        print(f"Agent Update Time: {agent_engine.update_time}")
        print()
        
        # Check if we can get sessions
        print("🧪 Testing Session Management")
        print("-" * 30)
        try:
            sessions = agent_engine.list_sessions(user_id="test_user")
            print(f"Sessions: {sessions}")
            print(f"Sessions type: {type(sessions)}")
            print()
        except Exception as e:
            print(f"❌ Error listing sessions: {e}")
            print()
        
        # Check operation schemas
        print("🧪 Testing Operation Schemas")
        print("-" * 30)
        try:
            schemas = agent_engine.operation_schemas
            print(f"Operation schemas: {schemas}")
            print(f"Schemas type: {type(schemas)}")
            print()
        except Exception as e:
            print(f"❌ Error getting schemas: {e}")
            print()
        
        print("✅ Agent Engine status check completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Agent Engine: {e}")
        return False

if __name__ == "__main__":
    test_agent_status()
