"""
Direct Firestore operations for custom data updates
"""

from google.cloud import firestore
import uuid
from datetime import datetime

def add_data_directly():
    """Add data directly using Firestore client."""
    
    # Connect to your database
    db = firestore.Client(project="agent-space-465923", database="anderson-db")
    
    # Your customer data
    customer_id = str(uuid.uuid4())
    customer_data = {
        "customer_id": customer_id,
        "customer_name": "Your Company Name",
        "customer_logo_url": "gs://your-bucket/logos/your-logo.png",
        "projects": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Your project data
    project_id = str(uuid.uuid4())
    project_data = {
        "project_id": project_id,
        "customer_name": "Your Company Name",
        "customer_logo_url": "gs://your-bucket/logos/your-logo.png",
        "project_title": "Your Project Title",
        "project_overview": "Your detailed project description...",
        "images": [
            {
                "image_url": "gs://your-bucket/projects/image1.png",
                "description": "Description of your image"
            }
        ],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # Add project to customer's project list
    customer_data["projects"].append(project_id)
    
    # Save to Firestore
    db.collection("customers").document(customer_id).set(customer_data)
    db.collection("projects").document(project_id).set(project_data)
    
    print(f"✅ Added customer: {customer_data['customer_name']}")
    print(f"✅ Added project: {project_data['project_title']}")

if __name__ == "__main__":
    add_data_directly()
