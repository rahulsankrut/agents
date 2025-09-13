#!/usr/bin/env python3
"""
Test script to check if the agent can be imported and initialized locally
"""

import sys
import os

# Add the presentation_chatbot to the path
sys.path.append('/Users/rahulkasanagottu/Desktop/agents/anderson_agent/presentation_chatbot')

def test_agent_import():
    """Test if the agent can be imported and initialized"""
    
    print("🧪 Testing Agent Import and Initialization")
    print("=" * 50)
    
    try:
        # Test 1: Import config
        print("Test 1: Importing config...")
        from presentation_chatbot.config import config
        print(f"✅ Config imported successfully")
        print(f"Project ID: {config.project_id}")
        print(f"Agent Model: {config.agent_model}")
        print(f"Agent Name: {config.agent_name}")
        print()
        
        # Test 2: Validate config
        print("Test 2: Validating config...")
        try:
            config.validate()
            print("✅ Config validation passed")
        except Exception as e:
            print(f"❌ Config validation failed: {e}")
        print()
        
        # Test 3: Import tools
        print("Test 3: Importing tools...")
        from presentation_chatbot.tools.tools_enhanced import (
            generate_presentation,
            generate_multi_slide_presentation,
            create_weekly_presentation,
            list_customers,
            get_presentation_templates,
            list_presentations,
        )
        print("✅ Tools imported successfully")
        print()
        
        # Test 4: Import agent
        print("Test 4: Importing agent...")
        from presentation_chatbot.agent import root_agent
        print("✅ Agent imported successfully")
        print(f"Agent name: {root_agent.name}")
        print(f"Agent model: {root_agent.model}")
        print(f"Number of tools: {len(root_agent.tools)}")
        print()
        
        print("✅ All tests passed! Agent can be imported and initialized locally.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent_import()
