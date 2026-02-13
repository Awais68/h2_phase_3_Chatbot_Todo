import { Task, User, AuthTokens, ApiError, SyncOperation } from '@/types'
import { useAuthStore } from '@/stores/useAuthStore'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Retry configuration
const MAX_RETRIES = 3
const RETRY_DELAY = 1000 // 1 second

// Helper function to delay execution
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {},
  requiresAuth: boolean = false,
  retryCount: number = 0
): Promise<T> {
  const { tokens } = useAuthStore.getState()

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }

  if (options.headers) {
    Object.assign(headers, options.headers)
  }

  if (requiresAuth && tokens?.accessToken) {
    headers['Authorization'] = `Bearer ${tokens.accessToken}`
  }

  const url = `${API_BASE_URL}${endpoint}`

  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 15000) // 15 second timeout

    const response = await fetch(url, {
      ...options,
      headers,
      mode: 'cors',
      credentials: 'omit',
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        message: response.statusText,
      }))

      const error: ApiError = {
        message: errorData.message || 'Request failed',
        status: response.status,
        code: errorData.code,
      }

      if (response.status === 401 && requiresAuth) {
        useAuthStore.getState().logout()
      }

      // Retry on server errors (5xx) but not client errors (4xx)
      if (response.status >= 500 && retryCount < MAX_RETRIES) {
        console.log(`Server error, retrying... (${retryCount + 1}/${MAX_RETRIES})`)
        await delay(RETRY_DELAY * (retryCount + 1))
        return fetchApi<T>(endpoint, options, requiresAuth, retryCount + 1)
      }

      throw error
    }

    if (response.status === 204) {
      return {} as T
    }

    return await response.json()
  } catch (error) {
    // Handle abort/timeout
    if (error instanceof Error && error.name === 'AbortError') {
      if (retryCount < MAX_RETRIES) {
        console.log(`Request timeout, retrying... (${retryCount + 1}/${MAX_RETRIES})`)
        await delay(RETRY_DELAY * (retryCount + 1))
        return fetchApi<T>(endpoint, options, requiresAuth, retryCount + 1)
      }
      throw {
        message: 'Request timed out',
        code: 'TIMEOUT_ERROR',
      } as ApiError
    }

    // Handle network errors with retry
    if (error instanceof TypeError && (error.message.includes('Failed to fetch') || error.message.includes('NetworkError'))) {
      if (retryCount < MAX_RETRIES) {
        console.log(`Network error, retrying... (${retryCount + 1}/${MAX_RETRIES})`)
        await delay(RETRY_DELAY * (retryCount + 1))
        return fetchApi<T>(endpoint, options, requiresAuth, retryCount + 1)
      }
      throw {
        message: 'Network error - please check your connection',
        code: 'NETWORK_ERROR',
      } as ApiError
    }

    if (error instanceof TypeError) {
      if (retryCount < MAX_RETRIES) {
        console.log(`Connection error, retrying... (${retryCount + 1}/${MAX_RETRIES})`)
        await delay(RETRY_DELAY * (retryCount + 1))
        return fetchApi<T>(endpoint, options, requiresAuth, retryCount + 1)
      }
      throw {
        message: `Connection error: ${error.message}`,
        code: 'CONNECTION_ERROR',
      } as ApiError
    }

    throw error
  }
}

async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  return fetchApi<T>(endpoint, options, true)
}

