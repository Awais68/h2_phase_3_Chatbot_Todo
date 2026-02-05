/**
 * Chat Tab Component - AI Chatbot Interface for Dashboard
 */
'use client';

import { useState, useRef, useEffect } from 'react';
import { useVoiceInput } from '@/hooks/useVoiceInput';
import { useVoiceOutput } from '@/hooks/useVoiceOutput';
import { formatDueDateForChat } from '@/utils/dateUtils';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  dueDate?: string | null;
  taskCreated?: boolean;
}

interface ChatTabProps {
  userId: string; // Changed to string for Better Auth compatibility
  isDark?: boolean; // Theme support
  onTasksUpdated?: () => void; // Callback to refresh tasks in dashboard
}

export default function ChatTab({ userId, isDark = false, onTasksUpdated }: ChatTabProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { transcript, isListening, startListening, stopListening } = useVoiceInput();
  const { speak, isSpeaking } = useVoiceOutput();

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Update input when voice transcript changes
  useEffect(() => {
    if (transcript) {
      setInput(transcript);
    }
  }, [transcript]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    // Use 'demo' as default userId if none provided to prevent double slash in API URL
    const effectiveUserId = userId && userId.trim() ? userId : 'demo';

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageContent = input;
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${effectiveUserId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: messageContent
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      // Update conversation ID
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Extract due date from tool calls if task was created with due date
      let dueDate: string | null = null;
      let taskCreated = false;

      if (data.tool_calls && Array.isArray(data.tool_calls)) {
        const taskCreationCall = data.tool_calls.find(
          (call: any) => call.name === 'add_task_with_due_date'
        );
        if (taskCreationCall?.result) {
          dueDate = taskCreationCall.result.due_date || null;
          taskCreated = true;
        }
      }

      // Add assistant response
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        dueDate,
        taskCreated,
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Speak the response if voice output is enabled
      speak(data.response);

      // Trigger task refresh if callback provided
      if (onTasksUpdated) {
        onTasksUpdated();
      }

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleVoiceInput = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  return (
    <div className={`flex flex-col h-full rounded-lg shadow-lg backdrop-blur-xl border transition-all duration-300 ${isDark
      ? 'bg-slate-800/40 border-cyan-500/20'
      : 'bg-white/60 border-sky-200/60'
      }`}>
      {/* Chat Header */}
      <div className={`p-4 border-b ${isDark ? 'border-cyan-500/20' : 'border-sky-200/60'}`}>
        <h2 className={`text-xl font-semibold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
          AI Task Assistant
        </h2>
        <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
          Ask me to manage your tasks using natural language
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className={`text-center mt-8 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
            <p className="text-lg mb-2">👋 Hi! I'm your AI task assistant.</p>
            <p className="text-sm">Try saying:</p>
            <ul className="text-sm mt-2 space-y-1">
              <li>"Add a task to buy groceries"</li>
              <li>"Show me all my tasks"</li>
              <li>"Mark task 1 as complete"</li>
              <li>"Create a daily recurring task"</li>
            </ul>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg p-3 ${message.role === 'user'
                ? isDark
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white'
                  : 'bg-gradient-to-r from-cyan-400 to-blue-500 text-white'
                : isDark
                  ? 'bg-slate-700/50 text-white border border-cyan-500/20'
                  : 'bg-gray-100 text-gray-800 border border-sky-200'
                }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>

              {/* Display due date if task was created with one */}
              {message.taskCreated && message.dueDate && (
                <div className={`mt-2 pt-2 border-t text-xs ${
                  isDark ? 'border-cyan-500/30' : 'border-gray-300'
                }`}>
                  <span className="font-semibold">📅 Due: </span>
                  {formatDueDateForChat(message.dueDate)}
                </div>
              )}

              <p className="text-xs mt-1 opacity-70">
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className={`rounded-lg p-3 ${isDark ? 'bg-slate-700/50' : 'bg-gray-100'}`}>
              <div className="flex space-x-2">
                <div className={`w-2 h-2 rounded-full animate-bounce ${isDark ? 'bg-cyan-400' : 'bg-gray-400'}`}></div>
                <div className={`w-2 h-2 rounded-full animate-bounce ${isDark ? 'bg-cyan-400' : 'bg-gray-400'}`} style={{ animationDelay: '0.1s' }}></div>
                <div className={`w-2 h-2 rounded-full animate-bounce ${isDark ? 'bg-cyan-400' : 'bg-gray-400'}`} style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className={`p-4 border-t ${isDark ? 'border-cyan-500/20' : 'border-sky-200/60'}`}>
        <div className="flex space-x-2">
          <button
            onClick={toggleVoiceInput}
            className={`p-3 rounded-lg transition-colors ${isListening
              ? 'bg-red-500 text-white'
              : isDark
                ? 'bg-slate-700/50 text-cyan-400 hover:bg-slate-600/50 border border-cyan-500/20'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            title={isListening ? 'Stop listening' : 'Start voice input'}
          >
            {isListening ? '🔴' : '🎤'}
          </button>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message or use voice input..."
            className={`flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${isDark
              ? 'bg-slate-700/50 border-cyan-500/20 text-white focus:ring-cyan-400 placeholder-gray-400'
              : 'bg-gray-50 border-gray-300 text-gray-800 focus:ring-blue-500'
              }`}
            disabled={isLoading}
          />

          <button
            onClick={sendMessage}
            disabled={!input.trim() || isLoading}
            className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg hover:from-cyan-400 hover:to-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02]"
          >
            Send
          </button>
        </div>

        {isListening && (
          <p className={`text-sm mt-2 animate-pulse ${isDark ? 'text-red-400' : 'text-red-500'}`}>
            🎤 Listening... Speak now
          </p>
        )}

        {isSpeaking && (
          <p className={`text-sm mt-2 ${isDark ? 'text-cyan-400' : 'text-blue-500'}`}>
            🔊 Speaking...
          </p>
        )}
      </div>
    </div>
  );
}
