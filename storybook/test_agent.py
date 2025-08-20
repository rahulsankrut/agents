#!/usr/bin/env python3
"""
Test script for the Storybook Agent
This script tests the basic functionality without requiring the Google API.
"""

import sys
import os

# Add the current directory to the path so we can import the agent module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_story_creation():
    """Test story creation functionality."""
    print("🧪 Testing story creation...")
    
    try:
        from agent import create_story, STORIES_DB
        
        # Test creating a story
        result = create_story(
            title="Test Story",
            genre="fantasy",
            main_character="test hero",
            setting="test setting",
            plot_points=2
        )
        
        if result["status"] == "success":
            print("✅ Story creation test passed!")
            print(f"   Created story: {result['story']['title']}")
            print(f"   Story ID: {result['story']['id']}")
            print(f"   Word count: {result['story']['word_count']}")
            return True
        else:
            print("❌ Story creation test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Story creation test failed with error: {e}")
        return False

def test_story_management():
    """Test story management functionality."""
    print("🧪 Testing story management...")
    
    try:
        from agent import list_stories, get_story, edit_story, delete_story
        
        # Test listing stories
        list_result = list_stories()
        if list_result["status"] == "success" and list_result["count"] > 0:
            print("✅ Story listing test passed!")
            
            # Get the first story
            first_story_id = list_result["stories"][0]["id"]
            get_result = get_story(first_story_id)
            
            if get_result["status"] == "success":
                print("✅ Story retrieval test passed!")
                
                # Test editing
                edit_result = edit_story(
                    story_id=first_story_id,
                    title="Updated Test Story"
                )
                
                if edit_result["status"] == "success":
                    print("✅ Story editing test passed!")
                    
                    # Test deletion
                    delete_result = delete_story(first_story_id)
                    if delete_result["status"] == "success":
                        print("✅ Story deletion test passed!")
                        return True
                    else:
                        print("❌ Story deletion test failed!")
                        return False
                else:
                    print("❌ Story editing test failed!")
                    return False
            else:
                print("❌ Story retrieval test failed!")
                return False
        else:
            print("❌ Story listing test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Story management test failed with error: {e}")
        return False

def test_creative_tools():
    """Test creative assistance tools."""
    print("🧪 Testing creative tools...")
    
    try:
        from agent import generate_story_ideas, analyze_story
        
        # Test story idea generation
        ideas_result = generate_story_ideas(genre="sci-fi", theme="adventure")
        if ideas_result["status"] == "success" and len(ideas_result["ideas"]) > 0:
            print("✅ Story idea generation test passed!")
            print(f"   Generated {len(ideas_result['ideas'])} ideas")
        else:
            print("❌ Story idea generation test failed!")
            return False
        
        # Test story analysis (need a story first)
        from agent import create_story
        test_story = create_story(
            title="Analysis Test Story",
            genre="mystery",
            main_character="detective",
            setting="dark city",
            plot_points=3
        )
        
        if test_story["status"] == "success":
            analysis_result = analyze_story(test_story["story"]["id"])
            if analysis_result["status"] == "success":
                print("✅ Story analysis test passed!")
                print(f"   Analysis completed for: {analysis_result['analysis']['title']}")
            else:
                print("❌ Story analysis test failed!")
                return False
        else:
            print("❌ Could not create test story for analysis!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Creative tools test failed with error: {e}")
        return False

def test_export_functionality():
    """Test story export functionality."""
    print("🧪 Testing export functionality...")
    
    try:
        from agent import export_story, create_story
        
        # Create a test story for export
        test_story = create_story(
            title="Export Test Story",
            genre="romance",
            main_character="lover",
            setting="beautiful garden",
            plot_points=2
        )
        
        if test_story["status"] == "success":
            story_id = test_story["story"]["id"]
            
            # Test JSON export
            json_export = export_story(story_id, "json")
            if json_export["status"] == "success":
                print("✅ JSON export test passed!")
            else:
                print("❌ JSON export test failed!")
                return False
            
            # Test text export
            text_export = export_story(story_id, "text")
            if text_export["status"] == "success":
                print("✅ Text export test passed!")
            else:
                print("❌ Text export test failed!")
                return False
            
            # Test markdown export
            md_export = export_story(story_id, "markdown")
            if md_export["status"] == "success":
                print("✅ Markdown export test passed!")
            else:
                print("❌ Markdown export test failed!")
                return False
            
            return True
        else:
            print("❌ Could not create test story for export!")
            return False
            
    except Exception as e:
        print(f"❌ Export functionality test failed with error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Storybook Agent Tests...")
    print("=" * 50)
    
    tests = [
        ("Story Creation", test_story_creation),
        ("Story Management", test_story_management),
        ("Creative Tools", test_creative_tools),
        ("Export Functionality", test_export_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The storybook agent is working correctly.")
        print("\n💡 You can now:")
        print("   • Run the full demo: python demo.py")
        print("   • Use the agent with Google ADK")
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
