'use client'

import dynamic from 'next/dynamic'

const LandingPage = dynamic(() => import('@/components/LandingPage').then(mod => ({ default: mod.LandingPage })), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="text-cyan-400 animate-pulse text-xl font-mono">Initializing Mission Control...</div>
    </div>
  ),
})

export default function Home() {
  return <LandingPage />
}
