'use client'

import { useState, FormEvent } from 'react'
import { Plus } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { useTaskStore } from '@/stores/useTaskStore'
import { syncManager } from '@/lib/sync'
import { api } from '@/lib/api'

/**
 * AddTaskForm Component
 * Mobile-optimized form for creating new tasks
 * - Optimized for mobile keyboard
 * - Works offline with sync queue
 * - Auto-focus and submit on enter
 */
export function AddTaskForm() {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { isOffline } = useTaskStore()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    if (!title.trim()) return

    setIsSubmitting(true)

    try {
      const taskData = {
        title: title.trim(),
        description: description.trim() || undefined,
      }

      if (isOffline) {
        // Offline mode - queue operation
        await syncManager.createTaskOffline(taskData)
      } else {
        // Online mode - call API directly
        try {
          const task = await api.tasks.create(taskData)
          useTaskStore.getState().addTask(task)
        } catch (error) {
          // Fallback to offline if API fails
          await syncManager.createTaskOffline(taskData)
        }
      }

      // Clear form
      setTitle('')
      setDescription('')
    } catch (error) {
      console.error('Failed to create task:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card className="p-4">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="space-y-2">
          <Input
            type="text"
            placeholder="Task title *"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={isSubmitting}
            autoComplete="off"
            className="text-base" // Prevent iOS zoom on input focus
            required
          />
          <Input
            type="text"
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isSubmitting}
            autoComplete="off"
            className="text-base" // Prevent iOS zoom on input focus
          />
        </div>

        <Button
          type="submit"
          disabled={!title.trim() || isSubmitting}
          className="w-full"
          size="lg"
        >
          <Plus className="h-5 w-5 mr-2" />
          {isSubmitting ? 'Adding...' : 'Add Task'}
        </Button>
      </form>
    </Card>
  )
}
