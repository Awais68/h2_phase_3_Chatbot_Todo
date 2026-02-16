"""
Enhanced Backend Validation for Shopping List Persistence
Ensures data integrity at the database layer

Add these validations to backend/todo_chatbot/src/services/task_service.py
"""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ShoppingListValidationError(Exception):
    """Custom exception for shopping list validation errors"""
    pass


def validate_shopping_list_structure(shopping_list: Optional[List[Dict[str, Any]]]) -> tuple[bool, List[str], List[Dict[str, Any]]]:
    """
    Validate and sanitize shopping list data structure
    
    Args:
        shopping_list: Raw shopping list data from frontend
        
    Returns:
        Tuple of (is_valid, errors, sanitized_list)
    """
    errors = []
    
    # None or empty list is valid
    if shopping_list is None:
        return True, [], []
    
    if not isinstance(shopping_list, list):
        errors.append("shopping_list must be an array")
        return False, errors, []
    
    sanitized_list = []
    
    for idx, category in enumerate(shopping_list):
        # Validate category is a dictionary
        if not isinstance(category, dict):
            errors.append(f"Category at index {idx} must be an object")
            continue
        
        # Validate required category fields
        if 'id' not in category or not category['id']:
            errors.append(f"Category at index {idx} missing 'id' field")
            continue
            
        if 'name' not in category or not category['name']:
            errors.append(f"Category at index {idx} missing 'name' field")
            continue
        
        if 'items' not in category:
            errors.append(f"Category '{category.get('name')}' missing 'items' field")
            continue
        
        if not isinstance(category['items'], list):
            errors.append(f"Category '{category['name']}' items must be an array")
            continue
        
        # Validate and sanitize items
        sanitized_items = []
        
        for item_idx, item in enumerate(category['items']):
            if not isinstance(item, dict):
                errors.append(f"Item {item_idx} in category '{category['name']}' must be an object")
                continue
            
            # Validate required item fields
            required_fields = ['id', 'name', 'price', 'quantity']
            missing_fields = [f for f in required_fields if f not in item or item[f] is None]
            
            if missing_fields:
                errors.append(
                    f"Item {item_idx} in category '{category['name']}' missing fields: {', '.join(missing_fields)}"
                )
                continue
            
            # Validate data types and values
            try:
                item_id = str(item['id'])
                item_name = str(item['name']).strip()
                item_price = float(item['price'])
                item_quantity = int(item['quantity'])
                item_completed = bool(item.get('completed', False))
                
                # Validate constraints
                if not item_name:
                    errors.append(f"Item {item_idx} in category '{category['name']}' has empty name")
                    continue
                
                if item_price < 0:
                    errors.append(f"Item '{item_name}' has negative price: {item_price}")
                    item_price = 0  # Auto-correct to 0
                
                if item_quantity < 0:
                    errors.append(f"Item '{item_name}' has negative quantity: {item_quantity}")
                    item_quantity = 1  # Auto-correct to 1
                
                # Add sanitized item
                sanitized_items.append({
                    'id': item_id,
                    'name': item_name,
                    'price': item_price,
                    'quantity': item_quantity,
                    'completed': item_completed,
                })
                
            except (ValueError, TypeError) as e:
                errors.append(
                    f"Item {item_idx} in category '{category['name']}' has invalid data type: {str(e)}"
                )
                continue
        
        # Only add category if it has valid items
        if sanitized_items:
            sanitized_list.append({
                'id': str(category['id']),
                'name': str(category['name']).strip(),
                'items': sanitized_items,
            })
    
    is_valid = len(errors) == 0
    return is_valid, errors, sanitized_list


def log_shopping_list_update(task_id: int, user_id: int, shopping_list: List[Dict[str, Any]]):
    """
    Log shopping list updates for debugging and monitoring
    
    Args:
        task_id: Task ID
        user_id: User ID
        shopping_list: Shopping list data
    """
    try:
        num_categories = len(shopping_list)
        num_items = sum(len(cat['items']) for cat in shopping_list)
        completed_items = sum(
            sum(1 for item in cat['items'] if item.get('completed', False))
            for cat in shopping_list
        )
        
        logger.info(
            f"✅ Updated shopping list for task {task_id} (user {user_id}): "
            f"{num_categories} categories, {num_items} items ({completed_items} completed)"
        )
        
        # Log detailed info at debug level
        for category in shopping_list:
            logger.debug(
                f"  Category '{category['name']}': {len(category['items'])} items"
            )
            for item in category['items']:
                status = "✓" if item.get('completed') else "○"
                logger.debug(
                    f"    {status} {item['name']} - "
                    f"${item['price']:.2f} x {item['quantity']}"
                )
                
    except Exception as e:
        logger.warning(f"Failed to log shopping list update: {str(e)}")


