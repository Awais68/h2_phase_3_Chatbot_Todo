'use client'

import { useEffect, useRef } from 'react'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions
} from 'chart.js'
import { Doughnut } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend)

interface Mission {
  id: string
  name: string
  priority: 'critical' | 'high' | 'normal' | 'low'
  status: 'pending' | 'in-progress' | 'completed' | 'archived'
  recursion: 'none' | 'daily' | 'weekly' | 'monthly'
  time: string
  createdAt: Date
}

interface StatusChartProps {
  missions: Mission[]
}

export function StatusChart({ missions }: StatusChartProps) {
  const data: ChartData<'doughnut'> = {
    labels: ['Pending', 'In Progress', 'Completed', 'Archived'],
    datasets: [
      {
        data: [
          missions.filter(m => m.status === 'pending').length,
          missions.filter(m => m.status === 'in-progress').length,
          missions.filter(m => m.status === 'completed').length,
          missions.filter(m => m.status === 'archived').length,
        ],
        backgroundColor: [
          'rgba(107, 114, 128, 0.8)',   // Muted for pending
          'rgba(0, 255, 255, 0.8)',     // Cyan for in-progress
          'rgba(57, 255, 20, 0.8)',     // Green for completed
          'rgba(255, 0, 128, 0.8)',     // Magenta for archived
        ],
        borderColor: [
          'rgba(107, 114, 128, 1)',
          'rgba(0, 255, 255, 1)',
          'rgba(57, 255, 20, 1)',
          'rgba(255, 0, 128, 1)',
        ],
        borderWidth: 2,
        hoverOffset: 4,
      },
    ],
  }

  const options: ChartOptions<'doughnut'> = {
    responsive: true,
    maintainAspectRatio: true,
    cutout: '65%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: 'rgba(0, 255, 255, 0.8)',
          font: {
            family: "'Roboto Mono', monospace",
            size: 11,
          },
          padding: 15,
          usePointStyle: true,
          pointStyle: 'circle',
        },
      },
      tooltip: {
        backgroundColor: 'rgba(20, 30, 50, 0.95)',
        titleColor: 'rgba(0, 255, 255, 1)',
        bodyColor: 'rgba(0, 200, 200, 1)',
        borderColor: 'rgba(0, 255, 255, 0.3)',
        borderWidth: 1,
        padding: 12,
        titleFont: {
          family: "'Orbitron', sans-serif",
          size: 13,
        },
        bodyFont: {
          family: "'Roboto Mono', monospace",
          size: 12,
        },
        callbacks: {
          label: function(context) {
            const value = context.raw as number
            const total = context.dataset.data.reduce((a, b) => (a as number) + (b as number), 0) as number
            const percentage = ((value / total) * 100).toFixed(1)
            return `${context.label}: ${value} (${percentage}%)`
          }
        }
      },
    },
    animation: {
      animateScale: true,
      animateRotate: true,
      duration: 1000,
      easing: 'easeOutQuart',
    },
  }

  return (
    <div className="relative w-full aspect-square max-w-[200px] mx-auto">
      <Doughnut data={data} options={options} />
      {/* Center Text */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="text-center">
          <div className="font-display text-2xl font-bold text-primary">
            {missions.filter(m => m.status === 'completed').length}
          </div>
          <div className="font-mono text-xs text-muted-foreground">
            Done
          </div>
        </div>
      </div>
    </div>
  )
}
