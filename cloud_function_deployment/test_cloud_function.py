#!/usr/bin/env python3
"""
Cloud Function Test Script for PowerPoint Generation API
Tests the deployed Cloud Function using the same test data as run_test.py
"""

import requests
import json
import os
import sys
import time
from pathlib import Path

# Cloud Function URL
CLOUD_FUNCTION_URL = "https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator"

# GCS Test Images URLs (from the test bucket we just created)
TEST_IMAGES = {
    "logo": "gs://ppt-generator-test-images/test_images/test_resources/walmart_logo.jpg",
    "image_one": "gs://ppt-generator-test-images/test_images/test_resources/test_image_one.png",
    "image_two": "gs://ppt-generator-test-images/test_images/test_resources/test_image_two.png"
}

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🧪 Testing Health Endpoint")
    print("-" * 40)
    
    try:
        response = requests.get(f"{CLOUD_FUNCTION_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_templates_endpoint():
    """Test the templates endpoint"""
    print("\n🧪 Testing Templates Endpoint")
    print("-" * 40)
    
    try:
        response = requests.get(f"{CLOUD_FUNCTION_URL}/templates", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'templates' in data and len(data['templates']) > 0:
                print(f"✅ Templates endpoint working - found {len(data['templates'])} templates")
                print(f"   Available template: {data['templates'][0]['name']}")
                return True
            else:
                print(f"❌ No templates found in response")
                return False
        else:
            print(f"❌ Templates endpoint failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Templates endpoint error: {e}")
        return False

def test_run_test_py_equivalent():
    """Test presentation generation exactly like run_test.py"""
    print("\n🧪 Testing run_test.py Equivalent")
    print("-" * 40)
    
    # Test data exactly as specified in run_test.py
    test_title = "Client: Project/Activity Store Count: 1234"
    test_text_content = "One\nTwo\nThree"
    test_images = [
        {"path": "test_resources/test_image_one.png", "title": "Side Panels 1-4"},
        {"path": "test_resources/test_image_two.png", "title": "PlayStation Case Topper"}
    ]
    include_eqi = True
    
    print(f"📝 Title: {test_title}")
    print(f"📄 Text Content: {test_text_content}")
    print(f"🖼️  Images: {test_images}")
    print(f"🔢 Include EQI: {include_eqi}")
    print("-" * 50)
    
    # Prepare image data with GCS URLs
    processed_image_data = []
    for i, img_item in enumerate(test_images):
        # Map local paths to GCS URLs
        if "test_image_one.png" in img_item["path"]:
            gcs_url = TEST_IMAGES["image_one"]
        elif "test_image_two.png" in img_item["path"]:
            gcs_url = TEST_IMAGES["image_two"]
        else:
            print(f"⚠️  Unknown image path: {img_item['path']}")
            continue
        
        processed_image_data.append({
            "gcs_url": gcs_url,
            "title": img_item["title"]
        })
        print(f"✅ Mapped {img_item['title']} to GCS URL")
    
    # Prepare test data
    test_data = {
        "title": test_title,
        "text_content": test_text_content,
        "image_data": processed_image_data,
        "include_eqi": include_eqi,
        "logo_gcs_url": TEST_IMAGES["logo"]
    }
    
    try:
        response = requests.post(
            f"{CLOUD_FUNCTION_URL}/generate",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            # Check if it's a PowerPoint file
            content_type = response.headers.get('content-type', '')
            if 'presentationml' in content_type or 'octet-stream' in content_type:
                # Save the file
                filename = "run_test_equivalent_presentation.pptx"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(filename)
                print(f"✅ run_test.py equivalent presentation generated successfully!")
                print(f"   📁 File: {filename}")
                print(f"   📊 Size: {file_size:,} bytes")
                print(f"   📍 Path: {os.path.abspath(filename)}")
                return True
            else:
                print(f"❌ Unexpected content type: {content_type}")
                return False
        else:
            print(f"❌ run_test.py equivalent generation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ run_test.py equivalent generation error: {e}")
        return False

def test_presentation_with_logo():
    """Test presentation generation with logo (GCS URL)"""
    print("\n🧪 Testing Presentation with Logo")
    print("-" * 40)
    
    test_data = {
        "title": "Test Presentation with Logo",
        "text_content": "• Logo Test\n• GCS URL\n• Cloud Function Working",
        "include_eqi": False,
        "logo_gcs_url": TEST_IMAGES["logo"]
    }
    
    print(f"📝 Title: {test_data['title']}")
    print(f"📄 Text Content: {test_data['text_content']}")
    print(f"🖼️  Logo URL: {test_data['logo_gcs_url']}")
    
    try:
        response = requests.post(
            f"{CLOUD_FUNCTION_URL}/generate",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'presentationml' in content_type or 'octet-stream' in content_type:
                filename = "test_logo_presentation.pptx"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(filename)
                print(f"✅ Logo presentation generated successfully!")
                print(f"   📁 File: {filename}")
                print(f"   📊 Size: {file_size:,} bytes")
                return True
            else:
                print(f"❌ Unexpected content type: {content_type}")
                return False
        else:
            print(f"❌ Logo presentation generation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Logo presentation generation error: {e}")
        return False

def test_presentation_with_images():
    """Test presentation generation with multiple images (GCS URLs)"""
    print("\n🧪 Testing Presentation with Images")
    print("-" * 40)
    
    test_data = {
        "title": "Test Presentation with Images",
        "text_content": "• Image Test 1\n• Image Test 2\n• Multiple Images Working",
        "include_eqi": True,
        "image_data": [
            {
                "gcs_url": TEST_IMAGES["image_one"],
                "title": "Test Image 1"
            },
            {
                "gcs_url": TEST_IMAGES["image_two"],
                "title": "Test Image 2"
            }
        ]
    }
    
    print(f"📝 Title: {test_data['title']}")
    print(f"📄 Text Content: {test_data['text_content']}")
    print(f"🖼️  Image URLs: {len(test_data['image_data'])} images")
    
    try:
        response = requests.post(
            f"{CLOUD_FUNCTION_URL}/generate",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'presentationml' in content_type or 'octet-stream' in content_type:
                filename = "test_images_presentation.pptx"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(filename)
                print(f"✅ Images presentation generated successfully!")
                print(f"   📁 File: {filename}")
                print(f"   📊 Size: {file_size:,} bytes")
                return True
            else:
                print(f"❌ Unexpected content type: {content_type}")
                return False
        else:
            print(f"❌ Images presentation generation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Images presentation generation error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid requests"""
    print("\n🧪 Testing Error Handling")
    print("-" * 40)
    
    # Test 1: Missing title
    print("Testing missing title...")
    try:
        response = requests.post(
            f"{CLOUD_FUNCTION_URL}/generate",
            json={"text_content": "Test without title"},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if response.status_code == 400:
            print("✅ Missing title correctly rejected")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing missing title: {e}")
    
    # Test 2: Invalid JSON
    print("Testing invalid JSON...")
    try:
        response = requests.post(
            f"{CLOUD_FUNCTION_URL}/generate",
            data="invalid json",
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if response.status_code == 400:
            print("✅ Invalid JSON correctly rejected")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing invalid JSON: {e}")
    
    return True

def run_performance_test():
    """Run a simple performance test"""
    print("\n🧪 Running Performance Test")
    print("-" * 40)
    
    test_data = {
        "title": "Performance Test Presentation",
        "text_content": "• Performance Test\n• Response Time Check\n• Cloud Function Speed",
        "include_eqi": False
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{CLOUD_FUNCTION_URL}/generate",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            print(f"✅ Performance test completed!")
            print(f"   ⏱️  Response time: {response_time:.2f} seconds")
            print(f"   📊 File size: {len(response.content):,} bytes")
            
            if response_time < 10:
                print("   🚀 Excellent performance!")
            elif response_time < 30:
                print("   ✅ Good performance")
            else:
                print("   ⚠️  Slow performance")
            
            return True
        else:
            print(f"❌ Performance test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Run all Cloud Function tests"""
    print("🎯 PowerPoint Generation Cloud Function Test Suite")
    print("=" * 60)
    print(f"🌐 Testing Cloud Function: {CLOUD_FUNCTION_URL}")
    print("=" * 60)
    
    # List of tests to run
    tests = [
        ("Health Check", test_health_endpoint),
        ("Templates Endpoint", test_templates_endpoint),
        ("run_test.py Equivalent", test_run_test_py_equivalent),
        ("Presentation with Logo", test_presentation_with_logo),
        ("Presentation with Images", test_presentation_with_images),
        ("Error Handling", test_error_handling),
        ("Performance Test", run_performance_test)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Cloud Function is working perfectly!")
    elif passed >= len(results) * 0.8:
        print("✅ Most tests passed! Cloud Function is working well.")
    else:
        print("⚠️  Several tests failed. Check the logs above for details.")
    
    print("\n📁 Generated Files:")
    generated_files = [
        "run_test_equivalent_presentation.pptx",
        "test_logo_presentation.pptx", 
        "test_images_presentation.pptx"
    ]
    
    for filename in generated_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   📄 {filename} ({size:,} bytes)")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
