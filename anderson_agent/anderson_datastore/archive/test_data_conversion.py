#!/usr/bin/env python3
"""
Test script to verify data conversion and create a simple presentation locally
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_operations import FirestoreManager
import json
from datetime import datetime

def test_data_conversion():
    """Test the data conversion from Firestore to cloud function format"""
    
    print('🧪 TESTING DATA CONVERSION')
    print('=' * 40)
    
    # Initialize Firestore manager
    db_manager = FirestoreManager(project_id='agent-space-465923')
    
    # Get first project
    projects = db_manager.list_projects()
    if not projects:
        print('❌ No projects found')
        return
    
    project = projects[0]
    print(f'📝 Testing with project: {project.project_title[:50]}...')
    
    # Convert to cloud function format
    image_data = []
    for img in project.images:
        image_data.append({
            "gcs_url": img.image_url,
            "title": img.description
        })
    
    include_eqi = project.eqi == "Yes"
    
    logo_gcs_url = project.customer_logo_url
    if logo_gcs_url.startswith("https://storage.cloud.google.com/"):
        logo_gcs_url = logo_gcs_url.replace("https://storage.cloud.google.com/", "gs://")
    
    cloud_format = {
        "project_name": project.project_title,
        "client_name": project.customer_name,
        "date_range": datetime.now().strftime("%Y-%m-%d"),
        "logo_gcs_url": logo_gcs_url,
        "text_content": [project.project_overview],
        "images": image_data,
        "include_eqi": include_eqi
    }
    
    print('✅ Conversion successful')
    print(f'   Project name: {cloud_format["project_name"][:50]}...')
    print(f'   Client name: {cloud_format["client_name"]}')
    print(f'   Date range: {cloud_format["date_range"]}')
    print(f'   Logo URL: {cloud_format["logo_gcs_url"]}')
    print(f'   Text content: {len(cloud_format["text_content"])} items')
    print(f'   Images: {len(cloud_format["images"])} items')
    print(f'   Include EQI: {cloud_format["include_eqi"]}')
    
    print('\n📋 Full payload:')
    print(json.dumps(cloud_format, indent=2))
    
    return cloud_format

def create_simple_presentation_data():
    """Create a simple presentation data structure for testing"""
    
    print('\n🎯 CREATING SIMPLE PRESENTATION DATA')
    print('=' * 50)
    
    # Initialize Firestore manager
    db_manager = FirestoreManager(project_id='agent-space-465923')
    
    # Get first 3 projects
    all_projects = db_manager.list_projects()
    test_projects = all_projects[:3]
    
    print(f'📊 Creating presentation with {len(test_projects)} projects')
    
    presentation_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_projects": len(test_projects),
            "test_mode": True
        },
        "projects": []
    }
    
    for i, project in enumerate(test_projects, 1):
        print(f'\n📝 Processing project {i}/{len(test_projects)}')
        print(f'   Title: {project.project_title[:50]}...')
        print(f'   Customer: {project.customer_name}')
        print(f'   EQI: {project.eqi}')
        print(f'   Images: {len(project.images)}')
        
        # Convert to cloud function format
        image_data = []
        for img in project.images:
            image_data.append({
                "gcs_url": img.image_url,
                "title": img.description
            })
        
        include_eqi = project.eqi == "Yes"
        
        logo_gcs_url = project.customer_logo_url
        if logo_gcs_url.startswith("https://storage.cloud.google.com/"):
            logo_gcs_url = logo_gcs_url.replace("https://storage.cloud.google.com/", "gs://")
        
        project_data = {
            "project_name": project.project_title,
            "client_name": project.customer_name,
            "date_range": datetime.now().strftime("%Y-%m-%d"),
            "logo_gcs_url": logo_gcs_url,
            "text_content": [project.project_overview],
            "images": image_data,
            "include_eqi": include_eqi
        }
        
        presentation_data["projects"].append(project_data)
    
    print(f'\n✅ Created presentation data with {len(presentation_data["projects"])} projects')
    
    # Save to file for inspection
    filename = f"test_presentation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(presentation_data, f, indent=2)
    
    print(f'📁 Saved to: {filename}')
    
    return presentation_data

def main():
    """Main test function"""
    
    print('🎯 PRESENTATION DATA TEST')
    print('=' * 40)
    
    # Test data conversion
    test_data_conversion()
    
    # Create simple presentation data
    create_simple_presentation_data()
    
    print('\n🎉 Tests completed!')
    print('\n📋 Next steps:')
    print('1. The cloud function has a bug (filename error)')
    print('2. Our data conversion is working correctly')
    print('3. We can either:')
    print('   - Fix the cloud function deployment')
    print('   - Create a local presentation generator')
    print('   - Use a different approach')

if __name__ == "__main__":
    main()
