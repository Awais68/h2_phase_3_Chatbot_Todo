'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Sparkles, AlertCircle, Clock, FolderOpen, Zap, CheckCircle, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface Task {
  id: number
  title: string
  description: string
  completed: boolean
}

interface DuplicateDetection {
  task_ids: number[]
  similarity_score: number
  confidence: number
  suggestion: string
}

interface PriorityAnalysis {
  task_id: number
  priority: string
  confidence: number
  reasoning: string
  keywords: string[]
}

interface TimeEstimate {
  task_id: number
  estimated_hours: number
  confidence_interval: { min: number; max: number }
  confidence: number
  complexity_factors: string[]
}

interface TaskGrouping {
  name: string
  task_ids: number[]
  category: string
  confidence: number
  reasoning: string
}

interface AutomationOpportunity {
  task_ids: number[]
  automation_type: string
  confidence: number
  suggestion: string
  implementation: string
}

interface OptimizationResults {
  duplicates: DuplicateDetection[]
  priorities: PriorityAnalysis[]
  time_estimates: TimeEstimate[]
  groups: TaskGrouping[]
  automations: AutomationOpportunity[]
  total_suggestions: number
  analysis_timestamp: string
}

interface TaskOptimizerProps {
  tasks: Task[]
  onClose: () => void
}

/**
 * TaskOptimizer Component
 * Displays AI-powered task optimization suggestions
 */
export function TaskOptimizer({ tasks, onClose }: TaskOptimizerProps) {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<OptimizationResults | null>(null)
  const [error, setError] = useState<string | null>(null)

  const runOptimization = async () => {
    setLoading(true)
    setError(null)

    try {
      // Call the optimizer API endpoint
      const response = await fetch('/api/optimize-tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tasks }),
      })

      if (!response.ok) {
        throw new Error('Optimization failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to optimize tasks')
    } finally {
      setLoading(false)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'destructive'
      case 'medium': return 'default'
      case 'low': return 'secondary'
      default: return 'outline'
    }
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            <CardTitle>Task Optimizer</CardTitle>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
        <CardDescription>
          AI-powered analysis to optimize your tasks
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Run optimization button */}
        {!results && (
          <div className="text-center py-8">
            <Button
              onClick={runOptimization}
              disabled={loading || tasks.length === 0}
              className="w-full max-w-xs"
            >
              {loading ? (
                <>
                  <Sparkles className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing {tasks.length} tasks...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Optimize {tasks.length} Tasks
                </>
              )}
            </Button>
            {tasks.length === 0 && (
              <p className="mt-4 text-sm text-muted-foreground">
                Add some tasks first to see optimization suggestions
              </p>
            )}
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="flex items-center gap-2 p-4 text-sm text-destructive border border-destructive rounded-lg">
            <AlertCircle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="space-y-6">
            {/* Summary */}
            <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
              <div>
                <p className="font-semibold">Optimization Complete</p>
                <p className="text-sm text-muted-foreground">
                  Found {results.total_suggestions} suggestions
                </p>
              </div>
              <Button variant="outline" size="sm" onClick={runOptimization}>
                Re-analyze
              </Button>
            </div>

            {/* Duplicates */}
            {results.duplicates.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 text-warning" />
                  <h3 className="font-semibold">Duplicate Tasks</h3>
                  <Badge variant="secondary">{results.duplicates.length}</Badge>
                </div>
                {results.duplicates.map((dup, idx) => (
                  <Card key={idx} className="border-warning/50">
                    <CardContent className="pt-4">
                      <p className="text-sm font-medium mb-2">
                        Tasks: {dup.task_ids.join(', ')}
                      </p>
                      <p className="text-sm text-muted-foreground mb-2">
                        {dup.suggestion}
                      </p>
                      <div className="flex gap-2">
                        <Badge variant="outline">
                          Similarity: {(dup.similarity_score * 100).toFixed(0)}%
                        </Badge>
                        <Badge variant="outline">
                          Confidence: {(dup.confidence * 100).toFixed(0)}%
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Priorities */}
            {results.priorities.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 text-primary" />
                  <h3 className="font-semibold">Priority Suggestions</h3>
                  <Badge variant="secondary">{results.priorities.slice(0, 5).length}</Badge>
                </div>
                <div className="space-y-2">
                  {results.priorities.slice(0, 5).map((priority, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex-1">
                        <p className="text-sm font-medium">Task #{priority.task_id}</p>
                        <p className="text-xs text-muted-foreground">{priority.reasoning}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={getPriorityColor(priority.priority) as any}>
                          {priority.priority.toUpperCase()}
                        </Badge>
                        <Badge variant="outline">
                          {(priority.confidence * 100).toFixed(0)}%
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Time Estimates */}
            {results.time_estimates.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-info" />
                  <h3 className="font-semibold">Time Estimates</h3>
                  <Badge variant="secondary">{results.time_estimates.slice(0, 5).length}</Badge>
                </div>
                <div className="space-y-2">
                  {results.time_estimates.slice(0, 5).map((estimate, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex-1">
                        <p className="text-sm font-medium">Task #{estimate.task_id}</p>
                        <p className="text-xs text-muted-foreground">
                          {estimate.complexity_factors.join(', ')}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-semibold">{estimate.estimated_hours}h</p>
                        <p className="text-xs text-muted-foreground">
                          {estimate.confidence_interval.min}h - {estimate.confidence_interval.max}h
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Task Groups */}
            {results.groups.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <FolderOpen className="h-4 w-4 text-success" />
                  <h3 className="font-semibold">Grouping Suggestions</h3>
                  <Badge variant="secondary">{results.groups.length}</Badge>
                </div>
                {results.groups.map((group, idx) => (
                  <Card key={idx} className="border-success/50">
                    <CardContent className="pt-4">
                      <p className="text-sm font-medium mb-2">{group.name}</p>
                      <p className="text-sm text-muted-foreground mb-2">
                        {group.reasoning}
                      </p>
                      <div className="flex gap-2">
                        <Badge variant="outline">{group.category}</Badge>
                        <Badge variant="outline">
                          {group.task_ids.length} tasks
                        </Badge>
                        <Badge variant="outline">
                          {(group.confidence * 100).toFixed(0)}% confidence
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Automation Opportunities */}
            {results.automations.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Zap className="h-4 w-4 text-primary" />
                  <h3 className="font-semibold">Automation Opportunities</h3>
                  <Badge variant="secondary">{results.automations.length}</Badge>
                </div>
                {results.automations.map((auto, idx) => (
                  <Card key={idx} className="border-primary/50">
                    <CardContent className="pt-4">
                      <p className="text-sm font-medium mb-2">
                        {auto.automation_type.charAt(0).toUpperCase() + auto.automation_type.slice(1)}
                      </p>
                      <p className="text-sm text-muted-foreground mb-2">
                        {auto.suggestion}
                      </p>
                      <p className="text-xs text-muted-foreground mb-2 italic">
                        {auto.implementation}
                      </p>
                      <div className="flex gap-2">
                        <Badge variant="outline">
                          {auto.task_ids.length} task(s)
                        </Badge>
                        <Badge variant="outline">
                          {(auto.confidence * 100).toFixed(0)}% confidence
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* No suggestions */}
            {results.total_suggestions === 0 && (
              <div className="text-center py-8">
                <CheckCircle className="h-12 w-12 text-success mx-auto mb-4" />
                <p className="font-semibold">All good!</p>
                <p className="text-sm text-muted-foreground">
                  Your tasks are already well-organized.
                </p>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
