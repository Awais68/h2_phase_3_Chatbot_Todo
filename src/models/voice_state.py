"""Voice conversation state management for multi-turn voice input."""

from dataclasses import dataclass, field
from typing import Any
from src.models.enums import ConversationStep


@dataclass
class VoiceState:
    """Tracks state of multi-turn voice conversation.

    Attributes:
        current_step: Current step in the conversation flow
        collected_data: Dictionary of collected field values (title, priority, due_date, recurrence)
        step_history: Stack of previous steps for "go back" functionality
        confidence_scores: Recognition confidence for each field (0.0-1.0)
    """
    current_step: ConversationStep = ConversationStep.IDLE
    collected_data: dict[str, Any] = field(default_factory=dict)
    step_history: list[ConversationStep] = field(default_factory=list)
    confidence_scores: dict[str, float] = field(default_factory=dict)

    def reset(self) -> None:
        """Reset state to initial values."""
        self.current_step = ConversationStep.IDLE
        self.collected_data.clear()
        self.step_history.clear()
        self.confidence_scores.clear()

    def go_back(self) -> ConversationStep | None:
        """Return to previous step in conversation.

        Returns:
            Previous ConversationStep if history exists, None otherwise
        """
        if self.step_history:
            previous_step = self.step_history.pop()
            self.current_step = previous_step
            return previous_step
        return None

    def add_to_history(self, step: ConversationStep) -> None:
        """Add current step to history before advancing.

        Args:
            step: ConversationStep to add to history
        """
        self.step_history.append(step)

    def is_complete(self) -> bool:
        """Check if all required fields have been collected.

        Returns:
            True if title is present (minimum requirement), False otherwise
        """
        return 'title' in self.collected_data and bool(self.collected_data['title'])
