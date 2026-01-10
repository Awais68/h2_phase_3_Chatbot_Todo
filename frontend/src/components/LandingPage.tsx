'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  Zap,
  Shield,
  Users,
  BarChart3,
  ArrowRight,
  CheckCircle2,
  Terminal,
  Cpu,
  Globe
} from 'lucide-react'
import ParticlesBackground from './ParticlesBackground'
import Logo from './Logo'

const features = [
  {
    icon: Zap,
    title: 'Smart Mission Management',
    description: 'Create, edit, and delete missions with AI-powered prioritization',
    color: 'text-primary'
  },
  {
    icon: Globe,
    title: 'Real-time Sync',
    description: 'Works seamlessly across web and mobile devices',
    color: 'text-success'
  },
  {
    icon: Users,
    title: 'Collaborate',
    description: 'Share missions with team members and track progress together',
    color: 'text-accent'
  },
  {
    icon: BarChart3,
    title: 'Analytics & Reports',
    description: 'Track productivity trends with visual insights',
    color: 'text-warning'
  },
  {
    icon: Shield,
    title: 'Secure Protocol',
    description: 'End-to-end encryption with BetterAuth security',
    color: 'text-primary'
  },
  {
    icon: Cpu,
    title: 'Voice Commands',
    description: 'Control your missions with voice in English or Urdu',
    color: 'text-success'
  }
]

const steps = [
  {
    step: '01',
    title: 'Initialize Protocol',
    description: 'Create your account and configure your mission parameters',
    icon: Terminal
  },
  {
    step: '02',
    title: 'Deploy Missions',
    description: 'Add tasks, set priorities, and define recursion patterns',
    icon: Cpu
  },
  {
    step: '03',
    title: 'Execute & Track',
    description: 'Monitor progress with real-time analytics and achievements',
    icon: Zap
  }
]

