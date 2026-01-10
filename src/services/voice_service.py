"""Voice input service with multi-turn conversation support."""

from typing import Optional, Any
from datetime import date
from src.models.voice_state import VoiceState
from src.models.enums import ConversationStep, Priority, Recurrence
from src.services.voice_normalizer import VoiceNormalizer

# Check if SpeechRecognition is available
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    sr = None  # type: ignore


class VoiceService:
    """Handles multi-turn voice input conversation for task creation.

    Uses a state machine approach to guide users through sequential prompts:
    1. User says "add task"
    2. System prompts for title
    3. System prompts for priority
    4. System prompts for due date
    5. System prompts for recurrence
    6. System shows confirmation summary

    Supports error recovery via "go back" command.
    """

    def __init__(self):
        """Initialize voice service."""
        if not VOICE_AVAILABLE:
            raise ImportError(
                "SpeechRecognition not installed. "
                "Install with: uv add SpeechRecognition PyAudio"
            )

        self.state = VoiceState()
        self.recognizer = sr.Recognizer()  # type: ignore
        self.normalizer = VoiceNormalizer()

    def is_available(self) -> bool:
        """Check if voice input is available.

        Returns:
            True if SpeechRecognition is installed, False otherwise
        """
        return VOICE_AVAILABLE

    def start_conversation(self) -> None:
        """Start voice conversation by listening for 'add task' command."""
        self.state.reset()
        self.state.current_step = ConversationStep.AWAITING_COMMAND
        print("🎤 Listening... Say 'add task'")

        try:
            audio = self._listen()
            command = self._transcribe(audio)

            if command and 'add task' in command.lower():
                print(f"✓ Command recognized: {command}")
                self.state.current_step = ConversationStep.AWAITING_TITLE
            else:
                print(f"❌ Command not recognized: '{command}'. Please say 'add task'")
                self.state.reset()

        except Exception as e:
            print(f"❌ Error: {e}")
            self.state.reset()

    def collect_title(self) -> Optional[str]:
        """Prompt for and collect task title.

        Returns:
            Collected title string, or None if failed
        """
        print("\n🎤 What's the task title?")

        try:
            audio = self._listen()
            title = self._transcribe(audio)

            if title:
                print(f"✓ Title: {title}")
                self.state.collected_data['title'] = title
                self.state.add_to_history(ConversationStep.AWAITING_TITLE)
                self.state.current_step = ConversationStep.AWAITING_PRIORITY
                return title
            else:
                print("❌ Could not understand title. Please try again.")
                return None

        except Exception as e:
            print(f"❌ Error collecting title: {e}")
            return None

    def collect_priority(self) -> Optional[Priority]:
        """Prompt for and collect priority with flexible normalization.

        Returns:
            Normalized Priority enum, or None if failed
        """
        print("\n🎤 What priority? Say high, medium, low, or none")

        try:
            audio = self._listen()
            priority_text = self._transcribe(audio)

            if priority_text:
                # Check for go back command
                if self.normalizer.is_go_back_command(priority_text):
                    self._handle_go_back()
                    return None

                # Normalize to Priority enum
                priority = self.normalizer.normalize_priority(priority_text)
                print(f"✓ Priority: {priority.value.title()}")

                self.state.collected_data['priority'] = priority
                self.state.add_to_history(ConversationStep.AWAITING_PRIORITY)
                self.state.current_step = ConversationStep.AWAITING_DUE_DATE
                return priority
            else:
                print("❌ Could not understand priority. Please try again.")
                return None

        except Exception as e:
            print(f"❌ Error collecting priority: {e}")
            return None

    def collect_due_date(self, date_parser_func) -> Optional[date]:
        """Prompt for and collect due date.

        Args:
            date_parser_func: Function to parse date strings (from lib.date_parser)

        Returns:
            Parsed date object, or None if no due date or failed
        """
        print("\n🎤 When is it due? Say a date or 'none'")

        try:
            audio = self._listen()
            date_text = self._transcribe(audio)

            if date_text:
                # Check for go back command
                if self.normalizer.is_go_back_command(date_text):
                    self._handle_go_back()
                    return None

                # Check if user said "none"
                if date_text.lower().strip() in ['none', 'no', 'skip']:
                    print("✓ Due Date: None")
                    self.state.collected_data['due_date'] = None
                    self.state.add_to_history(ConversationStep.AWAITING_DUE_DATE)
                    self.state.current_step = ConversationStep.AWAITING_RECURRENCE
                    return None

                # Parse date
                due_date = date_parser_func(date_text)
                if due_date:
                    print(f"✓ Due Date: {due_date}")
                    self.state.collected_data['due_date'] = due_date
                    self.state.add_to_history(ConversationStep.AWAITING_DUE_DATE)
                    self.state.current_step = ConversationStep.AWAITING_RECURRENCE
                    return due_date
                else:
                    print(f"❌ Could not parse date: '{date_text}'. Please try again or say 'none'")
                    return None
            else:
                print("❌ Could not understand date. Please try again.")
                return None

        except Exception as e:
            print(f"❌ Error collecting due date: {e}")
            return None

    def collect_recurrence(self) -> Optional[Recurrence]:
        """Prompt for and collect recurrence pattern.

        Returns:
            Normalized Recurrence enum, or None if failed
        """
        print("\n🎤 Any recurrence? Say daily, weekly, monthly, or none")

        try:
            audio = self._listen()
            recurrence_text = self._transcribe(audio)

            if recurrence_text:
                # Check for go back command
                if self.normalizer.is_go_back_command(recurrence_text):
                    self._handle_go_back()
                    return None

                # Normalize to Recurrence enum
                recurrence = self.normalizer.normalize_recurrence(recurrence_text)
                print(f"✓ Recurrence: {recurrence.value.title()}")

                self.state.collected_data['recurrence'] = recurrence
                self.state.add_to_history(ConversationStep.AWAITING_RECURRENCE)
                self.state.current_step = ConversationStep.CONFIRMATION
                return recurrence
            else:
                print("❌ Could not understand recurrence. Please try again.")
                return None

        except Exception as e:
            print(f"❌ Error collecting recurrence: {e}")
            return None

    def show_confirmation(self) -> dict[str, Any]:
        """Display summary and get final confirmation.

        Returns:
            Dictionary with collected data if confirmed, empty dict if cancelled
        """
        print("\n" + "="*50)
        print("Task Summary:")
        print("="*50)
        print(f"  Title: {self.state.collected_data.get('title', 'N/A')}")
        print(f"  Priority: {self.state.collected_data.get('priority', Priority.NONE).value.title()}")
        print(f"  Due Date: {self.state.collected_data.get('due_date', 'None')}")
        print(f"  Recurrence: {self.state.collected_data.get('recurrence', Recurrence.NONE).value.title()}")
        print("="*50)
        print("\n🎤 Say 'yes' to create, 'edit' to modify, or 'cancel'")

        try:
            audio = self._listen()
            response = self._transcribe(audio)

            if response:
                if self.normalizer.is_confirmation(response):
                    print("✓ Task confirmed!")
                    return self.state.collected_data.copy()
                elif 'edit' in response.lower():
                    print("📝 Edit mode not yet implemented. Please confirm or cancel.")
                    return {}
                elif self.normalizer.is_cancellation(response):
                    print("❌ Task creation cancelled")
                    self.state.reset()
                    return {}
                else:
                    print(f"❌ Response not understood: '{response}'. Say 'yes', 'edit', or 'cancel'")
                    return {}
            else:
                print("❌ Could not understand response")
                return {}

        except Exception as e:
            print(f"❌ Error in confirmation: {e}")
            return {}

    def _listen(self, timeout: int = 5) -> Any:
        """Listen for audio input from microphone.

        Args:
            timeout: Maximum seconds to wait for speech

        Returns:
            AudioData object from speech_recognition

        Raises:
            Exception if microphone unavailable or timeout
        """
        with sr.Microphone() as source:  # type: ignore
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🎧 Listening...")
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            return audio

    def _transcribe(self, audio) -> Optional[str]:
        """Transcribe audio to text using Google Speech Recognition API.

        Args:
            audio: AudioData object from speech_recognition

        Returns:
            Transcribed text string, or None if failed

        Raises:
            Exception if API request fails
        """
        try:
            # Use Google Speech Recognition API
            text = self.recognizer.recognize_google(audio)
            print(f"📝 You said: '{text}'")
            return text

        except sr.UnknownValueError:  # type: ignore
            print("❌ Could not understand audio. Please speak clearly.")
            return None

        except sr.RequestError as e:  # type: ignore
            print(f"❌ Voice service unavailable: {e}")
            print("Please use keyboard input instead.")
            raise

    def _handle_go_back(self) -> None:
        """Handle 'go back' command by returning to previous step."""
        previous_step = self.state.go_back()

        if previous_step:
            print(f"⬅️  Going back to {previous_step.value}")
            self.state.current_step = previous_step
        else:
            print("❌ Cannot go back further (already at beginning)")
            self.state.current_step = ConversationStep.AWAITING_TITLE
