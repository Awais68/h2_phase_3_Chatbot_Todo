"""
API routers for the application.
"""
from . import auth, tasks, sync, push, chat, analytics, recurring, history

__all__ = ["auth", "tasks", "sync", "push", "chat", "analytics", "recurring", "history"]
