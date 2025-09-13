#!/usr/bin/env python3
"""
Test script for presentation generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_operations import FirestoreManager

def test_database_connection():
    """Test database connection and data"""
    
    print('🧪 TESTING DATABASE CONNECTION')
    print('=' * 40)
    
    try:
        # Initialize Firestore manager
        db_manager = FirestoreManager(project_id='agent-space-465923')
        
        # Get all projects
        projects = db_manager.list_projects()
        
        print(f'✅ Database connection successful')
        print(f'📊 Total projects: {len(projects)}')
        
        if len(projects) > 0:
            print('\n📋 Sample project:')
            sample = projects[0]
            print(f'   Title: {sample.project_title[:60]}...')
            print(f'   Customer: {sample.customer_name}')
            print(f'   EQI: {sample.eqi}')
            print(f'   Images: {len(sample.images)}')
            
            if sample.images:
                print(f'   First image: {sample.images[0].image_url}')
                print(f'   Description: {sample.images[0].description[:50]}...')
        
        return True
        
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        return False

def test_cloud_function_format():
    """Test converting project to cloud function format"""
    
    print('\n🧪 TESTING CLOUD FUNCTION FORMAT CONVERSION')
    print('=' * 50)
    
    try:
        # Initialize Firestore manager
        db_manager = FirestoreManager(project_id='agent-space-465923')
        
        # Get first project
        projects = db_manager.list_projects()
        if not projects:
            print('❌ No projects found')
            return False
        
        project = projects[0]
        print(f'📝 Testing with project: {project.project_title[:50]}...')
        
        # Convert to cloud function format
        from generate_presentation import convert_firestore_to_cloud_function_format
        cloud_format = convert_firestore_to_cloud_function_format(project)
        
        print('✅ Conversion successful')
        print(f'   Title: {cloud_format["title"][:50]}...')
        print(f'   Logo URL: {cloud_format["logo_gcs_url"]}')
        print(f'   Text content: {len(cloud_format["text_content"])} items')
        print(f'   Images: {len(cloud_format["image_data"])} items')
        print(f'   Include EQI: {cloud_format["include_eqi"]}')
        
        return True
        
    except Exception as e:
        print(f'❌ Conversion failed: {e}')
        return False

def main():
    """Main test function"""
    
    print('🎯 PRESENTATION GENERATION TEST')
    print('=' * 40)
    
    # Test database connection
    db_ok = test_database_connection()
    
    if db_ok:
        # Test cloud function format conversion
        format_ok = test_cloud_function_format()
        
        if format_ok:
            print('\n🎉 All tests passed! Ready to generate presentation.')
        else:
            print('\n❌ Format conversion test failed.')
    else:
        print('\n❌ Database connection test failed.')

if __name__ == "__main__":
    main()
