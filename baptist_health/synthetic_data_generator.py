import random
from datetime import date, timedelta, datetime
from google.cloud import firestore
import uuid

# --- Configuration ---
PROJECT_ID = "agent-space-465923"  
DATABASE_ID = "timecard-demo-database"
RAHUL_MANAGER_ID = f"manager_rahul_{uuid.uuid4().hex[:8]}"
DREW_MANAGER_ID = f"manager_drew_{uuid.uuid4().hex[:8]}"
NUM_EMPLOYEES_PER_MANAGER = 20
EMPLOYEE_NAMES = [
    "Olivia Chen", "Benjamin Carter", "Sophia Rodriguez", "Liam Goldberg", "Ava Nguyen",
    "Noah Williams", "Isabella Martinez", "Mason Garcia", "Harper Thompson", "Ethan Moore",
    "Evelyn White", "Alexander Hall", "Mia Lewis", "James Walker", "Charlotte Green",
    "William Clark", "Amelia Hill", "Michael Scott", "Emily Baker", "David Adams",
    "Jessica Wright", "Chris Martinez", "Ashley Davis", "Kevin Harris", "Sarah Wilson",
    "Daniel Brown", "Lisa Johnson", "Robert Taylor", "Jennifer Anderson", "Christopher Lee",
    "Michelle Garcia", "Andrew Wilson", "Stephanie Moore", "Matthew Davis", "Nicole Jackson",
    "Ryan Thompson", "Amanda White", "Joshua Harris", "Rachel Martin", "Brandon Young"
]

def get_db_client():
    """Initializes and returns the Firestore client."""
    try:
        return firestore.Client(project=PROJECT_ID, database=DATABASE_ID)
    except Exception as e:
        print(f"Error: Could not connect to Firestore.")
        print(f"Please ensure you have authenticated with 'gcloud auth application-default login'")
        print(f"and that your project ID '{PROJECT_ID}' is correct.")
        raise e

def clear_collection(db, collection_name):
    """Deletes all documents in a collection."""
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    for doc in docs:
        print(f"Deleting doc: {doc.id} from {collection_name}")
        doc.reference.delete()

def seed_manager_and_employees(db):
    """Creates two managers and employees who report to them."""
    print("Seeding managers and employees...")
    employees_ref = db.collection('employees')
    managers_ref = db.collection('managers')

    batch = db.batch()
    all_employee_ids = []

    # Create Rahul's team (first 20 employees)
    rahul_employee_ids = []
    for i in range(NUM_EMPLOYEES_PER_MANAGER):
        emp_id = f"emp_rahul_{uuid.uuid4().hex[:8]}"
        rahul_employee_ids.append(emp_id)
        all_employee_ids.append(emp_id)
        emp_doc_ref = employees_ref.document(emp_id)
        batch.set(emp_doc_ref, {
            'employee_id': emp_id,
            'name': EMPLOYEE_NAMES[i],
            'manager_id': RAHUL_MANAGER_ID
        })

    # Create Drew's team (next 20 employees)
    drew_employee_ids = []
    for i in range(NUM_EMPLOYEES_PER_MANAGER, NUM_EMPLOYEES_PER_MANAGER * 2):
        emp_id = f"emp_drew_{uuid.uuid4().hex[:8]}"
        drew_employee_ids.append(emp_id)
        all_employee_ids.append(emp_id)
        emp_doc_ref = employees_ref.document(emp_id)
        batch.set(emp_doc_ref, {
            'employee_id': emp_id,
            'name': EMPLOYEE_NAMES[i],
            'manager_id': DREW_MANAGER_ID
        })

    # Create Rahul manager document
    rahul_manager_ref = managers_ref.document(RAHUL_MANAGER_ID)
    batch.set(rahul_manager_ref, {
        'manager_id': RAHUL_MANAGER_ID,
        'name': 'Rahul',
        'employee_ids': rahul_employee_ids
    })

    # Create Drew manager document
    drew_manager_ref = managers_ref.document(DREW_MANAGER_ID)
    batch.set(drew_manager_ref, {
        'manager_id': DREW_MANAGER_ID,
        'name': 'Drew',
        'employee_ids': drew_employee_ids
    })

    batch.commit()
    print(f"Seeded 2 managers and {NUM_EMPLOYEES_PER_MANAGER * 2} employees.")
    print(f"Rahul: {len(rahul_employee_ids)} employees")
    print(f"Drew: {len(drew_employee_ids)} employees")
    return all_employee_ids

