/**
 * Recurring Tasks Tab Component - Manage Recurring Tasks
 */
'use client';

import { useState, useEffect } from 'react';

interface RecurringTask {
  recurring_task_id: number;
  title: string;
  description: string;
  frequency: string;
  frequency_value: number | null;
  is_active: boolean;
  last_generated: string | null;
  created_at: string;
}

interface RecurringTabProps {
  userId: number;
}

export default function RecurringTab({ userId }: RecurringTabProps) {
  const [recurringTasks, setRecurringTasks] = useState<RecurringTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    frequency: 'daily',
    frequency_value: null as number | null
  });

  useEffect(() => {
    fetchRecurringTasks();
  }, [userId]);

  const fetchRecurringTasks = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/recurring`);
      const data = await response.json();
      setRecurringTasks(data.recurring_tasks || []);
    } catch (error) {
      console.error('Error fetching recurring tasks:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const createRecurringTask = async () => {
    if (!formData.title.trim()) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/recurring`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setFormData({ title: '', description: '', frequency: 'daily', frequency_value: null });
        setShowCreateForm(false);
        fetchRecurringTasks();
      }
    } catch (error) {
      console.error('Error creating recurring task:', error);
    }
  };

  const toggleTaskStatus = async (taskId: number, isActive: boolean) => {
    const endpoint = isActive ? 'pause' : 'resume';
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/recurring/${taskId}/${endpoint}`,
        { method: 'PATCH' }
      );

      if (response.ok) {
        fetchRecurringTasks();
      }
    } catch (error) {
      console.error('Error toggling task status:', error);
    }
  };

  const deleteRecurringTask = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this recurring task?')) return;

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/recurring/${taskId}`,
        { method: 'DELETE' }
      );

      if (response.ok) {
        fetchRecurringTasks();
      }
    } catch (error) {
      console.error('Error deleting recurring task:', error);
    }
  };

  const getFrequencyLabel = (frequency: string, value: number | null) => {
    if (frequency === 'daily') return 'Daily';
    if (frequency === 'weekly') {
      const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      return `Weekly (${value !== null ? days[value] : 'Every week'})`;
    }
    if (frequency === 'monthly') {
      return `Monthly (Day ${value || 1})`;
    }
    return frequency;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading recurring tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto p-6 bg-gray-50 dark:bg-gray-900">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
          Recurring Tasks
        </h2>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          {showCreateForm ? 'Cancel' : '+ New Recurring Task'}
        </button>
      </div>

      {/* Create Form */}
      {showCreateForm && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">
            Create Recurring Task
          </h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Title *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="e.g., Daily standup meeting"
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Optional description"
                rows={3}
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Frequency *
              </label>
              <select
                value={formData.frequency}
                onChange={(e) => setFormData({ ...formData, frequency: e.target.value })}
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>

            {formData.frequency === 'weekly' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Day of Week
                </label>
                <select
                  value={formData.frequency_value || 0}
                  onChange={(e) => setFormData({ ...formData, frequency_value: parseInt(e.target.value) })}
                  className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                >
                  <option value="0">Sunday</option>
                  <option value="1">Monday</option>
                  <option value="2">Tuesday</option>
                  <option value="3">Wednesday</option>
                  <option value="4">Thursday</option>
                  <option value="5">Friday</option>
                  <option value="6">Saturday</option>
                </select>
              </div>
            )}

            {formData.frequency === 'monthly' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Day of Month (1-31)
                </label>
                <input
                  type="number"
                  min="1"
                  max="31"
                  value={formData.frequency_value || 1}
                  onChange={(e) => setFormData({ ...formData, frequency_value: parseInt(e.target.value) })}
                  className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>
            )}

            <button
              onClick={createRecurringTask}
              disabled={!formData.title.trim()}
              className="w-full px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Create Recurring Task
            </button>
          </div>
        </div>
      )}

      {/* Recurring Tasks List */}
      {recurringTasks.length === 0 ? (
        <div className="text-center text-gray-500 dark:text-gray-400 mt-12">
          <p className="text-lg">No recurring tasks yet</p>
          <p className="text-sm mt-2">Create your first recurring task to get started!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {recurringTasks.map((task) => (
            <div
              key={task.recurring_task_id}
              className="bg-white dark:bg-gray-800 rounded-lg shadow p-6"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
                      {task.title}
                    </h3>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        task.is_active
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                      }`}
                    >
                      {task.is_active ? 'Active' : 'Paused'}
                    </span>
                  </div>

                  {task.description && (
                    <p className="text-gray-600 dark:text-gray-400 mt-2">
                      {task.description}
                    </p>
                  )}

                  <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500 dark:text-gray-400">
                    <span className="flex items-center">
                      🔄 {getFrequencyLabel(task.frequency, task.frequency_value)}
                    </span>
                    {task.last_generated && (
                      <span className="flex items-center">
                        📅 Last: {new Date(task.last_generated).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex space-x-2 ml-4">
                  <button
                    onClick={() => toggleTaskStatus(task.recurring_task_id, task.is_active)}
                    className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                      task.is_active
                        ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200 dark:bg-yellow-900 dark:text-yellow-200'
                        : 'bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900 dark:text-green-200'
                    }`}
                  >
                    {task.is_active ? 'Pause' : 'Resume'}
                  </button>

                  <button
                    onClick={() => deleteRecurringTask(task.recurring_task_id)}
                    className="px-3 py-1 bg-red-100 text-red-800 rounded-lg hover:bg-red-200 dark:bg-red-900 dark:text-red-200 text-sm transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
