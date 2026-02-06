'use client'

import { useEffect } from 'react'
import { WifiOff, Wifi, RefreshCw, CheckCircle2, XCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTaskStore } from '@/stores/useTaskStore'
import { syncManager } from '@/lib/sync'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

/**
 * OfflineIndicator Component
 * Shows network status and sync operations
 * - Green: Online and synced
 * - Yellow: Syncing
 * - Red: Offline or sync error
 * - Button to manually trigger sync
 */
export function OfflineIndicator() {
  const { isOffline, syncStatus } = useTaskStore()

  const handleSync = async () => {
    await syncManager.syncWithBackend()
  }

  const getStatusConfig = () => {
    if (isOffline) {
      return {
        icon: WifiOff,
        text: 'Working Offline',
        color: 'text-orange-500',
        bgColor: 'bg-orange-500/10',
        show: true,
      }
    }

    if (syncStatus === 'syncing') {
      return {
        icon: RefreshCw,
        text: 'Syncing...',
        color: 'text-blue-500',
        bgColor: 'bg-blue-500/10',
        show: true,
        animate: true,
      }
    }

    if (syncStatus === 'error') {
      return {
        icon: XCircle,
        text: 'Sync Failed - Working Offline',
        color: 'text-red-500',
        bgColor: 'bg-red-500/10',
        show: true,
      }
    }

    if (syncStatus === 'success') {
      return {
        icon: CheckCircle2,
        text: 'Synced',
        color: 'text-green-500',
        bgColor: 'bg-green-500/10',
        show: true, // Show success briefly
      }
    }

    return {
      icon: Wifi,
      text: 'Online',
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
      show: false, // Hide when online and idle
    }
  }

  const status = getStatusConfig()
  const Icon = status.icon

  // Auto-hide success message after 2 seconds
  useEffect(() => {
    if (syncStatus === 'success') {
      const timer = setTimeout(() => {
        useTaskStore.getState().setSyncStatus('idle')
      }, 2000)
      return () => clearTimeout(timer)
    }
  }, [syncStatus])

  return (
    <AnimatePresence>
      {status.show && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.2 }}
          className="fixed top-0 left-0 right-0 z-50 flex items-center justify-center p-4"
        >
          <div className={cn(
            "flex items-center gap-3 px-4 py-2.5 rounded-full shadow-lg border backdrop-blur-sm",
            status.bgColor
          )}>
            <Icon
              className={cn(
                "h-5 w-5",
                status.color,
                status.animate && "animate-spin"
              )}
            />
            <span className={cn("text-sm font-medium", status.color)}>
              {status.text}
            </span>

            {(isOffline || syncStatus === 'error') && (
              <Button
                size="sm"
                variant="ghost"
                onClick={handleSync}
                disabled={syncStatus === 'syncing'}
                className="h-7 px-2 -mr-1"
              >
                <RefreshCw className="h-4 w-4" />
              </Button>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
