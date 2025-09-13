"""
Simple Database Setup Script
Creates the Firestore database and populates it with sample data using basic Firestore operations.
"""

import os
import sys
import uuid
from datetime import datetime
from google.cloud import firestore

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_data import SAMPLE_PROJECTS, SAMPLE_CUSTOMERS, TEST_SCENARIOS
from schema import ImageData

# Set project ID
PROJECT_ID = "agent-space-465923"


def create_sample_data_simple():
    """Create sample data using basic Firestore operations."""
    
    print("🚀 Setting up Anderson Firestore Database...")
    print(f"Project ID: {PROJECT_ID}")
    print()
    
    # Initialize Firestore client
    try:
        db = firestore.Client(project=PROJECT_ID, database="anderson-db")
        print("✅ Firestore connection established to anderson-db")
    except Exception as e:
        print(f"❌ Failed to connect to Firestore: {e}")
        return False
    
    print("\n📊 Creating sample customers and projects...")
    
    # Track created items
    created_customers = []
    created_projects = []
    
    try:
        # Create sample projects
        for i, project_data in enumerate(SAMPLE_PROJECTS, 1):
            print(f"Creating project {i}/{len(SAMPLE_PROJECTS)}: {project_data['project_title']}")
            
            # Generate unique IDs
            project_id = str(uuid.uuid4())
            customer_id = str(uuid.uuid4())
            
            # Prepare project document
            project_doc = {
                'project_id': project_id,
                'customer_name': project_data["customer_name"],
                'customer_logo_url': project_data["customer_logo_url"],
                'project_title': project_data["project_title"],
                'project_overview': project_data["project_overview"],
                'images': [
                    {
                        'image_url': img.image_url,
                        'description': img.description
                    } for img in project_data["images"]
                ],
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Save project to Firestore
            db.collection('projects').document(project_id).set(project_doc)
            
            # Check if customer already exists
            customer_query = db.collection('customers').where('customer_name', '==', project_data["customer_name"]).limit(1)
            existing_customers = list(customer_query.stream())
            
            if existing_customers:
                # Customer exists, add project to their list
                customer_doc = existing_customers[0]
                customer_data = customer_doc.to_dict()
                customer_data['projects'].append(project_id)
                customer_data['updated_at'] = datetime.now()
                
                db.collection('customers').document(customer_doc.id).set(customer_data)
                customer_id = customer_doc.id
            else:
                # Create new customer
                customer_doc = {
                    'customer_id': customer_id,
                    'customer_name': project_data["customer_name"],
                    'customer_logo_url': project_data["customer_logo_url"],
                    'projects': [project_id],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                
                db.collection('customers').document(customer_id).set(customer_doc)
            
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
        import traceback
        traceback.print_exc()
        return False


def create_additional_walmart_projects():
    """Create additional Walmart projects to demonstrate multiple projects per customer."""
    
    print("\n🔗 Creating additional Walmart projects...")
    
    try:
        db = firestore.Client(project=PROJECT_ID, database="anderson-db")
        
        # Additional Walmart projects
        additional_projects = [
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
        
        for project_data in additional_projects:
            project_id = str(uuid.uuid4())
            
            # Prepare project document
            project_doc = {
                'project_id': project_id,
                'customer_name': "Walmart Inc.",
                'customer_logo_url': "gs://anderson-agent-storage/logos/walmart-logo.png",
                'project_title': project_data["project_title"],
                'project_overview': project_data["project_overview"],
                'images': [
                    {
                        'image_url': img.image_url,
                        'description': img.description
                    } for img in project_data["images"]
                ],
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Save project
            db.collection('projects').document(project_id).set(project_doc)
            
            # Add to Walmart's project list
            walmart_query = db.collection('customers').where('customer_name', '==', 'Walmart Inc.').limit(1)
            walmart_docs = list(walmart_query.stream())
            
            if walmart_docs:
                walmart_doc = walmart_docs[0]
                walmart_data = walmart_doc.to_dict()
                walmart_data['projects'].append(project_id)
                walmart_data['updated_at'] = datetime.now()
                
                db.collection('customers').document(walmart_doc.id).set(walmart_data)
            
            print(f"  ✅ Created: {project_data['project_title']} (ID: {project_id})")
        
        print("✅ Additional Walmart projects created!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating additional projects: {e}")
        return False


def verify_database():
    """Verify the database setup by querying the data."""
    
    print("\n🔍 Verifying database setup...")
    
    try:
        db = firestore.Client(project=PROJECT_ID, database="anderson-db")
        
        # Get all customers
        customers = list(db.collection('customers').stream())
        print(f"📊 Total customers in database: {len(customers)}")
        
        # Get all projects
        projects = list(db.collection('projects').stream())
        print(f"📊 Total projects in database: {len(projects)}")
        
        # Show detailed breakdown
        print(f"\n📋 Detailed breakdown:")
        for customer_doc in customers:
            customer_data = customer_doc.to_dict()
            print(f"  🏢 {customer_data['customer_name']}")
            print(f"    - Customer ID: {customer_data['customer_id']}")
            print(f"    - Logo: {customer_data['customer_logo_url']}")
            print(f"    - Projects: {len(customer_data['projects'])}")
            
            # Get projects for this customer
            for project_id in customer_data['projects']:
                project_doc = db.collection('projects').document(project_id).get()
                if project_doc.exists:
                    project_data = project_doc.to_dict()
                    print(f"      📁 {project_data['project_title']}")
                    print(f"        - Project ID: {project_data['project_id']}")
                    print(f"        - Images: {len(project_data['images'])}")
                    for img in project_data['images']:
                        print(f"          🖼️  {img['description']}")
            print()
        
        print("✅ Database verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False


def main():
    """Main function to set up the database and populate with sample data."""
    
    print("=" * 60)
    print("🏗️  ANDERSON FIRESTORE DATABASE SETUP (Simple Version)")
    print("=" * 60)
    
    # Step 1: Create sample data
    if not create_sample_data_simple():
        print("❌ Failed to create sample data")
        return
    
    # Step 2: Create additional Walmart projects
    if not create_additional_walmart_projects():
        print("❌ Failed to create additional Walmart projects")
        return
    
    # Step 3: Verify everything
    if not verify_database():
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
    print("\n🚀 Your Anderson Firestore Database is ready to use!")
    print("\nNext steps:")
    print("  - Check your Firestore console to see the data")
    print("  - Use the FirestoreManager class in your applications")


if __name__ == "__main__":
    main()
