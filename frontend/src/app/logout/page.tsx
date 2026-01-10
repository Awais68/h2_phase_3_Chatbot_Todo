'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { LogOut, Terminal } from 'lucide-react'

export default function LogoutPage() {
  const router = useRouter()

  useEffect(() => {
    // Clear authentication state
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')

    // Redirect to auth page after brief animation
    const timer = setTimeout(() => {
      router.push('/auth')
    }, 1500)

    return () => clearTimeout(timer)
  }, [router])

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center">
        {/* Icon */}
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="mb-8"
        >
          <div className="w-20 h-20 mx-auto rounded-full bg-destructive/20 flex items-center justify-center">
            <LogOut className="h-10 w-10 text-destructive" />
          </div>
        </motion.div>

        {/* Text */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h1 className="font-display text-2xl font-bold mb-2">
            Mission <span className="text-destructive">Aborted</span>
          </h1>
          <p className="font-mono text-muted-foreground mb-4">
            You have been logged out successfully.
          </p>

          {/* Terminal-style loading */}
          <div className="bg-card/50 border border-primary/30 rounded-lg p-4 text-left">
            <div className="flex items-center gap-2 mb-2 pb-2 border-b border-primary/20">
              <Terminal className="h-4 w-4 text-primary" />
              <span className="font-mono text-xs text-muted-foreground">system.log</span>
            </div>
            <div className="font-mono text-sm space-y-1">
              <p className="text-success">✓ Session terminated</p>
              <p className="text-success">✓ Cache cleared</p>
              <p className="text-primary animate-pulse">
                Redirecting<span className="loading-dots"><span>.</span><span>.</span><span>.</span></span>
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
