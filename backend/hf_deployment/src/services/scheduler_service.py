"""
Scheduler Service for background job management using APScheduler.

This service handles:
- Notification scheduling for due tasks
- Recurring task instance creation
- Daily history cleanup (2-year retention)
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import pytz
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# Standalone job functions (must be at module level for pickle serialization)

def cleanup_old_history_job():
    """
    Standalone function for cleaning up old history entries.
    This must be a module-level function for APScheduler to serialize it.
    """
    logger.info("Running daily history cleanup...")

    from sqlmodel import Session, select
    from src.db.session import engine
    from src.models.task_history import TaskHistory

    try:
        with Session(engine) as session:
            # Find and delete entries past retention period
            now = datetime.now(pytz.UTC)
            old_entries = session.exec(
                select(TaskHistory).where(TaskHistory.retention_until < now)
            ).all()

            count = len(old_entries)

            for entry in old_entries:
                session.delete(entry)

            session.commit()
            logger.info(f"Cleaned up {count} old history entries")

    except Exception as e:
        logger.error(f"History cleanup failed: {e}")


class SchedulerService:
    """Background job scheduler for recurring tasks and notifications."""

    def __init__(self, database_url: str):
        """
        Initialize scheduler with PostgreSQL job persistence.

        Args:
            database_url: PostgreSQL connection string for job store
        """
        jobstores = {
            'default': SQLAlchemyJobStore(url=database_url)
        }

        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            timezone=pytz.UTC
        )

        self._started = False

    def start(self):
        """Start the scheduler if not already running."""
        if not self._started:
            self.scheduler.start()
            self._started = True
            logger.info("SchedulerService started")

    def shutdown(self):
        """Shutdown the scheduler gracefully."""
        if self._started:
            self.scheduler.shutdown(wait=True)
            self._started = False
            logger.info("SchedulerService shutdown")

    def schedule_notification(
        self,
        task_id: int,
        task_title: str,
        due_date: datetime,
        reminder_minutes: int = 15
    ):
        """
        Schedule a notification for a task.

        Args:
            task_id: Task ID for notification
            task_title: Task title to display in notification
            due_date: When task is due (UTC)
            reminder_minutes: Minutes before due_date to send reminder

        Note:
            Frontend handles actual browser notification display.
            Backend schedules notification triggers and can send push notifications.
        """
        reminder_time = due_date - timedelta(minutes=reminder_minutes)

        # Only schedule if reminder time is in the future
        if reminder_time > datetime.now(pytz.UTC):
            self.scheduler.add_job(
                func=self._send_notification_trigger,
                trigger=DateTrigger(run_date=reminder_time),
                args=[task_id, task_title, reminder_minutes],
                id=f'notification_{task_id}_{reminder_minutes}',
                replace_existing=True
            )
            logger.info(f"Scheduled notification for task {task_id} at {reminder_time}")

        # Also schedule notification at exact due time
        if due_date > datetime.now(pytz.UTC):
            self.scheduler.add_job(
                func=self._send_notification_trigger,
                trigger=DateTrigger(run_date=due_date),
                args=[task_id, task_title, 0],
                id=f'notification_{task_id}_due',
                replace_existing=True
            )
            logger.info(f"Scheduled due notification for task {task_id} at {due_date}")

    def cancel_notification(self, task_id: int):
        """
        Cancel all scheduled notifications for a task.

        Args:
            task_id: Task ID to cancel notifications for
        """
        job_ids = [
            f'notification_{task_id}_15',  # Default reminder
            f'notification_{task_id}_due'  # Due time notification
        ]

        for job_id in job_ids:
            try:
                self.scheduler.remove_job(job_id)
                logger.info(f"Cancelled notification job {job_id}")
            except Exception:
                # Job may not exist, ignore
                pass

    def schedule_recurring_task_creation(
        self,
        task_id: int,
        recurrence_pattern: str,
        next_occurrence: datetime
    ):
        """
        Schedule creation of next recurring task instance.

        Args:
            task_id: Original recurring task ID
            recurrence_pattern: Pattern type (daily/weekly/monthly/yearly)
            next_occurrence: When to create next instance (UTC)
        """
        self.scheduler.add_job(
            func=self._create_recurring_task_instance,
            trigger=DateTrigger(run_date=next_occurrence),
            args=[task_id],
            id=f'recurring_task_{task_id}',
            replace_existing=True
        )
        logger.info(f"Scheduled recurring task creation for task {task_id} at {next_occurrence}")

    def schedule_history_cleanup(self):
        """
        Schedule daily cleanup of history entries older than 2 years.
        Runs at 2 AM UTC daily.
        """
        self.scheduler.add_job(
            func=cleanup_old_history_job,
            trigger=CronTrigger(hour=2, minute=0, timezone=pytz.UTC),
            id='history_cleanup_daily',
            replace_existing=True
        )
        logger.info("Scheduled daily history cleanup at 2 AM UTC")

    async def _send_notification_trigger(
        self,
        task_id: int,
        task_title: str,
        reminder_minutes: int
    ):
        """
        Backend notification trigger (placeholder for push service).

        In production, this would:
        1. Retrieve user's notification preferences
        2. Send push notification via service (e.g., Firebase Cloud Messaging)
        3. Log notification event

        Args:
            task_id: Task ID
            task_title: Task title for notification
            reminder_minutes: Minutes before due (0 = at due time)
        """
        logger.info(
            f"Notification trigger for task {task_id}: '{task_title}' "
            f"({'due now' if reminder_minutes == 0 else f'due in {reminder_minutes} minutes'})"
        )

        # TODO: Implement push notification sending
        # For now, frontend handles notifications via browser API
        pass

    async def _create_recurring_task_instance(self, original_task_id: int):
        """
        Create next instance of a recurring task.

        Args:
            original_task_id: ID of the recurring task template
        """
        logger.info(f"Creating recurring instance for task {original_task_id}")

        # Import here to avoid circular dependency
        from .task_service import TaskService

        try:
            task_service = TaskService()
            await task_service.create_recurring_instance(original_task_id)
            logger.info(f"Successfully created recurring instance for task {original_task_id}")
        except Exception as e:
            logger.error(f"Failed to create recurring instance for task {original_task_id}: {e}")



# Global scheduler instance (initialized on app startup)
scheduler_service: Optional[SchedulerService] = None


def get_scheduler() -> SchedulerService:
    """
    Get the global scheduler instance.

    Returns:
        SchedulerService instance

    Raises:
        RuntimeError: If scheduler not initialized
    """
    if scheduler_service is None:
        raise RuntimeError("SchedulerService not initialized. Call initialize_scheduler() on startup.")
    return scheduler_service


def initialize_scheduler(database_url: str) -> SchedulerService:
    """
    Initialize the global scheduler instance.

    Args:
        database_url: PostgreSQL connection string

    Returns:
        Initialized SchedulerService instance
    """
    global scheduler_service

    if scheduler_service is None:
        scheduler_service = SchedulerService(database_url)
        scheduler_service.start()
        scheduler_service.schedule_history_cleanup()
        logger.info("SchedulerService initialized and history cleanup scheduled")

    return scheduler_service


def shutdown_scheduler():
    """Shutdown the global scheduler instance."""
    global scheduler_service

    if scheduler_service is not None:
        scheduler_service.shutdown()
        scheduler_service = None
        logger.info("SchedulerService shutdown complete")
