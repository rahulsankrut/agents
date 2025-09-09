"""Timecard management tools for the agent."""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from tabulate import tabulate

from ..shared_libraries.firestore_client import FirestoreClient
from ..config import Config

logger = logging.getLogger(__name__)
config = Config()

# Global manager context - this will be set once and used throughout the session
_current_manager = None


def get_db_client() -> FirestoreClient:
    """Get Firestore client instance."""
    return FirestoreClient(
        project_id=config.agent_settings.project_id,
        database_id=config.agent_settings.database_id
    )


def set_manager_context(manager_name: str) -> Dict[str, Any]:
    """
    Set the current manager context for the session.
    
    Args:
        manager_name: The name of the manager (e.g., "Rahul" or "Drew")
    
    Returns:
        Dictionary containing confirmation of the manager context
    """
    global _current_manager
    
    try:
        db = get_db_client()
        
        # Verify the manager exists
        manager_id = db.get_manager_id_by_name(manager_name)
        if not manager_id:
            return {
                "status": "error",
                "message": f"Manager '{manager_name}' not found in the system. Available managers are: Rahul, Drew",
                "current_manager": _current_manager
            }
        
        # Set the global context
        _current_manager = manager_name
        
        # Get some basic info about the manager's team
        employees = db.get_employees_by_manager_name(manager_name)
        
        return {
            "status": "success",
            "message": f"Manager context set to {manager_name}. You now have access to {len(employees)} employees.",
            "current_manager": _current_manager,
            "team_size": len(employees),
            "manager_id": manager_id
        }
        
    except Exception as e:
        logger.error(f"Error setting manager context for {manager_name}: {e}")
        return {
            "status": "error",
            "message": f"Error setting manager context: {str(e)}",
            "current_manager": _current_manager
        }


def get_current_manager() -> Optional[str]:
    """Get the current manager context."""
    return _current_manager


