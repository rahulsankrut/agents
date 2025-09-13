#!/usr/bin/env python3
"""
Test script for the updated cloud function with multi-slide presentation capability
"""

import requests
import json
import sys
import os

# Add the anderson_datastore to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'anderson_datastore'))

from firestore_operations import FirestoreManager
from schema import Project

# Cloud function configuration
CLOUD_FUNCTION_URL = "https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator"
OUTPUT_BUCKET = "gs://agent-space-465923-presentations"

def get_projects_from_firestore():
    """Get all projects from Firestore"""
    try:
        manager = FirestoreManager()
        projects = manager.list_projects()
        print(f"✅ Retrieved {len(projects)} projects from Firestore")
        return projects
    except Exception as e:
        print(f"❌ Error retrieving projects from Firestore: {e}")
        return []

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

def test_multi_slide_endpoint():
    """Test the new multi-slide endpoint with a few projects"""
    
    print("🔄 Testing multi-slide presentation generation...")
    
    # Get projects from Firestore
    projects = get_projects_from_firestore()
    if not projects:
        print("❌ No projects found in Firestore")
        return False
    
    # Test with first 3 projects
    test_projects = projects[:3]
    print(f"📊 Testing with {len(test_projects)} projects:")
    for i, project in enumerate(test_projects, 1):
        print(f"   {i}. {project.project_title[:50]}...")
    
    # Convert projects to cloud function format
    projects_data = []
    for project in test_projects:
        project_data = convert_firestore_to_cloud_function_format(project)
        projects_data.append(project_data)
    
    # Prepare the request payload
    payload = {
        "projects": projects_data
    }
    
    try:
        print(f"🔄 Calling cloud function multi-slide endpoint...")
        
        # Make the request
        response = requests.post(
            CLOUD_FUNCTION_URL + "/generate_multi",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            # The response contains binary PowerPoint data
            pptx_data = response.content
            print(f"✅ Successfully generated multi-slide presentation ({len(pptx_data)} bytes)")
            
            # Save the presentation locally
            filename = f"test_multi_slide_presentation.pptx"
            with open(filename, 'wb') as f:
                f.write(pptx_data)
            print(f"💾 Saved presentation as: {filename}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout calling cloud function")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_all_projects_multi_slide():
    """Test the multi-slide endpoint with all projects"""
    
    print("🔄 Testing multi-slide presentation generation with ALL projects...")
    
    # Get all projects from Firestore
    projects = get_projects_from_firestore()
    if not projects:
        print("❌ No projects found in Firestore")
        return False
    
    print(f"📊 Testing with ALL {len(projects)} projects")
    
    # Convert projects to cloud function format
    projects_data = []
    for project in projects:
        project_data = convert_firestore_to_cloud_function_format(project)
        projects_data.append(project_data)
    
    # Prepare the request payload
    payload = {
        "projects": projects_data
    }
    
    try:
        print(f"🔄 Calling cloud function multi-slide endpoint...")
        
        # Make the request
        response = requests.post(
            CLOUD_FUNCTION_URL + "/generate_multi",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=600  # 10 minute timeout for all projects
        )
        
        if response.status_code == 200:
            # The response contains binary PowerPoint data
            pptx_data = response.content
            print(f"✅ Successfully generated multi-slide presentation ({len(pptx_data)} bytes)")
            
            # Save the presentation locally
            filename = f"full_multi_slide_presentation.pptx"
            with open(filename, 'wb') as f:
                f.write(pptx_data)
            print(f"💾 Saved presentation as: {filename}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout calling cloud function")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_cloud_function_status():
    """Check if the cloud function is running and show available endpoints"""
    
    try:
        print("🔄 Checking cloud function status...")
        
        response = requests.get(CLOUD_FUNCTION_URL, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Cloud function is running!")
            print(f"📋 Available endpoints:")
            for endpoint, method in data.get('endpoints', {}).items():
                print(f"   {method} {endpoint}")
            return True
        else:
            print(f"❌ Cloud function returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking cloud function status: {e}")
        return False

def main():
    """Main function to run tests"""
    
    print("🚀 Testing Updated Cloud Function - Multi-Slide Presentation")
    print("=" * 60)
    
    # Check cloud function status
    if not check_cloud_function_status():
        print("❌ Cloud function is not accessible. Please check deployment.")
        return
    
    print("\n" + "=" * 60)
    
    # Test with a few projects first
    print("🧪 Test 1: Multi-slide presentation with 3 projects")
    if test_multi_slide_endpoint():
        print("✅ Test 1 passed!")
    else:
        print("❌ Test 1 failed!")
        return
    
    print("\n" + "=" * 60)
    
    # Ask user if they want to test with all projects
    print("🧪 Test 2: Multi-slide presentation with ALL projects")
    user_input = input("Do you want to test with all projects? This may take longer (y/n): ").strip().lower()
    
    if user_input in ['y', 'yes', '1', 'true']:
        if test_all_projects_multi_slide():
            print("✅ Test 2 passed!")
        else:
            print("❌ Test 2 failed!")
    else:
        print("⏭️  Skipping Test 2")
    
    print("\n" + "=" * 60)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    main()
