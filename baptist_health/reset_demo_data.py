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

def reset_current_week_timecards(db):
    """Resets the current week (2025-08-29) timecards back to original state."""
    print("Resetting current week timecards for demo...")
    
    timecards_ref = db.collection('timecards')
    employees_ref = db.collection('employees')
    
    # Get all employees
    employees_query = employees_ref.stream()
    employee_docs = list(employees_query)
    
    # Get manager ID from first employee
    if employee_docs:
        manager_id = employee_docs[0].get('manager_id')
    else:
        print("No employees found!")
        return
    
    # Delete existing timecards for current week
    current_week_query = timecards_ref.where('pay_period_end', '==', '2025-08-29')
    current_week_docs = current_week_query.stream()
    
    batch = db.batch()
    deleted_count = 0
    for doc in current_week_docs:
        batch.delete(doc.reference)
        deleted_count += 1
    
    batch.commit()
    print(f"Deleted {deleted_count} existing timecards for current week.")
    
    # Recreate timecards for current week with original distribution
    batch = db.batch()
    created_count = 0
    
    for emp_doc in employee_docs:
        is_submitted = random.random() > 0.1  # 90% chance of being submitted
        
        if not is_submitted:
            # Create a "not submitted" timecard record
            timecard_data = {
                'employee_id': emp_doc.id,
                'manager_id': manager_id,
                'pay_period_end': '2025-08-29',
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
                'manager_id': manager_id,
                'pay_period_end': '2025-08-29',
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
    print(f"Created {created_count} new timecards for current week.")
    print("✅ Demo reset complete! Current week is ready for agent interaction.")

def main():
    """Main function to reset demo data."""
    print("--- Demo Reset Script ---")
    print("This will reset the current week (2025-08-29) timecards to their original state.")
    print("Historical data (Aug 8, 15, 22) will remain unchanged.")
    
    confirmation = input("Are you sure you want to reset the current week? (y/n): ")
    if confirmation.lower() != 'y':
        print("Reset cancelled.")
        return

    db = get_db_client()
    reset_current_week_timecards(db)
    
    print("\n--- Reset Complete! ---")
    print("Current week timecards are now ready for the next demo.")
    print("Expected distribution:")
    print("- ~22 submitted timecards (19 standard, 3 with exceptions)")
    print("- ~3 not submitted timecards")
    print("- All pending approval (no approved_at/approved_by data)")

if __name__ == '__main__':
    main()
