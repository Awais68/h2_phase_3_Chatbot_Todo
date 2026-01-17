/**
 * Analytics Tab Component - Task Analytics and Visualizations
 */
'use client';

import { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Line, Bar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(ArcElement, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

interface AnalyticsTabProps {
  userId: number;
}

interface TaskStatistics {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  completion_rate: number;
}

interface TimelineData {
  date: string;
  created: number;
  completed: number;
}

interface ProductivityHour {
  hour: number;
  tasks_completed: number;
}

export default function AnalyticsTab({ userId }: AnalyticsTabProps) {
  const [statistics, setStatistics] = useState<TaskStatistics | null>(null);
  const [timeline, setTimeline] = useState<TimelineData[]>([]);
  const [productivity, setProductivity] = useState<ProductivityHour[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, [userId]);

  const fetchAnalytics = async () => {
    setIsLoading(true);
    try {
      // Fetch statistics
      const statsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/analytics/overview`);
      const statsData = await statsResponse.json();
      setStatistics(statsData);

      // Fetch timeline
      const timelineResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/analytics/timeline?days=30`);
      const timelineData = await timelineResponse.json();
      setTimeline(timelineData.timeline);

      // Fetch productivity
      const productivityResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/analytics/productivity`);
      const productivityData = await productivityResponse.json();
      setProductivity(productivityData.productivity_by_hour);

    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading analytics...</p>
        </div>
      </div>
    );
  }

  // Pie chart data for completion rate
  const pieData = {
    labels: ['Completed', 'Pending'],
    datasets: [
      {
        data: [statistics?.completed_tasks || 0, statistics?.pending_tasks || 0],
        backgroundColor: ['#10b981', '#f59e0b'],
        borderColor: ['#059669', '#d97706'],
        borderWidth: 1,
      },
    ],
  };

  // Line chart data for tasks over time
  const lineData = {
    labels: timeline.map(t => new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
    datasets: [
      {
        label: 'Created',
        data: timeline.map(t => t.created),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
      {
        label: 'Completed',
        data: timeline.map(t => t.completed),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
      },
    ],
  };

  // Bar chart data for productivity by hour
  const barData = {
    labels: productivity.map(p => `${p.hour}:00`),
    datasets: [
      {
        label: 'Tasks Completed',
        data: productivity.map(p => p.tasks_completed),
        backgroundColor: '#8b5cf6',
        borderColor: '#7c3aed',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="h-full overflow-y-auto p-6 bg-gray-50 dark:bg-gray-900">
      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
        Task Analytics
      </h2>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Tasks</p>
          <p className="text-3xl font-bold text-gray-800 dark:text-white mt-2">
            {statistics?.total_tasks || 0}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <p className="text-sm text-gray-600 dark:text-gray-400">Completed</p>
          <p className="text-3xl font-bold text-green-500 mt-2">
            {statistics?.completed_tasks || 0}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <p className="text-sm text-gray-600 dark:text-gray-400">Pending</p>
          <p className="text-3xl font-bold text-yellow-500 mt-2">
            {statistics?.pending_tasks || 0}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <p className="text-sm text-gray-600 dark:text-gray-400">Completion Rate</p>
          <p className="text-3xl font-bold text-blue-500 mt-2">
            {statistics?.completion_rate.toFixed(1) || 0}%
          </p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Completion Rate Pie Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">
            Task Status Distribution
          </h3>
          <div className="h-64 flex items-center justify-center">
            <Pie data={pieData} options={{ maintainAspectRatio: false }} />
          </div>
        </div>

        {/* Tasks Over Time Line Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">
            Tasks Over Time (Last 30 Days)
          </h3>
          <div className="h-64">
            <Line
              data={lineData}
              options={{
                maintainAspectRatio: false,
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                  },
                },
              }}
            />
          </div>
        </div>

        {/* Productivity by Hour Bar Chart */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">
            Productivity by Hour of Day
          </h3>
          <div className="h-64">
            <Bar
              data={barData}
              options={{
                maintainAspectRatio: false,
                responsive: true,
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      stepSize: 1,
                    },
                  },
                },
              }}
            />
          </div>
        </div>
      </div>

      {/* Refresh Button */}
      <div className="mt-6 text-center">
        <button
          onClick={fetchAnalytics}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Refresh Analytics
        </button>
      </div>
    </div>
  );
}
