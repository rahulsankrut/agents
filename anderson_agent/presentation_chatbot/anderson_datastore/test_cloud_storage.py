#!/usr/bin/env python3
"""
Test script for Cloud Storage functionality
"""

import requests
import json
import sys
import os

# Add the anderson_datastore to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'anderson_datastore'))

from firestore_operations import FirestoreManager

# Cloud function configuration
CLOUD_FUNCTION_URL = "https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator"

def convert_firestore_to_cloud_function_format(project):
    """Convert Firestore project to cloud function format"""
    
    # Convert image data
    image_data = []
    for img in project.images:
        image_data.append({
            "gcs_url": img.image_url,  # Already in gs:// format
            "title": img.description
        })
    
    # Convert EQI from Yes/No to boolean
    include_eqi = project.eqi == "Yes"
    
    # Convert customer logo URL to GCS format if needed
    logo_gcs_url = project.customer_logo_url
    if logo_gcs_url.startswith("https://storage.cloud.google.com/"):
        # Convert https://storage.cloud.google.com/bucket/path to gs://bucket/path
        logo_gcs_url = logo_gcs_url.replace("https://storage.cloud.google.com/", "gs://")
    
    return {
        "title": project.project_title,
        "logo_gcs_url": logo_gcs_url,
        "text_content": [project.project_overview],
        "image_data": image_data,
        "include_eqi": include_eqi
    }

def test_single_slide_cloud_storage():
    """Test single slide generation with Cloud Storage"""
    
    print("🧪 Testing Single Slide with Cloud Storage")
    print("=" * 50)
    
    # Get one project from Firestore
    try:
        manager = FirestoreManager()
        projects = manager.list_projects()
        
        if not projects:
            print("❌ No projects found in Firestore")
            return False
        
        # Take the first project
        project = projects[0]
        print(f"📊 Testing with project: {project.project_title[:50]}...")
        
        # Convert to cloud function format
        project_data = convert_firestore_to_cloud_function_format(project)
        
        print(f"🔄 Calling single slide endpoint...")
        
        response = requests.post(
            CLOUD_FUNCTION_URL + "/generate",
            json=project_data,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )
        
        if response.status_code == 200:
            response_data = response.json()
            cloud_storage_url = response_data.get('presentation_url')
            filename = response_data.get('filename')
            
            print(f"✅ Successfully generated single slide presentation")
            print(f"🌐 Cloud Storage URL: {cloud_storage_url}")
            print(f"📁 Filename: {filename}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multi_slide_cloud_storage():
    """Test multi-slide generation with Cloud Storage"""
    
    print("\n🧪 Testing Multi-Slide with Cloud Storage")
    print("=" * 50)
    
    # Get 3 projects from Firestore
    try:
        manager = FirestoreManager()
        projects = manager.list_projects()
        
        if not projects:
            print("❌ No projects found in Firestore")
            return False
        
        # Take first 3 projects
        test_projects = projects[:3]
        print(f"📊 Testing with {len(test_projects)} projects")
        
        # Convert projects to cloud function format
        projects_data = []
        for project in test_projects:
            project_data = convert_firestore_to_cloud_function_format(project)
            projects_data.append(project_data)
        
        # Prepare payload
        payload = {
            "projects": projects_data
        }
        
        print(f"🔄 Calling multi-slide endpoint...")
        
        response = requests.post(
            CLOUD_FUNCTION_URL + "/generate_multi",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )
        
        if response.status_code == 200:
            response_data = response.json()
            cloud_storage_url = response_data.get('presentation_url')
            filename = response_data.get('filename')
            project_count = response_data.get('project_count')
            
            print(f"✅ Successfully generated multi-slide presentation")
            print(f"🌐 Cloud Storage URL: {cloud_storage_url}")
            print(f"📁 Filename: {filename}")
            print(f"📊 Project Count: {project_count}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    
    print("🚀 Cloud Storage Integration Test")
    print("=" * 50)
    
    # Test single slide
    single_success = test_single_slide_cloud_storage()
    
    # Test multi-slide
    multi_success = test_multi_slide_cloud_storage()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"   Single Slide: {'✅ PASS' if single_success else '❌ FAIL'}")
    print(f"   Multi-Slide: {'✅ PASS' if multi_success else '❌ FAIL'}")
    
    if single_success and multi_success:
        print("\n🎉 All tests passed! Cloud Storage integration is working!")
        print("📁 Presentations are now stored in Cloud Storage instead of local files")
    else:
        print("\n❌ Some tests failed!")

if __name__ == "__main__":
    main()
