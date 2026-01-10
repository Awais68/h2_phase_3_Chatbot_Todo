'use client'

import dynamic from 'next/dynamic'

const AuthPage = dynamic(() => import('@/components/AuthPage').then(mod => ({ default: mod.AuthPage })), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="text-cyan-400 animate-pulse text-xl font-mono">Initializing Security Protocol...</div>
    </div>
  ),
})

export default function Auth() {
  return <AuthPage />
}
