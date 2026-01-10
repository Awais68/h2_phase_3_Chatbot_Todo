# Voice Command System Design for MissionImpossible

**Application**: MissionImpossible (Task/Mission Management)
**Created**: 2026-01-03
**Version**: 1.0
**Dependencies**: react-speech-recognition 4.0.1, Web Speech API

---

## 1. Command Mapping Table

### 1.1 English Voice Commands

| Action | Command Patterns | Example | Parsed Output |
|--------|------------------|---------|---------------|
| **Add Task** | "Add mission [title]"<br>"Create task [title]"<br>"New task [title]"<br>"Add [title]" | "Add mission Finish report" | `{ action: 'add', params: { title: 'Finish report' } }` |
| **Complete Task** | "Complete mission [id/title]"<br>"Done [id/title]"<br>"Mark complete [id/title]"<br>"Finish task [id/title]" | "Complete mission Finish report" | `{ action: 'complete', params: { id: 'Finish report' } }` |
| **Delete Task** | "Delete mission [id/title]"<br>"Remove [id/title]"<br>"Delete task [id/title]"<br>"Erase [id/title]" | "Delete mission 1" | `{ action: 'delete', params: { id: '1' } }` |
| **Search Tasks** | "Find mission [query]"<br>"Search for [query]"<br>"Find [query]"<br>"Search [query]" | "Find mission urgent" | `{ action: 'search', params: { query: 'urgent' } }` |
| **Navigate Tabs** | "Go to missions"<br>"Go to completed"<br>"Show active"<br>"Show all" | "Go to completed" | `{ action: 'navigate', params: { tab: 'completed' } }` |
| **Help** | "Help"<br>"What can I say?"<br>"Voice commands" | "Help" | `{ action: 'help' }` |

### 1.2 Urdu Voice Commands (Urdu Script)

| Action | Command Patterns (Urdu) | Example | Parsed Output |
|--------|-------------------------|---------|---------------|
| **Add Task** | "نیا کام بناؤ [عنوان]"<br>"کام شامل کرو [عنوان]"<br>"نیا مشن [عنوان]" | "نیا کام بناؤ رپورٹ مکمل کرو" | `{ action: 'add', params: { title: 'رپورٹ مکمل کرو' }, language: 'ur' }` |
| **Complete Task** | "کام مکمل کرو [آئی ڈی/عنوان]"<br>"کام ختم کرو [آئی ڈی]"<br>"مکمل کر لو [آئی ڈی]" | "کام مکمل کرو رپورٹ" | `{ action: 'complete', params: { id: 'رپورٹ' }, language: 'ur' }` |
| **Delete Task** | "کام حذف کرو [آئی ڈی]"<br>"کام ہٹاؤ [آئی ڈی]"<br>"ختم کر دو [آئی ڈی]" | "کام حذف کرو 1" | `{ action: 'delete', params: { id: '1' }, language: 'ur' }` |
| **Search Tasks** | "کام تلاش کرو [استفسار]"<br>"[استفسار] تلاش کرو"<br>"[استفسار] ڈھونڈو" | "جلدی کام تلاش کرو" | `{ action: 'search', params: { query: 'جلدی' }, language: 'ur' }` |
| **Navigate Tabs** | "مکمل کام دکھاؤ"<br>"جلدی کام دکھاؤ"<br>"سب کام دکھاؤ"<br>"مشان والا صفحہ جاؤ" | "مکمل کام دکھاؤ" | `{ action: 'navigate', params: { tab: 'completed' }, language: 'ur' }` |
| **Help** | "مدد کرو"<br>"کیا کر سکتے ہو؟"<br>"کمانڈس بتاؤ" | "مدد کرو" | `{ action: 'help' }` |

### 1.3 Roman Urdu Voice Commands

| Action | Command Patterns (Roman Urdu) | Example | Parsed Output |
|--------|-------------------------------|---------|---------------|
| **Add Task** | "Naya kam banaow [title]"<br>"Kam shamil karo [title]"<br>"New task [title]" | "Naya kam banaow report complete karo" | `{ action: 'add', params: { title: 'report complete karo' }, language: 'ur' }` |
| **Complete Task** | "Kam mukammal karo [id]"<br>"Task complete karo [id]"<br>"Done [id]" | "Kam mukammal karo report" | `{ action: 'complete', params: { id: 'report' }, language: 'ur' }` |
| **Delete Task** | "Kam hatao [id]"<br>"Task delete karo [id]"<br>"Remove [id]" | "Task hatao 1" | `{ action: 'delete', params: { id: '1' }, language: 'ur' }` |

