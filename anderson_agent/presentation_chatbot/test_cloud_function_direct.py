#!/usr/bin/env python3
"""
Simple test to debug logo and EQI issues
"""

import requests
import json

def test_cloud_function_directly():
    """Test the cloud function directly with minimal data"""
    
    print("🧪 Testing Cloud Function Directly")
    print("=" * 50)
    
    # Test data with explicit logo and EQI
    test_data = {
        "projects": [
            {
                "title": "Test Project with Logo and EQI",
                "logo_gcs_url": "gs://anderson_images/customer_logos/walmart-logo.png",
                "text_content": ["This is a test project", "With explicit logo and EQI"],
                "image_data": [
                    {
                        "gcs_url": "gs://anderson_images/project_images/1-1.png",
                        "title": "Test Image"
                    }
                ],
                "include_eqi": True
            }
        ]
    }
    
    cloud_function_url = "https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator"
    
    try:
        print(f"Sending request to {cloud_function_url}/generate_multi")
        print(f"Request data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            f"{cloud_function_url}/generate_multi",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=120
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Success! Cloud Storage URL: {response_data.get('presentation_url')}")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_cloud_function_directly()
