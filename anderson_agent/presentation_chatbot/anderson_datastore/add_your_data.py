"""
Example: How to update the database with your own data
"""

from firestore_operations import FirestoreManager
from schema import ImageData

def add_your_customer_and_project():
    """Example of adding your own customer and project data."""
    
    # Initialize the database manager
    db_manager = FirestoreManager(project_id="agent-space-465923")
    
    # Your customer data
    customer_name = "Your Company Name"
    customer_logo_url = "gs://your-bucket/logos/your-logo.png"
    
    # Your project images
    your_images = [
        ImageData(
            image_url="gs://your-bucket/projects/your-image1.png",
            description="Description of your first image"
        ),
        ImageData(
            image_url="gs://your-bucket/projects/your-image2.jpg",
            description="Description of your second image"
        )
    ]
    
    # Create your project
    project_id = db_manager.create_project(
        customer_name=customer_name,
        customer_logo_url=customer_logo_url,
        project_title="Your Project Title",
        project_overview="""Detailed description of your project.
        
        This is where you can put a comprehensive overview of what your project does,
        its objectives, and expected outcomes. You can write as much as needed here."""
        images=your_images
    )
    
    print(f"✅ Created your project with ID: {project_id}")
    return project_id

def update_existing_project():
    """Example of updating an existing project."""
    
    db_manager = FirestoreManager(project_id="agent-space-465923")
    
    # Get an existing project (example: first Walmart project)
    walmart_projects = db_manager.get_projects_by_customer_name("Walmart Inc.")
    if walmart_projects:
        project = walmart_projects[0]
        
        # Add new images to the project
        new_images = [
            ImageData(
                image_url="gs://your-bucket/projects/new-image.png",
                description="New image added to existing project"
            )
        ]
        
        # Update the project
        success = db_manager.update_project(
            project_id=project.project_id,
            images=project.images + new_images  # Add to existing images
        )
        
        if success:
            print("✅ Project updated successfully!")
        else:
            print("❌ Failed to update project")

if __name__ == "__main__":
    # Add your data
    add_your_customer_and_project()
    
    # Update existing data
    update_existing_project()
