"""
Database Setup and Sample Data Population Script
Creates the Firestore database and populates it with sample data.
"""

import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_operations import FirestoreManager
from test_data import SAMPLE_PROJECTS, SAMPLE_CUSTOMERS, TEST_SCENARIOS
from schema import ImageData

# Set project ID
PROJECT_ID = "agent-space-465923"


def create_database_and_sample_data():
    """Create the database and populate it with sample data."""
    
    print("🚀 Setting up Anderson Firestore Database...")
    print(f"Project ID: {PROJECT_ID}")
    print()
    
    # Initialize Firestore manager
    try:
        db_manager = FirestoreManager(project_id=PROJECT_ID)
        print("✅ Firestore connection established")
    except Exception as e:
        print(f"❌ Failed to connect to Firestore: {e}")
        return False
    
    print("\n📊 Creating sample customers and projects...")
    
    # Track created items
    created_customers = []
    created_projects = []
    
    try:
        # Create sample projects (this will also create customers automatically)
        for i, project_data in enumerate(SAMPLE_PROJECTS, 1):
            print(f"Creating project {i}/{len(SAMPLE_PROJECTS)}: {project_data['project_title']}")
            
            project_id = db_manager.create_project(
                customer_name=project_data["customer_name"],
                customer_logo_url=project_data["customer_logo_url"],
                project_title=project_data["project_title"],
                project_overview=project_data["project_overview"],
                images=project_data["images"]
            )
            
            created_projects.append({
                "project_id": project_id,
                "title": project_data["project_title"],
                "customer": project_data["customer_name"]
            })
            
            print(f"  ✅ Created project: {project_data['project_title']}")
            print(f"  📁 Project ID: {project_id}")
            print(f"  🖼️  Images: {len(project_data['images'])}")
            print()
        
        print("🎉 Sample data creation completed!")
        print(f"📈 Summary:")
        print(f"  - Projects created: {len(created_projects)}")
        
        # Get unique customers
        unique_customers = list(set([p["customer"] for p in created_projects]))
        print(f"  - Unique customers: {len(unique_customers)}")
        
        # Show customer-project relationships
        print(f"\n🔗 Customer-Project Relationships:")
        for customer in unique_customers:
            customer_projects = [p for p in created_projects if p["customer"] == customer]
            print(f"  📋 {customer}: {len(customer_projects)} projects")
            for project in customer_projects:
                print(f"    - {project['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False


def create_additional_test_scenarios():
    """Create additional test scenarios for edge cases."""
    
    print("\n🧪 Creating additional test scenarios...")
    
    try:
        db_manager = FirestoreManager(project_id=PROJECT_ID)
        
        for scenario_name, scenario_data in TEST_SCENARIOS.items():
            print(f"Creating {scenario_name}...")
            
            project_id = db_manager.create_project(
                customer_name=scenario_data["customer_name"],
                customer_logo_url=scenario_data["customer_logo_url"],
                project_title=scenario_data["project_title"],
                project_overview=scenario_data["project_overview"],
                images=scenario_data["images"]
            )
            
            print(f"  ✅ Created {scenario_name} (ID: {project_id})")
        
        print("✅ Additional test scenarios created!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test scenarios: {e}")
        return False


def verify_database_setup():
    """Verify the database setup by querying the data."""
    
    print("\n🔍 Verifying database setup...")
    
    try:
        db_manager = FirestoreManager(project_id=PROJECT_ID)
        
        # Get all customers
        customers = db_manager.list_customers()
        print(f"📊 Total customers in database: {len(customers)}")
        
        # Get all projects
        projects = db_manager.list_projects()
        print(f"📊 Total projects in database: {len(projects)}")
        
        # Show detailed breakdown
        print(f"\n📋 Detailed breakdown:")
        for customer in customers:
            customer_projects = db_manager.get_projects_by_customer(customer.customer_id)
            print(f"  🏢 {customer.customer_name}")
            print(f"    - Customer ID: {customer.customer_id}")
            print(f"    - Logo: {customer.customer_logo_url}")
            print(f"    - Projects: {len(customer_projects)}")
            
            for project in customer_projects:
                print(f"      📁 {project.project_title}")
                print(f"        - Project ID: {project.project_id}")
                print(f"        - Images: {len(project.images)}")
                for img in project.images:
                    print(f"          🖼️  {img.description}")
            print()
        
        print("✅ Database verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False


def create_multiple_projects_example():
    """Create multiple projects for the same customer to demonstrate the relationship."""
    
    print("\n🔗 Creating multiple projects for Walmart to demonstrate customer-project relationship...")
    
    try:
        db_manager = FirestoreManager(project_id=PROJECT_ID)
        
        # Additional Walmart projects
        additional_walmart_projects = [
            {
                "project_title": "Walmart Supply Chain Optimization",
                "project_overview": "Advanced supply chain management system using AI and machine learning to optimize inventory flow, reduce costs, and improve delivery times across Walmart's global network.",
                "images": [
                    ImageData(
                        image_url="gs://anderson-agent-storage/projects/walmart-supply-chain-dashboard.png",
                        description="Supply chain optimization dashboard showing real-time inventory levels"
                    ),
                    ImageData(
                        image_url="gs://anderson-agent-storage/projects/walmart-logistics-network.jpg",
                        description="Global logistics network visualization with optimized routes"
                    )
                ]
            },
            {
                "project_title": "Walmart Customer Analytics Platform",
                "project_overview": "Comprehensive customer analytics platform that analyzes shopping patterns, preferences, and behavior to provide personalized recommendations and improve customer experience.",
                "images": [
                    ImageData(
                        image_url="gs://anderson-agent-storage/projects/walmart-customer-analytics.png",
                        description="Customer analytics dashboard with shopping pattern insights"
                    ),
                    ImageData(
                        image_url="gs://anderson-agent-storage/projects/walmart-personalization-engine.jpg",
                        description="AI-powered personalization engine interface"
                    )
                ]
            }
        ]
        
        for project_data in additional_walmart_projects:
            project_id = db_manager.create_project(
                customer_name="Walmart Inc.",
                customer_logo_url="gs://anderson-agent-storage/logos/walmart-logo.png",
                project_title=project_data["project_title"],
                project_overview=project_data["project_overview"],
                images=project_data["images"]
            )
            
            print(f"  ✅ Created: {project_data['project_title']} (ID: {project_id})")
        
        # Show Walmart's total projects
        walmart_projects = db_manager.get_projects_by_customer_name("Walmart Inc.")
        print(f"\n📊 Walmart now has {len(walmart_projects)} total projects:")
        for project in walmart_projects:
            print(f"  - {project.project_title}")
        
        print("✅ Multiple projects example completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating multiple projects example: {e}")
        return False


def main():
    """Main function to set up the database and populate with sample data."""
    
    print("=" * 60)
    print("🏗️  ANDERSON FIRESTORE DATABASE SETUP")
    print("=" * 60)
    
    # Step 1: Create database and sample data
    if not create_database_and_sample_data():
        print("❌ Failed to create database and sample data")
        return
    
    # Step 2: Create additional test scenarios
    if not create_additional_test_scenarios():
        print("❌ Failed to create additional test scenarios")
        return
    
    # Step 3: Create multiple projects example
    if not create_multiple_projects_example():
        print("❌ Failed to create multiple projects example")
        return
    
    # Step 4: Verify everything
    if not verify_database_setup():
        print("❌ Database verification failed")
        return
    
    print("\n" + "=" * 60)
    print("🎉 DATABASE SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📋 What was created:")
    print("  ✅ Firestore collections: 'customers' and 'projects'")
    print("  ✅ 5 sample customers with detailed information")
    print("  ✅ 7+ sample projects with multiple images each")
    print("  ✅ Customer-project relationships established")
    print("  ✅ Multiple projects per customer demonstrated")
    print("  ✅ Edge case test scenarios")
    print("\n🚀 Your Anderson Firestore Database is ready to use!")
    print("\nNext steps:")
    print("  - Run 'python example_usage.py' to see usage examples")
    print("  - Check your Firestore console to see the data")
    print("  - Use the FirestoreManager class in your applications")


if __name__ == "__main__":
    main()
