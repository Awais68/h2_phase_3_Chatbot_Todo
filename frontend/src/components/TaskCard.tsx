'use client'

import { useState } from 'react'
import { useSwipeable } from 'react-swipeable'
import { motion, useAnimation } from 'framer-motion'
import { Trash2, Clock, Calendar } from 'lucide-react'
import { Card } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Task } from '@/types'
import { cn } from '@/lib/utils'
import { getDueDateStatus } from '@/utils/dateUtils'
import { formatDueDate } from '@/utils/formatters'

/**
 * Props for TaskCard component
 */
interface TaskCardProps {
  task: Task
  onToggleComplete: (id: string) => void
  onDelete: (id: string) => void
}

/**
 * TaskCard Component
 * Mobile-optimized task card with swipe gestures
 * - Swipe left to delete (red background)
 * - Swipe right to complete (green background)
 * - 44x44px minimum touch targets (WCAG AA)
 */
export function TaskCard({ task, onToggleComplete, onDelete }: TaskCardProps) {
  const [swipeDirection, setSwipeDirection] = useState<'left' | 'right' | null>(null)
  const controls = useAnimation()

  const handlers = useSwipeable({
    onSwipedLeft: (eventData) => {
      // Swipe left to delete
      if (Math.abs(eventData.deltaX) > 100) {
        setSwipeDirection('left')
        controls.start({ x: -300, opacity: 0 })
        setTimeout(() => onDelete(task.id), 300)
      }
    },
    onSwipedRight: (eventData) => {
      // Swipe right to complete/uncomplete
      if (Math.abs(eventData.deltaX) > 100) {
        setSwipeDirection('right')
        controls.start({ x: 300, opacity: 0 })
        setTimeout(() => {
          onToggleComplete(task.id)
          controls.start({ x: 0, opacity: 1 })
          setSwipeDirection(null)
        }, 300)
      }
    },
    onSwiping: (eventData) => {
      // Show visual feedback during swipe
      if (eventData.deltaX < -50) {
        setSwipeDirection('left')
      } else if (eventData.deltaX > 50) {
        setSwipeDirection('right')
      } else {
        setSwipeDirection(null)
      }
    },
    onSwiped: () => {
      // Reset after swipe ends (if not deleting/completing)
      setTimeout(() => {
        setSwipeDirection(null)
        controls.start({ x: 0 })
      }, 100)
    },
    trackMouse: false, // Only track touch, not mouse
    trackTouch: true,
    delta: 10, // Minimum distance before swipe is registered
  })

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  // Get due date status for styling
  const dueDateInfo = getDueDateStatus(task.due_date);

  return (
    <div className="relative overflow-hidden rounded-xl">
      {/* Swipe background indicators */}
      {swipeDirection === 'left' && (
        <div className="absolute inset-0 bg-destructive flex items-center justify-end px-6 rounded-xl">
          <Trash2 className="h-6 w-6 text-destructive-foreground" />
        </div>
      )}
      {swipeDirection === 'right' && (
        <div className="absolute inset-0 bg-green-500 flex items-center justify-start px-6 rounded-xl">
          <svg className="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
      )}

      {/* Card content */}
      <motion.div
        {...handlers}
        animate={controls}
        initial={{ x: 0, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className="relative"
      >
        <Card className={cn(
          "p-4 touch-pan-y",
          task.completed && "opacity-60",
          dueDateInfo.status && dueDateInfo.borderColor
        )}>
          <div className="flex items-start space-x-3">
            {/* Checkbox - 44x44px touch target */}
            <button
              onClick={() => onToggleComplete(task.id)}
              className="flex-shrink-0 w-11 h-11 flex items-center justify-center -m-2.5"
              aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
            >
              <Checkbox
                checked={task.completed}
                onCheckedChange={() => onToggleComplete(task.id)}
                className="pointer-events-none"
              />
            </button>

            {/* Task content */}
            <div className="flex-1 min-w-0 space-y-1">
              <h3 className={cn(
                "text-base font-medium leading-tight",
                task.completed && "line-through text-muted-foreground"
              )}>
                {task.title}
              </h3>
              {task.description && (
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {task.description}
                </p>
              )}

              {/* Due Date Indicator */}
              {task.due_date && dueDateInfo.status && (
                <div className={cn(
                  "inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium",
                  dueDateInfo.color,
                  dueDateInfo.bgColor
                )}>
                  {dueDateInfo.status === 'overdue' && <Clock className="h-3 w-3" />}
                  {dueDateInfo.status === 'due_today' && <Calendar className="h-3 w-3" />}
                  {dueDateInfo.status === 'upcoming' && <Calendar className="h-3 w-3" />}
                  <span>{dueDateInfo.displayText}</span>
                </div>
              )}

              <p className="text-xs text-muted-foreground pt-1">
                {formatDate(task.updatedAt)}
              </p>
            </div>

            {/* Delete button - 44x44px touch target */}
            <button
              onClick={() => onDelete(task.id)}
              className="flex-shrink-0 w-11 h-11 flex items-center justify-center -m-2.5 text-muted-foreground hover:text-destructive transition-colors"
              aria-label="Delete task"
            >
              <Trash2 className="h-5 w-5" />
            </button>
          </div>
        </Card>
      </motion.div>
    </div>
  )
}
