#!/usr/bin/env python3
"""
Quick verification script to check if logos and EQI are being processed
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

def verify_logos_and_eqi():
    """Verify that logos and EQI are being processed correctly"""
    
    print("🔍 Verifying Logos and EQI Processing")
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
        print(f"🏢 Customer: {project.customer_name}")
        print(f"🎨 Logo URL: {project.customer_logo_url}")
        print(f"📈 EQI: {project.eqi}")
        print(f"🖼️  Images: {len(project.images)}")
        
        # Convert to cloud function format
        project_data = convert_firestore_to_cloud_function_format(project)
        
        print(f"\n📋 Converted Data:")
        print(f"   Title: {project_data['title'][:50]}...")
        print(f"   Logo GCS URL: {project_data['logo_gcs_url']}")
        print(f"   Include EQI: {project_data['include_eqi']}")
        print(f"   Image Count: {len(project_data['image_data'])}")
        
        # Test with single project
        payload = {
            "projects": [project_data]
        }
        
        print(f"\n🔄 Testing single project with logo and EQI...")
        
        response = requests.post(
            CLOUD_FUNCTION_URL + "/generate_multi",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300
        )
        
        if response.status_code == 200:
            pptx_data = response.content
            print(f"✅ Successfully generated presentation ({len(pptx_data)} bytes)")
            
            # Save the presentation
            filename = "verification_single_project.pptx"
            with open(filename, 'wb') as f:
                f.write(pptx_data)
            print(f"💾 Saved as: {filename}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    
    print("🧪 Logo and EQI Verification Test")
    print("=" * 50)
    
    success = verify_logos_and_eqi()
    
    if success:
        print("\n🎉 Verification completed successfully!")
        print("📊 Check the generated presentation to verify:")
        print("   ✅ Customer logos are displayed")
        print("   ✅ EQI sub-header is shown when include_eqi=True")
        print("   ✅ Project images are included")
        print("   ✅ Professional formatting is maintained")
    else:
        print("\n❌ Verification failed!")

if __name__ == "__main__":
    main()
