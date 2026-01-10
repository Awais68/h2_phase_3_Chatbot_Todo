'use client'

import dynamic from 'next/dynamic'

const Dashboard = dynamic(() => import('@/components/Dashboard'), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="text-cyan-400 animate-pulse text-xl font-mono">Compiling Mission...</div>
    </div>
  ),
})

export default function DashboardPage() {
  return <Dashboard />
}
