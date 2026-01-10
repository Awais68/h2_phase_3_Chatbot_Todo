'use client'

import { TaskCard } from './TaskCard'
import { TaskListSkeleton } from './TaskCardSkeleton'
import { useTaskStore } from '@/stores/useTaskStore'
import { syncManager } from '@/lib/sync'
import { api } from '@/lib/api'

/**
 * TaskList Component
 * Displays list of tasks with swipe gesture support
 * Handles online/offline task operations
 */
export function TaskList() {
  const { tasks, loading } = useTaskStore()
  const { isOffline } = useTaskStore()

  const handleToggleComplete = async (id: string) => {
    const task = tasks.find((t) => t.id === id)
    if (!task) return

    const updates = { completed: !task.completed }

    if (isOffline) {
      // Offline mode - queue operation
      await syncManager.updateTaskOffline(id, updates)
    } else {
      // Online mode - call API directly
      try {
        await api.tasks.update(id, updates)
        useTaskStore.getState().updateTask(id, updates)
      } catch (error) {
        // Fallback to offline if API fails
        await syncManager.updateTaskOffline(id, updates)
      }
    }
  }

  const handleDelete = async (id: string) => {
    if (isOffline) {
      // Offline mode - queue operation
      await syncManager.deleteTaskOffline(id)
    } else {
      // Online mode - call API directly
      try {
        await api.tasks.delete(id)
        useTaskStore.getState().deleteTask(id)
      } catch (error) {
        // Fallback to offline if API fails
        await syncManager.deleteTaskOffline(id)
      }
    }
  }

  if (loading) {
    return <TaskListSkeleton count={3} />
  }

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
        <div className="text-6xl mb-4">📝</div>
        <h3 className="text-lg font-medium mb-2">No tasks yet</h3>
        <p className="text-sm text-muted-foreground max-w-sm">
          Add your first task to get started. You can add tasks even when offline!
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
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
