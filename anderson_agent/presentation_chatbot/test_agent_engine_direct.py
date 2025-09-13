#!/usr/bin/env python3
"""
Test script to interact with the deployed Agent Engine directly
"""

import vertexai
from vertexai import agent_engines
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_agent_engine():
    """Test the deployed Agent Engine directly"""
    
    # Initialize Vertex AI
    project_id = "agent-space-465923"
    location = "us-central1"
    
    print(f"🚀 Testing Agent Engine")
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
        
        # Test 1: Simple greeting
        print("🧪 Test 1: Simple Greeting")
        print("-" * 30)
        try:
            response = agent_engine.streaming_agent_run_with_events("Hello, can you help me?")
            print(f"Response: {response}")
            print(f"Response type: {type(response)}")
            print()
        except Exception as e:
            print(f"❌ Error in Test 1: {e}")
            print()
        
        # Test 2: List customers
        print("🧪 Test 2: List Customers")
        print("-" * 30)
        try:
            response = agent_engine.streaming_agent_run_with_events("List all customers")
            print(f"Response: {response}")
            print(f"Response type: {type(response)}")
            print()
        except Exception as e:
            print(f"❌ Error in Test 2: {e}")
            print()
        
        # Test 3: Create presentation
        print("🧪 Test 3: Create Presentation")
        print("-" * 30)
        try:
            response = agent_engine.streaming_agent_run_with_events("Create the presentation for this week")
            print(f"Response: {response}")
            print(f"Response type: {type(response)}")
            print()
        except Exception as e:
            print(f"❌ Error in Test 3: {e}")
            print()
        
        # Test 4: Check agent details and available methods
        print("🧪 Test 4: Agent Details and Methods")
        print("-" * 30)
        try:
            print(f"Agent Resource Name: {agent_engine.resource_name}")
            print(f"Agent Display Name: {agent_engine.display_name}")
            print(f"Agent Create Time: {agent_engine.create_time}")
            print(f"Agent Update Time: {agent_engine.update_time}")
            print(f"Available methods: {[method for method in dir(agent_engine) if not method.startswith('_')]}")
            print()
        except Exception as e:
            print(f"❌ Error in Test 4: {e}")
            print()
        
    except Exception as e:
        print(f"❌ Failed to connect to Agent Engine: {e}")
        return False
    
    print("✅ Agent Engine testing completed!")
    return True

if __name__ == "__main__":
    test_agent_engine()
