import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User, AuthTokens } from '@/types'

/**
 * Authentication store state interface
 */
interface AuthState {
  user: User | null
  tokens: AuthTokens | null
  isAuthenticated: boolean

  // Actions
  setUser: (user: User | null) => void
  setTokens: (tokens: AuthTokens | null) => void
  login: (user: User, tokens: AuthTokens) => void
  logout: () => void
}

/**
 * Zustand store for authentication
 * Persisted to localStorage for session management
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,

      setUser: (user) => set({ user, isAuthenticated: !!user }),

      setTokens: (tokens) => set({ tokens }),

      login: (user, tokens) => set({
        user,
        tokens,
        isAuthenticated: true
      }),

      logout: () => set({
        user: null,
        tokens: null,
        isAuthenticated: false
      }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated
      }),
    }
  )
)
