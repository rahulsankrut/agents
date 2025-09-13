#!/usr/bin/env python3
"""
Simple test to generate PowerPoint files from Firestore projects
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_operations import FirestoreManager
import requests
import json
from datetime import datetime

def test_pptx_generation():
    """Test generating PowerPoint files"""
    
    print('🧪 TESTING POWERPOINT GENERATION')
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
    
    payload = {
        "title": project.project_title,
        "logo_gcs_url": logo_gcs_url,
        "text_content": [project.project_overview],
        "image_data": image_data,
        "include_eqi": include_eqi
    }
    
    print(f'🔄 Calling cloud function...')
    
    # Call cloud function
    response = requests.post(
        "https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator/generate",
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=300
    )
    
    if response.status_code == 200:
        pptx_data = response.content
        print(f'✅ Successfully generated PowerPoint ({len(pptx_data)} bytes)')
        
        # Save locally
        safe_title = "".join(c for c in project.project_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:50]
        filename = f"test_{safe_title.replace(' ', '_')}.pptx"
        
        with open(filename, 'wb') as f:
            f.write(pptx_data)
        
        print(f'📁 Saved PowerPoint file: {filename}')
        print(f'📊 File size: {len(pptx_data)} bytes')
        
        return filename
    else:
        print(f'❌ Error: {response.status_code} - {response.text}')
        return None

if __name__ == "__main__":
    test_pptx_generation()
