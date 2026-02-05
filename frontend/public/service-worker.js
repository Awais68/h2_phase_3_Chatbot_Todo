/**
 * Service Worker for Task Manager PWA
 * Handles caching, push notifications, and background sync
 * Enhanced with due date notification support
 */

const CACHE_NAME = 'task-manager-v2'
const API_CACHE_NAME = 'task-manager-api-v1'

const urlsToCache = [
  '/',
  '/manifest.json',
  '/icon-192x192.png',
  '/icon-512x512.png',
]

// Install event - cache essential resources
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installing...')

  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => {
        console.log('[ServiceWorker] Caching app shell')
        return cache.addAll(urlsToCache)
      })
      .then(() => self.skipWaiting())
  )
})

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activating...')

  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
              console.log('[ServiceWorker] Removing old cache:', cacheName)
              return caches.delete(cacheName)
            }
          })
        )
      })
      .then(() => self.clients.claim())
  )
})

// Fetch event - network first, fall back to cache
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Handle API requests differently
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache successful GET requests
          if (request.method === 'GET' && response.ok) {
            const responseToCache = response.clone()
            caches.open(API_CACHE_NAME).then((cache) => {
              cache.put(request, responseToCache)
            })
          }
          return response
        })
        .catch(() => {
          // Network failed, try cache for GET requests
          if (request.method === 'GET') {
            return caches.match(request)
          }
          // For other methods, return error response
          return new Response(
            JSON.stringify({ error: 'Network unavailable' }),
            {
              status: 503,
              headers: { 'Content-Type': 'application/json' },
            }
          )
        })
    )
    return
  }

  // Default fetch handler for static assets
  event.respondWith(
    fetch(request)
      .then((response) => {
        // Clone the response
        const responseToCache = response.clone()

        // Cache the response for next time
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(request, responseToCache)
        })

        return response
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(request)
      })
  )
})

// Push notification event - handle server push notifications
self.addEventListener('push', (event) => {
  console.log('[ServiceWorker] Push notification received')

  const defaultOptions = {
    icon: '/icon-192x192.png',
    badge: '/icon-72x72.png',
    vibrate: [200, 100, 200],
    requireInteraction: false,
  }

  if (event.data) {
    try {
      const data = event.data.json()
      const title = data.title || 'Task Manager'
      const body = data.body || 'You have a new notification'
      const tag = data.tag || 'task-notification'

      event.waitUntil(
        self.registration.showNotification(title, {
          ...defaultOptions,
          body,
          tag,
          data: data.data || {},
          actions: data.actions || [
            {
              action: 'view',
              title: 'View Task',
            },
            {
              action: 'dismiss',
              title: 'Dismiss',
            },
          ],
        })
      )
    } catch (error) {
      console.error('[ServiceWorker] Error parsing push data:', error)
      event.waitUntil(
        self.registration.showNotification('Task Manager', {
          ...defaultOptions,
          body: 'You have a new notification',
        })
      )
    }
  }
})

// Notification click event - handle user interaction with notifications
self.addEventListener('notificationclick', (event) => {
  console.log('[ServiceWorker] Notification clicked:', event.action)

  event.notification.close()

  if (event.action === 'dismiss') {
    // User dismissed the notification
    return
  }

  // Default action or 'view' action - open the app
  const urlToOpen = event.notification.data?.url || '/'

  event.waitUntil(
    clients
      .matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // Check if there's already a window open
        for (const client of clientList) {
          if (client.url === urlToOpen && 'focus' in client) {
            return client.focus()
          }
        }
        // No window open, open a new one
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen)
        }
      })
  )
})

// Background sync event - handle offline task sync
self.addEventListener('sync', (event) => {
  console.log('[ServiceWorker] Background sync triggered:', event.tag)

  if (event.tag === 'sync-tasks') {
    event.waitUntil(
      // Sync logic will be handled by the app
      // This just confirms the sync was triggered
      self.clients
        .matchAll()
        .then((clients) => {
          clients.forEach((client) => {
            client.postMessage({
              type: 'SYNC_TASKS',
              timestamp: Date.now(),
            })
          })
        })
        .then(() => {
          return self.registration.showNotification('Task Manager', {
            body: 'Tasks synced successfully',
            icon: '/icon-192x192.png',
            badge: '/icon-72x72.png',
            tag: 'sync-complete',
          })
        })
        .catch((error) => {
          console.error('[ServiceWorker] Sync failed:', error)
        })
    )
  }
})

// Message event - handle messages from the app
self.addEventListener('message', (event) => {
  console.log('[ServiceWorker] Message received:', event.data)

  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }

  if (event.data && event.data.type === 'SHOW_NOTIFICATION') {
    const { title, body, tag, data, requireInteraction } = event.data
    self.registration.showNotification(title, {
      body,
      icon: '/icon-192x192.png',
      badge: '/icon-72x72.png',
      tag: tag || 'app-notification',
      data: data || {},
      requireInteraction: requireInteraction || false,
      vibrate: [200, 100, 200],
    })
  }

  if (event.data && event.data.type === 'SCHEDULE_NOTIFICATION') {
    // Store scheduled notification data
    const { id, scheduledTime, title, body, tag, data } = event.data
    const delay = new Date(scheduledTime).getTime() - Date.now()

    if (delay > 0) {
      setTimeout(() => {
        self.registration.showNotification(title, {
          body,
          icon: '/icon-192x192.png',
          badge: '/icon-72x72.png',
          tag: tag || `scheduled-${id}`,
          data: data || {},
          requireInteraction: true,
          vibrate: [200, 100, 200],
          actions: [
            {
              action: 'view',
              title: 'View Task',
            },
            {
              action: 'snooze',
              title: 'Snooze',
            },
            {
              action: 'dismiss',
              title: 'Dismiss',
            },
          ],
        })
      }, delay)
    }
  }
})

// Periodic background sync (experimental)
self.addEventListener('periodicsync', (event) => {
  console.log('[ServiceWorker] Periodic sync triggered:', event.tag)

  if (event.tag === 'check-due-tasks') {
    event.waitUntil(
      // Check for tasks due soon
      self.clients
        .matchAll()
        .then((clients) => {
          clients.forEach((client) => {
            client.postMessage({
              type: 'CHECK_DUE_TASKS',
              timestamp: Date.now(),
            })
          })
        })
    )
  }
})

console.log('[ServiceWorker] Service worker loaded')
