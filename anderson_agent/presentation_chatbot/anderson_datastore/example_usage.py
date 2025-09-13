"""
Example usage of the Anderson Firestore Database
Demonstrates how to use the FirestoreManager for customer and project operations.
"""

from firestore_operations import FirestoreManager
from schema import ImageData
import os


def main():
    """Example usage of the Firestore database operations."""
    
    # Initialize Firestore manager
    # You can specify your GCP project ID here or set GOOGLE_CLOUD_PROJECT environment variable
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'agent-space-465923')
    db_manager = FirestoreManager(project_id=project_id, database_id="anderson-db")
    
    print("=== Anderson Firestore Database Example ===\n")
    
    # Example 1: Create a customer
    print("1. Creating a customer...")
    customer_id = db_manager.create_customer(
        customer_name="Walmart Inc.",
        customer_logo_url="gs://your-bucket/logos/walmart-logo.png"
    )
    print(f"Created customer with ID: {customer_id}\n")
    
    # Example 2: Create a project with images
    print("2. Creating a project with images...")
    
    # Define images for the project
    project_images = [
        ImageData(
            image_url="gs://your-bucket/projects/walmart-store-layout.png",
            description="Store layout optimization showing improved customer flow"
        ),
        ImageData(
            image_url="gs://your-bucket/projects/walmart-inventory-system.jpg",
            description="New inventory management system dashboard"
        ),
        ImageData(
            image_url="gs://your-bucket/projects/walmart-checkout-process.png",
            description="Streamlined checkout process with reduced wait times"
        )
    ]
    
    project_id = db_manager.create_project(
        customer_name="Walmart Inc.",
        customer_logo_url="gs://your-bucket/logos/walmart-logo.png",
        project_title="Walmart Store Optimization Initiative",
        project_overview="""This comprehensive project focuses on optimizing Walmart store operations 
        through advanced analytics and process improvements. The initiative includes:
        
        1. Store Layout Optimization: Redesigning store layouts to improve customer flow and increase sales
        2. Inventory Management: Implementing AI-powered inventory tracking and restocking systems
        3. Checkout Process Enhancement: Reducing wait times through better queue management and self-checkout integration
        4. Employee Training: Comprehensive training programs for staff on new systems and processes
        
        Expected outcomes include a 15% increase in customer satisfaction, 20% reduction in checkout wait times,
        and 10% improvement in inventory turnover rates.""",
        images=project_images
    )
    print(f"Created project with ID: {project_id}\n")
    
    # Example 3: Retrieve customer information
    print("3. Retrieving customer information...")
    customer = db_manager.get_customer(customer_id)
    if customer:
        print(f"Customer Name: {customer.customer_name}")
        print(f"Customer Logo: {customer.customer_logo_url}")
        print(f"Number of Projects: {len(customer.projects)}")
        print(f"Created: {customer.created_at}")
        print()
    
    # Example 4: Retrieve project information
    print("4. Retrieving project information...")
    project = db_manager.get_project(project_id)
    if project:
        print(f"Project Title: {project.project_title}")
        print(f"Customer: {project.customer_name}")
        print(f"Number of Images: {len(project.images)}")
        print("Images:")
        for i, img in enumerate(project.images, 1):
            print(f"  {i}. {img.description}")
            print(f"     URL: {img.image_url}")
        print()
    
    # Example 5: List all customers
    print("5. Listing all customers...")
    customers = db_manager.list_customers()
    for customer in customers:
        print(f"- {customer.customer_name} (ID: {customer.customer_id})")
    print()
    
    # Example 6: List all projects
    print("6. Listing all projects...")
    projects = db_manager.list_projects()
    for project in projects:
        print(f"- {project.project_title} (Customer: {project.customer_name})")
    print()
    
    # Example 7: Update project
    print("7. Updating project...")
    updated_images = project_images + [
        ImageData(
            image_url="gs://your-bucket/projects/walmart-results-dashboard.png",
            description="Final results dashboard showing 18% improvement in customer satisfaction"
        )
    ]
    
    success = db_manager.update_project(
        project_id=project_id,
        images=updated_images
    )
    if success:
        print("Project updated successfully!")
        updated_project = db_manager.get_project(project_id)
        print(f"Updated project now has {len(updated_project.images)} images")
    print()
    
    # Example 8: Get projects by customer
    print("8. Getting projects by customer...")
    walmart_projects = db_manager.get_projects_by_customer_name("Walmart Inc.")
    print(f"Walmart has {len(walmart_projects)} projects:")
    for proj in walmart_projects:
        print(f"  - {proj.project_title}")
    print()
    
    print("=== Example completed successfully! ===")


def create_sample_data():
    """Create sample data for testing purposes."""
    
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'agent-space-465923')
    db_manager = FirestoreManager(project_id=project_id, database_id="anderson-db")
    
    print("Creating sample data...")
    
    # Sample customers and projects
    sample_data = [
        {
            "customer_name": "Target Corporation",
            "customer_logo_url": "gs://your-bucket/logos/target-logo.png",
            "project_title": "Target Digital Transformation",
            "project_overview": "Comprehensive digital transformation initiative focusing on e-commerce platform enhancement, mobile app optimization, and omnichannel customer experience.",
            "images": [
                ImageData("gs://your-bucket/projects/target-mobile-app.png", "Redesigned mobile app interface"),
                ImageData("gs://your-bucket/projects/target-ecommerce-platform.jpg", "Enhanced e-commerce platform dashboard")
            ]
        },
        {
            "customer_name": "Amazon",
            "customer_logo_url": "gs://your-bucket/logos/amazon-logo.png",
            "project_title": "Amazon Warehouse Automation",
            "project_overview": "Implementation of advanced robotics and AI systems for warehouse operations, including automated picking, sorting, and inventory management.",
            "images": [
                ImageData("gs://your-bucket/projects/amazon-robotics-system.png", "Robotic picking system in action"),
                ImageData("gs://your-bucket/projects/amazon-warehouse-layout.jpg", "Optimized warehouse layout design"),
                ImageData("gs://your-bucket/projects/amazon-inventory-ai.png", "AI-powered inventory management system")
            ]
        },
        {
            "customer_name": "Home Depot",
            "customer_logo_url": "gs://your-bucket/logos/homedepot-logo.png",
            "project_title": "Home Depot Customer Experience Enhancement",
            "project_overview": "Multi-faceted project to improve customer experience through better store navigation, enhanced product discovery, and personalized recommendations.",
            "images": [
                ImageData("gs://your-bucket/projects/homedepot-store-navigation.png", "Interactive store navigation system"),
                ImageData("gs://your-bucket/projects/homedepot-product-recommendations.jpg", "AI-powered product recommendation engine")
            ]
        }
    ]
    
    # Create all sample data
    for data in sample_data:
        try:
            project_id = db_manager.create_project(
                customer_name=data["customer_name"],
                customer_logo_url=data["customer_logo_url"],
                project_title=data["project_title"],
                project_overview=data["project_overview"],
                images=data["images"]
            )
            print(f"Created project: {data['project_title']} (ID: {project_id})")
        except Exception as e:
            print(f"Error creating project {data['project_title']}: {e}")
    
    print("Sample data creation completed!")


if __name__ == "__main__":
    # Run the example
    main()
    
    # Uncomment the line below to create sample data
    # create_sample_data()
