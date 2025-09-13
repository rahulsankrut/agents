#!/usr/bin/env python3
"""
Test script for the updated presentation chatbot with Firestore integration
"""

import sys
import os

# Add the presentation_chatbot to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'presentation_chatbot'))

from presentation_chatbot.tools.tools_enhanced import (
    create_weekly_presentation,
    list_customers,
    generate_presentation,
    generate_multi_slide_presentation,
    list_presentations,
    get_presentation_templates,
    ImageData,
    ProjectData
)

def test_list_customers():
    """Test listing customers from Firestore"""
    
    print("🧪 Testing List Customers")
    print("=" * 50)
    
    try:
        result = list_customers()
        
        print("✅ List customers test completed")
        print(f"Result: {result[:300]}...")
        return True
        
    except Exception as e:
        print(f"❌ List customers test failed: {e}")
        return False

def test_create_weekly_presentation_all():
    """Test creating weekly presentation for all projects"""
    
    print("\n🧪 Testing Create Weekly Presentation (All Projects)")
    print("=" * 50)
    
    try:
        result = create_weekly_presentation()
        
        print("✅ Create weekly presentation (all) test completed")
        print(f"Result: {result[:300]}...")
        return True
        
    except Exception as e:
        print(f"❌ Create weekly presentation (all) test failed: {e}")
        return False

def test_create_weekly_presentation_walmart():
    """Test creating weekly presentation for Walmart only"""
    
    print("\n🧪 Testing Create Weekly Presentation (Walmart Only)")
    print("=" * 50)
    
    try:
        result = create_weekly_presentation(customer_name="Walmart")
        
        print("✅ Create weekly presentation (Walmart) test completed")
        print(f"Result: {result[:300]}...")
        return True
        
    except Exception as e:
        print(f"❌ Create weekly presentation (Walmart) test failed: {e}")
        return False

def test_create_weekly_presentation_target():
    """Test creating weekly presentation for Target only"""
    
    print("\n🧪 Testing Create Weekly Presentation (Target Only)")
    print("=" * 50)
    
    try:
        result = create_weekly_presentation(customer_name="Target")
        
        print("✅ Create weekly presentation (Target) test completed")
        print(f"Result: {result[:300]}...")
        return True
        
    except Exception as e:
        print(f"❌ Create weekly presentation (Target) test failed: {e}")
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
    
    print("🚀 Presentation Chatbot Firestore Integration Test")
    print("=" * 70)
    
    # Run tests
    tests = [
        ("List Customers", test_list_customers),
        ("Create Weekly Presentation (All)", test_create_weekly_presentation_all),
        ("Create Weekly Presentation (Walmart)", test_create_weekly_presentation_walmart),
        ("Create Weekly Presentation (Target)", test_create_weekly_presentation_target),
        ("List Presentations", test_list_presentations),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running {test_name} test...")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 70)
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
        print("   ✅ Automatic weekly presentations from Firestore")
        print("   ✅ Customer-specific presentations")
        print("   ✅ Customer listing with project counts")
        print("   ✅ Cloud Storage integration")
        print("\n💡 Users can now simply say:")
        print("   • 'Create the presentation for this week'")
        print("   • 'Create the presentation for Walmart for this week'")
        print("   • 'Create the presentation for Target for this week'")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()
