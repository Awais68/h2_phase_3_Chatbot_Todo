"""
Voice command parsing for task management.
Supports natural language commands for all task operations.
"""

import re
from typing import Optional
from dataclasses import dataclass
from datetime import date


@dataclass
class VoiceCommand:
    """Parsed voice command structure."""
    action: str  # add, list, update, delete, complete, filter, search, sort
    task_id: Optional[int] = None
    title: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[list[str]] = None
    filter_type: Optional[str] = None  # status, priority, tag
    filter_value: Optional[str] = None
    search_keyword: Optional[str] = None
    sort_by: Optional[str] = None  # priority, due_date, created_date


def parse_voice_command(text: str) -> Optional[VoiceCommand]:
    """
    Parse natural language voice command into structured command.

    Args:
        text: Voice command text

    Returns:
        VoiceCommand object if parsed successfully, None otherwise
    """
    if not text or not text.strip():
        return None

    text = text.lower().strip()

    # Add task command
    if any(phrase in text for phrase in ["add task", "create task", "new task"]):
        return _parse_add_command(text)

    # List/Show tasks
    if any(phrase in text for phrase in ["list tasks", "show tasks", "display tasks", "view tasks"]):
        return VoiceCommand(action="list")

    # Update task
    if any(phrase in text for phrase in ["update task", "edit task", "modify task"]):
        return _parse_update_command(text)

    # Delete task
    if any(phrase in text for phrase in ["delete task", "remove task"]):
        return _parse_delete_command(text)

    # Complete task
    if any(phrase in text for phrase in ["complete task", "finish task", "mark task complete", "mark task done"]):
        return _parse_complete_command(text)

    # Filter command
    if any(phrase in text for phrase in ["filter by", "show only", "filter tasks"]):
        return _parse_filter_command(text)

    # Search command
    if any(phrase in text for phrase in ["search", "find", "look for"]):
        return _parse_search_command(text)

    # Sort command
    if any(phrase in text for phrase in ["sort by", "order by"]):
        return _parse_sort_command(text)

    return None


def _parse_add_command(text: str) -> Optional[VoiceCommand]:
    """Parse add task command."""
    # Extract title (after "add task" or similar)
    patterns = [
        r"(?:add|create|new)\s+task\s+(.+?)(?:\s+priority|\s+due|\s+tags?|$)",
        r"(?:add|create|new)\s+task\s+(.+)"
    ]

    title = None
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            title = match.group(1).strip()
            break

    if not title:
        return None

    # Extract priority
    priority = None
    if "high priority" in text or "priority high" in text:
        priority = "high"
    elif "medium priority" in text or "priority medium" in text:
        priority = "medium"
    elif "low priority" in text or "priority low" in text:
        priority = "low"

    # Extract due date
    due_date = None
    due_patterns = [
        r"due\s+(?:date\s+)?(.+?)(?:\s+tags?|$)",
        r"deadline\s+(.+?)(?:\s+tags?|$)"
    ]
    for pattern in due_patterns:
        match = re.search(pattern, text)
        if match:
            due_date = match.group(1).strip()
            break

    # Extract tags
    tags = None
    tag_match = re.search(r"tags?\s+(.+?)$", text)
    if tag_match:
        tag_str = tag_match.group(1).strip()
        tags = [t.strip() for t in re.split(r"[,\s]+", tag_str) if t.strip()]

    return VoiceCommand(
        action="add",
        title=title,
        priority=priority,
        due_date=due_date,
        tags=tags
    )


def _parse_update_command(text: str) -> Optional[VoiceCommand]:
    """Parse update task command."""
    # Extract task ID
    id_match = re.search(r"(?:task\s+)?(?:number\s+)?(\d+)", text)
    if not id_match:
        return None

    task_id = int(id_match.group(1))

    # Extract new title
    title = None
    title_patterns = [
        r"(?:new\s+)?title\s+(.+?)(?:\s+priority|\s+due|$)",
        r"(?:rename\s+to|change\s+to)\s+(.+?)(?:\s+priority|\s+due|$)"
    ]
    for pattern in title_patterns:
        match = re.search(pattern, text)
        if match:
            title = match.group(1).strip()
            break

    return VoiceCommand(
        action="update",
        task_id=task_id,
        title=title
    )


def _parse_delete_command(text: str) -> Optional[VoiceCommand]:
    """Parse delete task command."""
    # Extract task ID
    id_match = re.search(r"(?:task\s+)?(?:number\s+)?(\d+)", text)
    if not id_match:
        return None

    return VoiceCommand(
        action="delete",
        task_id=int(id_match.group(1))
    )


def _parse_complete_command(text: str) -> Optional[VoiceCommand]:
    """Parse complete task command."""
    # Extract task ID
    id_match = re.search(r"(?:task\s+)?(?:number\s+)?(\d+)", text)
    if not id_match:
        return None

    return VoiceCommand(
        action="complete",
        task_id=int(id_match.group(1))
    )


def _parse_filter_command(text: str) -> Optional[VoiceCommand]:
    """Parse filter command."""
    # Determine filter type
    if "status" in text:
        # Extract status value
        if "pending" in text:
            filter_value = "pending"
        elif "completed" in text or "complete" in text:
            filter_value = "completed"
        elif "overdue" in text:
            filter_value = "overdue"
        else:
            filter_value = None

        return VoiceCommand(
            action="filter",
            filter_type="status",
            filter_value=filter_value
        )

    elif "priority" in text:
        # Extract priority value
        if "high" in text:
            filter_value = "high"
        elif "medium" in text:
            filter_value = "medium"
        elif "low" in text:
            filter_value = "low"
        else:
            filter_value = None

        return VoiceCommand(
            action="filter",
            filter_type="priority",
            filter_value=filter_value
        )

    elif "tag" in text:
        # Extract tag value
        tag_match = re.search(r"tag\s+(.+?)$", text)
        if tag_match:
            filter_value = tag_match.group(1).strip()
        else:
            filter_value = None

        return VoiceCommand(
            action="filter",
            filter_type="tag",
            filter_value=filter_value
        )

    return None


def _parse_search_command(text: str) -> Optional[VoiceCommand]:
    """Parse search command."""
    # Extract search keyword
    patterns = [
        r"(?:search|find|look\s+for)\s+(?:task\s+)?(.+?)$",
        r"(?:search|find|look\s+for)\s+(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            keyword = match.group(1).strip()
            return VoiceCommand(
                action="search",
                search_keyword=keyword
            )

    return None


def _parse_sort_command(text: str) -> Optional[VoiceCommand]:
    """Parse sort command."""
    sort_by = None

    if "priority" in text:
        sort_by = "priority"
    elif "due date" in text or "deadline" in text:
        sort_by = "due_date"
    elif "created" in text or "creation" in text:
        sort_by = "created_date"

    if sort_by:
        return VoiceCommand(
            action="sort",
            sort_by=sort_by
        )

    return None


def get_voice_input() -> Optional[str]:
    """
    Capture voice input from microphone using speech recognition.

    Returns:
        Transcribed text if successful, None otherwise
    """
    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening... (speak now)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        print("Processing...")
        text = recognizer.recognize_google(audio)
        return text

    except ImportError:
        print("Error: speech_recognition package not installed")
        print("Install with: uv add SpeechRecognition")
        return None
    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.")
        return None
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from speech service: {e}")
        return None
    except Exception as e:
        print(f"Error capturing voice input: {e}")
        return None