---

## 2. Speech Recognition Configuration

### 2.1 Web Speech API Setup

```typescript
// /frontend/src/lib/voice-recognition.ts

export interface VoiceRecognitionConfig {
  language: 'en-US' | 'ur-PK'          // Language code
  continuous: boolean                   // Continuous listening mode
  interimResults: boolean               // Show interim results
  maxAlternatives: number              // Number of alternatives (1-5)
  confidenceThreshold: number          // Minimum confidence (0.0 - 1.0)
  restartOnEnd: boolean                // Auto-restart after speech ends
  silenceTimeout: number              // Silence timeout in ms (3000-10000)
}

export const DEFAULT_CONFIG: VoiceRecognitionConfig = {
  language: 'en-US',
  continuous: false,                    // Push-to-talk by default
  interimResults: true,
  maxAlternatives: 3,
  confidenceThreshold: 0.7,            // Standard threshold for reliable recognition
  restartOnEnd: false,
  silenceTimeout: 5000,                // 5 seconds of silence ends session
}
```

### 2.2 Browser Compatibility Matrix

| Browser | Speech Recognition | Speech Synthesis | Notes |
|---------|-------------------|------------------|-------|
| **Chrome** | Full Support (v25+) | Full Support | Best accuracy, both languages |
| **Edge** | Full Support | Full Support | Chromium-based, good Urdu support |
| **Safari** | Partial (macOS 14.4+, iOS 17.4+) | Full Support | Limited Urdu recognition |
| **Firefox** | Not Supported | Full Support | Requires extension or API fallback |
| **Opera** | Full Support | Full Support | Chromium-based |

**Fallback Strategy**:
1. Primary: Web Speech API (Chrome, Edge, Safari)
2. Secondary: react-speech-recognition with polyfill check
3. Fallback: Show disabled state with helpful message

### 2.3 Recognition Lifecycle Management

```typescript
class VoiceRecognitionManager {
  private recognition: SpeechRecognition | null = null
  private isActive: boolean = false
  private silenceTimer: ReturnType<typeof setTimeout> | null = null

  // States: idle -> listening -> processing -> idle/error
  private state: VoiceState = 'idle'

  start(): void {
    if (!this.isSupported()) {
      this.handleError('unsupported')
      return
    }

    try {
      this.recognition?.start()
      this.isActive = true
      this.setState('listening')
      this.startSilenceTimer()
    } catch (error) {
      this.handleError('start-failed')
    }
  }

  stop(): void {
    this.recognition?.stop()
    this.isActive = false
    this.setState('idle')
    this.clearSilenceTimer()
  }

  abort(): void {
    this.recognition?.abort()
    this.isActive = false
    this.setState('idle')
    this.clearSilenceTimer()
  }

  private startSilenceTimer(): void {
    this.clearSilenceTimer()
    this.silenceTimer = setTimeout(() => {
      this.handleSilenceTimeout()
    }, this.config.silenceTimeout)
  }

  private handleSilenceTimeout(): void {
    this.speak(getFeedbackMessage('silenceTimeout', this.language))
    this.stop()
  }
}
```

---

## 3. Speech Synthesis Responses

### 3.1 Feedback Message Mapping