export function LandingPage() {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  return (
    <div className="min-h-screen bg-background relative">
      {/* Particles Background */}
      <ParticlesBackground />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: isLoaded ? 1 : 0, x: isLoaded ? 0 : -50 }}
              transition={{ duration: 0.8 }}
            >
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/30 mb-6">
                <span className="w-2 h-2 bg-success rounded-full animate-pulse" />
                <span className="font-mono text-xs uppercase tracking-widest text-primary">
                  System Online
                </span>
              </div>

              {/* Logo with New Rocker font */}
              <div className="mb-6 ">
                <Logo size="lg" showText={true} />
              </div>

              <p className="font-mono text-lg text-muted-foreground mb-8 max-w-lg">
                The ultimate mission control system. Track, manage, and complete
                objectives with cyberpunk efficiency. Your tasks, elevated.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/auth" className="btn-primary text-center group">
                  <span>Initialize Mission</span>
                  <ArrowRight className="inline-block ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Link>
                <Link href="/auth?mode=signin" className="btn-secondary text-center">
                  Access Protocol
                </Link>
              </div>

              {/* Feature Highlights */}
              <div className="mt-12 flex flex-wrap gap-4">
                {['Fast', 'Secure', 'Smart'].map((feature) => (
                  <div
                    key={feature}
                    className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-secondary/50 border border-primary/20"
                  >
                    <CheckCircle2 className="h-4 w-4 text-success" />
                    <span className="font-mono text-xs">{feature}</span>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Right Illustration */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: isLoaded ? 1 : 0, x: isLoaded ? 0 : 50 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="relative bg-card/50 backdrop-blur border border-primary/30 rounded-2xl p-6 shadow-2xl shadow-primary/10">
                {/* Terminal Header */}
                <div className="flex items-center gap-2 mb-4 pb-4 border-b border-primary/20">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-destructive/80" />
                    <div className="w-3 h-3 rounded-full bg-warning/80" />
                    <div className="w-3 h-3 rounded-full bg-success/80" />
                  </div>
                  <span className="font-mono text-xs text-muted-foreground ml-2">
                    mission_control.exe
                  </span>
                </div>

                {/* Mock Task List */}
                <div className="space-y-3">
                  {[
                    { title: 'Complete system architecture', status: 'done', time: '10:23' },
                    { title: 'Deploy to production', status: 'pending', time: '14:00' },
                    { title: 'Review security protocols', status: 'progress', time: 'Now' },
                    { title: 'Optimize database queries', status: 'pending', time: '16:30' }
                  ].map((task, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.4 + i * 0.1 }}
                      className={`flex items-center justify-between p-3 rounded-lg border ${task.status === 'done'
                        ? 'bg-success/10 border-success/30'
                        : task.status === 'progress'
                          ? 'bg-primary/10 border-primary/30'
                          : 'bg-secondary/30 border-primary/20'
                        }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-2 h-2 rounded-full ${task.status === 'done' ? 'bg-success' :
                          task.status === 'progress' ? 'bg-primary animate-pulse' : 'bg-muted-foreground'
                          }`} />
                        <span className={`font-mono text-sm ${task.status === 'done' ? 'line-through text-muted-foreground' : 'text-foreground'
                          }`}>
                          {task.title}
                        </span>
                      </div>
                      <span className="font-mono text-xs text-muted-foreground">{task.time}</span>
                    </motion.div>
                  ))}
                </div>

                {/* Stats Bar */}
                <div className="mt-6 pt-4 border-t border-primary/20 grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="font-display text-2xl text-primary">12</div>
                    <div className="font-mono text-xs text-muted-foreground">Active</div>
                  </div>
                  <div className="text-center">
                    <div className="font-display text-2xl text-success">8</div>
                    <div className="font-mono text-xs text-muted-foreground">Done</div>
                  </div>
                  <div className="text-center">
                    <div className="font-display text-2xl text-accent">3</div>
                    <div className="font-mono text-xs text-muted-foreground">Priority</div>
                  </div>
                </div>
              </div>

              {/* Floating Elements */}
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity }}
                className="absolute -top-4 -right-4 w-20 h-20 bg-primary/20 rounded-full blur-2xl"
              />
              <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 4, repeat: Infinity }}
                className="absolute -bottom-4 -left-4 w-32 h-32 bg-accent/20 rounded-full blur-2xl"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="font-display text-4xl font-bold mb-4">
              System <span className="text-primary">Capabilities</span>
            </h2>
            <p className="font-mono text-muted-foreground max-w-2xl mx-auto">
              Everything you need to manage your missions with precision and style
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="group p-6 rounded-xl bg-card/30 border border-primary/20 hover:border-primary/50 transition-all duration-300 card-glow-hover"
              >
                <div className={`mb-4 ${feature.color}`}>
                  <feature.icon className="h-8 w-8" />
                </div>
                <h3 className="font-display text-xl font-bold mb-2">{feature.title}</h3>
                <p className="font-mono text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 relative bg-secondary/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="font-display text-4xl font-bold mb-4">
              Operational <span className="text-primary">Protocol</span>
            </h2>
            <p className="font-mono text-muted-foreground max-w-2xl mx-auto">
              Three simple steps to mission mastery
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2 }}
                className="relative text-center"
              >
                {/* Connector Line */}
                {i < steps.length - 1 && (
                  <div className="hidden md:block absolute top-12 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-primary/50 to-primary/20" />
                )}

                <div className="relative z-10 mb-6">
                  <div className="w-24 h-24 mx-auto rounded-full bg-card border-2 border-primary/50 flex items-center justify-center group hover:border-primary transition-colors">
                    <step.icon className="h-10 w-10 text-primary group-hover:scale-110 transition-transform" />
                  </div>
                </div>

                <div className="font-mono text-xs text-primary mb-2">STEP {step.step}</div>
                <h3 className="font-display text-xl font-bold mb-2">{step.title}</h3>
                <p className="font-mono text-sm text-muted-foreground">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="p-12 rounded-2xl bg-gradient-to-br from-primary/10 via-card to-accent/10 border border-primary/30"
          >
            <h2 className="font-display text-4xl font-bold mb-4">
              Ready to <span className="text-primary">Deploy</span>?
            </h2>
            <p className="font-mono text-muted-foreground mb-8 max-w-lg mx-auto">
              Join thousands of operatives who have upgraded their task management system
            </p>
            <Link href="/auth" className="btn-primary inline-flex items-center gap-2 text-lg px-8 py-4">
              <span>Initialize Now</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-primary/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-2">
              <Terminal className="h-5 w-5 text-primary" />
              <span className="font-display font-bold">MissionImpossible</span>
            </div>

            <nav className="flex flex-wrap justify-center gap-6">
              {['About', 'Features', 'Contact', 'Privacy', 'Terms'].map((item) => (
                <Link
                  key={item}
                  href={`/${item.toLowerCase()}`}
                  className="font-mono text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                  {item}
                </Link>
              ))}
            </nav>

            <div className="flex items-center gap-4">
              {['twitter', 'github', 'discord'].map((social) => (
                <a
                  key={social}
                  href={`/${social}`}
                  className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center hover:bg-primary hover:text-background transition-colors"
                >
                  <span className="sr-only">{social}</span>
                  <div className="w-4 h-4 bg-current rounded-sm" />
                </a>
              ))}
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-primary/10 text-center">
            <p className="font-mono text-xs text-muted-foreground">
              &copy; 2025 MissionImpossible. All systems operational.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
