/**
 * Recurring Tasks Tab Component - Display Tasks with Recursion
 */
'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Repeat, Calendar, CheckCircle, Clock } from 'lucide-react';
import { useSession } from '@/lib/auth-client';
import { api } from '@/lib/api';

// Helper function to get consistent userId
const getUserId = (session: any): string => {
  return session?.user?.email || session?.user?.id || 'anonymous';
};

interface RecurringTask {
  id: string;
  title: string;
  description: string;
  recursion: string;
  priority: string;
  status: string;
  category: string;
  dueDate: string;
  createdAt: string;
  shoppingList?: any[];
  tags: string[];
}

interface RecurringTabProps {
  isDark: boolean;
}

export default function RecursionTab({ isDark }: RecurringTabProps) {
  const { data: session } = useSession();
  const [recurringTasks, setRecurringTasks] = useState<RecurringTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedTask, setSelectedTask] = useState<RecurringTask | null>(null);

  useEffect(() => {
    if (session?.user) {
      fetchRecurringTasks();
    }
  }, [session]);

  const fetchRecurringTasks = async () => {
    if (!session?.user) return;
    
    setIsLoading(true);
    try {
      const userId = getUserId(session);
      const userEmail = session?.user?.email;
      const userName = session?.user?.name;

      // Fetch all tasks and filter those with recursion field
      const tasks = await api.tasks.list({ userId, userEmail, userName });
      
      // Filter tasks that have recursion set
      const recurringTasks: RecurringTask[] = tasks
        .filter((task: any) => task.recursion)
        .map((task: any) => ({
          id: task.id.toString(),
          title: task.title,
          description: task.description || '',
          recursion: task.recursion,
          priority: task.priority || 'medium',
          status: task.status || 'pending',
          category: task.category || 'General',
          dueDate: task.dueDate || task.due_date,
          createdAt: task.createdAt || task.created_at,
          shoppingList: task.shopping_list || task.shoppingList || task.subitems || [],
          tags: task.tags || []
        }));
      
      setRecurringTasks(recurringTasks);
    } catch (error) {
      console.error('Error fetching recurring tasks:', error);
      setRecurringTasks([]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return 'No date set';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'high':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  if (!session?.user) {
    return (
      <div className="flex items-center justify-center h-full p-6">
        <div className="text-center">
          <p className="text-gray-600 dark:text-gray-400">Please log in to view recurring tasks</p>
        </div>
      </div>
    );
  }

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
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
            <Repeat className="w-6 h-6" />
            Recurring Tasks
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Tasks with monthly, weekly, or daily recurrence
          </p>
        </div>
        <div className="text-sm text-gray-600 dark:text-gray-400">
          {recurringTasks.length} {recurringTasks.length === 1 ? 'task' : 'tasks'}
        </div>
      </div>

      {recurringTasks.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <Repeat className="w-16 h-16 text-gray-400 dark:text-gray-600 mb-4" />
          <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">
            No recurring tasks
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 max-w-sm">
            Tasks marked with recursion (weekly, monthly, daily) will appear here
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {recurringTasks.map((task) => (
            <motion.div
              key={task.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg p-5 hover:shadow-xl transition-all cursor-pointer border-l-4 ${
                task.priority === 'critical' ? 'border-red-500' :
                task.priority === 'high' ? 'border-orange-500' :
                task.priority === 'medium' ? 'border-yellow-500' :
                'border-green-500'
              }`}
              onClick={() => setSelectedTask(selectedTask?.id === task.id ? null : task)}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-1">
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                      {task.description}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2 mb-3">
                <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>
                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                  <Repeat className="w-3 h-3" />
                  {task.recursion}
                </span>
                {task.status === 'completed' && (
                  <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                    <CheckCircle className="w-3 h-3" />
                    Completed
                  </span>
                )}
              </div>

              <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                <span className="flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  {formatDate(task.dueDate)}
                </span>
                <span>{task.category}</span>
              </div>

              {/* Sub-items/Shopping List */}
              {selectedTask?.id === task.id && task.shoppingList && task.shoppingList.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700"
                >
                  <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                    Sub-items:
                  </h4>
                  {task.shoppingList.map((category: any, idx: number) => (
                    <div key={idx} className="mb-2">
                      {category.name && (
                        <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                          {category.name}
                        </p>
                      )}
                      {category.items && category.items.length > 0 && (
                        <ul className="space-y-1 ml-2">
                          {category.items.map((item: any, itemIdx: number) => (
                            <li key={itemIdx} className="text-xs text-gray-600 dark:text-gray-400 flex items-center gap-2">
                              <span className={item.completed ? 'line-through' : ''}>
                                • {item.name} {item.quantity > 1 && `(${item.quantity})`}
                              </span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ))}
                </motion.div>
              )}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
