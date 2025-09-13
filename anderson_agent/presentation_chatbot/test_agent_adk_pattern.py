#!/usr/bin/env python3
"""
Test script for the deployed Agent Engine based on ADK samples pattern
"""

import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
import json

def pretty_print_event(event):
    """Pretty prints an event with truncation for long content."""
    if "content" not in event:
        print(f"[{event.get('author', 'unknown')}]: {event}")
        return
        
    author = event.get("author", "unknown")
    parts = event["content"].get("parts", [])
    
    for part in parts:
        if "text" in part:
            text = part["text"]
            print(f"[{author}]: {text}")
        elif "functionCall" in part:
            func_call = part["functionCall"]
            print(f"[{author}]: Function call: {func_call.get('name', 'unknown')}")
            # Truncate args if too long
            args = json.dumps(func_call.get("args", {}))
            if len(args) > 100:
                args = args[:97] + "..."
            print(f"  Args: {args}")
        elif "functionResponse" in part:
            func_response = part["functionResponse"]
            print(f"[{author}]: Function response: {func_response.get('name', 'unknown')}")
            # Truncate response if too long
            response = json.dumps(func_response.get("response", {}))
            if len(response) > 100:
                response = response[:97] + "..."
            print(f"  Response: {response}")

def test_agent_engine():
    """Test the deployed Agent Engine using ADK samples pattern"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Vertex AI
    project_id = "agent-space-465923"
    location = "us-central1"
    
    print(f"🚀 Testing Agent Engine (ADK Samples Pattern)")
    print(f"Project: {project_id}")
    print(f"Location: {location}")
    print("=" * 50)
    
    try:
        vertexai.init(
            project=project_id,
            location=location,
        )
        
        # Get the deployed agent
        agent_engine_id = "8105287458662383616"
        print(f"📋 Agent Engine ID: {agent_engine_id}")
        
        agent_engine = agent_engines.get(agent_engine_id)
        print(f"✅ Successfully connected to Agent Engine")
        print(f"Agent Name: {agent_engine.display_name}")
        print()
        
        # Test 1: Create a session and test simple greeting
        print("🧪 Test 1: Create Session and Simple Greeting")
        print("-" * 30)
        try:
            session = agent_engine.create_session(user_id="test_user")
            print(f"Session created: {session['id']}")
            
            print("Testing simple greeting...")
            for event in agent_engine.stream_query(
                user_id="test_user",
                session_id=session["id"],
                message="Hello, can you help me?"
            ):
                pretty_print_event(event)
            print()
        except Exception as e:
            print(f"❌ Error in Test 1: {e}")
            print()
        
        # Test 2: List customers
        print("🧪 Test 2: List Customers")
        print("-" * 30)
        try:
            for event in agent_engine.stream_query(
                user_id="test_user",
                session_id=session["id"],
                message="List all customers"
            ):
                pretty_print_event(event)
            print()
        except Exception as e:
            print(f"❌ Error in Test 2: {e}")
            print()
        
        # Test 3: Create presentation
        print("🧪 Test 3: Create Presentation")
        print("-" * 30)
        try:
            for event in agent_engine.stream_query(
                user_id="test_user",
                session_id=session["id"],
                message="Create the presentation for this week"
            ):
                pretty_print_event(event)
            print()
        except Exception as e:
            print(f"❌ Error in Test 3: {e}")
            print()
        
        print("✅ Agent Engine testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Agent Engine: {e}")
        return False

if __name__ == "__main__":
    test_agent_engine()
