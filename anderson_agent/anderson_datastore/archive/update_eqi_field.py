"""
Script to update existing projects with EQI field
"""

from firestore_operations import FirestoreManager
from google.cloud import firestore
from datetime import datetime

def update_existing_projects_with_eqi():
    """Add EQI field to all existing projects."""
    
    print("🔄 Updating existing projects with EQI field...")
    
    # Connect to database
    db = firestore.Client(project="agent-space-465923", database="anderson-db")
    
    # Get all projects
    projects_ref = db.collection('projects')
    projects = list(projects_ref.stream())
    
    print(f"Found {len(projects)} projects to update")
    
    updated_count = 0
    
    for project_doc in projects:
        project_data = project_doc.to_dict()
        project_id = project_doc.id
        
        # Check if EQI field already exists
        if 'eqi' not in project_data:
            # Add EQI field (default to False for existing projects)
            project_data['eqi'] = False
            project_data['updated_at'] = datetime.now()
            
            # Update the document
            projects_ref.document(project_id).set(project_data)
            updated_count += 1
            
            print(f"  ✅ Updated project: {project_data.get('project_title', 'Unknown')}")
        else:
            print(f"  ⏭️  Skipped project: {project_data.get('project_title', 'Unknown')} (already has EQI)")
    
    print(f"\n🎉 Update completed! Updated {updated_count} projects with EQI field.")

def test_eqi_functionality():
    """Test the EQI functionality with FirestoreManager."""
    
    print("\n🧪 Testing EQI functionality...")
    
    db_manager = FirestoreManager(project_id="agent-space-465923")
    
    # Get a project to test
    projects = db_manager.list_projects()
    if projects:
        project = projects[0]
        print(f"Testing with project: {project.project_title}")
        print(f"Current EQI value: {project.eqi}")
        
        # Update EQI to True
        success = db_manager.update_project(
            project_id=project.project_id,
            eqi=True
        )
        
        if success:
            # Verify the update
            updated_project = db_manager.get_project(project.project_id)
            print(f"Updated EQI value: {updated_project.eqi}")
            print("✅ EQI functionality working correctly!")
        else:
            print("❌ Failed to update EQI")
    else:
        print("No projects found to test")

if __name__ == "__main__":
    update_existing_projects_with_eqi()
    test_eqi_functionality()
