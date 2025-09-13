"""
Update EQI values from True/False to Yes/No
"""

from google.cloud import firestore
from datetime import datetime

def update_eqi_values():
    """Update EQI values from True/False to Yes/No."""
    
    print("🔄 Updating EQI values from True/False to Yes/No...")
    
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
        
        # Check current EQI value and convert
        current_eqi = project_data.get('eqi')
        
        if current_eqi is True:
            project_data['eqi'] = 'Yes'
            project_data['updated_at'] = datetime.now()
            projects_ref.document(project_id).set(project_data)
            updated_count += 1
            print(f"  ✅ Updated project: {project_data.get('project_title', 'Unknown')} (True → Yes)")
        elif current_eqi is False:
            project_data['eqi'] = 'No'
            project_data['updated_at'] = datetime.now()
            projects_ref.document(project_id).set(project_data)
            updated_count += 1
            print(f"  ✅ Updated project: {project_data.get('project_title', 'Unknown')} (False → No)")
        elif current_eqi == 'Yes' or current_eqi == 'No':
            print(f"  ⏭️  Skipped project: {project_data.get('project_title', 'Unknown')} (already Yes/No)")
        else:
            print(f"  ⚠️  Unknown EQI value for project: {project_data.get('project_title', 'Unknown')} ({current_eqi})")
    
    print(f"\n🎉 Update completed! Updated {updated_count} projects with Yes/No EQI values.")

def verify_eqi_values():
    """Verify that all EQI values are now Yes/No."""
    
    print("\n🔍 Verifying EQI values...")
    
    # Connect to database
    db = firestore.Client(project="agent-space-465923", database="anderson-db")
    
    # Get all projects
    projects_ref = db.collection('projects')
    projects = list(projects_ref.stream())
    
    yes_count = 0
    no_count = 0
    other_count = 0
    
    for project_doc in projects:
        project_data = project_doc.to_dict()
        eqi_value = project_data.get('eqi')
        
        if eqi_value == 'Yes':
            yes_count += 1
        elif eqi_value == 'No':
            no_count += 1
        else:
            other_count += 1
            print(f"  ⚠️  Project with non-standard EQI: {project_data.get('project_title', 'Unknown')} ({eqi_value})")
    
    print(f"📊 EQI Value Summary:")
    print(f"  - Yes: {yes_count}")
    print(f"  - No: {no_count}")
    print(f"  - Other: {other_count}")
    
    if other_count == 0:
        print("✅ All EQI values are now Yes/No!")
    else:
        print("⚠️  Some projects still have non-standard EQI values")

if __name__ == "__main__":
    update_eqi_values()
    verify_eqi_values()