```typescript
// /frontend/src/lib/voice-synthesis.ts

export const VOICE_FEEDBACK = {
  en: {
    // Success messages
    missionAdded: 'Mission added successfully',
    missionCompleted: 'Mission marked as complete',
    missionDeleted: 'Mission deleted',
    missionUpdated: 'Mission updated',
    searchResults: 'Showing search results',

    // Status messages
    listening: 'Listening...',
    processing: 'Processing your command',
    commandReceived: 'Command received',

    // Error messages
    notSupported: 'Voice recognition is not supported in this browser',
    microphoneDenied: 'Microphone access was denied. Please enable permissions.',
    noSpeechDetected: 'No speech detected. Please try again.',
    commandNotRecognized: 'Command not recognized. Please try again.',
    lowConfidence: 'I did not understand clearly. Please speak again.',
    taskNotFound: 'Mission not found',

    // Navigation feedback
    navigatingToMissions: 'Showing all missions',
    navigatingToCompleted: 'Showing completed missions',
    navigatingToActive: 'Showing active missions',
  },
  ur: {
    // Success messages
    missionAdded: 'کام شامل ہو گیا',
    missionCompleted: 'کام مکمل ہو گیا',
    missionDeleted: 'کام حذف ہو گیا',
    missionUpdated: 'کام تبدیل ہو گیا',
    searchResults: 'تلاش کے نتائج دکھائے جا رہے ہیں',

    // Status messages
    listening: 'سن رہا ہوں...',
    processing: 'آپ کا کمانڈ پراسیس ہو رہا ہے',
    commandReceived: 'کمانڈ مل گیا',

    // Error messages
    notSupported: 'آپ کے براؤزر میں وائس ریکگنیشن سپورٹ نہیں ہے',
    microphoneDenied: 'مائیکروفون کی اجازت نہیں دی گئی',
    noSpeechDetected: 'کوئی آواز نہیں سنی گئی۔ دوبارہ کوشش کریں۔',
    commandNotRecognized: 'کمانڈ سمجھ نہیں آئی۔ دوبارہ کوشش کریں۔',
    lowConfidence: 'صاف بولیں۔',
    taskNotFound: 'کام نہیں ملا',

    // Navigation feedback
    navigatingToMissions: 'سب کام دکھائے جا رہے ہیں',
    navigatingToCompleted: 'مکمل کام دکھائے جا رہے ہیں',
    navigatingToActive: 'جلدی کام دکھائے جا رہے ہیں',
  },
}
```

### 3.2 Speech Configuration

```typescript
export const SPEECH_CONFIG = {
  en: {
    language: 'en-US',
    rate: 0.9,           // Slightly slower for clarity
    pitch: 1.0,
    volume: 0.8,
    preferredVoice: null, // Use browser default
  },
  ur: {
    language: 'ur-PK',
    rate: 0.85,          // Slower for Urdu articulation
    pitch: 1.0,
    volume: 0.8,
    preferredVoice: null,
  },
}
```

### 3.3 Audio Feedback Priority Queue

| Priority | Event | Audio Cue |
|----------|-------|-----------|
| 1 | Error (permission denied) | Error sound + spoken message |
| 2 | Command received | Brief acknowledgment |
| 3 | Success confirmation | Success sound |
| 4 | Status update (listening) | Minimal beep only |

---

## 4. Error Handling Strategy

### 4.1 Error Categories and Recovery

```typescript
type VoiceError =
  | 'unsupported'           // Browser doesn't support API
  | 'permission-denied'     // User denied microphone access
  | 'no-speech-detected'    // User didn't speak within timeout
  | 'network-error'         // Recognition service unavailable
  | 'command-unrecognized'  // Speech recognized but not a command
  | 'low-confidence'        // Speech recognized with low confidence
  | 'task-not-found'        // Referenced task doesn't exist
  | 'audio-capture-error'   // Microphone hardware issue
```

### 4.2 Error Recovery Flowchart

```
Voice Input Activated
        |
        v
    [Check Support]
        |
   +----+----+
   |         |
Not Supported  Supported
   |         |
   v         v
Show Help    [Check Permission]
Message      [Request Permission]
             +----+----+
             |         |
          Denied     Granted
             |         |
             v         v
        Show Guide   Start
        to Enable    Listening
        Mic          |
                     v
              [Silence Timeout?]
                +----+----+
               Yes          No
                |          |
                v          v
            Show Error   [Process Speech]
            Try Again    |
                         v
                   [Confidence OK?]
                   +----+----+
                  No           Yes
                   |           |
                   v           v
              Spoken         [Parse Command]
              Retry Msg      |
                           [Valid Command?]
                           +----+----+
                          No           Yes
                           |           |
                           v           v
                      Spoken         Execute
                      Help          Command
                                     |
                                     v
                               [Success?]
                               +----+----+
                              No           Yes
                               |           |
                               v           v
                           Error Msg    Success
                           Recovery     Feedback
```

