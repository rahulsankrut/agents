#!/usr/bin/env python3
"""
Test script for the Inspirational Stories Agent
This script tests the basic functionality without requiring the Google API.
"""

import sys
import os

# Add the current directory to the path so we can import the agent module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_agent_creation():
    """Test that the agent can be created successfully."""
    print("🧪 Testing agent creation...")
    
    try:
        from agent import root_agent
        
        print("✅ Agent created successfully!")
        print(f"🤖 Agent name: {root_agent.name}")
        print(f"📝 Description: {root_agent.description}")
        print(f"🛠️ Available tools: {len(root_agent.tools)}")
        
        # List available tools
        for i, tool in enumerate(root_agent.tools):
            print(f"  {i+1}. {tool.__name__}: {tool.__doc__.split('.')[0] if tool.__doc__ else 'No description'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation test failed with error: {e}")
        return False

def test_data_structures():
    """Test that the data structures are properly initialized."""
    print("🧪 Testing data structures...")
    
    try:
        from agent import STORIES_DB, RESEARCH_DB, STORY_COUNTER, RESEARCH_COUNTER
        
        print("✅ Data structures initialized successfully!")
        print(f"📚 Stories database: {len(STORIES_DB)} entries")
        print(f"🔍 Research database: {len(RESEARCH_DB)} entries")
        print(f"📖 Story counter: {STORY_COUNTER}")
        print(f"🔬 Research counter: {RESEARCH_COUNTER}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data structures test failed with error: {e}")
        return False

def test_function_imports():
    """Test that all functions can be imported successfully."""
    print("🧪 Testing function imports...")
    
    try:
        from agent import (
            research_famous_person,
            create_inspirational_story,
            suggest_inspirational_people,
            enhance_story_for_children,
            list_stories,
            get_story,
            list_research,
            export_story
        )
        
        print("✅ All functions imported successfully!")
        print(f"🔍 research_famous_person: {research_famous_person.__name__}")
        print(f"📚 create_inspirational_story: {create_inspirational_story.__name__}")
        print(f"🎯 suggest_inspirational_people: {suggest_inspirational_people.__name__}")
        print(f"🔧 enhance_story_for_children: {enhance_story_for_children.__name__}")
        print(f"📋 list_stories: {list_stories.__name__}")
        print(f"📖 get_story: {get_story.__name__}")
        print(f"🔬 list_research: {list_research.__name__}")
        print(f"📤 export_story: {export_story.__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Function imports test failed with error: {e}")
        return False

def test_basic_operations():
    """Test basic operations that don't require API calls."""
    print("🧪 Testing basic operations...")
    
    try:
        from agent import list_stories, list_research
        
        # Test listing empty databases
        stories_result = list_stories()
        if stories_result["status"] == "success" and stories_result["count"] == 0:
            print("✅ Stories listing works correctly (empty database)")
        else:
            print("❌ Stories listing failed")
            return False
        
        research_result = list_research()
        if research_result["status"] == "success" and research_result["count"] == 0:
            print("✅ Research listing works correctly (empty database)")
        else:
            print("❌ Research listing failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic operations test failed with error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Inspirational Stories Agent Tests...")
    print("=" * 60)
    
    tests = [
        ("Agent Creation", test_agent_creation),
        ("Data Structures", test_data_structures),
        ("Function Imports", test_function_imports),
        ("Basic Operations", test_basic_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The inspirational stories agent is working correctly.")
        print("\n💡 You can now:")
        print("   • Run the full demo: python demo.py")
        print("   • Use the agent with Google ADK")
        print("   • Research famous personalities")
        print("   • Create inspirational children's stories")
        print("   • Customize and extend the agent")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\n🔧 Common issues:")
        print("   • Make sure all dependencies are installed")
        print("   • Check that the agent.py file is properly formatted")
        print("   • Verify Python version compatibility")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
