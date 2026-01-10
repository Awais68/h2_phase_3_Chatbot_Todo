'use client'

import { useState, useEffect } from 'react'
import { Bell, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { pushNotifications } from '@/lib/notifications'

/**
 * NotificationPrompt Component
 * Prompts user to enable push notifications
 * Shows once, can be dismissed permanently
 */
export function NotificationPrompt() {
  const [showPrompt, setShowPrompt] = useState(false)
  const [isSubscribing, setIsSubscribing] = useState(false)

  useEffect(() => {
    const checkPermission = async () => {
      if (!pushNotifications.isSupported()) return

      const permission = pushNotifications.getPermission()
      const hasSubscription = await pushNotifications.hasSubscription()
      const dismissed = localStorage.getItem('notification-prompt-dismissed')

      // Show prompt if not granted, not subscribed, and not dismissed
      if (permission !== 'granted' && !hasSubscription && !dismissed) {
        // Wait 3 seconds after app load to show
        setTimeout(() => {
          setShowPrompt(true)
        }, 3000)
      }
    }

    checkPermission()
  }, [])

  const handleEnable = async () => {
    setIsSubscribing(true)
    try {
      const subscription = await pushNotifications.subscribe()
      if (subscription) {
        setShowPrompt(false)
      }
    } catch (error) {
      console.error('Failed to subscribe:', error)
    } finally {
      setIsSubscribing(false)
    }
  }

  const handleDismiss = () => {
    localStorage.setItem('notification-prompt-dismissed', 'true')
    setShowPrompt(false)
  }

  return (
    <AnimatePresence>
      {showPrompt && (
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 50 }}
          transition={{ duration: 0.3 }}
          className="fixed bottom-4 left-4 right-4 z-50 max-w-md mx-auto"
        >
          <Card className="p-4 shadow-xl border-2">
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                <Bell className="h-5 w-5 text-primary" />
              </div>

              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-semibold mb-1">
                  Enable Notifications
                </h3>
                <p className="text-xs text-muted-foreground mb-3">
                  Get notified about your tasks and sync updates even when the app is closed
                </p>

                <div className="flex gap-2">
                  <Button
                    size="sm"
                    onClick={handleEnable}
                    disabled={isSubscribing}
                    className="flex-1"
                  >
                    {isSubscribing ? 'Enabling...' : 'Enable'}
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={handleDismiss}
                    disabled={isSubscribing}
                  >
                    Later
                  </Button>
                </div>
              </div>

              <button
                onClick={handleDismiss}
                className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full hover:bg-muted transition-colors"
                disabled={isSubscribing}
                aria-label="Dismiss"
              >
                <X className="h-4 w-4 text-muted-foreground" />
              </button>
            </div>
          </Card>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