### 4.3 User-Facing Error Messages

```typescript
export const ERROR_MESSAGES = {
  unsupported: {
    en: 'Voice recognition is not supported in your browser. Please use Chrome, Edge, or Safari.',
    ur: 'آپ کے براؤزر میں وائس ریکگنیشن سپورٹ نہیں ہے۔ برائے مہربانی کروم، ایج، یا سفاری استعمال کریں۔',
  },
  'permission-denied': {
    en: 'Microphone access was denied. To enable: Click the lock icon in your address bar, select "Site Settings", and allow microphone access.',
    ur: 'مائیکروفون کی اجازت نہیں دی گئی۔ فعال کرنے کے لیے: اپنے ایڈریس بار میں لاک آئیکن پر کلک کریں، "سائٹ سیٹنگز" کا انتخاب کریں، اور مائیکروفون کی اجازت دیں۔',
  },
  'no-speech-detected': {
    en: "I didn't hear anything. Please speak clearly and try again.",
    ur: 'میں نے کچھ نہیں سنا۔ برائے مہربانی صاف بولیں اور دوبارہ کوشش کریں۔',
  },
  'low-confidence': {
    en: "I didn't understand clearly. Please speak more slowly and distinctly.",
    ur: 'صاف نہیں سمجھ آیا۔ برائے مہربانی آہستہ اور صاف بولیں۔',
  },
  'task-not-found': {
    en: "I couldn't find that mission. Please check the name or number and try again.",
    ur: 'وہ کام نہیں ملا۔ برائے مہربانی نام یا نمبر چیک کریں اور دوبارہ کوشش کریں۔',
  },
}
```

### 4.4 Retry Mechanism

```typescript
interface RetryConfig {
  maxAttempts: number
  backoffMs: number
  maxBackoffMs: number
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxAttempts: 3,
  backoffMs: 1000,
  maxBackoffMs: 5000,
}

class VoiceCommandHandler {
  private attemptCount: number = 0

  handleRetry(): void {
    if (this.attemptCount < this.config.maxAttempts) {
      this.attemptCount++
      const delay = Math.min(
        this.config.backoffMs * Math.pow(2, this.attemptCount - 1),
        this.config.maxBackoffMs
      )
      setTimeout(() => {
        this.speak(getFeedbackMessage('tryAgain', this.language))
        this.restartListening()
      }, delay)
    } else {
      this.speak(getFeedbackMessage('maxAttemptsReached', this.language))
      this.suggestManualInput()
    }
  }
}
```

---

## 5. Privacy Considerations

### 5.1 Data Collection Policy

| Data Type | Collected | Storage | Retention |
|-----------|-----------|---------|-----------|
| Voice Input Text | Yes | Local State | Session only |
| Audio Buffer | No | N/A | N/A |
| Confidence Scores | Yes | Local State | Session only |
| Command History | Optional | localStorage | Until cleared |
| Language Preference | Yes | localStorage | Persistent |

### 5.2 Privacy-First Design Principles

```typescript
class PrivacyManager {
  // No audio is ever transmitted to servers
  // All speech recognition happens locally in browser

  // Voice data is processed entirely client-side
  private processLocally(transcript: string): string {
    // Web Speech API processes audio locally
    // No audio data leaves the browser
    return transcript
  }

  // Optional: Local storage for preferences
  private storePreferences(prefs: VoicePreferences): void {
    localStorage.setItem('voice-prefs', JSON.stringify(prefs))
    // No PII, no audio, no server sync
  }

  // User can clear all voice data
  clearVoiceData(): void {
    localStorage.removeItem('voice-prefs')
    // Session data cleared on page refresh
  }
}
```

### 5.3 Consent Management Flow

```
1. User clicks microphone button
         |
         v
2. Check if user has previously granted permission
         |
   +-----+-----+
   |           |
  Yes          No
   |           |
   v           v
Start      Show Permission Dialog
Listening  "Allow microphone access for voice commands?"
         |
   +-----+-----+
   |           |
  Allow       Deny
   |           |
   v           v
Start    Show Guidance
Listening  "Permission denied. Enable in browser settings."
```

### 5.4 Security Measures

