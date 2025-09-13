#!/usr/bin/env python3
"""
Comprehensive test to interact with the deployed Agent Engine
"""

import vertexai
from vertexai import agent_engines
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_agent_comprehensive():
    """Comprehensive test of the deployed Agent Engine"""
    
    # Initialize Vertex AI
    project_id = "agent-space-465923"
    location = "us-central1"
    
    print(f"🚀 Comprehensive Agent Engine Test")
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
        print()
        
        # Test 1: Create a session
        print("🧪 Test 1: Create Session")
        print("-" * 30)
        try:
            session = agent_engine.create_session(user_id="test_user")
            print(f"Session created: {session}")
            print(f"Session type: {type(session)}")
            print()
        except Exception as e:
            print(f"❌ Error creating session: {e}")
            print()
        
        # Test 2: Try to query the agent
        print("🧪 Test 2: Query Agent")
        print("-" * 30)
        try:
            # Try different query methods
            print("Trying stream_query...")
            response = agent_engine.stream_query(user_id="test_user", query="Hello, can you help me?")
            print(f"Stream query response: {response}")
            print(f"Response type: {type(response)}")
            print()
        except Exception as e:
            print(f"❌ Error with stream_query: {e}")
            print()
        
        # Test 3: Try async query
        print("🧪 Test 3: Async Query")
        print("-" * 30)
        try:
            print("Trying async_stream_query...")
            response = agent_engine.async_stream_query(user_id="test_user", query="Hello, can you help me?")
            print(f"Async stream query response: {response}")
            print(f"Response type: {type(response)}")
            print()
        except Exception as e:
            print(f"❌ Error with async_stream_query: {e}")
            print()
        
        print("✅ Comprehensive Agent Engine test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Agent Engine: {e}")
        return False

if __name__ == "__main__":
    test_agent_comprehensive()
