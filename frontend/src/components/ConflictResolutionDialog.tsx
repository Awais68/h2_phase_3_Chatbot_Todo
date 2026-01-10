'use client'

import { AlertCircle } from 'lucide-react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Task } from '@/types'
import { syncManager } from '@/lib/sync'
import { useTaskStore } from '@/stores/useTaskStore'

/**
 * Props for ConflictResolutionDialog
 */
interface ConflictResolutionDialogProps {
  conflicts: Task[]
  onResolve: () => void
}

/**
 * ConflictResolutionDialog Component
 * Shows UI for resolving sync conflicts
 * User can choose to keep local or remote version
 */
export function ConflictResolutionDialog({
  conflicts,
  onResolve,
}: ConflictResolutionDialogProps) {
  if (conflicts.length === 0) return null

  const handleResolve = async (taskId: string, useLocal: boolean) => {
    await syncManager.resolveConflict(taskId, useLocal)
    onResolve()
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4"
    >
      <Card className="w-full max-w-lg max-h-[80vh] overflow-y-auto p-6 space-y-4">
        {/* Header */}
        <div className="flex items-center gap-3 pb-2 border-b">
          <div className="flex-shrink-0 w-10 h-10 rounded-full bg-orange-500/10 flex items-center justify-center">
            <AlertCircle className="h-6 w-6 text-orange-500" />
          </div>
          <div>
            <h2 className="text-lg font-semibold">Sync Conflicts</h2>
            <p className="text-sm text-muted-foreground">
              {conflicts.length} task{conflicts.length > 1 ? 's' : ''} modified in both places
            </p>
          </div>
        </div>

        {/* Conflict list */}
        <div className="space-y-4">
          {conflicts.map((task) => (
            <ConflictItem
              key={task.id}
              task={task}
              onResolve={(useLocal) => handleResolve(task.id, useLocal)}
            />
          ))}
        </div>
      </Card>
    </motion.div>
  )
}

/**
 * Individual conflict item
 */
function ConflictItem({
  task,
  onResolve,
}: {
  task: Task
  onResolve: (useLocal: boolean) => void
}) {
  const { tasks } = useTaskStore()
  const localTask = tasks.find((t) => t.id === task.id)

  return (
    <div className="border rounded-lg p-4 space-y-3">
      <h3 className="font-medium text-sm">
        {task.title}
      </h3>

      <div className="grid grid-cols-2 gap-3">
        {/* Local version */}
        <div className="space-y-2">
          <p className="text-xs font-medium text-muted-foreground">
            Your Device
          </p>
          <div className="text-sm space-y-1 p-2 rounded bg-muted/50">
            {localTask && (
              <>
                <p className={localTask.completed ? 'line-through' : ''}>
                  {localTask.title}
                </p>
                {localTask.description && (
                  <p className="text-xs text-muted-foreground line-clamp-2">
                    {localTask.description}
                  </p>
                )}
                <p className="text-xs text-muted-foreground">
                  v{localTask.version}
                </p>
              </>
            )}
          </div>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onResolve(true)}
            className="w-full"
          >
            Keep This
          </Button>
        </div>

        {/* Remote version */}
        <div className="space-y-2">
          <p className="text-xs font-medium text-muted-foreground">
            Server
          </p>
          <div className="text-sm space-y-1 p-2 rounded bg-muted/50">
            <p className={task.completed ? 'line-through' : ''}>
              {task.title}
            </p>
            {task.description && (
              <p className="text-xs text-muted-foreground line-clamp-2">
                {task.description}
              </p>
            )}
            <p className="text-xs text-muted-foreground">
              v{task.version}
            </p>
          </div>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onResolve(false)}
            className="w-full"
          >
            Use Server
          </Button>
        </div>
      </div>
    </div>
  )
}