- **No Audio Upload**: Speech recognition happens entirely in-browser
- **No Third-Party API Calls**: Uses native Web Speech API
- **Session Isolation**: Voice state is cleared on page refresh
- **Optional History**: Command history stored locally, never transmitted
- **User Control**: Easy permission management and data clearing

---

## 6. Integration Points with React Components

### 6.1 Custom Hook: useVoiceCommands

```typescript
// /frontend/src/hooks/useVoiceCommands.ts
'use client'

import { useState, useCallback, useEffect } from 'react'
import { useSpeechRecognition } from 'react-speech-recognition'
import {
  VoiceRecognitionManager,
  VoiceRecognitionConfig,
  VoiceRecognitionStatus,
} from '@/lib/voice-recognition'
import {
  VoiceSynthesisManager,
  VOICE_FEEDBACK,
} from '@/lib/voice-synthesis'
import { parseVoiceCommand, VoiceCommand } from '@/lib/voice-commands'
import { useTaskStore } from '@/stores/useTaskStore'

interface UseVoiceCommandsOptions {
  language?: 'en' | 'ur'
  continuous?: boolean
  onCommand?: (command: VoiceCommand) => void
  onError?: (error: string) => void
}

export function useVoiceCommands(options: UseVoiceCommandsOptions = {}) {
  const {
    language = 'en',
    continuous = false,
    onCommand,
    onError,
  } = options

  const { addTask, updateTask, deleteTask } = useTaskStore()
  const [status, setStatus] = useState<VoiceRecognitionStatus>('idle')
  const [transcript, setTranscript] = useState('')
  const [lastCommand, setLastCommand] = useState<VoiceCommand | null>(null)

  // Recognition manager ref
  const recognitionRef = useRef<VoiceRecognitionManager | null>(null)

  // Synthesis manager ref
  const synthesisRef = useRef<VoiceSynthesisManager | null>(null)

  // Initialize managers
  useEffect(() => {
    recognitionRef.current = new VoiceRecognitionManager(
      {
        language: language === 'en' ? 'en-US' : 'ur-PK',
        continuous,
        interimResults: true,
        confidenceThreshold: 0.7,
      },
      {
        onTranscript: (t) => {
          setTranscript(t.text)
          if (t.isFinal) {
            handleFinalTranscript(t.text, t.confidence)
          }
        },
        onStart: () => setStatus('listening'),
        onEnd: () => setStatus('idle'),
        onError: (err) => {
          setStatus('error')
          onError?.(err)
        },
      }
    )

    synthesisRef.current = new VoiceSynthesisManager({
      language: language === 'en' ? 'en-US' : 'ur-PK',
    })

    return () => {
      recognitionRef.current?.destroy()
      synthesisRef.current?.destroy()
    }
  }, [language, continuous])

  // Process final transcript
  const handleFinalTranscript = useCallback((text: string, confidence: number) => {
    const command = parseVoiceCommand(text, language)
    setLastCommand(command)

    if (command.action === 'unknown') {
      speak(VOICE_FEEDBACK[language].commandNotRecognized)
      onError?.('command-not-recognized')
      return
    }

    if (confidence < 0.7) {
      speak(VOICE_FEEDBACK[language].lowConfidence)
      return
    }

    speak(VOICE_FEEDBACK[language].commandReceived)
    executeCommand(command)
    onCommand?.(command)
  }, [language, onCommand, onError])

  // Execute parsed command
  const executeCommand = useCallback(async (command: VoiceCommand) => {
    switch (command.action) {
      case 'add':
        if (command.params.title) {
          await api.tasks.create({ title: command.params.title })
          speak(VOICE_FEEDBACK[language].missionAdded)
        }
        break
      case 'complete':
        // Task completion logic
        speak(VOICE_FEEDBACK[language].missionCompleted)
        break
      case 'delete':
        // Task deletion logic
        speak(VOICE_FEEDBACK[language].missionDeleted)
        break
      case 'search':
        // Search logic
        speak(VOICE_FEEDBACK[language].searchResults)
        break
      case 'navigate':
        // Navigation logic
        speak(VOICE_FEEDBACK[language].navigatingToMissions)
        break
    }
  }, [language])

  // Speak feedback
  const speak = useCallback((text: string) => {
    synthesisRef.current?.speak(text)
  }, [])

  // Toggle listening
  const toggleListening = useCallback(() => {
    if (status === 'listening') {
      recognitionRef.current?.stop()
    } else {
      recognitionRef.current?.start()
    }
  }, [status])

  // Keyboard shortcut (Alt+M)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.altKey && e.key === 'm') {
        e.preventDefault()
        toggleListening()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [toggleListening])

  return {
    status,
    transcript,
    lastCommand,
    isListening: status === 'listening',
    isSupported: recognitionRef.current?.isSupported() ?? false,
    toggleListening,
    speak,
    language,
    setLanguage: (lang: 'en' | 'ur') => {
      recognitionRef.current?.setLanguage(lang === 'en' ? 'en-US' : 'ur-PK')
      synthesisRef.current?.setLanguage(lang === 'en' ? 'en-US' : 'ur-PK')
    },
  }
}
```

