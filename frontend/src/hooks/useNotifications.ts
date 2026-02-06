/**
 * Custom hook for managing browser notifications
 * Handles permission requests and scheduling notifications
 */

import { useState, useEffect, useCallback } from 'react'

export type NotificationPermissionState = 'default' | 'granted' | 'denied'

interface NotificationOptions {
  title: string
  body: string
  icon?: string
  tag?: string
  data?: any
  requireInteraction?: boolean
  silent?: boolean
}

interface ScheduledNotification {
  id: string
  scheduledTime: Date
  options: NotificationOptions
  timeoutId?: NodeJS.Timeout
}

export const useNotifications = () => {
  const [permission, setPermission] = useState<NotificationPermissionState>('default')
  const [isSupported, setIsSupported] = useState(false)
  const [scheduledNotifications, setScheduledNotifications] = useState<Map<string, ScheduledNotification>>(
    new Map()
  )

  // Check browser notification support
  useEffect(() => {
    if (typeof window !== 'undefined' && 'Notification' in window) {
      setIsSupported(true)
      setPermission(Notification.permission as NotificationPermissionState)
    } else {
      setIsSupported(false)
      console.warn('Browser does not support notifications')
    }
  }, [])

  /**
   * Request notification permission from the user
   * @returns Promise resolving to the permission state
   */
  const requestPermission = useCallback(async (): Promise<NotificationPermissionState> => {
    if (!isSupported) {
      console.warn('Notifications are not supported in this browser')
      return 'denied'
    }

    try {
      const result = await Notification.requestPermission()
      setPermission(result as NotificationPermissionState)
      return result as NotificationPermissionState
    } catch (error) {
      console.error('Error requesting notification permission:', error)
      return 'denied'
    }
  }, [isSupported])

  /**
   * Show an immediate notification
   * @param options Notification options
   */
  const showNotification = useCallback(
    async (options: NotificationOptions): Promise<void> => {
      if (!isSupported) {
        console.warn('Notifications are not supported')
        return
      }

      // Request permission if not already granted
      let currentPermission = permission
      if (currentPermission === 'default') {
        currentPermission = await requestPermission()
      }

      if (currentPermission !== 'granted') {
        console.warn('Notification permission not granted')
        return
      }

      try {
        // Try to use service worker notification first
        if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
          const registration = await navigator.serviceWorker.ready
          await registration.showNotification(options.title, {
            body: options.body,
            icon: options.icon || '/icon-192x192.png',
            badge: '/icon-72x72.png',
            tag: options.tag,
            data: options.data,
            requireInteraction: options.requireInteraction,
            silent: options.silent,
          })
        } else {
          // Fallback to regular notification
          new Notification(options.title, {
            body: options.body,
            icon: options.icon || '/icon-192x192.png',
            tag: options.tag,
            data: options.data,
            requireInteraction: options.requireInteraction,
            silent: options.silent,
          })
        }
      } catch (error) {
        console.error('Error showing notification:', error)
      }
    },
    [isSupported, permission, requestPermission]
  )

  /**
   * Schedule a notification to be shown at a specific time
   * @param id Unique identifier for the scheduled notification
   * @param scheduledTime When to show the notification
   * @param options Notification options
   */
  const scheduleNotification = useCallback(
    (id: string, scheduledTime: Date, options: NotificationOptions): void => {
      if (!isSupported) {
        console.warn('Notifications are not supported')
        return
      }

      // Cancel existing notification with same ID
      const existing = scheduledNotifications.get(id)
      if (existing?.timeoutId) {
        clearTimeout(existing.timeoutId)
      }

      const now = new Date()
      const delay = scheduledTime.getTime() - now.getTime()

      if (delay <= 0) {
        // Time has passed, show immediately
        showNotification(options)
        return
      }

      // Schedule the notification
      const timeoutId = setTimeout(() => {
        showNotification(options)
        // Remove from scheduled list after showing
        setScheduledNotifications((prev) => {
          const next = new Map(prev)
          next.delete(id)
          return next
        })
      }, delay)

      // Store in scheduled notifications map
      setScheduledNotifications((prev) => {
        const next = new Map(prev)
        next.set(id, {
          id,
          scheduledTime,
          options,
          timeoutId,
        })
        return next
      })
    },
    [isSupported, scheduledNotifications, showNotification]
  )

  /**
   * Cancel a scheduled notification
   * @param id Unique identifier of the notification to cancel
   */
  const cancelScheduledNotification = useCallback((id: string): void => {
    const notification = scheduledNotifications.get(id)
    if (notification?.timeoutId) {
      clearTimeout(notification.timeoutId)
      setScheduledNotifications((prev) => {
        const next = new Map(prev)
        next.delete(id)
        return next
      })
    }
  }, [scheduledNotifications])

  /**
   * Cancel all scheduled notifications
   */
  const cancelAllScheduledNotifications = useCallback((): void => {
    scheduledNotifications.forEach((notification) => {
      if (notification.timeoutId) {
        clearTimeout(notification.timeoutId)
      }
    })
    setScheduledNotifications(new Map())
  }, [scheduledNotifications])

  // Cleanup timeouts on unmount
  useEffect(() => {
    return () => {
      scheduledNotifications.forEach((notification) => {
        if (notification.timeoutId) {
          clearTimeout(notification.timeoutId)
        }
      })
    }
  }, [scheduledNotifications])

  return {
    permission,
    isSupported,
    requestPermission,
    showNotification,
    scheduleNotification,
    cancelScheduledNotification,
    cancelAllScheduledNotifications,
    scheduledNotifications: Array.from(scheduledNotifications.values()),
  }
}
