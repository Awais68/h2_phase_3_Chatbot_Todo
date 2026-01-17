/**
 * AI Chatbot Page - Main page with Chat, Analytics, and Recurring tabs
 */
'use client';

import { useState } from 'react';
import ChatTab from '@/components/ChatTab';
import AnalyticsTab from '@/components/AnalyticsTab';
import RecurringTab from '@/components/RecurringTab';

type TabType = 'chat' | 'analytics' | 'recurring';

export default function ChatbotPage() {
  const [activeTab, setActiveTab] = useState<TabType>('chat');
  const userId = 1; // TODO: Get from authentication context

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Todo AI Chatbot
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Manage your tasks with AI-powered natural language interface
          </p>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="flex border-b border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex-1 px-6 py-4 text-center font-medium transition-colors ${
                activeTab === 'chat'
                  ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
              }`}
            >
              💬 Chat
            </button>

            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex-1 px-6 py-4 text-center font-medium transition-colors ${
                activeTab === 'analytics'
                  ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
              }`}
            >
              📊 Analytics
            </button>

            <button
              onClick={() => setActiveTab('recurring')}
              className={`flex-1 px-6 py-4 text-center font-medium transition-colors ${
                activeTab === 'recurring'
                  ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
              }`}
            >
              🔄 Recurring
            </button>
          </div>

          {/* Tab Content */}
          <div className="h-[calc(100vh-16rem)]">
            {activeTab === 'chat' && <ChatTab userId={userId.toString()} />}
            {activeTab === 'analytics' && <AnalyticsTab userId={userId} />}
            {activeTab === 'recurring' && <RecurringTab userId={userId} />}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 mt-8">
        <div className="text-center text-sm text-gray-600 dark:text-gray-400">
          <p>Todo AI Chatbot - Phase III Implementation</p>
          <p className="mt-1">
            Powered by OpenAI Agents SDK, MCP Tools, FastAPI, and Next.js
          </p>
        </div>
      </footer>
    </div>
  );
}
