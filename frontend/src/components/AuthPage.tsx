'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { motion } from 'framer-motion'
import { Terminal, ArrowRight, User, Lock, Eye, EyeOff, Mail, AlertCircle, CheckCircle2 } from 'lucide-react'
import { signIn, signUp } from '@/lib/auth-client'

type AuthMode = 'signin' | 'signup'

export function AuthPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [mode, setMode] = useState<AuthMode>('signin')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  // Form states
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  // Check for mode in URL
  useEffect(() => {
    const modeParam = searchParams.get('mode')
    if (modeParam === 'signin' || modeParam === 'signup') {
      setMode(modeParam)
    }
  }, [searchParams])

  // Password strength
  const getPasswordStrength = () => {
    if (!password) return { level: '', color: '', width: '0%' }
    const strength = password.length
    if (strength < 8) return { level: 'Weak', color: 'bg-destructive', width: '33%' }
    if (strength < 12) return { level: 'Medium', color: 'bg-warning', width: '66%' }
    return { level: 'Strong', color: 'bg-success', width: '100%' }
  }

  const passwordStrength = getPasswordStrength()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      if (mode === 'signup') {
        if (!username.trim()) {
          setError('Operative ID (Username) is required')
          setIsLoading(false)
          return
        }
        if (!email.trim()) {
          setError('Secure Channel (Email) is required')
          setIsLoading(false)
          return
        }
        if (password !== confirmPassword) {
          setError('Passwords do not match')
          setIsLoading(false)
          return
        }
        if (password.length < 8) {
          setError('Password must be at least 8 characters')
          setIsLoading(false)
          return
        }

        // Sign up with better-auth
        const result = await signUp.email({
          email,
          password,
          name: username,
        })

        if (result.error) {
          setError(result.error.message || 'Signup failed')
          setIsLoading(false)
          return
        }

        router.push('/dashboard')
      } else {
        if (!email.trim()) {
          setError('Email is required')
          setIsLoading(false)
          return
        }
        if (!password.trim()) {
          setError('Password is required')
          setIsLoading(false)
          return
        }

        // Sign in with better-auth
        const result = await signIn.email({
          email,
          password,
        })

        if (result.error) {
          setError(result.error.message || 'Login failed')
          setIsLoading(false)
          return
        }

        router.push('/dashboard')
      }
    } catch (err: unknown) {
      const error = err as { message?: string }
      setError(error.message || 'Authentication failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const switchMode = () => {
    setMode(mode === 'signin' ? 'signup' : 'signin')
    setError('')
    setPassword('')
    setConfirmPassword('')
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(0,255,255,0.05),transparent_50%)]" />
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-primary rounded-full"
            initial={{
              x: typeof window !== 'undefined' ? Math.random() * window.innerWidth : 0,
              y: typeof window !== 'undefined' ? Math.random() * window.innerHeight : 0,
            }}
            animate={{
              y: [null, -200],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: Math.random() * 4 + 3,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* Logo */}
      <div className="absolute top-6 left-6 flex items-center gap-2">
        <Terminal className="h-6 w-6 text-primary" />
        <span className="font-display font-bold text-lg">MissionImpossible</span>
      </div>

      {/* Auth Container */}
      <div className="relative w-full max-w-md">
        {/* Clippath Container */}
        <div
          className="relative bg-card/50 backdrop-blur border border-primary/30 rounded-2xl overflow-hidden"
          style={{
            clipPath: mode === 'signin'
              ? 'polygon(0 0, 100% 0, 100% 100%, 0 100%)'
              : 'polygon(0 0, 100% 0, 100% 100%, 0 100%)',
          }}
        >
          {/* Header */}
          <div className="p-8 pb-4">
            <motion.div
              key={mode}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <h1 className="font-display text-3xl font-bold text-center mb-2">
                {mode === 'signin' ? 'Access Protocol' : 'Initialize System'}
              </h1>
              <p className="font-mono text-sm text-muted-foreground text-center">
                {mode === 'signin'
                  ? 'Enter your credentials to access the system'
                  : 'Create your operative account'}
              </p>
            </motion.div>
          </div>

          {/* Form */}
          <div className="p-8 pt-4">
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-center gap-2 p-3 rounded-lg bg-destructive/10 border border-destructive/30 text-destructive"
                >
                  <AlertCircle className="h-4 w-4 flex-shrink-0" />
                  <span className="font-mono text-sm">{error}</span>
                </motion.div>
              )}

              {/* Email Field */}
              <div>
                <label className="block font-mono text-xs text-muted-foreground mb-2">
                  {mode === 'signup' ? 'Secure Channel (Email)' : 'Email Address'}
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="operative@example.com"
                    className="input-terminal w-full pl-10"
                    required
                  />
                </div>
              </div>

              {/* Username - Only for signup */}
              {mode === 'signup' && (
                <div>
                  <label className="block font-mono text-xs text-muted-foreground mb-2">
                    Operative ID (Username)
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <input
                      type="text"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      placeholder="Enter your operative ID"
                      className="input-terminal w-full pl-10"
                    />
                  </div>
                </div>
              )}

              {/* Password Field */}
              <div>
                <label className="block font-mono text-xs text-muted-foreground mb-2">
                  {mode === 'signin' ? 'Access Key (Password)' : 'Create Password'}
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder={mode === 'signin' ? 'Enter your password' : 'Create password (min 8 chars)'}
                    className="input-terminal w-full pl-10 pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {mode === 'signup' && password && (
                  <div className="mt-2">
                    <div className="flex items-center gap-2 mb-1">
                      <div className="h-1 flex-1 bg-secondary rounded-full overflow-hidden">
                        <div
                          className={`h-full ${passwordStrength.color} transition-all duration-300`}
                          style={{ width: passwordStrength.width }}
                        />
                      </div>
                      {passwordStrength.level && (
                        <span className="font-mono text-xs text-muted-foreground">
                          {passwordStrength.level}
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Confirm Password - Only for signup */}
              {mode === 'signup' && (
                <div>
                  <label className="block font-mono text-xs text-muted-foreground mb-2">
                    Confirm Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="Confirm your password"
                      className="input-terminal w-full pl-10 pr-10"
                      required
                    />
                    {confirmPassword && (
                      <div className="absolute right-3 top-1/2 -translate-y-1/2">
                        {confirmPassword === password ? (
                          <CheckCircle2 className="h-4 w-4 text-success" />
                        ) : (
                          <AlertCircle className="h-4 w-4 text-destructive" />
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary w-full flex items-center justify-center gap-2 py-3"
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-background/30 border-t-background rounded-full animate-spin" />
                    <span>Authenticating...</span>
                  </>
                ) : (
                  <>
                    <span>{mode === 'signin' ? 'Access System' : 'Initialize Account'}</span>
                    <ArrowRight className="h-4 w-4" />
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Footer */}
          <div className="p-8 pt-0">
            <div className="relative flex items-center gap-4">
              <div className="flex-1 h-px bg-gradient-to-r from-transparent to-primary/30" />
              <span className="font-mono text-xs text-muted-foreground">OR</span>
              <div className="flex-1 h-px bg-gradient-to-l from-transparent to-primary/30" />
            </div>

            {/* Switch Mode */}
            <div className="mt-6 text-center">
              <p className="font-mono text-sm text-muted-foreground">
                {mode === 'signin' ? "New operative? " : "Already registered? "}
                <button
                  onClick={switchMode}
                  className="text-primary hover:underline transition-colors"
                >
                  {mode === 'signin' ? 'Initialize System' : 'Access Protocol'}
                </button>
              </p>
            </div>

            {/* Demo Login */}
            <button
              onClick={() => router.push('/dashboard')}
              className="mt-4 w-full py-2 px-4 rounded-lg border border-primary/30 text-primary hover:bg-primary/10 transition-colors font-mono text-sm"
            >
              Skip to Demo Dashboard
            </button>
          </div>
        </div>

        {/* Decorative Elements */}
        <motion.div
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 4, repeat: Infinity }}
          className="absolute -top-10 -right-10 w-32 h-32 bg-primary/10 rounded-full blur-3xl"
        />
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 5, repeat: Infinity }}
          className="absolute -bottom-10 -left-10 w-40 h-40 bg-accent/10 rounded-full blur-3xl"
        />
      </div>
    </div>
  )
}
