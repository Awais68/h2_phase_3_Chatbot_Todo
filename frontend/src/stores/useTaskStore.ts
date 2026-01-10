import { create } from 'zustand'
import { Task } from '@/types'

/**
 * Task store state interface
 */
interface TaskState {
  tasks: Task[]
  loading: boolean
  error: string | null
  syncStatus: 'idle' | 'syncing' | 'success' | 'error'
  isOffline: boolean

  // Actions
  setTasks: (tasks: Task[]) => void
  addTask: (task: Task) => void
  updateTask: (id: string, updates: Partial<Task>) => void
  deleteTask: (id: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  setSyncStatus: (status: 'idle' | 'syncing' | 'success' | 'error') => void
  setOffline: (offline: boolean) => void
  clearTasks: () => void
}

/**
 * Zustand store for task management
 * Provides global state management for tasks, loading, and sync status
 */
export const useTaskStore = create<TaskState>((set) => ({
  tasks: [],
  loading: false,
  error: null,
  syncStatus: 'idle',
  isOffline: false,

  setTasks: (tasks) => set({ tasks }),

  addTask: (task) => set((state) => ({
    tasks: [...state.tasks, task]
  })),

  updateTask: (id, updates) => set((state) => ({
    tasks: state.tasks.map((task) =>
      task.id === id ? { ...task, ...updates, version: task.version + 1 } : task
    ),
  })),

  deleteTask: (id) => set((state) => ({
    tasks: state.tasks.filter((task) => task.id !== id),
  })),

  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),

  setSyncStatus: (syncStatus) => set({ syncStatus }),

  setOffline: (isOffline) => set({ isOffline }),

  clearTasks: () => set({ tasks: [] }),
}))