# ENHANCED UPDATE FUNCTION - Add this to task_service.py

def update_task_enhanced(session, task_id: int, task_data, user_id: int):
    """
    Enhanced task update with shopping list validation
    
    REPLACE the existing update_task function with this version
    """
    from src.services.task_service import TaskService
    from datetime import datetime
    
    # Get existing task
    task = TaskService.get_task_by_id(session, task_id, user_id)
    if not task:
        return None

    # Track completion status for history
    was_incomplete = not task.completed
    is_being_completed = task_data.completed is True

    # Update standard fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    if task_data.category is not None:
        task.category = task_data.category
    if task_data.tags is not None:
        task.tags = task_data.tags
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.recursion is not None:
        task.recursion = task_data.recursion
    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    # ENHANCED: Validate and sanitize shopping list
    if task_data.shopping_list is not None:
        is_valid, errors, sanitized = validate_shopping_list_structure(task_data.shopping_list)
        
        if errors:
            # Log warnings but don't fail - use sanitized version
            logger.warning(
                f"Shopping list validation warnings for task {task_id}: "
                f"{len(errors)} issues found, using sanitized version"
            )
            for error in errors[:5]:  # Log first 5 errors
                logger.warning(f"  - {error}")
        
        # Store sanitized shopping list
        task.shopping_list = sanitized
        
        # Log the update for monitoring
        log_shopping_list_update(task_id, user_id, sanitized)
        
        # CRITICAL: Ensure empty shopping list is explicitly saved as empty array
        if not sanitized:
            logger.info(f"Task {task_id} shopping list cleared (empty array saved)")
    
    # ENHANCED: Update subitems with validation (existing logic)
    if task_data.subitems is not None:
        if isinstance(task_data.subitems, list):
            task.subitems = task_data.subitems
        else:
            logger.warning(f"Invalid subitems format for task {task_id}, ignoring")

    # Update metadata
    task.updated_at = datetime.utcnow()
    task.version += 1

    # Commit to database
    try:
        session.add(task)
        session.commit()
        session.refresh(task)
        
        logger.info(f"✅ Task {task_id} updated successfully (version {task.version})")
        
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Failed to update task {task_id}: {str(e)}")
        raise

    # Create history entry if task completed
    if was_incomplete and is_being_completed:
        from src.services.history_service import HistoryService
        from src.models.task_history import HistoryActionType
        try:
            HistoryService.create_history_entry(
                session=session,
                task=task,
                action_type=HistoryActionType.COMPLETED,
                action_by=user_id
            )
            logger.info(f"Created history entry for completed task {task_id}")
        except Exception as e:
            logger.warning(f"Failed to create history entry for task {task_id}: {str(e)}")

    return task


# DATABASE CONSISTENCY CHECK - Run periodically or on-demand

def check_shopping_list_consistency(session):
    """
    Check all tasks for shopping list data consistency
    Returns report of any issues found
    
    Can be run as a management command or scheduled task
    """
    from src.models.task import Task
    
    report = {
        'total_tasks': 0,
        'tasks_with_shopping_list': 0,
        'tasks_with_invalid_data': 0,
        'issues': [],
    }
    
    tasks = session.query(Task).all()
    report['total_tasks'] = len(tasks)
    
    for task in tasks:
        if task.shopping_list:
            report['tasks_with_shopping_list'] += 1
            
            # Validate structure
            is_valid, errors, _ = validate_shopping_list_structure(task.shopping_list)
            
            if not is_valid:
                report['tasks_with_invalid_data'] += 1
                report['issues'].append({
                    'task_id': task.id,
                    'task_title': task.title,
                    'errors': errors,
                })
    
    logger.info(
        f"Shopping list consistency check complete: "
        f"{report['tasks_with_shopping_list']}/{report['total_tasks']} tasks have shopping lists, "
        f"{report['tasks_with_invalid_data']} have issues"
    )
    
    return report


# USAGE IN ROUTES

"""
In your FastAPI route handler:

from src.services.task_service_enhanced import update_task_enhanced

@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db)
):
    try:
        task = update_task_enhanced(session, task_id, task_data, user_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {
            "status": "success",
            "task": task,
            "message": "Task updated successfully"
        }
        
    except ShoppingListValidationError as e:
        logger.error(f"Shopping list validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid shopping list data: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
"""


# LOGGING CONFIGURATION

"""
Add to your logging configuration:

[loggers]
keys=root,task_service

[logger_task_service]
level=INFO
handlers=console,file
qualname=task_service
propagate=0

[handlers]
keys=console,file

[handler_file]
class=handlers.RotatingFileHandler
level=INFO
formatter=detailed
args=('logs/task_service.log', 'a', 10485760, 5)

This will create detailed logs in logs/task_service.log with:
- All shopping list updates
- Validation warnings
- Sync operations
- Error details
"""
