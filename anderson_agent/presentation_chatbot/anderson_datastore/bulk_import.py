"""
Bulk data import script for adding multiple customers and projects
"""

from firestore_operations import FirestoreManager
from schema import ImageData
import uuid
from datetime import datetime

def bulk_import_your_data():
    """Import multiple customers and projects at once."""
    
    db_manager = FirestoreManager(project_id="agent-space-465923")
    
    # Your data - modify this with your actual data
    your_data = [
        {
            "customer_name": "Your Company 1",
            "customer_logo_url": "gs://your-bucket/logos/company1-logo.png",
            "projects": [
                {
                    "project_title": "Project 1 Title",
                    "project_overview": "Detailed description of project 1...",
                    "images": [
                        ImageData("gs://your-bucket/projects/project1-image1.png", "First image description"),
                        ImageData("gs://your-bucket/projects/project1-image2.jpg", "Second image description")
                    ]
                },
                {
                    "project_title": "Project 2 Title", 
                    "project_overview": "Detailed description of project 2...",
                    "images": [
                        ImageData("gs://your-bucket/projects/project2-image1.png", "Project 2 image description")
                    ]
                }
            ]
        },
        {
            "customer_name": "Your Company 2",
            "customer_logo_url": "gs://your-bucket/logos/company2-logo.png",
            "projects": [
                {
                    "project_title": "Another Project",
                    "project_overview": "Description of another project...",
                    "images": [
                        ImageData("gs://your-bucket/projects/another-image.png", "Another image description")
                    ]
                }
            ]
        }
    ]
    
    print("🚀 Starting bulk import...")
    
    for customer_data in your_data:
        print(f"\n📋 Processing customer: {customer_data['customer_name']}")
        
        for project_data in customer_data["projects"]:
            try:
                project_id = db_manager.create_project(
                    customer_name=customer_data["customer_name"],
                    customer_logo_url=customer_data["customer_logo_url"],
                    project_title=project_data["project_title"],
                    project_overview=project_data["project_overview"],
                    images=project_data["images"]
                )
                print(f"  ✅ Created project: {project_data['project_title']}")
                
            except Exception as e:
                print(f"  ❌ Failed to create project: {project_data['project_title']} - {e}")
    
    print("\n🎉 Bulk import completed!")

if __name__ == "__main__":
    bulk_import_your_data()