### 6.2 Voice Microphone Button Component

```typescript
// /frontend/src/components/VoiceInputButton.tsx
'use client'

import { Mic, MicOff, Waves } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { useVoiceCommands } from '@/hooks/useVoiceCommands'
import { cn } from '@/lib/utils'

interface VoiceInputButtonProps {
  onCommand?: (command: VoiceCommand) => void
  size?: 'sm' | 'md' | 'lg'
  showStatus?: boolean
}

export function VoiceInputButton({
  onCommand,
  size = 'md',
  showStatus = true,
}: VoiceInputButtonProps) {
  const {
    status,
    isListening,
    isSupported,
    toggleListening,
    language,
    setLanguage,
  } = useVoiceCommands({ onCommand })

  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12',
  }

  if (!isSupported) {
    return null // Hide on unsupported browsers
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="relative">
            <Button
              variant={isListening ? 'default' : 'outline'}
              size="icon"
              className={cn(sizeClasses[size], isListening && 'animate-pulse')}
              onClick={toggleListening}
              aria-label={isListening ? 'Stop listening' : 'Start listening'}
              aria-pressed={isListening}
            >
              {isListening ? (
                <Mic className="h-5 w-5" />
              ) : (
                <MicOff className="h-5 w-5" />
              )}
            </Button>

            {/* Listening indicator */}
            {isListening && (
              <div className="absolute -top-1 -right-1 flex gap-0.5">
                <Waves className="h-3 w-3 text-green-500 animate-pulse" />
              </div>
            )}
          </div>
        </TooltipTrigger>

        <TooltipContent>
          <div className="text-center">
            <p>{isListening ? 'Click to stop' : 'Click to speak'}</p>
            <p className="text-xs text-muted-foreground">
              Press Alt+M as shortcut
            </p>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
```

### 6.3 Voice Status Indicator Component

```typescript
// /frontend/src/components/VoiceStatusIndicator.tsx
'use client'

import { VoiceRecognitionStatus } from '@/lib/voice-recognition'
import { cn } from '@/lib/utils'

interface VoiceStatusIndicatorProps {
  status: VoiceRecognitionStatus
  language: 'en' | 'ur'
  className?: string
}

const STATUS_CONFIG = {
  idle: {
    label: { en: 'Tap microphone to start', ur: 'بولنے کے لیے مائیکروفون چلائیں' },
    color: 'bg-gray-400',
    animate: false,
  },
  listening: {
    label: { en: 'Listening...', ur: 'سن رہا ہوں...' },
    color: 'bg-green-500',
    animate: true,
  },
  processing: {
    label: { en: 'Processing...', ur: 'پراسیسنگ...' },
    color: 'bg-blue-500',
    animate: true,
  },
  error: {
    label: { en: 'Error - try again', ur: 'خرابی - دوبارہ کوشش کریں' },
    color: 'bg-red-500',
    animate: false,
  },
  unsupported: {
    label: { en: 'Voice not supported', ur: 'وائس سپورٹ نہیں' },
    color: 'bg-gray-300',
    animate: false,
  },
}

export function VoiceStatusIndicator({ status, language, className }: VoiceStatusIndicatorProps) {
  const config = STATUS_CONFIG[status]

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div
        className={cn(
          'h-3 w-3 rounded-full',
          config.color,
          config.animate && 'animate-pulse'
        )}
      />
      <span className="text-sm text-muted-foreground">
        {config.label[language]}
      </span>
    </div>
  )
}
```

