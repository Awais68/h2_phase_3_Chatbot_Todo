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

      // Register service worker for notifications and offline support
      if ('serviceWorker' in navigator) {
        try {
          // Register the service worker
          const registration = await navigator.serviceWorker.register('/service-worker.js', {
            scope: '/',
          });

          console.log('Service Worker registered successfully:', registration.scope);

          // Wait for service worker to be ready
          await navigator.serviceWorker.ready;
          console.log('Service Worker is ready');

          // Listen for messages from service worker
          navigator.serviceWorker.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'NOTIFICATION_CLICK') {
              console.log('Notification clicked:', event.data.taskId);
              // Handle notification click (e.g., navigate to task)
            }
          });

        } catch (error) {
          console.error('Service Worker registration failed:', error);
        }
      } else {
        console.warn('Service Worker not supported in this browser');
      }
    }

    init()
  }, [])

  return <>{children}</>
}
