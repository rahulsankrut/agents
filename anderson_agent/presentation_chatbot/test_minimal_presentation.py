#!/usr/bin/env python3
"""
Test script to verify GCS access from cloud function perspective
"""

import requests
import json

def test_minimal_presentation():
    """Test with minimal data - no logos or images"""
    
    print("🧪 Testing Minimal Presentation (No Logos/Images)")
    print("=" * 60)
    
    # Test data with no logos or images
    test_data = {
        "projects": [
            {
                "title": "Test Project - No Assets",
                "text_content": ["This is a test project", "With no logos or images"],
                "image_data": [],
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
            
            # Download and check file size
            import urllib.request
            url = response_data.get('presentation_url')
            filename = "minimal_test.pptx"
            urllib.request.urlretrieve(url, filename)
            
            import os
            file_size = os.path.getsize(filename)
            print(f"📁 Downloaded file size: {file_size} bytes")
            
            if file_size > 1000:  # Should be much larger than 298 bytes
                print("✅ File size looks good!")
            else:
                print("❌ File size is suspiciously small")
            
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_minimal_presentation()
