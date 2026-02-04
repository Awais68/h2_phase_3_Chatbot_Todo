/**
 * Core domain types for the Task Management PWA
 */

export interface Task {
  id: string
  title: string
  description?: string
  completed: boolean
  createdAt: string
  updatedAt: string
  userId: string
  version: number
}

export interface User {
  id: string
  email: string
  name?: string
}

export interface Item {
  id: string
  name: string
  price: number
  quantity: number
  completed?: boolean
}

export interface Category {
  id: string
  name: string
  items: Item[]
}

export interface Mission {
  id: string
  title: string
  description: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  status: 'pending' | 'active' | 'completed' | 'failed'
  dueDate: string
  createdAt: string
  tags: string[]
  category: string
  recursion?: string
  shoppingList?: Category[]
}

export interface SyncOperation {
  id: string
  operation: 'create' | 'update' | 'delete'
  taskId: string
  data: Partial<Task>
  timestamp: string
  synced: boolean
}

export interface PushSubscription {
  endpoint: string
  keys: {
    p256dh: string
    auth: string
  }
}

export interface AuthTokens {
  accessToken: string
  refreshToken?: string
}

export interface ApiError {
  message: string
  code?: string
  status?: number
}