def seed_timecards(db, manager_id, manager_name):
    """Creates timecard entries for all employees for multiple pay periods."""
    print(f"Seeding timecards for {manager_name}...")
    timecards_ref = db.collection('timecards')
    employees_ref = db.collection('employees')
    
    # Get all employees for this manager
    employees_query = employees_ref.where('manager_id', '==', manager_id).stream()
    employee_docs = list(employees_query)

    pay_periods = [
        "2025-08-01",
        "2025-08-08",
        "2025-08-15",
        "2025-08-22",
        "2025-08-29",
        "2025-09-05"
    ]

    batch = db.batch()
    for emp_doc in employee_docs:
        for pay_period in pay_periods:
            is_submitted = random.random() > 0.1  # 90% chance of being submitted

            if not is_submitted:
                # Create a "not submitted" timecard record
                timecard_data = {
                    'employee_id': emp_doc.id,
                    'manager_id': manager_id,
                    'pay_period_end': pay_period,
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
                
                # Determine status and approval data based on pay period
                if pay_period in ["2025-08-01", "2025-08-08", "2025-08-15", "2025-08-22", "2025-08-29"]:
                    # Past pay periods - most should be approved
                    if not has_exception:
                        # Standard timecards from past periods should be approved
                        status = 'approved'
                        approved_at = f"{pay_period} 16:00:00"  # End of pay period
                        approved_by = manager_name
                    else:
                        # Exceptions from past periods - 70% resolved, 30% still pending
                        status = 'approved' if random.random() > 0.3 else 'submitted'
                        approved_at = f"{pay_period} 16:00:00" if status == 'approved' else None
                        approved_by = manager_name if status == 'approved' else None
                else:
                    # Current week (2025-09-05) - keep pending for demo
                    status = 'submitted'
                    approved_at = None
                    approved_by = None
                
                timecard_data = {
                    'employee_id': emp_doc.id,
                    'manager_id': manager_id,
                    'pay_period_end': pay_period,
                    'status': status,
                    'has_exception': has_exception,
                    'exception_reason': exception_reason,
                    'total_hours': round(random.uniform(38.0, 45.0), 2),
                    'overtime_hours': round(random.uniform(0.0, 5.0), 2) if has_exception else 0,
                    'notes': "Manager approval required." if has_exception else "Standard hours.",
                    'approved_at': approved_at,  # Will be set when approved by agent
                    'approved_by': approved_by   # Will be set when approved by agent
                }
            
            # Add the generated timecard to the batch
            batch.set(timecards_ref.document(), timecard_data)

    batch.commit()
    print(f"Seeded timecards for {len(employee_docs)} employees across {len(pay_periods)} pay periods.")

def seed_schedules(db, manager_id, manager_name):
    """Creates monthly schedule documents for all employees."""
    print(f"Seeding schedules for {manager_name}...")
    schedules_ref = db.collection('schedules')
    employees_ref = db.collection('employees')

    employees_query = employees_ref.where('manager_id', '==', manager_id).stream()
    employee_docs = list(employees_query)

    batch = db.batch()

    for year, month in [(2025, 9), (2025, 10)]:
        for emp_doc in employee_docs:
            schedule_doc_id = f"{emp_doc.id}_{year}_{month}"
            schedule_doc_ref = schedules_ref.document(schedule_doc_id)
            
            daily_shifts = {}
            start_date = date(year, month, 1)
            # Find the number of days in the month
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month + 1, 1)
            
            current_date = start_date
            while current_date < end_date:
                # Assuming employees work weekdays (Monday=0, Sunday=6)
                if current_date.weekday() < 5:
                    shift_start_hour = random.choice([7, 8])
                    shift_start_minute = random.choice([0, 30])
                    shift_end_hour = shift_start_hour + 8
                    shift_end_minute = shift_start_minute

                    start_time = f"{shift_start_hour:02d}:{shift_start_minute:02d}"
                    end_time = f"{shift_end_hour:02d}:{shift_end_minute:02d}"
                    
                    daily_shifts[current_date.strftime('%Y-%m-%d')] = f"{start_time}-{end_time}"
                current_date += timedelta(days=1)
            
            schedule_data = {
                'employee_id': emp_doc.id,
                'manager_id': manager_id,
                'year': year,
                'month': month,
                'daily_shifts': daily_shifts
            }
            batch.set(schedule_doc_ref, schedule_data)
    
    batch.commit()
    print("Seeded monthly schedules.")

def main():
    """Main function to run the seeding process."""
    print("--- Starting Firestore Seeding Script ---")
    
    db = get_db_client()
    
    confirmation = input("This will DELETE all existing data in collections (managers, employees, timecards, schedules). Are you sure? (y/n): ")
    if confirmation.lower() != 'y':
        print("Operation cancelled.")
        return

    # Clear existing data
    clear_collection(db, 'timecards')
    clear_collection(db, 'schedules')
    clear_collection(db, 'employees')
    clear_collection(db, 'managers')

    # Seed new data
    seed_manager_and_employees(db)
    seed_timecards(db, RAHUL_MANAGER_ID, 'Rahul')
    seed_timecards(db, DREW_MANAGER_ID, 'Drew')
    seed_schedules(db, RAHUL_MANAGER_ID, 'Rahul')
    seed_schedules(db, DREW_MANAGER_ID, 'Drew')

    print("\n--- Seeding Complete! ---")
    print(f"Your Firestore database '{DATABASE_ID}' in project '{PROJECT_ID}' has been populated.")

if __name__ == '__main__':
    main()

