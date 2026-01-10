"""
Event Publisher Service for Kafka Integration.

Publishes task events to Kafka topics for async processing.
Integrated with Dapr pub/sub component.
"""

import json
import logging
from typing import Optional
from datetime import datetime

from ..models.events.task_events import (
    BaseTaskEvent,
    TaskCreatedEvent,
    TaskUpdatedEvent,
    TaskDeletedEvent,
    TaskCompletedEvent,
)

logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Event publisher for task events.

    Publishes events to Kafka via Dapr pub/sub component.
    Supports both direct Kafka publishing and Dapr-based publishing.
    """

    def __init__(
        self,
        kafka_bootstrap_servers: Optional[str] = None,
        dapr_enabled: bool = True,
        dapr_pubsub_name: str = "pubsub",
    ):
        """
        Initialize event publisher.

        Args:
            kafka_bootstrap_servers: Kafka broker addresses (comma-separated)
            dapr_enabled: Whether to use Dapr for pub/sub
            dapr_pubsub_name: Dapr pub/sub component name
        """
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.dapr_enabled = dapr_enabled
        self.dapr_pubsub_name = dapr_pubsub_name
        self.producer = None

        if not dapr_enabled and kafka_bootstrap_servers:
            self._init_kafka_producer()

    def _init_kafka_producer(self):
        """Initialize Kafka producer (if not using Dapr)."""
        try:
            from kafka import KafkaProducer

            self.producer = KafkaProducer(
                bootstrap_servers=self.kafka_bootstrap_servers.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                acks="all",
                retries=3,
                compression_type="snappy",
                max_in_flight_requests_per_connection=5,
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            self.producer = None

    async def publish_event(self, event: BaseTaskEvent) -> bool:
        """
        Publish an event to the appropriate topic.

        Args:
            event: Event to publish

        Returns:
            True if published successfully, False otherwise
        """
        try:
            topic = self._get_topic_name(event.event_type)
            event_data = event.model_dump(mode="json")

            if self.dapr_enabled:
                return await self._publish_via_dapr(topic, event_data)
            else:
                return self._publish_via_kafka(topic, event_data, event.task_id)
        except Exception as e:
            logger.error(f"Failed to publish event {event.event_id}: {e}")
            return False

    async def _publish_via_dapr(self, topic: str, event_data: dict) -> bool:
        """Publish event via Dapr pub/sub."""
        try:
            import httpx

            # Dapr pub/sub endpoint
            dapr_url = f"http://localhost:3500/v1.0/publish/{self.dapr_pubsub_name}/{topic}"

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    dapr_url,
                    json=event_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5.0,
                )

                if response.status_code in (200, 204):
                    logger.info(f"Event published to topic {topic} via Dapr")
                    return True
                else:
                    logger.error(
                        f"Failed to publish via Dapr: {response.status_code} - {response.text}"
                    )
                    return False
        except Exception as e:
            logger.error(f"Error publishing via Dapr: {e}")
            return False

    def _publish_via_kafka(self, topic: str, event_data: dict, key: str) -> bool:
        """Publish event directly to Kafka."""
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return False

        try:
            future = self.producer.send(topic, value=event_data, key=key)
            record_metadata = future.get(timeout=10)
            logger.info(
                f"Event published to topic {topic} (partition {record_metadata.partition}, offset {record_metadata.offset})"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to publish to Kafka: {e}")
            return False

    def _get_topic_name(self, event_type: str) -> str:
        """Get Kafka topic name from event type."""
        # Map event types to Kafka topics
        topic_map = {
            "task.created": "task.created",
            "task.updated": "task.updated",
            "task.deleted": "task.deleted",
            "task.completed": "task.completed",
        }
        return topic_map.get(event_type, "task.events")

    async def publish_task_created(
        self, task_id: str, title: str, user_id: Optional[str] = None, **kwargs
    ) -> bool:
        """Convenience method to publish task created event."""
        event = TaskCreatedEvent(
            task_id=task_id, title=title, user_id=user_id, **kwargs
        )
        return await self.publish_event(event)

    async def publish_task_updated(
        self, task_id: str, changes: dict, user_id: Optional[str] = None, **kwargs
    ) -> bool:
        """Convenience method to publish task updated event."""
        event = TaskUpdatedEvent(
            task_id=task_id, changes=changes, user_id=user_id, **kwargs
        )
        return await self.publish_event(event)

    async def publish_task_deleted(
        self, task_id: str, task_title: str, user_id: Optional[str] = None, **kwargs
    ) -> bool:
        """Convenience method to publish task deleted event."""
        event = TaskDeletedEvent(
            task_id=task_id, task_title=task_title, user_id=user_id, **kwargs
        )
        return await self.publish_event(event)

    async def publish_task_completed(
        self, task_id: str, task_title: str, user_id: Optional[str] = None, **kwargs
    ) -> bool:
        """Convenience method to publish task completed event."""
        event = TaskCompletedEvent(
            task_id=task_id, task_title=task_title, user_id=user_id, **kwargs
        )
        return await self.publish_event(event)

    def close(self):
        """Close the event publisher and cleanup resources."""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")


# Global event publisher instance
_event_publisher: Optional[EventPublisher] = None


def get_event_publisher() -> EventPublisher:
    """Get or create the global event publisher instance."""
    global _event_publisher
    if _event_publisher is None:
        import os

        _event_publisher = EventPublisher(
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            dapr_enabled=os.getenv("DAPR_ENABLED", "true").lower() == "true",
            dapr_pubsub_name=os.getenv("DAPR_PUBSUB_NAME", "pubsub"),
        )
    return _event_publisher
