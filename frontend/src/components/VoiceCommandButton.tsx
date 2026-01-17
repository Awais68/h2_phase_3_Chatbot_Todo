'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, MicOff, Volume2 } from 'lucide-react'

interface VoiceCommandButtonProps {
  onCommand: (command: string) => boolean | void
  size?: 'sm' | 'md' | 'lg'
}

// Add type declarations for Speech Recognition

export default function VoiceCommandButton({ onCommand, size = 'md' }: VoiceCommandButtonProps) {
  const [isListening, setIsListening] = useState(false)
  const [isSupported, setIsSupported] = useState(true)
  const [transcript, setTranscript] = useState('')
  const [feedback, setFeedback] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [autoSendCountdown, setAutoSendCountdown] = useState<number | null>(null)

  const recognitionRef = useRef<SpeechRecognition | null>(null)
  const autoSendTimerRef = useRef<NodeJS.Timeout | null>(null)

  // Store callback in ref to avoid stale closures
  const onCommandRef = useRef(onCommand)

  useEffect(() => {
    onCommandRef.current = onCommand
  }, [onCommand])

  // Cleanup auto-send timer on unmount
  useEffect(() => {
    return () => {
      if (autoSendTimerRef.current) {
        clearTimeout(autoSendTimerRef.current)
      }
    }
  }, [])

  useEffect(() => {
    // Check for browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      setIsSupported(false)
      console.log('Speech Recognition not supported in this browser')
      return
    }

    const recognition: any = new (window.SpeechRecognition || window.webkitSpeechRecognition)()
    recognition.continuous = false
    recognition.interimResults = true
    recognition.lang = 'en-US'

    recognition.onstart = () => {
      console.log('Voice recognition started')
      setIsListening(true)
      setTranscript('')
      setError(null)
      setFeedback('')
      setAutoSendCountdown(null)
      // Clear any existing timer
      if (autoSendTimerRef.current) {
        clearTimeout(autoSendTimerRef.current)
      }
    }

    recognition.onresult = (event: any) => {
      const current = event.resultIndex
      const result = event.results[current]
      const transcriptText = result[0].transcript

      console.log('Recognized:', transcriptText, 'Final:', result.isFinal)
      setTranscript(transcriptText)

      if (result.isFinal) {
        // Start auto-send countdown (3 seconds)
        setAutoSendCountdown(3)

        // Clear any existing timer
        if (autoSendTimerRef.current) {
          clearTimeout(autoSendTimerRef.current)
        }

        // Countdown animation
        let countdown = 3
        const countdownInterval = setInterval(() => {
          countdown -= 1
          setAutoSendCountdown(countdown)
          if (countdown <= 0) {
            clearInterval(countdownInterval)
          }
        }, 1000)

        // Auto-send after 3 seconds
        autoSendTimerRef.current = setTimeout(() => {
          console.log('Auto-sending command:', transcriptText)
          // Use ref to get latest callback
          const wasHandled = onCommandRef.current(transcriptText)
          console.log('Command handled:', wasHandled)

          // Provide feedback
          if (wasHandled) {
            setFeedback('✓ Command executed!')
            speak('Mission initialized successfully')
          } else {
            setFeedback('Command recognized')
            speak('Processing command')
          }

          setAutoSendCountdown(null)
        }, 3000)
      }
    }

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error)
      setIsListening(false)
      setAutoSendCountdown(null)
      if (autoSendTimerRef.current) {
        clearTimeout(autoSendTimerRef.current)
      }
      if (event.error === 'not-allowed') {
        setError('Microphone access denied - please allow microphone')
      } else if (event.error === 'no-speech') {
        setError('No speech detected - try again')
      } else if (event.error === 'aborted') {
        setError('Recognition aborted')
      } else {
        setError(`Error: ${event.error}`)
      }
    }

    recognition.onend = () => {
      console.log('Voice recognition ended')
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      recognition.stop()
    }
  }, [])

  const speak = useCallback((text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 1.1
      utterance.pitch = 1
      utterance.volume = 0.8
      window.speechSynthesis.speak(utterance)
    }
  }, [])

  const toggleListening = useCallback(() => {
    if (!recognitionRef.current) return

    if (isListening) {
      recognitionRef.current.stop()
    } else {
      setError(null)
      setFeedback('')
      try {
        recognitionRef.current.start()
      } catch (e) {
        console.error('Failed to start recognition:', e)
        setError('Failed to start - try again')
      }
    }
  }, [isListening])

  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12',
  }

  const iconSizes = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6',
  }

  if (!isSupported) {
    return null
  }

  return (
    <div className="relative">
      <button
        onClick={toggleListening}
        className={`relative flex items-center justify-center rounded-full transition-all shadow-lg ${isListening
          ? 'bg-gradient-to-r from-purple-500 to-violet-600 text-white animate-pulse shadow-purple-500/50'
          : 'bg-gradient-to-r from-purple-400 to-violet-500 hover:from-purple-500 hover:to-violet-600 text-white shadow-purple-400/30'
          } ${sizeClasses[size]}`}
        title={isListening ? 'Stop listening' : 'Start voice command'}
      >
        {isListening ? (
          <Mic className={`${iconSizes[size]} animate-pulse`} />
        ) : (
          <Mic className={iconSizes[size]} />
        )}
      </button>

      {/* Sound Wave Animation */}
      <AnimatePresence>
        {isListening && (
          <div className="absolute left-1/2 bottom-full mb-2 -translate-x-1/2 flex items-end gap-0.5">
            {[...Array(5)].map((_, i) => (
              <motion.div
                key={i}
                className="w-1 bg-purple-500 rounded-full"
                initial={{ height: 4 }}
                animate={{ height: [4, 16, 8, 20, 4] }}
                transition={{
                  duration: 0.5,
                  repeat: Infinity,
                  delay: i * 0.1,
                  ease: 'easeInOut',
                }}
              />
            ))}
          </div>
        )}
      </AnimatePresence>

      {/* Feedback Overlay */}
      <AnimatePresence>
        {(isListening || error || feedback || autoSendCountdown !== null) && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute top-full right-0 mt-2 min-w-[200px] bg-card border border-purple-500/30 rounded-lg shadow-lg shadow-purple-500/10 p-3 z-50"
          >
            {error ? (
              <div className="flex items-center gap-2 text-red-500 text-sm">
                <MicOff className="h-4 w-4" />
                <span className="font-mono">{error}</span>
              </div>
            ) : isListening ? (
              <>
                <div className="flex items-center gap-2 text-purple-500 mb-2">
                  <Mic className="h-4 w-4 animate-pulse" />
                  <span className="font-mono text-xs uppercase tracking-wider">Listening...</span>
                </div>
                {transcript && (
                  <p className="font-mono text-sm text-foreground bg-secondary/30 rounded px-2 py-1">
                    &quot;{transcript}&quot;
                  </p>
                )}
                {autoSendCountdown !== null && (
                  <div className="mt-2 flex items-center gap-2">
                    <div className="flex-1 h-1 bg-secondary rounded-full overflow-hidden">
                      <motion.div
                        className="h-full bg-gradient-to-r from-purple-500 to-violet-600"
                        initial={{ width: '100%' }}
                        animate={{ width: '0%' }}
                        transition={{ duration: 3, ease: 'linear' }}
                      />
                    </div>
                    <span className="font-mono text-xs text-purple-500 font-bold">
                      {autoSendCountdown}s
                    </span>
                  </div>
                )}
                {feedback && (
                  <p className="font-mono text-xs text-success mt-2">
                    {feedback}
                  </p>
                )}
              </>
            ) : feedback ? (
              <div className="flex items-center gap-2 text-green-500 text-sm">
                <span className="font-mono">{feedback}</span>
              </div>
            ) : null}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
