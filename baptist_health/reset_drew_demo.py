import random
from datetime import date, timedelta
from google.cloud import firestore
import uuid

# --- Configuration ---
PROJECT_ID = "agent-space-465923"  
DATABASE_ID = "timecard-demo-database"

def get_db_client():
    """Initializes and returns the Firestore client."""
    try:
        return firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    except Exception as e:
        print(f"Error: Could not connect to Firestore.")
        print(f"Please ensure you have authenticated with 'gcloud auth application-default login'")
        print(f"and that your project ID '{PROJECT_ID}' is correct.")
        raise e

def get_drew_manager_info(db):
    """Gets Drew's manager information from the database."""
    managers_ref = db.collection('managers')
    managers_query = managers_ref.where('name', '==', 'Drew').stream()
    manager_docs = list(managers_query)
    
    if not manager_docs:
        print("Error: Drew not found in database.")
        return None
    
    return manager_docs[0].to_dict()

def reset_drew_current_week_timecards(db):
    """Resets Drew's current week (2025-09-05) timecards back to original state."""
    print("Resetting Drew's current week timecards...")
    
    drew_info = get_drew_manager_info(db)
    if not drew_info:
        return
    
    timecards_ref = db.collection('timecards')
    employees_ref = db.collection('employees')
    
    # Get all employees for Drew
    employees_query = employees_ref.where('manager_id', '==', drew_info['manager_id']).stream()
    employee_docs = list(employees_query)
    
    if not employee_docs:
        print("No employees found for Drew!")
        return
    
    # Delete existing timecards for current week for Drew
    current_week_query = timecards_ref.where('pay_period_end', '==', '2025-09-05').where('manager_id', '==', drew_info['manager_id'])
    current_week_docs = current_week_query.stream()
    
    batch = db.batch()
    deleted_count = 0
    for doc in current_week_docs:
        batch.delete(doc.reference)
        deleted_count += 1
    
    batch.commit()
    print(f"Deleted {deleted_count} existing timecards for current week for Drew.")
    
    # Recreate timecards for current week with original distribution
    batch = db.batch()
    created_count = 0
    
    for emp_doc in employee_docs:
        is_submitted = random.random() > 0.1  # 90% chance of being submitted
        
        if not is_submitted:
            # Create a "not submitted" timecard record
            timecard_data = {
                'employee_id': emp_doc.id,
                'manager_id': drew_info['manager_id'],
                'pay_period_end': '2025-09-05',
                'status': 'not submitted',
                'has_exception': True,
                'exception_reason': 'Not Submitted',
                'total_hours': 0,
                'overtime_hours': 0,
                'notes': '',
                'approved_at': None,
                'approved_by': None
            }
        else:
            # Create a standard, submitted timecard (with a chance of other exceptions)
            has_exception = random.random() <= 0.15  # 15% chance of an exception on submitted cards
            exception_reason = ""
            if has_exception:
                exception_reason = random.choice([
                    "Overtime exceeds policy without pre-approval.",
                    "Missing punch on a scheduled day.",
                    "Incorrect pay code used for on-call hours.",
                    "Shift duration does not match scheduled hours."
                ])
            
            # Current week - keep pending for demo
            status = 'submitted'
            approved_at = None
            approved_by = None
            
            timecard_data = {
                'employee_id': emp_doc.id,
                'manager_id': drew_info['manager_id'],
                'pay_period_end': '2025-09-05',
                'status': status,
                'has_exception': has_exception,
                'exception_reason': exception_reason,
                'total_hours': round(random.uniform(38.0, 45.0), 2),
                'overtime_hours': round(random.uniform(0.0, 5.0), 2) if has_exception else 0,
                'notes': "Manager approval required." if has_exception else "Standard hours.",
                'approved_at': approved_at,
                'approved_by': approved_by
            }
        
        # Add the generated timecard to the batch
        batch.set(timecards_ref.document(), timecard_data)
        created_count += 1
    
    batch.commit()
    print(f"Created {created_count} new timecards for current week for Drew.")
    print("✅ Drew's demo reset complete! Current week is ready for agent interaction.")

def main():
    """Main function to reset Drew's demo data."""
    print("--- Drew's Demo Reset Script ---")
    print("This will reset Drew's current week (2025-09-05) timecards to their original state.")
    print("Historical data (Aug 1, 8, 15, 22, 29) will remain unchanged.")
    print("Rahul's data will remain completely untouched.")
    
    confirmation = input("Are you sure you want to reset Drew's current week? (y/n): ")
    if confirmation.lower() != 'y':
        print("Reset cancelled.")
        return

    db = get_db_client()
    reset_drew_current_week_timecards(db)
    
    print("\n--- Drew's Reset Complete! ---")
    print("Drew's current week timecards are now ready for the next demo.")
    print("Expected distribution for Drew's team:")
    print("- ~18 submitted timecards (16 standard, 2 with exceptions)")
    print("- ~2 not submitted timecards")
    print("- All pending approval (no approved_at/approved_by data)")
    print("- Total: 20 employees for Drew")

if __name__ == '__main__':
    main()
