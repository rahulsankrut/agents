#!/usr/bin/env python3
"""
Simple Multi-Slide Presentation Generator
Creates a single PowerPoint presentation with multiple slides from Firestore projects
"""

import requests
import json
import sys
import os
from datetime import datetime

# Add the anderson_datastore to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'anderson_datastore'))

from firestore_operations import FirestoreManager
from schema import Project

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

def generate_multi_slide_presentation(projects=None, output_filename=None):
    """Generate a multi-slide presentation from Firestore projects"""
    
    print("🚀 Multi-Slide Presentation Generator")
    print("=" * 50)
    
    # Get projects from Firestore
    try:
        manager = FirestoreManager()
        if projects is None:
            projects = manager.list_projects()
        
        if not projects:
            print("❌ No projects found in Firestore")
            return False
        
        print(f"📊 Found {len(projects)} projects in Firestore")
        
    except Exception as e:
        print(f"❌ Error retrieving projects from Firestore: {e}")
        return False
    
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
            timeout=600  # 10 minute timeout
        )
        
        if response.status_code == 200:
            # The response now contains JSON with Cloud Storage URL
            response_data = response.json()
            cloud_storage_url = response_data.get('presentation_url')
            filename = response_data.get('filename', 'presentation.pptx')
            
            print(f"✅ Successfully generated multi-slide presentation")
            print(f"🌐 Cloud Storage URL: {cloud_storage_url}")
            
            # Optionally download the file locally
            if output_filename is None:
                output_filename = filename
            
            try:
                # Download from Cloud Storage URL
                download_response = requests.get(cloud_storage_url, timeout=60)
                if download_response.status_code == 200:
                    with open(output_filename, 'wb') as f:
                        f.write(download_response.content)
                    print(f"💾 Downloaded presentation as: {output_filename}")
                else:
                    print(f"⚠️  Could not download file locally, but it's available at: {cloud_storage_url}")
            except Exception as e:
                print(f"⚠️  Could not download file locally: {e}")
                print(f"📁 File is available at: {cloud_storage_url}")
            
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

def generate_by_customer(customer_name):
    """Generate a multi-slide presentation for a specific customer"""
    
    print(f"🏢 Generating presentation for customer: {customer_name}")
    print("=" * 50)
    
    try:
        manager = FirestoreManager()
        projects = manager.get_projects_by_customer_name(customer_name)
        
        if not projects:
            print(f"❌ No projects found for customer: {customer_name}")
            return False
        
        print(f"📊 Found {len(projects)} projects for {customer_name}")
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{customer_name}_presentation_{timestamp}.pptx"
        
        return generate_multi_slide_presentation(projects, output_filename)
        
    except Exception as e:
        print(f"❌ Error retrieving projects for customer {customer_name}: {e}")
        return False

def main():
    """Main function with command line interface"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "all":
            # Generate presentation with all projects
            success = generate_multi_slide_presentation()
            if success:
                print("\n🎉 Multi-slide presentation generated successfully!")
            else:
                print("\n❌ Failed to generate multi-slide presentation")
        
        elif command == "customer":
            # Generate presentation for specific customer
            if len(sys.argv) > 2:
                customer_name = sys.argv[2]
                success = generate_by_customer(customer_name)
                if success:
                    print(f"\n🎉 Multi-slide presentation for {customer_name} generated successfully!")
                else:
                    print(f"\n❌ Failed to generate multi-slide presentation for {customer_name}")
            else:
                print("❌ Please specify customer name: python multi_slide_generator.py customer Walmart")
        
        elif command == "help":
            print("📚 Multi-Slide Presentation Generator Help")
            print("=" * 50)
            print("Usage:")
            print("  python multi_slide_generator.py all                    # Generate with all projects")
            print("  python multi_slide_generator.py customer <name>       # Generate for specific customer")
            print("  python multi_slide_generator.py help                  # Show this help")
            print("")
            print("Examples:")
            print("  python multi_slide_generator.py all")
            print("  python multi_slide_generator.py customer Walmart")
            print("  python multi_slide_generator.py customer Target")
            print("  python multi_slide_generator.py customer \"Sam's Club\"")
        
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python multi_slide_generator.py help' for usage information")
    
    else:
        # Interactive mode
        print("🎯 Multi-Slide Presentation Generator")
        print("=" * 50)
        print("Choose an option:")
        print("1. Generate presentation with ALL projects")
        print("2. Generate presentation for specific customer")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            success = generate_multi_slide_presentation()
            if success:
                print("\n🎉 Multi-slide presentation generated successfully!")
            else:
                print("\n❌ Failed to generate multi-slide presentation")
        
        elif choice == "2":
            customer_name = input("Enter customer name: ").strip()
            if customer_name:
                success = generate_by_customer(customer_name)
                if success:
                    print(f"\n🎉 Multi-slide presentation for {customer_name} generated successfully!")
                else:
                    print(f"\n❌ Failed to generate multi-slide presentation for {customer_name}")
            else:
                print("❌ Customer name cannot be empty")
        
        elif choice == "3":
            print("👋 Goodbye!")
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