def get_summary(pay_period_end: str, manager_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a summary of timecards for a specific pay period and manager.
    
    Args:
        pay_period_end: The pay period end date (YYYY-MM-DD format)
        manager_name: The name of the manager (e.g., "Rahul" or "Drew"). If not provided, uses current manager context.
    
    Returns:
        Dictionary containing summary statistics and breakdown
    """
    try:
        # Use provided manager_name or fall back to current context
        effective_manager = manager_name or _current_manager
        
        db = get_db_client()
        timecards = db.get_timecards_by_pay_period(pay_period_end, effective_manager)
        
        if not timecards:
            manager_msg = f" for manager {effective_manager}" if effective_manager else ""
            return {
                "status": "no_data",
                "message": f"No timecards found for pay period ending {pay_period_end}{manager_msg}",
                "summary": {}
            }
        
        # Get employee names for mapping
        if effective_manager:
            employees = db.get_employees_by_manager_name(effective_manager)
        else:
            # Fallback to getting manager ID from first timecard
            manager_id = timecards[0].get('manager_id')
            employees = db.get_employees_by_manager(manager_id)
        
        employee_map = {emp['employee_id']: emp['name'] for emp in employees}
        
        # Calculate statistics
        total_timecards = len(timecards)
        submitted = [tc for tc in timecards if tc['status'] == 'submitted']
        approved = [tc for tc in timecards if tc['status'] == 'approved']
        not_submitted = [tc for tc in timecards if tc['status'] == 'not submitted']
        with_exceptions = [tc for tc in timecards if tc.get('has_exception', False)]
        without_exceptions = [tc for tc in timecards if not tc.get('has_exception', False)]
        
        # Standard timecards (submitted with no exceptions)
        standard_timecards = [tc for tc in submitted if not tc.get('has_exception', False)]
        
        summary = {
            "pay_period_end": pay_period_end,
            "total_timecards": total_timecards,
            "submitted": len(submitted),
            "approved": len(approved),
            "not_submitted": len(not_submitted),
            "with_exceptions": len(with_exceptions),
            "without_exceptions": len(without_exceptions),
            "standard_timecards": len(standard_timecards),
            "standard_timecard_ids": [tc['doc_id'] for tc in standard_timecards]
        }
        
        # Create detailed breakdown with employee names
        breakdown = []
        for tc in timecards:
            employee_id = tc.get('employee_id', 'Unknown')
            employee_name = employee_map.get(employee_id, employee_id)  # Use name if available, fallback to ID
            status = tc['status']
            has_exception = tc.get('has_exception', False)
            exception_reason = tc.get('exception_reason', '')
            
            breakdown.append({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "status": status,
                "has_exception": has_exception,
                "exception_reason": exception_reason,
                "total_hours": tc.get('total_hours', 0),
                "overtime_hours": tc.get('overtime_hours', 0)
            })
        
        return {
            "status": "success",
            "summary": summary,
            "breakdown": breakdown,
            "message": f"Found {total_timecards} timecards for pay period ending {pay_period_end}"
        }
        
    except Exception as e:
        logger.error(f"Error getting summary for pay period {pay_period_end}: {e}")
        return {
            "status": "error",
            "message": f"Error retrieving timecard summary: {str(e)}",
            "summary": {}
        }


def get_exceptions(pay_period_end: str, manager_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed information about timecards with exceptions.
    
    Args:
        pay_period_end: The pay period end date (YYYY-MM-DD format)
        manager_name: The name of the manager (e.g., "Rahul" or "Drew"). If not provided, uses current manager context.
    
    Returns:
        Dictionary containing exception details
    """
    try:
        # Use provided manager_name or fall back to current context
        effective_manager = manager_name or _current_manager
        
        db = get_db_client()
        timecards = db.get_timecards_by_pay_period(pay_period_end, effective_manager)
        
        if not timecards:
            manager_msg = f" for manager {effective_manager}" if effective_manager else ""
            return {
                "status": "no_data",
                "message": f"No timecards found for pay period ending {pay_period_end}{manager_msg}",
                "exceptions": []
            }
        
        # Get employee names for mapping
        if effective_manager:
            employees = db.get_employees_by_manager_name(effective_manager)
            employee_map = {emp['employee_id']: emp['name'] for emp in employees}
        else:
            if timecards:
                manager_id = timecards[0].get('manager_id')
                employees = db.get_employees_by_manager(manager_id)
                employee_map = {emp['employee_id']: emp['name'] for emp in employees}
            else:
                employee_map = {}
        
        # Filter for exceptions
        exceptions = [tc for tc in timecards if tc.get('has_exception', False)]
        
        if not exceptions:
            return {
                "status": "success",
                "message": f"No exceptions found for pay period ending {pay_period_end}",
                "exceptions": []
            }
        
        # Group by status
        not_submitted = [tc for tc in exceptions if tc['status'] == 'not submitted']
        submitted_with_exceptions = [tc for tc in exceptions if tc['status'] == 'submitted']
        
        exception_details = []
        for tc in exceptions:
            employee_id = tc.get('employee_id', 'Unknown')
            employee_name = employee_map.get(employee_id, employee_id)
            exception_details.append({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "status": tc['status'],
                "exception_reason": tc.get('exception_reason', ''),
                "total_hours": tc.get('total_hours', 0),
                "overtime_hours": tc.get('overtime_hours', 0),
                "notes": tc.get('notes', '')
            })
        
        return {
            "status": "success",
            "pay_period_end": pay_period_end,
            "total_exceptions": len(exceptions),
            "not_submitted": len(not_submitted),
            "submitted_with_exceptions": len(submitted_with_exceptions),
            "exceptions": exception_details,
            "message": f"Found {len(exceptions)} timecards with exceptions for pay period ending {pay_period_end}"
        }
        
    except Exception as e:
        logger.error(f"Error getting exceptions for pay period {pay_period_end}: {e}")
        return {
            "status": "error",
            "message": f"Error retrieving exceptions: {str(e)}",
            "exceptions": []
        }


def approve_standard_timecards(pay_period_end: str, manager_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Approve all standard timecards (submitted with no exceptions) for a pay period and manager.
    
    Args:
        pay_period_end: The pay period end date (YYYY-MM-DD format)
        manager_name: The name of the manager (e.g., "Rahul" or "Drew"). If not provided, uses current manager context.
    
    Returns:
        Dictionary containing approval results
    """
    try:
        # Use provided manager_name or fall back to current context
        effective_manager = manager_name or _current_manager
        
        db = get_db_client()
        timecards = db.get_timecards_by_pay_period(pay_period_end, effective_manager)
        
        if not timecards:
            manager_msg = f" for manager {effective_manager}" if effective_manager else ""
            return {
                "status": "no_data",
                "message": f"No timecards found for pay period ending {pay_period_end}{manager_msg}",
                "approved_count": 0
            }
        
        # Find standard timecards (submitted with no exceptions)
        standard_timecards = [
            tc for tc in timecards 
            if tc['status'] == 'submitted' and not tc.get('has_exception', False)
        ]
        
        if not standard_timecards:
            manager_msg = f" for manager {effective_manager}" if effective_manager else ""
            return {
                "status": "no_standard_timecards",
                "message": f"No standard timecards found for pay period ending {pay_period_end}{manager_msg}",
                "approved_count": 0
            }
        
        # Get timecard IDs to approve
        timecard_ids = [tc['doc_id'] for tc in standard_timecards]
        
        # Use the effective manager or fall back to config
        approved_by = effective_manager if effective_manager else config.agent_settings.manager_name
        
        # Approve the timecards
        success = db.approve_timecards(timecard_ids, approved_by)
        
        if success:
            manager_msg = f" for manager {manager_name}" if manager_name else ""
            return {
                "status": "success",
                "pay_period_end": pay_period_end,
                "manager_name": manager_name,
                "approved_count": len(timecard_ids),
                "approved_by": approved_by,
                "approved_at": datetime.now().isoformat(),
                "message": f"Successfully approved {len(timecard_ids)} standard timecards for pay period ending {pay_period_end}{manager_msg}"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to approve timecards",
                "approved_count": 0
            }
        
    except Exception as e:
        logger.error(f"Error approving timecards for pay period {pay_period_end}: {e}")
        return {
            "status": "error",
            "message": f"Error approving timecards: {str(e)}",
            "approved_count": 0
        }


def get_employee_schedule(employee_id: str, year: int, month: int) -> Dict[str, Any]:
    """
    Get employee schedule for a specific month.
    
    Args:
        employee_id: The employee ID
        year: The year (e.g., 2025)
        month: The month (1-12)
    
    Returns:
        Dictionary containing schedule information
    """
    try:
        db = get_db_client()
        schedule = db.get_employee_schedule(employee_id, year, month)
        
        if not schedule:
            return {
                "status": "no_data",
                "message": f"No schedule found for employee {employee_id} for {year}-{month:02d}",
                "schedule": {}
            }
        
        return {
            "status": "success",
            "employee_id": employee_id,
            "year": year,
            "month": month,
            "schedule": schedule,
            "message": f"Retrieved schedule for employee {employee_id} for {year}-{month:02d}"
        }
        
    except Exception as e:
        logger.error(f"Error getting schedule for employee {employee_id}: {e}")
        return {
            "status": "error",
            "message": f"Error retrieving schedule: {str(e)}",
            "schedule": {}
        }


def get_historical_comparison(current_period: str, comparison_period: str, manager_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Compare two pay periods to show trends.
    
    Args:
        current_period: Current pay period end date (YYYY-MM-DD)
        comparison_period: Comparison pay period end date (YYYY-MM-DD)
        manager_name: The name of the manager (e.g., "Rahul" or "Drew"). If not provided, uses current manager context.
    
    Returns:
        Dictionary containing comparison data
    """
    try:
        # Use provided manager_name or fall back to current context
        effective_manager = manager_name or _current_manager
        
        db = get_db_client()
        
        # Get timecards for both periods
        current_timecards = db.get_timecards_by_pay_period(current_period, effective_manager)
        comparison_timecards = db.get_timecards_by_pay_period(comparison_period, effective_manager)
        
        # Calculate statistics for current period
        current_exceptions = len([tc for tc in current_timecards if tc.get('has_exception', False)])
        current_not_submitted = len([tc for tc in current_timecards if tc['status'] == 'not submitted'])
        
        # Calculate statistics for comparison period
        comparison_exceptions = len([tc for tc in comparison_timecards if tc.get('has_exception', False)])
        comparison_not_submitted = len([tc for tc in comparison_timecards if tc['status'] == 'not submitted'])
        
        # Calculate changes
        exception_change = current_exceptions - comparison_exceptions
        not_submitted_change = current_not_submitted - comparison_not_submitted
        
        comparison_data = {
            "current_period": {
                "pay_period_end": current_period,
                "total_timecards": len(current_timecards),
                "exceptions": current_exceptions,
                "not_submitted": current_not_submitted
            },
            "comparison_period": {
                "pay_period_end": comparison_period,
                "total_timecards": len(comparison_timecards),
                "exceptions": comparison_exceptions,
                "not_submitted": comparison_not_submitted
            },
            "changes": {
                "exception_change": exception_change,
                "not_submitted_change": not_submitted_change,
                "exception_trend": "higher" if exception_change > 0 else "lower" if exception_change < 0 else "same",
                "not_submitted_trend": "higher" if not_submitted_change > 0 else "lower" if not_submitted_change < 0 else "same"
            }
        }
        
        return {
            "status": "success",
            "comparison": comparison_data,
            "message": f"Comparison between {current_period} and {comparison_period} completed"
        }
        
    except Exception as e:
        logger.error(f"Error comparing pay periods: {e}")
        return {
            "status": "error",
            "message": f"Error comparing pay periods: {str(e)}",
            "comparison": {}
        }


def draft_reminder_message(employee_ids: List[str], pay_period_end: str, manager_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Draft a reminder message for employees who haven't submitted timecards.
    
    Args:
        employee_ids: List of employee IDs to send reminders to
        pay_period_end: The pay period end date
        manager_name: The name of the manager (e.g., "Rahul" or "Drew"). If not provided, uses current manager context.
    
    Returns:
        Dictionary containing the drafted message
    """
    try:
        # Use provided manager_name or fall back to current context
        effective_manager = manager_name or _current_manager
        
        db = get_db_client()
        
        # Get employee names for the effective manager
        if effective_manager:
            all_employees = db.get_employees_by_manager_name(effective_manager)
            employee_map = {emp['employee_id']: emp['name'] for emp in all_employees}
            employee_names = [employee_map.get(emp_id, emp_id) for emp_id in employee_ids]
        else:
            # Fallback: try to get employees from timecards
            timecards = db.get_timecards_by_pay_period(pay_period_end)
            if timecards:
                manager_id = timecards[0].get('manager_id')
                all_employees = db.get_employees_by_manager(manager_id)
                employee_map = {emp['employee_id']: emp['name'] for emp in all_employees}
                employee_names = [employee_map.get(emp_id, emp_id) for emp_id in employee_ids]
                effective_manager = config.agent_settings.manager_name
            else:
                # Final fallback: use IDs as names
                employee_names = employee_ids
                effective_manager = config.agent_settings.manager_name
        
        # Build the message
        message = f"""
Dear Team,

This is a friendly reminder that your timecard for the pay period ending {pay_period_end} has not been submitted yet.

Please submit your timecard as soon as possible to ensure timely processing and avoid any delays in your paycheck.

If you have any questions or need assistance, please don't hesitate to reach out.

Thank you for your attention to this matter.

Best regards,
{effective_manager}
        """.strip()
        
        return {
            "status": "success",
            "employee_ids": employee_ids,
            "employee_names": employee_names,
            "pay_period_end": pay_period_end,
            "manager_name": effective_manager,
            "message": message,
            "subject": f"Timecard Reminder - Pay Period Ending {pay_period_end}"
        }
        
    except Exception as e:
        logger.error(f"Error drafting reminder message: {e}")
        return {
            "status": "error",
            "message": f"Error drafting reminder: {str(e)}",
            "employee_ids": employee_ids,
            "pay_period_end": pay_period_end
        }
