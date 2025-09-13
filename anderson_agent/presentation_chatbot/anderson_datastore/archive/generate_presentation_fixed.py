#!/usr/bin/env python3
"""
Generate PowerPoint presentation from Firestore projects using cloud function
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_operations import FirestoreManager
import requests
import json
from datetime import datetime
from google.cloud import storage

# Configuration
CLOUD_FUNCTION_URL = "https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator"
OUTPUT_BUCKET = "agent-space-465923-presentations"
PROJECT_ID = "agent-space-465923"

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

def call_cloud_function(project_data):
    """Call the cloud function to generate a slide for a project"""
    
    try:
        print(f"🔄 Calling cloud function for: {project_data['title'][:50]}...")
        
        # Make the request
        response = requests.post(
            CLOUD_FUNCTION_URL + "/generate",
            json=project_data,
            headers={'Content-Type': 'application/json'},
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            # The response contains binary PowerPoint data
            pptx_data = response.content
            print(f"✅ Successfully generated slide ({len(pptx_data)} bytes)")
            return pptx_data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout calling cloud function")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def save_pptx_to_gcs(pptx_data, filename):
    """Save PowerPoint file to Google Cloud Storage"""
    
    try:
        # Initialize GCS client
        client = storage.Client(project=PROJECT_ID)
        bucket = client.bucket(OUTPUT_BUCKET)
        
        # Create blob
        blob = bucket.blob(filename)
        
        # Upload the binary data
        blob.upload_from_string(
            pptx_data,
            content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        
        print(f"✅ PowerPoint saved to gs://{OUTPUT_BUCKET}/{filename}")
        return f"gs://{OUTPUT_BUCKET}/{filename}"
        
    except Exception as e:
        print(f"❌ Error saving PowerPoint to GCS: {e}")
        return None

def save_pptx_locally(pptx_data, filename):
    """Save PowerPoint file locally"""
    
    try:
        with open(filename, 'wb') as f:
            f.write(pptx_data)
        
        print(f"✅ PowerPoint saved locally: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Error saving PowerPoint locally: {e}")
        return None

def generate_test_presentation():
    """Generate presentation with 2-3 test projects"""
    
    print('🧪 GENERATING TEST PRESENTATION (2-3 projects)')
    print('=' * 60)
    
    # Initialize Firestore manager
    db_manager = FirestoreManager(project_id=PROJECT_ID)
    
    # Get all projects
    all_projects = db_manager.list_projects()
    print(f'📊 Found {len(all_projects)} projects in database')
    
    if len(all_projects) < 2:
        print('❌ Not enough projects for testing')
        return
    
    # Select first 3 projects for testing
    test_projects = all_projects[:3]
    print(f'🎯 Testing with {len(test_projects)} projects')
    
    # Generate slides for each project
    generated_slides = []
    failed_projects = []
    
    for i, project in enumerate(test_projects, 1):
        print(f'\n📝 Processing project {i}/{len(test_projects)}')
        print(f'   Title: {project.project_title[:60]}...')
        print(f'   Customer: {project.customer_name}')
        print(f'   EQI: {project.eqi}')
        print(f'   Images: {len(project.images)}')
        
        # Convert to cloud function format
        project_data = convert_firestore_to_cloud_function_format(project)
        
        # Call cloud function
        pptx_data = call_cloud_function(project_data)
        
        if pptx_data:
            # Save individual PowerPoint file
            safe_title = "".join(c for c in project.project_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # Limit length
            filename = f"test_slide_{i}_{safe_title.replace(' ', '_')}.pptx"
            
            # Save locally
            local_path = save_pptx_locally(pptx_data, filename)
            
            # Save to GCS
            gcs_path = save_pptx_to_gcs(pptx_data, filename)
            
            generated_slides.append({
                "project_id": project.project_id,
                "project_title": project.project_title,
                "customer_name": project.customer_name,
                "local_file": local_path,
                "gcs_file": gcs_path,
                "file_size": len(pptx_data)
            })
        else:
            failed_projects.append(project.project_title)
    
    # Create summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_projects": len(test_projects),
            "successful_slides": len(generated_slides),
            "failed_projects": failed_projects,
            "test_mode": True
        },
        "slides": generated_slides
    }
    
    # Save summary to JSON
    summary_filename = f"test_presentation_summary_{timestamp}.json"
    with open(summary_filename, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f'\n🎉 Test presentation generated successfully!')
    print(f'📁 Summary saved to: {summary_filename}')
    print(f'📊 Generated {len(generated_slides)} PowerPoint slides')
    print(f'📂 Individual slides saved locally and to GCS')
    if failed_projects:
        print(f'⚠️  Failed projects: {len(failed_projects)}')
        for failed in failed_projects:
            print(f'   - {failed}')

def generate_full_presentation():
    """Generate presentation with all projects"""
    
    print('🚀 GENERATING FULL PRESENTATION (All projects)')
    print('=' * 60)
    
    # Initialize Firestore manager
    db_manager = FirestoreManager(project_id=PROJECT_ID)
    
    # Get all projects
    all_projects = db_manager.list_projects()
    print(f'📊 Found {len(all_projects)} projects in database')
    
    if len(all_projects) == 0:
        print('❌ No projects found in database')
        return
    
    # Generate slides for each project
    generated_slides = []
    failed_projects = []
    
    for i, project in enumerate(all_projects, 1):
        print(f'\n📝 Processing project {i}/{len(all_projects)}')
        print(f'   Title: {project.project_title[:60]}...')
        print(f'   Customer: {project.customer_name}')
        print(f'   EQI: {project.eqi}')
        print(f'   Images: {len(project.images)}')
        
        # Convert to cloud function format
        project_data = convert_firestore_to_cloud_function_format(project)
        
        # Call cloud function
        pptx_data = call_cloud_function(project_data)
        
        if pptx_data:
            # Save individual PowerPoint file
            safe_title = "".join(c for c in project.project_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title[:50]  # Limit length
            filename = f"slide_{i:02d}_{safe_title.replace(' ', '_')}.pptx"
            
            # Save locally
            local_path = save_pptx_locally(pptx_data, filename)
            
            # Save to GCS
            gcs_path = save_pptx_to_gcs(pptx_data, filename)
            
            generated_slides.append({
                "project_id": project.project_id,
                "project_title": project.project_title,
                "customer_name": project.customer_name,
                "local_file": local_path,
                "gcs_file": gcs_path,
                "file_size": len(pptx_data)
            })
        else:
            failed_projects.append(project.project_title)
    
    # Create summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_projects": len(all_projects),
            "successful_slides": len(generated_slides),
            "failed_projects": failed_projects,
            "test_mode": False
        },
        "slides": generated_slides
    }
    
    # Save summary to JSON
    summary_filename = f"full_presentation_summary_{timestamp}.json"
    with open(summary_filename, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f'\n🎉 Full presentation generated successfully!')
    print(f'📁 Summary saved to: {summary_filename}')
    print(f'📊 Generated {len(generated_slides)} PowerPoint slides')
    print(f'📂 Individual slides saved locally and to GCS')
    if failed_projects:
        print(f'⚠️  Failed projects: {len(failed_projects)}')
        for failed in failed_projects:
            print(f'   - {failed}')

def main():
    """Main function"""
    
    print('🎯 PRESENTATION GENERATOR')
    print('=' * 40)
    print(f'Cloud Function: {CLOUD_FUNCTION_URL}')
    print(f'Output Bucket: gs://{OUTPUT_BUCKET}')
    print(f'Project ID: {PROJECT_ID}')
    print()
    
    # Ask user what to do
    choice = input('Choose an option:\n1. Test with 2-3 projects\n2. Generate full presentation\n3. Exit\nEnter choice (1-3): ')
    
    if choice == '1':
        generate_test_presentation()
    elif choice == '2':
        generate_full_presentation()
    elif choice == '3':
        print('👋 Goodbye!')
    else:
        print('❌ Invalid choice')

if __name__ == "__main__":
    main()
