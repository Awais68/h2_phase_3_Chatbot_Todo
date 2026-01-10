# Voice Interface Contract

**Branch**: `003-phase1-task-mgmt` | **Date**: 2025-12-27

## Voice Conversation Flow

### State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  IDLE ─────→ AWAITING_COMMAND ────→ AWAITING_TITLE                         │
│     ↑              ↓                       ↓                               │
│     │              │                       │                               │
│     │              └───────────────────────┘                               │
│     │                      (repeat "add task")                             │
│     ↓                                                                      │
│  CONFIRMATION ←──── AWAITING_RECURRENCE ←──── AWAITING_DUE_DATE            │
│     ↑                                          ↓                           │
│     │                                          │                           │
│     └──────────────────────────────────────────┘                           │
│                (go back to any field)                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step Details

| Step | Prompt | Expected Input | Normalized Output |
|------|--------|----------------|-------------------|
| AWAITING_COMMAND | "Say 'add task' to begin" | "add task" | Command recognized |
| AWAITING_TITLE | "What is the task title?" | Any phrase | Title string |
| AWAITING_PRIORITY | "What priority? Say high, medium, low, or none" | "high"/"very high"/"make it high" | `Priority.HIGH` |
| AWAITING_DUE_DATE | "When is it due? Say a date or 'none'" | "tomorrow"/"next Friday"/"2025-12-31"/"none" | date or None |
| AWAITING_RECURRENCE | "Any recurrence? Say daily, weekly, monthly, or none" | "daily"/"once a week" | `Recurrence.DAILY` |
| CONFIRMATION | "Review: Title: X, Priority: HIGH, Due: tomorrow, Recurrence: none. Say 'confirm' to save or 'edit [field]' to change" | "confirm"/"edit priority"/"edit due date" | Action |

---

## Audio Prompts

### System Prompts (TTS or Display)

| Step | Audio/Visual Prompt |
|------|---------------------|
| Activation | "Listening for command. Say 'add task' to create a new task." |
| Command recognized | "Adding new task. What is the task title?" |
| Listening for title | "Listening... Say the task title." |
| Title confirmed | "Title: [recognized]. What priority? Say high, medium, low, or none." |
| Priority confirmed | "Priority: [normalized]. When is it due? Say a date or 'none'." |
| Due date confirmed | "Due: [date]. Any recurrence? Say daily, weekly, monthly, or none." |
| Recurrence confirmed | "Recurrence: [pattern]. Review your task: [summary]. Say 'confirm' to save." |
| Confirmation | "Task created successfully! What would you like to do next?" |

### Error Prompts

| Error | Prompt |
|-------|--------|
| Command not recognized | "I didn't catch that. Say 'add task' to create a new task." |
| Low confidence | "I didn't quite hear that. Please repeat." |
| Unclear speech | "I'm having trouble understanding. You can say 'type instead' to switch to keyboard." |
| No microphone | "Microphone not available. Please use keyboard input." |

---

## Input Normalization

### Priority Normalization

| Input Phrase | Normalized Output |
|--------------|-------------------|
| "high", "very high", "highest", "make it high", "urgent" | `Priority.HIGH` |
| "medium", "med", "normal", "moderate" | `Priority.MEDIUM` |
| "low", "very low", "not important" | `Priority.LOW` |
| "none", "no priority", "unset" | `Priority.NONE` |

### Date Normalization

| Input Phrase | Normalized Output |
|--------------|-------------------|
| "today", "right now" | `date.today()` |
| "tomorrow", "tmr" | `date.today() + timedelta(days=1)` |
| "yesterday" | `date.today() - timedelta(days=1)` |
| "next week" | `date.today() + timedelta(days=7)` |
| "next Monday", "next Friday", etc. | Next occurrence of weekday |
| "2025-12-31", "12/31/2025" | `date(2025, 12, 31)` |
| "none", "no due date", "unset" | `None` |

### Recurrence Normalization

| Input Phrase | Normalized Output |
|--------------|-------------------|
| "daily", "every day", "once a day" | `Recurrence.DAILY` |
| "weekly", "every week", "once a week" | `Recurrence.WEEKLY` |
| "monthly", "every month", "once a month" | `Recurrence.MONTHLY` |
| "none", "no recurrence", "one time" | `Recurrence.NONE` |

---

## Error Handling

### Confidence Threshold

- **Threshold**: 70% confidence
- **Below threshold**: "I didn't catch that. Please repeat."
- **After 3 attempts**: Offer "Type instead" option

### Correction Commands

| Command | Action |
|---------|--------|
| "go back" | Return to previous step |
| "change [field]" | Return to specific field |
| "edit [field]" | Return to specific field |
| "start over" | Reset to IDLE |
| "cancel" | Cancel voice mode, return to menu |
| "type instead" | Fall back to keyboard input |

### Field Correction Examples

```
System: "Priority: HIGH. When is it due?"
User: "go back"
System: "What priority? Say high, medium, low, or none."

System: "Due: tomorrow. Any recurrence?"
User: "edit due date"
System: "When is it due? Say a date or 'none'."
```

---

## Confirmation Summary Display

```
╔════════════════════════════════════╗
║     Voice Task Summary             ║
╠════════════════════════════════════╣
│ Title:      Buy groceries          │
│ Priority:   🔴 HIGH                │
│ Due Date:   tomorrow (2025-12-28)  │
│ Recurrence: None                   │
╠════════════════════════════════════╣
│ Say "confirm" to create task       │
│ Say "edit [field]" to change       │
╚════════════════════════════════════╝
```

---

## Microphone Availability Check

### Detection Flow

```python
def check_microphone_available() -> bool:
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        return device_count > 0
    except:
        return False
```

### Graceful Degradation

| Condition | Behavior |
|-----------|----------|
| Microphone available | Voice input menu option enabled |
| Microphone unavailable | Voice input menu option disabled with message |
| PyAudio not installed | Voice input menu option disabled with installation hint |
| No internet | Voice input works with lower accuracy local engines |

### Disabled State Display

```
  8. Voice Input [DISABLED - Microphone not available]
     Use keyboard input instead
```

---

## Testing Contracts

### Voice Input Test Scenarios

| Scenario | Expected Behavior |
|----------|-------------------|
| Normal flow: "add task" → "buy milk" → "high" → "tomorrow" → "none" → "confirm" | Task created with correct values |
| Correction: "add task" → "buy milk" → "high" → "go back" → "low" | Priority corrected to LOW |
| Low confidence: 3 failed attempts at title | System offers "Type instead" option |
| No microphone: User selects Voice Input | Menu option disabled, clear message |
| "cancel" at any point | Returns to main menu, no task created |

### Acceptance Criteria

1. Voice input creates task with same data as keyboard input
2. "Go back" command works at any step
3. Input normalization handles variations ("very high" → HIGH)
4. Confidence <70% triggers retry after max 3 attempts
5. All functionality accessible without voice when unavailable
