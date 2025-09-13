#!/usr/bin/env python3
"""
Test script for the updated presentation chatbot
"""

import sys
import os
import json

# Add the presentation_chatbot to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'presentation_chatbot'))

from presentation_chatbot.tools.tools_enhanced import (
    generate_presentation,
    generate_multi_slide_presentation,
    get_presentation_templates,
    list_presentations,
    ImageData,
    ProjectData
)

def test_single_slide_presentation():
    """Test single slide presentation generation"""
    
    print("🧪 Testing Single Slide Presentation")
    print("=" * 50)
    
    # Test data
    title = "Test Single Slide Presentation"
    text_content = [
        "This is a test presentation",
        "Created by the updated chatbot",
        "With Cloud Storage integration"
    ]
    
    # Test image data
    image_data = [
        ImageData(
            gcs_url="gs://anderson_images/project_images/1-1.png",
            title="Test Image 1"
        )
    ]
    
    try:
        result = generate_presentation(
            title=title,
            text_content=text_content,
            image_data=image_data,
            include_eqi=True
        )
        
        print("✅ Single slide presentation test completed")
        print(f"Result: {result[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Single slide presentation test failed: {e}")
        return False

def test_multi_slide_presentation():
    """Test multi-slide presentation generation"""
    
    print("\n🧪 Testing Multi-Slide Presentation")
    print("=" * 50)
    
    # Test data for multiple projects
    projects = [
        ProjectData(
            title="Project 1: Test Project",
            text_content=["This is project 1", "With test content"],
            image_data=[
                ImageData(
                    gcs_url="gs://anderson_images/project_images/1-1.png",
                    title="Project 1 Image"
                )
            ],
            include_eqi=True
        ),
        ProjectData(
            title="Project 2: Another Test Project",
            text_content=["This is project 2", "With different content"],
            image_data=[
                ImageData(
                    gcs_url="gs://anderson_images/project_images/2-1.png",
                    title="Project 2 Image"
                )
            ],
            include_eqi=False
        )
    ]
    
    try:
        result = generate_multi_slide_presentation(projects=projects)
        
        print("✅ Multi-slide presentation test completed")
        print(f"Result: {result[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Multi-slide presentation test failed: {e}")
        return False

def test_get_templates():
    """Test getting presentation templates"""
    
    print("\n🧪 Testing Get Templates")
    print("=" * 50)
    
    try:
        result = get_presentation_templates()
        
        print("✅ Get templates test completed")
        print(f"Result: {result[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Get templates test failed: {e}")
        return False

def test_list_presentations():
    """Test listing presentations"""
    
    print("\n🧪 Testing List Presentations")
    print("=" * 50)
    
    try:
        result = list_presentations()
        
        print("✅ List presentations test completed")
        print(f"Result: {result[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ List presentations test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 Presentation Chatbot Update Test")
    print("=" * 60)
    
    # Run tests
    tests = [
        ("Single Slide Presentation", test_single_slide_presentation),
        ("Multi-Slide Presentation", test_multi_slide_presentation),
        ("Get Templates", test_get_templates),
        ("List Presentations", test_list_presentations),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running {test_name} test...")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Presentation chatbot is ready!")
        print("📁 The chatbot now supports:")
        print("   ✅ Single slide presentations with Cloud Storage")
        print("   ✅ Multi-slide presentations with Cloud Storage")
        print("   ✅ Template information")
        print("   ✅ Presentation listing")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()
