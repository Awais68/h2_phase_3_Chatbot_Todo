'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  Search,
  Filter,
  CheckCircle,
  Trash2,
  RotateCcw,
  Calendar,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

interface TaskHistoryItem {
  history_id: number
  original_task_id: number
  title: string
  description: string
  completed: boolean
  due_date: string | null
  recurrence_pattern: string | null
  action_type: 'completed' | 'deleted'
  action_date: string
  can_restore: boolean
  retention_until: string
}

interface HistoryResponse {
  items: TaskHistoryItem[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export function HistoryTab() {
  const [history, setHistory] = useState<TaskHistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [actionTypeFilter, setActionTypeFilter] = useState<'all' | 'completed' | 'deleted'>('all')
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [total, setTotal] = useState(0)
  const pageSize = 50

  useEffect(() => {
    fetchHistory()
  }, [searchQuery, actionTypeFilter, currentPage])

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const params = new URLSearchParams({
        page: currentPage.toString(),
        page_size: pageSize.toString(),
      })

      if (searchQuery) {
        params.append('search', searchQuery)
      }

      if (actionTypeFilter !== 'all') {
        params.append('action_type', actionTypeFilter)
      }

      // Use demo user ID if not authenticated
      const userId = localStorage.getItem('userId') || '1'
      params.append('user_id', userId)

      const response = await fetch(`${API_BASE_URL}/api/history?${params.toString()}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data: HistoryResponse = await response.json()

      setHistory(data.items)
      setTotalPages(data.total_pages)
      setTotal(data.total)
    } catch (error) {
      console.error('Failed to fetch history:', error)
      // Show empty state on error
      setHistory([])
      setTotalPages(1)
      setTotal(0)
    } finally {
      setLoading(false)
    }
  }

  const handleRestore = async (historyId: number) => {
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const userId = localStorage.getItem('userId') || '1'
      const response = await fetch(`${API_BASE_URL}/api/history/${historyId}/restore?user_id=${userId}`, {
        method: 'POST',
      })

      if (response.ok) {
        // Remove from history list
        setHistory((prev) => prev.filter((item) => item.history_id !== historyId))
        setTotal((prev) => prev - 1)
        alert('Task restored successfully!')
      } else {
        const error = await response.json()
        alert(`Failed to restore task: ${error.detail}`)
      }
    } catch (error) {
      console.error('Failed to restore task:', error)
      alert('Failed to restore task')
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="w-6 h-6" />
            Task History
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            View your completed and deleted tasks from the past 2 years
          </p>
        </CardHeader>
        <CardContent>
          {/* Filters and Search */}
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value)
                  setCurrentPage(1)
                }}
                className="pl-10"
              />
            </div>

            {/* Action Type Filter */}
            <div className="flex gap-2">
              <Button
                variant={actionTypeFilter === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => {
                  setActionTypeFilter('all')
                  setCurrentPage(1)
                }}
              >
                All ({total})
              </Button>
              <Button
                variant={actionTypeFilter === 'completed' ? 'default' : 'outline'}
                size="sm"
                onClick={() => {
                  setActionTypeFilter('completed')
                  setCurrentPage(1)
                }}
              >
                <CheckCircle className="w-4 h-4 mr-1" />
                Completed
              </Button>
              <Button
                variant={actionTypeFilter === 'deleted' ? 'default' : 'outline'}
                size="sm"
                onClick={() => {
                  setActionTypeFilter('deleted')
                  setCurrentPage(1)
                }}
              >
                <Trash2 className="w-4 h-4 mr-1" />
                Deleted
              </Button>
            </div>
          </div>

          {/* History List */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : history.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Calendar className="w-16 h-16 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium mb-2">No history entries</h3>
              <p className="text-sm text-muted-foreground max-w-sm">
                Your completed and deleted tasks will appear here
              </p>
            </div>
          ) : (
            <>
              <div className="space-y-3">
                {history.map((item) => (
                  <motion.div
                    key={item.history_id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="border rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="font-medium">{item.title}</h3>
                          <Badge
                            variant={item.action_type === 'completed' ? 'default' : 'destructive'}
                          >
                            {item.action_type === 'completed' ? (
                              <>
                                <CheckCircle className="w-3 h-3 mr-1" />
                                Completed
                              </>
                            ) : (
                              <>
                                <Trash2 className="w-3 h-3 mr-1" />
                                Deleted
                              </>
                            )}
                          </Badge>
                          {item.recurrence_pattern && (
                            <Badge variant="outline">
                              Recurring: {item.recurrence_pattern}
                            </Badge>
                          )}
                        </div>

                        {item.description && (
                          <p className="text-sm text-muted-foreground mb-2">
                            {item.description}
                          </p>
                        )}

                        <div className="flex items-center gap-4 text-xs text-muted-foreground">
                          <span>Action: {formatDate(item.action_date)}</span>
                          {item.due_date && (
                            <span>Due: {formatDate(item.due_date)}</span>
                          )}
                          <span>Retention: {formatDate(item.retention_until)}</span>
                        </div>
                      </div>

                      {item.can_restore && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleRestore(item.history_id)}
                          className="flex-shrink-0"
                        >
                          <RotateCcw className="w-4 h-4 mr-1" />
                          Restore
                        </Button>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between mt-6 pt-6 border-t">
                  <div className="text-sm text-muted-foreground">
                    Page {currentPage} of {totalPages} ({total} total entries)
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                      disabled={currentPage === 1}
                    >
                      <ChevronLeft className="w-4 h-4 mr-1" />
                      Previous
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                      disabled={currentPage === totalPages}
                    >
                      Next
                      <ChevronRight className="w-4 h-4 ml-1" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default HistoryTab