### 6.4 AddTaskForm with Voice Integration

```typescript
// /frontend/src/components/AddTaskForm.tsx (updated)
'use client'

import { useState, FormEvent } from 'react'
import { Plus, Mic } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { VoiceInputButton } from './VoiceInputButton'
import { useVoiceCommands } from '@/hooks/useVoiceCommands'
import { useTaskStore } from '@/stores/useTaskStore'
import { syncManager } from '@/lib/sync'
import { api } from '@/lib/api'

export function AddTaskForm() {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { isOffline } = useTaskStore()

  const handleVoiceCommand = useCallback((command: VoiceCommand) => {
    if (command.action === 'add' && command.params.title) {
      setTitle(command.params.title)
    }
  }, [])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return

    setIsSubmitting(true)
    // ... existing submit logic
    setIsSubmitting(false)
  }

  return (
    <Card className="p-4">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Input
              type="text"
              placeholder="Task title *"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isSubmitting}
              autoComplete="off"
              className="text-base"
              required
            />
            <VoiceInputButton
              onCommand={handleVoiceCommand}
              size="md"
            />
          </div>
          <Input
            type="text"
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isSubmitting}
            autoComplete="off"
            className="text-base"
          />
        </div>

        <Button
          type="submit"
          disabled={!title.trim() || isSubmitting}
          className="w-full"
          size="lg"
        >
          <Plus className="h-5 w-5 mr-2" />
          {isSubmitting ? 'Adding...' : 'Add Task'}
        </Button>
      </form>
    </Card>
  )
}
```

### 6.5 TaskList with Voice Commands

```typescript
// /frontend/src/components/TaskList.tsx (updated)
'use client'

import { TaskCard } from './TaskCard'
import { TaskListSkeleton } from './TaskCardSkeleton'
import { VoiceChatbot } from './VoiceChatbot'
import { useTaskStore } from '@/stores/useTaskStore'
import { syncManager } from '@/lib/sync'
import { api } from '@/lib/api'
import { useState } from 'react'

export function TaskList() {
  const { tasks, loading } = useTaskStore()
  const { isOffline } = useTaskStore()
  const [showVoiceChatbot, setShowVoiceChatbot] = useState(false)

  const handleVoiceCommand = useCallback((command: VoiceCommand) => {
    switch (command.action) {
      case 'complete':
        const taskToComplete = tasks.find(t =>
          t.title.toLowerCase().includes(command.params.id?.toLowerCase() || '')
        )
        if (taskToComplete) {
          handleToggleComplete(taskToComplete.id)
        }
        break
      case 'delete':
        const taskToDelete = tasks.find(t =>
          t.title.toLowerCase().includes(command.params.id?.toLowerCase() || '')
        )
        if (taskToDelete) {
          handleDelete(taskToDelete.id)
        }
        break
    }
  }, [tasks])

  const handleToggleComplete = async (id: string) => {
    // ... existing logic
  }

  const handleDelete = async (id: string) => {
    // ... existing logic
  }

  if (loading) {
    return <TaskListSkeleton count={3} />
  }

  return (
    <div className="space-y-3">
      {/* Voice chatbot toggle */}
      <div className="flex justify-end">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowVoiceChatbot(!showVoiceChatbot)}
        >
          {showVoiceChatbot ? 'Hide Voice' : 'Voice Commands'}
        </Button>
      </div>

      {/* Voice chatbot panel */}
      {showVoiceChatbot && (
        <VoiceChatbot onCommand={handleVoiceCommand} />
      )}

      {/* Task list */}
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggleComplete={handleToggleComplete}
          onDelete={handleDelete}
        />
      ))}
    </div>
  )
}
```

### 6.6 Keyboard Shortcuts

