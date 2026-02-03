"""
FastAPI routes for Dapr event subscriptions.

These endpoints handle incoming events from Dapr pub/sub.
"""

from fastapi import APIRouter, Request, Response, status
from typing import Dict
import logging

from ..services.event_subscriber import get_event_subscriber
from ..models.events.task_events import parse_task_event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/dapr/subscribe")
async def dapr_subscribe():
    """
    Dapr subscription endpoint.

    Returns the list of topics this service subscribes to.
    Dapr calls this endpoint to discover subscriptions.
    """
    subscriptions = [
        {
            "pubsubname": "pubsub",
            "topic": "task.created",
            "route": "/events/task/created",
        },
        {
            "pubsubname": "pubsub",
            "topic": "task.updated",
            "route": "/events/task/updated",
        },
        {
            "pubsubname": "pubsub",
            "topic": "task.deleted",
            "route": "/events/task/deleted",
        },
        {
            "pubsubname": "pubsub",
            "topic": "task.completed",
            "route": "/events/task/completed",
        },
    ]
    return subscriptions


@router.post("/task/created", status_code=status.HTTP_200_OK)
async def handle_task_created_event(request: Request):
    """Handle task.created events from Dapr."""
    try:
        event_data = await request.json()

        # Dapr wraps the event in a CloudEvent envelope
        # Extract the actual event data
        if "data" in event_data:
            event_data = event_data["data"]

        subscriber = get_event_subscriber()
        await subscriber.process_event(event_data)

        return {"success": True}
    except Exception as e:
        logger.error(f"Error processing task.created event: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/task/updated", status_code=status.HTTP_200_OK)
async def handle_task_updated_event(request: Request):
    """Handle task.updated events from Dapr."""
    try:
        event_data = await request.json()

        if "data" in event_data:
            event_data = event_data["data"]

        subscriber = get_event_subscriber()
        await subscriber.process_event(event_data)

        return {"success": True}
    except Exception as e:
        logger.error(f"Error processing task.updated event: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/task/deleted", status_code=status.HTTP_200_OK)
async def handle_task_deleted_event(request: Request):
    """Handle task.deleted events from Dapr."""
    try:
        event_data = await request.json()

        if "data" in event_data:
            event_data = event_data["data"]

        subscriber = get_event_subscriber()
        await subscriber.process_event(event_data)

        return {"success": True}
    except Exception as e:
        logger.error(f"Error processing task.deleted event: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/task/completed", status_code=status.HTTP_200_OK)
async def handle_task_completed_event(request: Request):
    """Handle task.completed events from Dapr."""
    try:
        event_data = await request.json()

        if "data" in event_data:
            event_data = event_data["data"]

        subscriber = get_event_subscriber()
        await subscriber.process_event(event_data)

        return {"success": True}
    except Exception as e:
        logger.error(f"Error processing task.completed event: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/health")
async def events_health_check():
    """Health check endpoint for event subscription service."""
    return {
        "status": "healthy",
        "service": "event-subscriber",
        "dapr_enabled": True,
    }