export const api = {
  auth: {
    register: async (email: string, username: string, password: string) => {
      const user = await fetchApi<User>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, username, password }),
      })
      const loginResponse = await fetchApi<{ access_token: string; token_type: string; user: User }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      return {
        user: loginResponse.user,
        tokens: {
          accessToken: loginResponse.access_token,
          tokenType: loginResponse.token_type,
        },
      }
    },

    login: async (username: string, password: string) => {
      const response = await fetchApi<{ access_token: string; token_type: string; user: User }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      return {
        user: response.user,
        tokens: {
          accessToken: response.access_token,
          tokenType: response.token_type,
        },
      }
    },

    me: async () => {
      return fetchWithAuth<User>('/auth/me')
    },
  },

  tasks: {
    list: async (options?: {
      userId?: string;
      userEmail?: string;
      userName?: string;
      status?: string;
      priority?: string;
      sortBy?: string;
      order?: string;
    }) => {
      const params = new URLSearchParams()
      if (options?.userId) params.append('user_id', options.userId)
      if (options?.status) params.append('status', options.status)
      if (options?.priority) params.append('priority', options.priority)
      if (options?.sortBy) params.append('sort_by', options.sortBy)
      if (options?.order) params.append('order', options.order)

      const query = params.toString()
      const headers: Record<string, string> = {}
      if (options?.userEmail) headers['X-User-Email'] = options.userEmail
      if (options?.userName) headers['X-User-Name'] = options.userName

      return fetchApi<Task[]>(`/tasks${query ? `?${query}` : ''}`, { headers })
    },

    create: async (data: {
      title: string;
      description?: string;
      priority?: string;
      status?: string;
      dueDate?: string;
      recursion?: string;
      category?: string;
      tags?: string[];
      shopping_list?: any[];
      userId?: string;
      userEmail?: string;
      userName?: string;
    }) => {
      const params = data.userId ? `?user_id=${encodeURIComponent(data.userId)}` : ''
      const headers: Record<string, string> = {}
      if (data.userEmail) headers['X-User-Email'] = data.userEmail
      if (data.userName) headers['X-User-Name'] = data.userName

      return fetchApi<Task>(`/tasks${params}`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          title: data.title,
          description: data.description || '',
          priority: data.priority,
          status: data.status,
          due_date: data.dueDate,
          recursion: data.recursion,
          category: data.category,
          tags: data.tags,
          shopping_list: data.shopping_list || []
        }),
      })
    },

    get: async (id: string, userId?: string) => {
      const params = userId ? `?user_id=${encodeURIComponent(userId)}` : ''
      return fetchApi<Task>(`/tasks/${id}${params}`)
    },

    update: async (id: string, data: {
      title?: string;
      description?: string;
      status?: string;
      priority?: string;
      completed?: boolean;
      dueDate?: string;
      recursion?: string;
      category?: string;
      tags?: string[];
      shoppingList?: any[];
      [key: string]: any; // Allow additional properties
    }, userId?: string) => {
      const params = userId ? `?user_id=${encodeURIComponent(userId)}` : ''
      // Filter out undefined values but keep falsy values like false/empty strings
      const payload: any = {};

      Object.keys(data).forEach(key => {
        if (data[key] !== undefined) {
          // Convert camelCase to snake_case for backend compatibility
          const snakeCaseKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
          payload[snakeCaseKey] = data[key];
        }
      });

      return fetchApi<Task>(`/tasks/${id}${params}`, {
        method: 'PUT',
        body: JSON.stringify(payload),
      })
    },

    delete: async (id: string, userId?: string) => {
      const params = userId ? `?user_id=${userId}` : ''
      return fetchApi<{ message: string; id: string }>(`/tasks/${id}${params}`, {
        method: 'DELETE',
      })
    },
  },

  trash: {
    list: async (userId?: string) => {
      const params = userId ? `?user_id=${userId}` : ''
      return fetchApi<Task[]>(`/trash/${params}`)
    },

    restore: async (trashId: string) => {
      return fetchApi<{ message: string; id: string }>(`/trash/${trashId}/restore`, {
        method: 'POST',
      })
    },

    permanentDelete: async (trashId: string) => {
      return fetchApi<{ message: string }>(`/trash/${trashId}`, {
        method: 'DELETE',
      })
    },

    empty: async () => {
      return fetchApi<{ message: string; deleted_count: number }>('/trash/empty', {
        method: 'DELETE',
      })
    },
  },

  sync: {
    push: async (operations: SyncOperation[]) => {
      return fetchWithAuth<{ synced: number; conflicts: any[] }>('/sync/push', {
        method: 'POST',
        body: JSON.stringify({ operations }),
      })
    },

    pull: async (lastSyncTime?: string) => {
      const params = lastSyncTime ? `?since=${lastSyncTime}` : ''
      return fetchWithAuth<{ tasks: Task[]; timestamp: string }>(`/sync/pull${params}`)
    },
  },

  chat: {
    send: async (
      conversationId: string | null,
      message: string,
      userId: string = '1',
      dueDateText?: string
    ) => {
      const payload: any = {
        conversation_id: conversationId,
        message: message,
      };

      // Add due_date_text if provided
      if (dueDateText) {
        payload.due_date_text = dueDateText;
      }

      return fetchApi<{
        conversation_id: string;
        message: string;
        response: string;
        tool_calls?: any[];
      }>(`/api/${userId}/chat`, {
        method: 'POST',
        body: JSON.stringify(payload),
      })
    },

    getHistory: async (conversationId: string, userId: string = '1') => {
      return fetchApi<{
        conversation_id: string;
        messages: Array<{ role: string; content: string; timestamp: string }>;
      }>(`/api/${userId}/chat/history/${conversationId}`)
    },
  },

  analytics: {
    getStats: async (userId?: string) => {
      const effectiveUserId = userId || '1'; // Use '1' as default demo user
      return fetchApi<{
        total_tasks: number;
        completed_tasks: number;
        pending_tasks: number;
        completion_rate: number;
      }>(`/api/${effectiveUserId}/analytics/overview`)
    },

    getTrends: async (days: number = 30, userId?: string) => {
      const effectiveUserId = userId || '1'; // Use '1' as default demo user
      const params = new URLSearchParams()
      params.append('days', days.toString())

      return fetchApi<{
        daily_completions: Record<string, number>;
        average_per_day: number;
      }>(`/api/${effectiveUserId}/analytics/timeline?${params.toString()}`)
    },
  },

  history: {
    list: async (options?: {
      userId?: string;
      actionType?: string;
      page?: number;
      pageSize?: number;
    }) => {
      const params = new URLSearchParams();
      if (options?.userId) params.append('user_id', options.userId);
      if (options?.actionType) params.append('action_type', options.actionType);
      if (options?.page) params.append('page', options.page.toString());
      if (options?.pageSize) params.append('page_size', options.pageSize.toString());
      
      return fetchApi<{
        items: any[];
        total: number;
        page: number;
        page_size: number;
        total_pages: number;
      }>(`/api/history/?${params.toString()}`);
    },
  },

  recurring: {
    list: async (userId?: string) => {
      const effectiveUserId = userId || '1'; // Use '1' as default demo user
      return fetchApi<any[]>(`/api/${effectiveUserId}/recurring`);
    },

    create: async (data: {
      title: string;
      description?: string;
      frequency: string;
      startDate?: string;
      userId?: string;
    }) => {
      const effectiveUserId = data.userId || '1'; // Use '1' as default demo user
      return fetchApi<any>(`/api/${effectiveUserId}/recurring`, {
        method: 'POST',
        body: JSON.stringify({
          title: data.title,
          description: data.description || "",
          frequency: data.frequency,
          frequency_value: data.frequency === 'weekly' ? 1 : data.frequency === 'monthly' ? 1 : 1, // Default to 1 for daily/weekly/monthly
        }),
      })
    },

    update: async (id: string, data: any, userId?: string) => {
      const effectiveUserId = userId || '1'; // Use '1' as default demo user
      return fetchApi<any>(`/api/${effectiveUserId}/recurring/${id}/pause`, { // Assuming we're pausing/resuming based on data
        method: 'PATCH',
        body: JSON.stringify(data),
      })
    },

    delete: async (id: string, userId?: string) => {
      const effectiveUserId = userId || '1'; // Use '1' as default demo user
      return fetchApi<{ message: string }>(`/api/${effectiveUserId}/recurring/${id}`, {
        method: 'DELETE',
      })
    },
  },
}
