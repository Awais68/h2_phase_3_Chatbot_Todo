"""
Sync service for offline change synchronization.
"""
from typing import List, Dict, Any
from datetime import datetime
from sqlmodel import Session, select
from src.models.sync_operation import SyncOperation, SyncOperationType
from src.models.task import Task, TaskCreate, TaskUpdate
from src.services.task_service import TaskService
import json


class SyncService:
    """Service for synchronizing offline changes."""

    @staticmethod
    def sync_operations(
        session: Session, user_id: int, operations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synchronize a batch of offline operations.

        Args:
            session: Database session
            user_id: ID of the user
            operations: List of operations to synchronize

        Returns:
            Dict containing sync results with success status, conflicts, and server updates
        """
        synced_count = 0
        conflicts = []
        server_updates = []

        for operation in operations:
            op_type = operation.get("type")
            client_id = operation.get("client_id")
            payload = operation.get("payload", {})

            try:
                if op_type == SyncOperationType.CREATE:
                    # Check if task already exists (duplicate sync)
                    existing_task = TaskService.get_task_by_client_id(session, client_id, user_id)
                    if existing_task:
                        # Already synced, skip
                        synced_count += 1
                        continue

                    # Create new task
                    task_data = TaskCreate(**payload, client_id=client_id)
                    task = TaskService.create_task(session, user_id, task_data)
                    server_updates.append({
                        "type": "create",
                        "client_id": client_id,
                        "server_id": task.id,
                        "task": task.model_dump()
                    })
                    synced_count += 1

                elif op_type == SyncOperationType.UPDATE:
                    task_id = payload.get("id")
                    client_version = payload.get("version", 1)

                    # Get current task version
                    task = TaskService.get_task_by_id(session, task_id, user_id)
                    if not task:
                        conflicts.append({
                            "type": "not_found",
                            "task_id": task_id,
                            "message": "Task not found on server"
                        })
                        continue

                    # Check for version conflict
                    if task.version > client_version:
                        conflicts.append({
                            "type": "version_conflict",
                            "task_id": task_id,
                            "client_version": client_version,
                            "server_version": task.version,
                            "server_task": task.model_dump()
                        })
                        continue

                    # Update task
                    update_data = TaskUpdate(
                        title=payload.get("title"),
                        description=payload.get("description"),
                        completed=payload.get("completed")
                    )
                    updated_task = TaskService.update_task(session, task_id, user_id, update_data)
                    if updated_task:
                        server_updates.append({
                            "type": "update",
                            "task_id": task_id,
                            "task": updated_task.model_dump()
                        })
                        synced_count += 1

                elif op_type == SyncOperationType.DELETE:
                    task_id = payload.get("id")
                    deleted = TaskService.delete_task(session, task_id, user_id)
                    if deleted:
                        server_updates.append({
                            "type": "delete",
                            "task_id": task_id
                        })
                        synced_count += 1

            except Exception as e:
                conflicts.append({
                    "type": "error",
                    "operation": operation,
                    "message": str(e)
                })

        return {
            "success": True,
            "synced_count": synced_count,
            "conflicts": conflicts,
            "server_updates": server_updates
        }

    @staticmethod
    def get_pending_operations(session: Session, user_id: int) -> List[SyncOperation]:
        """
        Get all pending sync operations for a user.

        Args:
            session: Database session
            user_id: ID of the user

        Returns:
            List[SyncOperation]: List of pending operations
        """
        statement = (
            select(SyncOperation)
            .where(SyncOperation.user_id == user_id, SyncOperation.is_synced == False)
            .order_by(SyncOperation.created_at)
        )
        return list(session.exec(statement).all())

    @staticmethod
    def mark_operations_synced(session: Session, operation_ids: List[int]) -> None:
        """
        Mark sync operations as completed.

        Args:
            session: Database session
            operation_ids: List of operation IDs to mark as synced
        """
        for op_id in operation_ids:
            operation = session.get(SyncOperation, op_id)
            if operation:
                operation.is_synced = True
                operation.synced_at = datetime.utcnow()
                session.add(operation)

        session.commit()
