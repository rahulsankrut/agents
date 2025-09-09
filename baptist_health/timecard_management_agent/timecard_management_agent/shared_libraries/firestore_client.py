"""Shared Firestore client utilities for the timecard management agent."""

import logging
from typing import Dict, List, Any, Optional
from google.cloud import firestore
from datetime import datetime

logger = logging.getLogger(__name__)


class FirestoreClient:
    """Firestore client wrapper for timecard operations."""
    
    def __init__(self, project_id: str, database_id: str):
        """Initialize Firestore client."""
        self.project_id = project_id
        self.database_id = database_id
        self.client = firestore.Client(project=project_id, database=database_id)
        
    def get_timecards_by_pay_period(self, pay_period_end: str, manager_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all timecards for a specific pay period, optionally filtered by manager."""
        try:
            timecards_ref = self.client.collection('timecards')
            query = timecards_ref.where('pay_period_end', '==', pay_period_end)
            
            # If manager_name is provided, filter by manager
            if manager_name:
                # First get the manager_id for the given manager_name
                manager_id = self.get_manager_id_by_name(manager_name)
                if manager_id:
                    query = query.where('manager_id', '==', manager_id)
                else:
                    logger.warning(f"Manager '{manager_name}' not found, returning all timecards")
            
            docs = query.stream()
            
            timecards = []
            for doc in docs:
                timecard_data = doc.to_dict()
                timecard_data['doc_id'] = doc.id
                timecards.append(timecard_data)
            
            logger.info(f"Retrieved {len(timecards)} timecards for pay period {pay_period_end}" + 
                       (f" for manager {manager_name}" if manager_name else ""))
            return timecards
            
        except Exception as e:
            logger.error(f"Error retrieving timecards for pay period {pay_period_end}: {e}")
            raise
    
    def get_manager_id_by_name(self, manager_name: str) -> Optional[str]:
        """Get manager ID by manager name."""
        try:
            managers_ref = self.client.collection('managers')
            query = managers_ref.where('name', '==', manager_name)
            docs = query.stream()
            
            for doc in docs:
                manager_data = doc.to_dict()
                logger.info(f"Found manager ID {doc.id} for manager {manager_name}")
                return doc.id
            
            logger.warning(f"Manager '{manager_name}' not found")
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving manager ID for {manager_name}: {e}")
            raise

    def get_employees_by_manager(self, manager_id: str) -> List[Dict[str, Any]]:
        """Get all employees for a specific manager."""
        try:
            employees_ref = self.client.collection('employees')
            query = employees_ref.where('manager_id', '==', manager_id)
            docs = query.stream()
            
            employees = []
            for doc in docs:
                employee_data = doc.to_dict()
                employee_data['doc_id'] = doc.id
                employees.append(employee_data)
            
            logger.info(f"Retrieved {len(employees)} employees for manager {manager_id}")
            return employees
            
        except Exception as e:
            logger.error(f"Error retrieving employees for manager {manager_id}: {e}")
            raise

    def get_employees_by_manager_name(self, manager_name: str) -> List[Dict[str, Any]]:
        """Get all employees for a specific manager by name."""
        try:
            manager_id = self.get_manager_id_by_name(manager_name)
            if not manager_id:
                return []
            
            return self.get_employees_by_manager(manager_id)
            
        except Exception as e:
            logger.error(f"Error retrieving employees for manager {manager_name}: {e}")
            raise
    
    def get_manager_info(self, manager_id: str) -> Optional[Dict[str, Any]]:
        """Get manager information."""
        try:
            manager_ref = self.client.collection('managers').document(manager_id)
            manager_doc = manager_ref.get()
            
            if manager_doc.exists:
                manager_data = manager_doc.to_dict()
                manager_data['doc_id'] = manager_doc.id
                logger.info(f"Retrieved manager info for {manager_id}")
                return manager_data
            else:
                logger.warning(f"Manager {manager_id} not found")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving manager {manager_id}: {e}")
            raise
    
    def get_employee_schedule(self, employee_id: str, year: int, month: int) -> Optional[Dict[str, Any]]:
        """Get employee schedule for a specific month."""
        try:
            schedules_ref = self.client.collection('schedules')
            schedule_doc_id = f"{employee_id}_{year}_{month}"
            schedule_ref = schedules_ref.document(schedule_doc_id)
            schedule_doc = schedule_ref.get()
            
            if schedule_doc.exists:
                schedule_data = schedule_doc.to_dict()
                schedule_data['doc_id'] = schedule_doc.id
                logger.info(f"Retrieved schedule for employee {employee_id}, {year}-{month}")
                return schedule_data
            else:
                logger.warning(f"Schedule not found for employee {employee_id}, {year}-{month}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving schedule for employee {employee_id}: {e}")
            raise
    
    def approve_timecards(self, timecard_ids: List[str], approved_by: str) -> bool:
        """Approve multiple timecards in a batch operation."""
        try:
            batch = self.client.batch()
            current_time = datetime.now().isoformat()
            
            for timecard_id in timecard_ids:
                timecard_ref = self.client.collection('timecards').document(timecard_id)
                batch.update(timecard_ref, {
                    'status': 'approved',
                    'approved_at': current_time,
                    'approved_by': approved_by
                })
            
            batch.commit()
            logger.info(f"Approved {len(timecard_ids)} timecards by {approved_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error approving timecards: {e}")
            raise
    
    def get_pay_periods(self) -> List[str]:
        """Get all available pay periods."""
        try:
            timecards_ref = self.client.collection('timecards')
            docs = timecards_ref.stream()
            
            pay_periods = set()
            for doc in docs:
                timecard_data = doc.to_dict()
                if 'pay_period_end' in timecard_data:
                    pay_periods.add(timecard_data['pay_period_end'])
            
            sorted_periods = sorted(list(pay_periods))
            logger.info(f"Retrieved {len(sorted_periods)} pay periods")
            return sorted_periods
            
        except Exception as e:
            logger.error(f"Error retrieving pay periods: {e}")
            raise
