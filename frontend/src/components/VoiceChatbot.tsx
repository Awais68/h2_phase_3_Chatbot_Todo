'use client'

/**
 * VoiceChatbot Component
 *
 * Voice-enabled task management interface
 * Supports push-to-talk and continuous listening modes
 * Multi-language support (English and Urdu)
 */

import { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { Mic, MicOff, Volume2, VolumeX, HelpCircle, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import {
  VoiceRecognitionManager,
  VoiceTranscript,
  VoiceRecognitionStatus,
} from '@/lib/voice-recognition'
import {
  VoiceSynthesisManager,
  playBeep,
  getFeedbackMessage,
} from '@/lib/voice-synthesis'
import {
  parseVoiceCommand,
  VoiceCommand,
  getCommandDescription,
  getVoiceCommandHelp,
} from '@/lib/voice-commands'
import { useTaskStore } from '@/stores/useTaskStore'
import { api } from '@/lib/api'
import { Task } from '@/types'

interface VoiceChatbotProps {
  onClose?: () => void
}

export default function VoiceChatbot({ onClose }: VoiceChatbotProps) {
  const { t, i18n } = useTranslation()
  const { tasks, addTask, updateTask, deleteTask } = useTaskStore()

  // Language state
  const [language, setLanguage] = useState<'en' | 'ur'>('en')

  // Voice recognition state
  const [status, setStatus] = useState<VoiceRecognitionStatus>('idle')
  const [transcript, setTranscript] = useState<string>('')
  const [confidence, setConfidence] = useState<number>(0)
  const [isListening, setIsListening] = useState(false)

  // Voice mode state
  const [isContinuousMode, setIsContinuousMode] = useState(false)
  const [isSpeechEnabled, setIsSpeechEnabled] = useState(true)

  // UI state
  const [showHelp, setShowHelp] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastCommand, setLastCommand] = useState<VoiceCommand | null>(null)

  // Refs
  const recognitionRef = useRef<VoiceRecognitionManager | null>(null)
  const synthesisRef = useRef<VoiceSynthesisManager | null>(null)

  /**
   * Initialize voice managers
   */
  useEffect(() => {
    // Initialize voice recognition
    recognitionRef.current = new VoiceRecognitionManager(
      {
        language: language === 'en' ? 'en-US' : 'ur-PK',
        continuous: isContinuousMode,
        interimResults: true,
      },
      {
        onTranscript: handleTranscript,
        onStart: () => {
          setIsListening(true)
          playBeep(800, 100)
        },
        onEnd: () => {
          setIsListening(false)
          playBeep(600, 100)
        },
        onError: (error) => {
          setError(error)
          setStatus('error')
        },
        onStatusChange: (newStatus) => {
          setStatus(newStatus)
        },
      }
    )

    // Initialize voice synthesis
    synthesisRef.current = new VoiceSynthesisManager(
      {
        language: language === 'en' ? 'en-US' : 'ur-PK',
      },
      {
        onError: (error) => {
          console.error('Speech synthesis error:', error)
        },
      }
    )

    // Cleanup on unmount
    return () => {
      recognitionRef.current?.destroy()
      synthesisRef.current?.destroy()
    }
  }, [])

  /**
   * Update language when changed
   */
  useEffect(() => {
    const langCode = language === 'en' ? 'en-US' : 'ur-PK'
    recognitionRef.current?.setLanguage(langCode)
    synthesisRef.current?.setLanguage(langCode)
    i18n.changeLanguage(language)
  }, [language, i18n])

  /**
   * Update continuous mode when changed
   */
  useEffect(() => {
    recognitionRef.current?.setContinuous(isContinuousMode)
  }, [isContinuousMode])

  /**
   * Handle voice transcript
   */
  const handleTranscript = (voiceTranscript: VoiceTranscript) => {
    setTranscript(voiceTranscript.text)
    setConfidence(voiceTranscript.confidence)

    // Only process final results
    if (voiceTranscript.isFinal) {
      processCommand(voiceTranscript.text, voiceTranscript.confidence)
    }
  }

  /**
   * Process voice command
   */
  const processCommand = async (text: string, confidence: number) => {
    // Parse command
    const command = parseVoiceCommand(text, language)
    setLastCommand(command)

    // Check confidence threshold
    if (confidence < 0.7) {
      const message = getFeedbackMessage('lowConfidence', language)
      setError(message)
      speak(message)
      return
    }

    // Check if command is recognized
    if (command.action === 'unknown') {
      const message = getFeedbackMessage('commandUnknown', language)
      setError(message)
      speak(message)
      return
    }

    // Execute command
    try {
      setError(null)
      const description = getCommandDescription(command)
      speak(description)

      await executeCommand(command)

      // Success feedback
      const successMessage = getFeedbackMessage('success', language)
      speak(successMessage)
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Command failed'
      setError(errorMessage)
      speak(getFeedbackMessage('error', language))
    }
  }

  /**
   * Execute voice command
   */
  const executeCommand = async (command: VoiceCommand) => {
    switch (command.action) {
      case 'add':
        if (command.params.title) {
          const newTask = await api.tasks.create({
            title: command.params.title,
            description: '',
          })
          addTask(newTask)
        }
        break

      case 'list':
        // Tasks are already displayed - just provide feedback
        break

      case 'complete':
        if (command.params.id) {
          const task = findTask(command.params.id)
          if (task) {
            const updatedTask = await api.tasks.update(task.id, {
              completed: true,
            })
            updateTask(task.id, updatedTask)
          }
        }
        break

      case 'delete':
        if (command.params.id) {
          const task = findTask(command.params.id)
          if (task) {
            await api.tasks.delete(task.id)
            deleteTask(task.id)
          }
        }
        break

      case 'update':
        if (command.params.id && command.params.title) {
          const task = findTask(command.params.id)
          if (task) {
            const updatedTask = await api.tasks.update(task.id, {
              title: command.params.title,
            })
            updateTask(task.id, updatedTask)
          }
        }
        break
    }
  }

  /**
   * Find task by ID or title
   */
  const findTask = (identifier: string): Task | undefined => {
    // Try to find by ID
    let task = tasks.find((t) => t.id === identifier)

    // Try to find by title
    if (!task) {
      task = tasks.find((t) =>
        t.title.toLowerCase().includes(identifier.toLowerCase())
      )
    }

    // Try to find by index (1-based)
    if (!task) {
      const index = parseInt(identifier, 10)
      if (!isNaN(index) && index > 0 && index <= tasks.length) {
        task = tasks[index - 1]
      }
    }

    return task
  }

  /**
   * Speak text with text-to-speech
   */
  const speak = (text: string) => {
    if (isSpeechEnabled && synthesisRef.current) {
      synthesisRef.current.speak(text)
    }
  }

  /**
   * Toggle voice recognition
   */
  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop()
    } else {
      recognitionRef.current?.start()
    }
  }

  /**
   * Toggle language
   */
  const toggleLanguage = () => {
    setLanguage((prev) => (prev === 'en' ? 'ur' : 'en'))
  }

  /**
   * Toggle continuous mode
   */
  const toggleContinuousMode = () => {
    setIsContinuousMode((prev) => !prev)
  }

  /**
   * Toggle speech feedback
   */
  const toggleSpeech = () => {
    setIsSpeechEnabled((prev) => !prev)
  }

  /**
   * Check if voice is supported
   */
  const isSupported = recognitionRef.current?.isSupported() ?? false

  /**
   * Get status color
   */
  const getStatusColor = (): string => {
    switch (status) {
      case 'listening':
        return 'text-green-500'
      case 'processing':
        return 'text-blue-500'
      case 'error':
        return 'text-red-500'
      case 'unsupported':
        return 'text-gray-500'
      default:
        return 'text-gray-400'
    }
  }

  /**
   * Render help panel
   */
  const renderHelp = () => {
    const commands = getVoiceCommandHelp(language)

    return (
      <Card className="p-4 mt-4 bg-blue-50 dark:bg-blue-900/20">
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-semibold">{t('voice.help')}</h3>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setShowHelp(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
        <ul className="space-y-2 text-sm">
          {commands.map((cmd, index) => (
            <li key={index} className="flex items-start">
              <span className="mr-2">•</span>
              <span>{cmd}</span>
            </li>
          ))}
        </ul>
      </Card>
    )
  }

  if (!isSupported) {
    return (
      <Card className="p-6 text-center">
        <MicOff className="h-12 w-12 mx-auto mb-4 text-gray-400" />
        <p className="text-gray-600 dark:text-gray-400">
          {t('voice.notSupported')}
        </p>
        {onClose && (
          <Button variant="outline" onClick={onClose} className="mt-4">
            Close
          </Button>
        )}
      </Card>
    )
  }

  return (
    <Card className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">{t('voice.title')}</h2>
        {onClose && (
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-5 w-5" />
          </Button>
        )}
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-2 mb-4">
        {/* Microphone button */}
        <Button
          variant={isListening ? 'default' : 'outline'}
          size="lg"
          onClick={toggleListening}
          className={isListening ? 'animate-pulse' : ''}
        >
          {isListening ? (
            <Mic className="h-5 w-5 mr-2" />
          ) : (
            <MicOff className="h-5 w-5 mr-2" />
          )}
          {isContinuousMode
            ? t('voice.continuousMode')
            : t('voice.pushToTalk')}
        </Button>

        {/* Language toggle */}
        <Button variant="outline" onClick={toggleLanguage}>
          {language === 'en' ? 'English' : 'اردو'}
        </Button>

        {/* Continuous mode toggle */}
        <Button
          variant="outline"
          onClick={toggleContinuousMode}
          title={t('voice.continuousMode')}
        >
          {isContinuousMode ? '∞' : '1'}
        </Button>

        {/* Speech feedback toggle */}
        <Button
          variant="outline"
          size="icon"
          onClick={toggleSpeech}
          title="Toggle speech feedback"
        >
          {isSpeechEnabled ? (
            <Volume2 className="h-4 w-4" />
          ) : (
            <VolumeX className="h-4 w-4" />
          )}
        </Button>

        {/* Help button */}
        <Button
          variant="outline"
          size="icon"
          onClick={() => setShowHelp(!showHelp)}
          title={t('voice.help')}
        >
          <HelpCircle className="h-4 w-4" />
        </Button>
      </div>

      {/* Status indicator */}
      <div className="flex items-center gap-2 mb-4">
        <div
          className={`h-3 w-3 rounded-full ${
            isListening ? 'bg-green-500 animate-pulse' : 'bg-gray-300'
          }`}
        />
        <span className={`text-sm ${getStatusColor()}`}>
          {isListening
            ? t('voice.listening')
            : status === 'processing'
              ? t('voice.processing')
              : t('voice.speak')}
        </span>
      </div>

      {/* Transcript display */}
      {transcript && (
        <Card className="p-4 mb-4 bg-gray-50 dark:bg-gray-800">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            {t('voice.transcript')}
          </div>
          <div className="font-medium">{transcript}</div>
          {confidence > 0 && (
            <div className="text-xs text-gray-500 mt-2">
              {t('voice.confidence')}: {Math.round(confidence * 100)}%
            </div>
          )}
          {confidence < 0.7 && confidence > 0 && (
            <div className="text-xs text-yellow-600 dark:text-yellow-400 mt-1">
              {t('voice.lowConfidence')}
            </div>
          )}
        </Card>
      )}

      {/* Last command display */}
      {lastCommand && lastCommand.action !== 'unknown' && (
        <Card className="p-4 mb-4 bg-blue-50 dark:bg-blue-900/20">
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            Last Command
          </div>
          <div className="font-medium">
            {getCommandDescription(lastCommand)}
          </div>
        </Card>
      )}

      {/* Error display */}
      {error && (
        <Card className="p-4 mb-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300">
          {error}
        </Card>
      )}

      {/* Help panel */}
      {showHelp && renderHelp()}

      {/* Visual waveform indicator */}
      {isListening && (
        <div className="flex justify-center items-center gap-1 h-12 mt-4">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="w-1 bg-blue-500 rounded-full animate-pulse"
              style={{
                height: `${20 + Math.random() * 30}px`,
                animationDelay: `${i * 0.1}s`,
              }}
            />
          ))}
        </div>
      )}
    </Card>
  )
}
