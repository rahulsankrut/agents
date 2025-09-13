#!/usr/bin/env python3
"""
Test script to properly interact with the deployed Agent Engine and see actual responses
"""

import vertexai
from vertexai import agent_engines
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_agent_responses():
    """Test the deployed Agent Engine and get actual responses"""
    
    # Initialize Vertex AI
    project_id = "agent-space-465923"
    location = "us-central1"
    
    print(f"🚀 Agent Engine Response Test")
    print(f"Project: {project_id}")
    print(f"Location: {location}")
    print("=" * 50)
    
    try:
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        
        # Get the deployed agent
        agent_engine_id = "3915813905300979712"
        print(f"📋 Agent Engine ID: {agent_engine_id}")
        
        agent_engine = vertexai.agent_engines.get(agent_engine_id)
        print(f"✅ Successfully connected to Agent Engine")
        print(f"Agent Name: {agent_engine.display_name}")
        print()
        
        # Test 1: Simple greeting
        print("🧪 Test 1: Simple Greeting")
        print("-" * 30)
        try:
            response_generator = agent_engine.stream_query(user_id="test_user", query="Hello, can you help me?")
            print("Response stream:")
            for response in response_generator:
                print(f"  {response}")
            print()
        except Exception as e:
            print(f"❌ Error in Test 1: {e}")
            print()
        
        # Test 2: List customers
        print("🧪 Test 2: List Customers")
        print("-" * 30)
        try:
            response_generator = agent_engine.stream_query(user_id="test_user", query="List all customers")
            print("Response stream:")
            for response in response_generator:
                print(f"  {response}")
            print()
        except Exception as e:
            print(f"❌ Error in Test 2: {e}")
            print()
        
        # Test 3: Create presentation
        print("🧪 Test 3: Create Presentation")
        print("-" * 30)
        try:
            response_generator = agent_engine.stream_query(user_id="test_user", query="Create the presentation for this week")
            print("Response stream:")
            for response in response_generator:
                print(f"  {response}")
            print()
        except Exception as e:
            print(f"❌ Error in Test 3: {e}")
            print()
        
        print("✅ Agent Engine response test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Agent Engine: {e}")
        return False

if __name__ == "__main__":
    test_agent_responses()
