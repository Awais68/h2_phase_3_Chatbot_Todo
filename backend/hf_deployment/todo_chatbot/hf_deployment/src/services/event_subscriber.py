"""
Event Subscriber Service for Kafka Integration.

Subscribes to task events from Kafka topics for analytics,
notifications, and other async processing.
"""

import json
import logging
from typing import Optional, Callable, Dict
from datetime import datetime

from ..models.events.task_events import (
    BaseTaskEvent,
    TaskCreatedEvent,
    TaskUpdatedEvent,
    TaskDeletedEvent,
    TaskCompletedEvent,
    parse_task_event,
)

logger = logging.getLogger(__name__)


class EventSubscriber:
    """
    Event subscriber for task events.

    Subscribes to Kafka topics via Dapr or directly to process events.
    Supports custom event handlers for different event types.
    """

    def __init__(
        self,
        kafka_bootstrap_servers: Optional[str] = None,
        kafka_group_id: str = "todo-app-consumer-group",
        dapr_enabled: bool = True,
    ):
        """
        Initialize event subscriber.

        Args:
            kafka_bootstrap_servers: Kafka broker addresses (comma-separated)
            kafka_group_id: Kafka consumer group ID
            dapr_enabled: Whether to use Dapr for pub/sub
        """
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_group_id = kafka_group_id
        self.dapr_enabled = dapr_enabled
        self.consumer = None
        self.handlers: Dict[str, list[Callable]] = {}
        self.running = False

        if not dapr_enabled and kafka_bootstrap_servers:
            self._init_kafka_consumer()

    def _init_kafka_consumer(self):
        """Initialize Kafka consumer (if not using Dapr)."""
        try:
            from kafka import KafkaConsumer

            self.consumer = KafkaConsumer(
                "task.created",
                "task.updated",
                "task.deleted",
                "task.completed",
                bootstrap_servers=self.kafka_bootstrap_servers.split(","),
                group_id=self.kafka_group_id,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                max_poll_records=100,
            )
            logger.info("Kafka consumer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            self.consumer = None

    def register_handler(self, event_type: str, handler: Callable):
        """
        Register a handler for a specific event type.

        Args:
            event_type: Type of event to handle (e.g., "task.created")
            handler: Async function to handle the event
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        logger.info(f"Registered handler for event type: {event_type}")

    async def process_event(self, event_data: dict):
        """
        Process a single event.

        Args:
            event_data: Raw event data dictionary
        """
        try:
            event = parse_task_event(event_data)
            event_type = event.event_type

            # Call registered handlers
            handlers = self.handlers.get(event_type, [])
            for handler in handlers:
                try:
                    await handler(event)
                except Exception as e:
                    logger.error(f"Error in handler for {event_type}: {e}")

            # Log event processing
            logger.info(
                f"Processed event {event.event_id} of type {event_type}"
            )
        except Exception as e:
            logger.error(f"Failed to process event: {e}")

    async def start_consuming(self):
        """Start consuming events from Kafka."""
        if self.dapr_enabled:
            logger.info("Event subscription via Dapr (HTTP endpoints)")
            # With Dapr, events are pushed to HTTP endpoints
            # The FastAPI routes handle the subscription
            return

        if not self.consumer:
            logger.error("Kafka consumer not initialized")
            return

        self.running = True
        logger.info("Starting Kafka event consumer")

        try:
            while self.running:
                message_batch = self.consumer.poll(timeout_ms=1000)
                for topic_partition, messages in message_batch.items():
                    for message in messages:
                        await self.process_event(message.value)
        except Exception as e:
            logger.error(f"Error in consumer loop: {e}")
        finally:
            self.running = False

    def stop_consuming(self):
        """Stop consuming events."""
        self.running = False
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")


# Example event handlers

async def handle_task_created(event: TaskCreatedEvent):
    """
    Handle task created events.

    Example: Send notification, update analytics, etc.
    """
    logger.info(
        f"Task created: {event.task_id} - {event.title} by user {event.user_id}"
    )
    # TODO: Implement actual notification logic
    # await send_notification(event.user_id, f"Task created: {event.title}")


async def handle_task_updated(event: TaskUpdatedEvent):
    """
    Handle task updated events.

    Example: Log changes, update search index, etc.
    """
    logger.info(
        f"Task updated: {event.task_id} - Changes: {event.changes}"
    )
    # TODO: Implement actual update logic
    # await update_search_index(event.task_id, event.changes)


async def handle_task_deleted(event: TaskDeletedEvent):
    """
    Handle task deleted events.

    Example: Archive task, cleanup resources, etc.
    """
    logger.info(
        f"Task deleted: {event.task_id} - {event.task_title} (soft: {event.soft_delete})"
    )
    # TODO: Implement actual cleanup logic
    # await archive_task(event.task_id)


async def handle_task_completed(event: TaskCompletedEvent):
    """
    Handle task completed events.

    Example: Update statistics, send congratulations, etc.
    """
    logger.info(
        f"Task completed: {event.task_id} - {event.task_title} (time: {event.time_to_complete}s)"
    )
    # TODO: Implement actual completion logic
    # await send_congratulations(event.user_id, event.task_title)


# Global event subscriber instance
_event_subscriber: Optional[EventSubscriber] = None


def get_event_subscriber() -> EventSubscriber:
    """Get or create the global event subscriber instance."""
    global _event_subscriber
    if _event_subscriber is None:
        import os

        _event_subscriber = EventSubscriber(
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            kafka_group_id=os.getenv("KAFKA_GROUP_ID", "todo-app-consumer-group"),
            dapr_enabled=os.getenv("DAPR_ENABLED", "true").lower() == "true",
        )

        # Register default handlers
        _event_subscriber.register_handler("task.created", handle_task_created)
        _event_subscriber.register_handler("task.updated", handle_task_updated)
        _event_subscriber.register_handler("task.deleted", handle_task_deleted)
        _event_subscriber.register_handler("task.completed", handle_task_completed)

    return _event_subscriber
