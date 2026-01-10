'use client'

import { useEffect, useRef } from 'react'

interface Node {
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  color: string
  pulsePhase: number
}

export default function ParticlesBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const nodesRef = useRef<Node[]>([])
  const mouseRef = useRef({ x: 0, y: 0, active: false })
  const animationRef = useRef<number>(0)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
      initNodes()
    }

    // Colors for the cyberpunk theme
    const colors = [
      'rgba(0, 255, 255, 0.8)',   // Cyan
      'rgba(138, 43, 226, 0.7)',  // Purple
      'rgba(255, 0, 128, 0.6)',   // Magenta
      'rgba(100, 149, 237, 0.7)', // Steel blue
      'rgba(147, 112, 219, 0.6)', // Medium purple
    ]

    // Initialize nodes
    const initNodes = () => {
      const nodeCount = Math.floor((canvas.width * canvas.height) / 15000)
      nodesRef.current = []

      for (let i = 0; i < nodeCount; i++) {
        nodesRef.current.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          radius: Math.random() * 2 + 1,
          color: colors[Math.floor(Math.random() * colors.length)],
          pulsePhase: Math.random() * Math.PI * 2,
        })
      }
    }

    // Draw connection lines between nearby nodes
    const drawConnections = () => {
      const nodes = nodesRef.current
      const maxDistance = 150

      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x
          const dy = nodes[i].y - nodes[j].y
          const distance = Math.sqrt(dx * dx + dy * dy)

          if (distance < maxDistance) {
            const opacity = (1 - distance / maxDistance) * 0.4
            ctx.beginPath()
            ctx.strokeStyle = `rgba(0, 255, 255, ${opacity})`
            ctx.lineWidth = 0.5
            ctx.moveTo(nodes[i].x, nodes[i].y)
            ctx.lineTo(nodes[j].x, nodes[j].y)
            ctx.stroke()
          }
        }

        // Connect to mouse if nearby
        if (mouseRef.current.active) {
          const dx = nodes[i].x - mouseRef.current.x
          const dy = nodes[i].y - mouseRef.current.y
          const distance = Math.sqrt(dx * dx + dy * dy)

          if (distance < 200) {
            const opacity = (1 - distance / 200) * 0.6
            ctx.beginPath()
            ctx.strokeStyle = `rgba(255, 0, 128, ${opacity})`
            ctx.lineWidth = 1
            ctx.moveTo(nodes[i].x, nodes[i].y)
            ctx.lineTo(mouseRef.current.x, mouseRef.current.y)
            ctx.stroke()
          }
        }
      }
    }

    // Draw nodes with glow effect
    const drawNodes = (time: number) => {
      const nodes = nodesRef.current

      for (const node of nodes) {
        // Pulsing effect
        const pulse = Math.sin(time * 0.002 + node.pulsePhase) * 0.3 + 0.7
        const glowRadius = node.radius * 3 * pulse

        // Outer glow
        const gradient = ctx.createRadialGradient(
          node.x, node.y, 0,
          node.x, node.y, glowRadius
        )
        gradient.addColorStop(0, node.color)
        gradient.addColorStop(1, 'transparent')

        ctx.beginPath()
        ctx.arc(node.x, node.y, glowRadius, 0, Math.PI * 2)
        ctx.fillStyle = gradient
        ctx.fill()

        // Core
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
        ctx.fillStyle = node.color
        ctx.fill()
      }
    }

    // Update node positions
    const updateNodes = () => {
      const nodes = nodesRef.current

      for (const node of nodes) {
        node.x += node.vx
        node.y += node.vy

        // Bounce off edges
        if (node.x < 0 || node.x > canvas.width) node.vx *= -1
        if (node.y < 0 || node.y > canvas.height) node.vy *= -1

        // Keep in bounds
        node.x = Math.max(0, Math.min(canvas.width, node.x))
        node.y = Math.max(0, Math.min(canvas.height, node.y))

        // Slight attraction to mouse
        if (mouseRef.current.active) {
          const dx = mouseRef.current.x - node.x
          const dy = mouseRef.current.y - node.y
          const distance = Math.sqrt(dx * dx + dy * dy)

          if (distance < 300 && distance > 0) {
            const force = 0.02 / distance
            node.vx += dx * force
            node.vy += dy * force
          }
        }

        // Speed limit
        const speed = Math.sqrt(node.vx * node.vx + node.vy * node.vy)
        if (speed > 1) {
          node.vx = (node.vx / speed) * 1
          node.vy = (node.vy / speed) * 1
        }
      }
    }

    // Draw grid pattern
    const drawGrid = () => {
      ctx.strokeStyle = 'rgba(0, 255, 255, 0.03)'
      ctx.lineWidth = 1

      const gridSize = 50
      for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas.height)
        ctx.stroke()
      }
      for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(canvas.width, y)
        ctx.stroke()
      }
    }

    // Animation loop
    const animate = (time: number) => {
      ctx.fillStyle = 'rgba(10, 10, 20, 0.1)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      drawGrid()
      drawConnections()
      drawNodes(time)
      updateNodes()

      animationRef.current = requestAnimationFrame(animate)
    }

    // Mouse handlers
    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current.x = e.clientX
      mouseRef.current.y = e.clientY
      mouseRef.current.active = true
    }

    const handleMouseLeave = () => {
      mouseRef.current.active = false
    }

    // Initialize
    resize()
    window.addEventListener('resize', resize)
    window.addEventListener('mousemove', handleMouseMove)
    window.addEventListener('mouseleave', handleMouseLeave)
    animationRef.current = requestAnimationFrame(animate)

    return () => {
      window.removeEventListener('resize', resize)
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('mouseleave', handleMouseLeave)
      cancelAnimationFrame(animationRef.current)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{ background: 'linear-gradient(135deg, #0a0a14 0%, #1a1a2e 50%, #0f0f23 100%)' }}
    />
  )
}
