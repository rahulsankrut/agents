#!/usr/bin/env python3
"""
Debug script to test logo and EQI handling in multi-slide presentations
"""

import sys
import os
import json

# Add the presentation_chatbot to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'presentation_chatbot'))

from presentation_chatbot.tools.tools_enhanced import (
    create_weekly_presentation,
    list_customers,
    ImageData,
    ProjectData
)

def test_single_project_with_logo_and_eqi():
    """Test creating a presentation with just one project to debug logo/EQI issues"""
    
    print("🧪 Testing Single Project with Logo and EQI")
    print("=" * 60)
    
    try:
        # Test with just Walmart projects (should have logos and EQI)
        result = create_weekly_presentation(customer_name="Walmart")
        
        print("✅ Single project test completed")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Single project test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_custom_project_data():
    """Test with custom project data to isolate the issue"""
    
    print("\n🧪 Testing Custom Project Data")
    print("=" * 60)
    
    try:
        # Create custom project data with explicit logo and EQI
        custom_projects = [
            ProjectData(
                title="Test Project with Logo and EQI",
                logo_gcs_url="gs://anderson_images/customer_logos/walmart-logo.png",
                text_content=["This is a test project", "With explicit logo and EQI"],
                image_data=[
                    ImageData(
                        gcs_url="gs://anderson_images/project_images/1-1.png",
                        title="Test Image"
                    )
                ],
                include_eqi=True
            )
        ]
        
        from presentation_chatbot.tools.tools_enhanced import generate_multi_slide_presentation
        result = generate_multi_slide_presentation(projects=custom_projects)
        
        print("✅ Custom project test completed")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Custom project test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    
    print("🔍 Debug: Logo and EQI Issues in Multi-Slide Presentations")
    print("=" * 70)
    
    # First, let's see what customers we have
    print("\n📋 Available Customers:")
    customers_result = list_customers()
    print(customers_result)
    
    # Test with single project
    test_single_project_with_logo_and_eqi()
    
    # Test with custom data
    test_custom_project_data()

if __name__ == "__main__":
    main()
