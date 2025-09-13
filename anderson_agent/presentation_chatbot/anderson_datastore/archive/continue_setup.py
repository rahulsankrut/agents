"""
Continue adding remaining sample data
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


def add_remaining_projects():
    """Add the remaining projects that failed to create."""
    
    print("🔄 Adding remaining sample projects...")
    
    try:
        db = firestore.Client(project=PROJECT_ID)
        
        # Get existing projects to avoid duplicates
        existing_projects = list(db.collection('projects').stream())
        existing_titles = [doc.to_dict()['project_title'] for doc in existing_projects]
        
        print(f"Found {len(existing_projects)} existing projects")
        
        # Add remaining projects
        for i, project_data in enumerate(SAMPLE_PROJECTS, 1):
            if project_data['project_title'] in existing_titles:
                print(f"Skipping project {i}: {project_data['project_title']} (already exists)")
                continue
                
            print(f"Adding project {i}: {project_data['project_title']}")
            
            try:
                # Generate unique IDs
                project_id = str(uuid.uuid4())
                
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
                else:
                    # Create new customer
                    customer_id = str(uuid.uuid4())
                    customer_doc = {
                        'customer_id': customer_id,
                        'customer_name': project_data["customer_name"],
                        'customer_logo_url': project_data["customer_logo_url"],
                        'projects': [project_id],
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    
                    db.collection('customers').document(customer_id).set(customer_doc)
                
                print(f"  ✅ Created: {project_data['project_title']}")
                
            except Exception as e:
                print(f"  ❌ Failed to create {project_data['project_title']}: {e}")
                continue
        
        print("✅ Finished adding remaining projects!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def add_walmart_projects():
    """Add additional Walmart projects."""
    
    print("\n🔗 Adding additional Walmart projects...")
    
    try:
        db = firestore.Client(project=PROJECT_ID)
        
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
            try:
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
                
            except Exception as e:
                print(f"  ❌ Failed to create {project_data['project_title']}: {e}")
                continue
        
        print("✅ Additional Walmart projects completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def show_database_summary():
    """Show a summary of the database contents."""
    
    print("\n📊 Database Summary:")
    
    try:
        db = firestore.Client(project=PROJECT_ID)
        
        # Get all customers
        customers = list(db.collection('customers').stream())
        print(f"📈 Total customers: {len(customers)}")
        
        # Get all projects
        projects = list(db.collection('projects').stream())
        print(f"📈 Total projects: {len(projects)}")
        
        print(f"\n📋 Customer-Project Breakdown:")
        for customer_doc in customers:
            customer_data = customer_doc.to_dict()
            print(f"  🏢 {customer_data['customer_name']}")
            print(f"    - Projects: {len(customer_data['projects'])}")
            
            # Show project titles
            for project_id in customer_data['projects']:
                project_doc = db.collection('projects').document(project_id).get()
                if project_doc.exists:
                    project_data = project_doc.to_dict()
                    print(f"      📁 {project_data['project_title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main function."""
    
    print("=" * 50)
    print("🔄 CONTINUING DATABASE SETUP")
    print("=" * 50)
    
    # Add remaining projects
    add_remaining_projects()
    
    # Add Walmart projects
    add_walmart_projects()
    
    # Show summary
    show_database_summary()
    
    print("\n🎉 Database setup completed!")


if __name__ == "__main__":
    main()
