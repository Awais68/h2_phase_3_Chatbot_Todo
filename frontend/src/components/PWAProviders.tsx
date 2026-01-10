'use client'

import { useEffect } from 'react'
import { setupAutoSync, syncManager } from '@/lib/sync'

/**
 * PWA Providers Component
 * Initializes PWA features like sync, service worker, etc.
 */
export function PWAProviders({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize app on mount
    const init = async () => {
      // Load tasks from IndexedDB/API
      await syncManager.loadTasks()

      // Setup automatic sync on network changes
      setupAutoSync()

      // Register service worker
      if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
        navigator.serviceWorker
          .register('/sw.js')
          .then((registration) => {
            console.log('Service Worker registered:', registration)
          })
          .catch((error) => {
            console.error('Service Worker registration failed:', error)
          })
      }
    }

    init()
  }, [])

  return <>{children}</>
}
