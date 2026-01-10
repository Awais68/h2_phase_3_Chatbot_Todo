'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, Terminal, User, LogOut, ChevronDown, Home, Target, Settings, HelpCircle } from 'lucide-react'
import Logo from './Logo'

const navItems = [
  { href: '/', label: 'Home', key: 'home', icon: Home },
  { href: '/dashboard', label: 'Dashboard', key: 'dashboard', icon: Target },
  { href: '/protocol', label: 'Protocol', key: 'protocol', icon: Settings },
  { href: '/auth', label: 'Login', key: 'login', icon: User },
]

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  const isAuthPage = pathname?.startsWith('/auth') || pathname?.startsWith('/dashboard')

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-primary/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <Logo size="sm" showText={true} />
          </Link>

          {/* Desktop Navigation */}
          {!isAuthPage && (
            <div className="hidden md:flex items-center gap-6">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.key}
                    href={item.href}
                    className="relative flex items-center gap-2 font-mono text-sm uppercase tracking-widest text-muted-foreground hover:text-primary transition-colors group"
                  >
                    <Icon className="w-4 h-4" />
                    <span className="relative z-10">{item.label}</span>
                    <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary group-hover:w-full transition-all duration-300" />
                  </Link>
                )
              })}
              <Link
                href="/auth"
                className="btn-primary text-sm"
              >
                Start for Free
              </Link>
            </div>
          )}

          {/* Mobile Menu Button */}
          {!isAuthPage && (
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 text-foreground hover:text-primary transition-colors"
              aria-label="Toggle menu"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          )}
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isOpen && !isAuthPage && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-gray-900/95 backdrop-blur-xl border-b border-primary/20"
          >
            <div className="px-4 py-4 space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.key}
                    href={item.href}
                    onClick={() => setIsOpen(false)}
                    className="flex items-center gap-3 font-mono text-sm uppercase tracking-widest text-muted-foreground hover:text-primary hover:bg-gray-800/50 transition-colors py-3 px-3 rounded-lg"
                  >
                    <Icon className="w-5 h-5" />
                    {item.label}
                  </Link>
                )
              })}
              <Link
                href="/auth"
                onClick={() => setIsOpen(false)}
                className="btn-primary w-full text-center text-sm block mt-4"
              >
                Start for Free
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}

export function DashboardNavbar({ user }: { user?: { name: string } | null }) {
  const [showUserMenu, setShowUserMenu] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/90 backdrop-blur-md border-b border-primary/20 h-16">
      <div className="h-full px-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/dashboard" className="flex items-center gap-2 group">
          <Logo size="sm" showText={true} />
        </Link>

        {/* User Menu */}
        <div className="relative">
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-800/50 transition-colors"
          >
            <User className="h-5 w-5 text-muted-foreground" />
            <span className="font-mono text-sm hidden sm:block">
              {user?.name || 'Operative'}
            </span>
            <ChevronDown className={`h-4 w-4 text-muted-foreground transition-transform ${showUserMenu ? 'rotate-180' : ''}`} />
          </button>

          <AnimatePresence>
            {showUserMenu && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute right-0 mt-2 w-48 bg-gray-900 border border-cyan-500/30 rounded-lg shadow-lg overflow-hidden"
              >
                <Link
                  href="/dashboard/settings"
                  className="flex items-center gap-2 px-4 py-3 text-sm hover:bg-gray-800 transition-colors"
                >
                  <Terminal className="h-4 w-4" />
                  Settings
                </Link>
                <button className="w-full flex items-center gap-2 px-4 py-3 text-sm text-red-400 hover:bg-gray-800 transition-colors">
                  <LogOut className="h-4 w-4" />
                  Abort Mission
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </nav>
  )
}