```typescript
// /frontend/src/components/KeyboardShortcuts.tsx
'use client'

import { useEffect } from 'react'

export function KeyboardShortcuts() {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Alt+M: Toggle voice input
      if (e.altKey && e.key === 'm') {
        e.preventDefault()
        // Dispatch event to toggle voice input
        window.dispatchEvent(new CustomEvent('voice:toggle'))
      }

      // Alt+L: Switch language
      if (e.altKey && e.key === 'l') {
        e.preventDefault()
        window.dispatchEvent(new CustomEvent('voice:toggle-language'))
      }

      // Escape: Stop listening
      if (e.key === 'Escape') {
        window.dispatchEvent(new CustomEvent('voice:stop'))
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return null
}
```

---

## 7. Accessibility Features

### 7.1 ARIA Attributes

```typescript
// All voice controls must have proper ARIA attributes
<Button
  aria-label="Start voice input"
  aria-pressed={isListening}
  aria-describedby="voice-help"
  role="button"
>
  <Mic />
</Button>

<div id="voice-help" className="sr-only">
  Press Alt+M to activate voice input
</div>
```

### 7.2 Screen Reader Support

- Status changes announced via `aria-live` region
- Transcript displayed with `sr-only` for screen readers
- Error messages announced immediately
- Visual indicators have text alternatives

### 7.3 Always-Listening Toggle (with Permission)

```typescript
const AlwaysListeningToggle = () => {
  const [isEnabled, setIsEnabled] = useState(false)
  const [hasPermission, setHasPermission] = useState(false)

  const requestPermission = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      stream.getTracks().forEach(track => track.stop())
      setHasPermission(true)
      setIsEnabled(true)
    } catch {
      setHasPermission(false)
    }
  }

  const toggleAlwaysListening = () => {
    if (!hasPermission) {
      requestPermission()
      return
    }
    setIsEnabled(!isEnabled)
  }

  return (
    <Switch
      checked={isEnabled}
      onCheckedChange={toggleAlwaysListening}
      disabled={!hasPermission}
      aria-label="Always listen for voice commands"
    />
  )
}
```

---

## 8. Browser Compatibility Matrix

| Feature | Chrome | Edge | Safari | Firefox |
|---------|--------|------|--------|---------|
| SpeechRecognition | Full | Full | Partial (17.4+) | Not Supported |
| SpeechSynthesis | Full | Full | Full | Full |
| Interim Results | Yes | Yes | No | N/A |
| Urdu Recognition | Yes | Yes | Limited | N/A |
| Continuous Mode | Yes | Yes | No | N/A |

---

## 9. Testing Checklist

### 9.1 Functional Tests

- [ ] Voice recognition starts on button click
- [ ] Voice recognition stops on button click
- [ ] Commands are parsed correctly (English)
- [ ] Commands are parsed correctly (Urdu)
- [ ] Error messages display appropriately
- [ ] Audio feedback plays for success
- [ ] Audio feedback plays for errors
- [ ] Keyboard shortcuts work (Alt+M, Escape)
- [ ] Permission denied scenario handled
- [ ] No speech detected scenario handled
- [ ] Task creation via voice works
- [ ] Task completion via voice works
- [ ] Task deletion via voice works

### 9.2 Accessibility Tests

- [ ] Keyboard navigation works
- [ ] Screen readers announce status
- [ ] Focus management is correct
- [ ] ARIA labels are present
- [ ] Color contrast meets WCAG AA

### 9.3 Performance Tests

- [ ] Voice activation takes < 500ms
- [ ] Recognition completes < 3s
- [ ] Audio feedback plays < 2s after recognition
- [ ] Memory usage is bounded

---

## 10. File Structure

```
frontend/src/
├── lib/
│   ├── voice-recognition.ts    # Speech recognition manager
│   ├── voice-synthesis.ts      # Text-to-speech manager
│   └── voice-commands.ts       # Command parser
├── hooks/
│   └── useVoiceCommands.ts     # Custom hook
├── components/
│   ├── VoiceChatbot.tsx        # Main voice interface
│   ├── VoiceInputButton.tsx    # Microphone button
│   └── VoiceStatusIndicator.tsx # Status display
└── stores/
    └── useVoiceStore.ts        # Voice state management (optional)
```

---

## 11. References

- [Web Speech API Specification](https://w3c.github.io/speech-api/)
- [react-speech-recognition Documentation](https://github.com/JamesBrill/react-speech-recognition)
- [WCAG 2.1 Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Speech Recognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)
- [MDN Speech Synthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis)
