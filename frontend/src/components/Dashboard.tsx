'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import {
    Plus,
    Search,
    Target,
    Clock,
    AlertTriangle,
    CheckCircle,
    Star,
    Filter,
    Calendar,
    X,
    MoreVertical,
    Edit,
    Trash2,
    Menu,
    ChevronLeft,
    RefreshCw,
    Flag,
    Sun,
    Moon,
    TrendingUp,
    Activity,
    Zap,
    BarChart3,
    LogOut,
    MessageSquare,
    Repeat,
    History,
    Bell,
} from 'lucide-react';
import VoiceCommandButton from './VoiceCommandButton';
import ParticlesBackground from './ParticlesBackground';
import ChatTab from './ChatTab';
import RecursionTab from './RecursionTab';
import { api } from '@/lib/api';
import { useSession, signOut } from '@/lib/auth-client';

// Helper function to get consistent userId
const getUserId = (session: any): string => {
  // Always prioritize email for consistency across all operations
  return session?.user?.email || session?.user?.id || 'anonymous';
};

// Types
interface Item {
  id: string;
  name: string;
  price: number;
  quantity: number;
  completed?: boolean;
}

interface Category {
  id: string;
  name: string;
  items: Item[];
}

interface Mission {
    id: string;
    title: string;
    description: string;
    priority: 'critical' | 'high' | 'medium' | 'low';
    status: 'pending' | 'active' | 'completed' | 'failed';
    dueDate: string;
    createdAt: string;
    tags: string[];
    category: string;
    recursion?: string;
    shoppingList?: Category[];
}

interface MissionTab {
    id: string;
    label: string;
    icon: React.ReactNode;
    count: number;
}

// Mock data
const mockMissions: Mission[] = [
    {
        id: '1',
        title: 'Secure Database Perimeter',
        description: 'Implement advanced encryption protocols for the main database infrastructure.',
        priority: 'critical',
        status: 'active',
        dueDate: '2025-01-20',
        createdAt: '2025-01-15T10:30:00Z',
        tags: ['security', 'database'],
        category: 'Infrastructure',
        recursion: 'Weekly',
    },
    {
        id: '2',
        title: 'Deploy Surveillance Network',
        description: 'Set up monitoring systems across all entry points.',
        priority: 'high',
        status: 'pending',
        dueDate: '2025-01-22',
        createdAt: '2025-01-14T08:00:00Z',
        tags: ['surveillance', 'security'],
        category: 'Operations',
    },
    {
        id: '3',
        title: 'Extract Intelligence Report',
        description: 'Compile quarterly security assessment.',
        priority: 'medium',
        status: 'completed',
        dueDate: '2025-01-18',
        createdAt: '2025-01-10T14:00:00Z',
        tags: ['reporting', 'intel'],
        category: 'Analysis',
        recursion: 'Monthly',
    },
    {
        id: '4',
        title: 'Update Firewall Configuration',
        description: 'Apply latest security patches to all firewall systems.',
        priority: 'high',
        status: 'pending',
        dueDate: '2025-01-25',
        createdAt: '2025-01-16T09:00:00Z',
        tags: ['security', 'maintenance'],
        category: 'Infrastructure',
    },
    {
        id: '5',
        title: 'Agent Training Session',
        description: 'Conduct security awareness training for new recruits.',
        priority: 'low',
        status: 'pending',
        dueDate: '2025-01-30',
        createdAt: '2025-01-12T11:00:00Z',
        tags: ['training', 'hr'],
        category: 'Training',
        recursion: 'Bi-weekly',
    },
        {
            id: '6',
            title: 'Grocery Shopping List',
            description: 'Weekly grocery shopping trip',
            priority: 'medium',
            status: 'active',
            dueDate: '2025-01-25',
            createdAt: '2025-01-18T10:00:00Z',
            tags: ['shopping', 'groceries'],
            category: 'Groceries',
            shoppingList: [
                {
                    id: '1',
                    name: 'Groceries',
                    items: [
                        { id: '1', name: 'Flour', price: 2.50, quantity: 2, completed: false },
                        { id: '2', name: 'Surf', price: 3.20, quantity: 1, completed: false },
                        { id: '3', name: 'Soap', price: 1.80, quantity: 3, completed: true },
                        { id: '4', name: 'Match Box', price: 0.50, quantity: 2, completed: false },
                    ]
                }
            ]
        },
        {
            id: '7',
            title: 'Office Supplies',
            description: 'Monthly office supplies purchase',
            priority: 'medium',
            status: 'active',
            dueDate: '2025-02-01',
            createdAt: '2025-01-18T11:00:00Z',
            tags: ['office', 'supplies'],
            category: 'Office',
            shoppingList: [
                {
                    id: '2',
                    name: 'Office Supplies',
                    items: [
                        { id: '5', name: 'Pens', price: 1.20, quantity: 10, completed: false },
                        { id: '6', name: 'Paper', price: 5.00, quantity: 2, completed: true },
                        { id: '7', name: 'Stapler', price: 8.50, quantity: 1, completed: false },
                    ]
                }
            ]
        },
    ];

// Helper function to format date
const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    });
};

// Status Card Component
const StatusCard = ({
    title,
    count,
    icon: Icon,
    color,
    trend,
    isDark
}: {
    title: string;
    count: number;
    icon: React.ElementType;
    color: string;
    trend?: number;
    isDark: boolean;
}) => {
    const colorClasses: Record<string, { bg: string; border: string; text: string; glow: string }> = {
        cyan: {
            bg: isDark ? 'bg-cyan-500/10' : 'bg-cyan-100/80',
            border: 'border-cyan-400/40',
            text: isDark ? 'text-cyan-400' : 'text-cyan-600',
            glow: 'shadow-cyan-500/20'
        },
        green: {
            bg: isDark ? 'bg-emerald-500/10' : 'bg-emerald-100/80',
            border: 'border-emerald-400/40',
            text: isDark ? 'text-emerald-400' : 'text-emerald-600',
            glow: 'shadow-emerald-500/20'
        },
        orange: {
            bg: isDark ? 'bg-orange-500/10' : 'bg-orange-100/80',
            border: 'border-orange-400/40',
            text: isDark ? 'text-orange-400' : 'text-orange-600',
            glow: 'shadow-orange-500/20'
        },
        purple: {
            bg: isDark ? 'bg-purple-500/10' : 'bg-purple-100/80',
            border: 'border-purple-400/40',
            text: isDark ? 'text-purple-400' : 'text-purple-600',
            glow: 'shadow-purple-500/20'
        },
    };

    const classes = colorClasses[color] || colorClasses.cyan;

    return (
        <motion.div
            whileHover={{ scale: 1.02, y: -2 }}
            className={`relative p-5 rounded-2xl backdrop-blur-xl border ${classes.bg} ${classes.border} 
                       shadow-lg ${classes.glow} transition-all duration-300`}
        >
            <div className="flex items-start justify-between">
                <div>
                    <p className={`text-sm font-medium ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>{title}</p>
                    <p className={`text-3xl font-bold mt-1 ${classes.text}`}>{count}</p>
                    {trend !== undefined && (
                        <div className={`flex items-center gap-1 mt-2 text-xs ${trend >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            <TrendingUp className={`w-3 h-3 ${trend < 0 ? 'rotate-180' : ''}`} />
                            <span>{Math.abs(trend)}% from last week</span>
                        </div>
                    )}
                </div>
                <div className={`p-3 rounded-xl ${classes.bg} ${classes.border} border`}>
                    <Icon className={`w-6 h-6 ${classes.text}`} />
                </div>
            </div>
        </motion.div>
    );
};

// Mini Chart Component
const MiniChart = ({ data, color, isDark }: { data: number[]; color: string; isDark: boolean }) => {
    const max = Math.max(...data);
    const colorMap: Record<string, string> = {
        cyan: isDark ? '#22d3ee' : '#0891b2',
        green: isDark ? '#34d399' : '#059669',
        orange: isDark ? '#fb923c' : '#ea580c',
        purple: isDark ? '#a78bfa' : '#7c3aed',
    };
    const barColor = colorMap[color] || colorMap.cyan;

    return (
        <div className="flex items-end gap-1 h-16">
            {data.map((value, i) => (
                <motion.div
                    key={i}
                    initial={{ height: 0 }}
                    animate={{ height: `${(value / max) * 100}%` }}
                    transition={{ delay: i * 0.1, duration: 0.5 }}
                    className="flex-1 rounded-t-sm"
                    style={{ backgroundColor: barColor, opacity: 0.3 + (i / data.length) * 0.7 }}
                />
            ))}
        </div>
    );
};

// MissionCard Component with ice colors
const MissionCard = ({
    mission,
    onEdit,
    onDelete,
    onToggleComplete,
    isDark
}: {
    mission: Mission;
    onEdit: (m: Mission) => void;
    onDelete: (id: string) => void;
    onToggleComplete: (id: string) => void;
    isDark: boolean;
}) => {
    const [showMenu, setShowMenu] = useState(false);

    const priorityColors = {
        critical: isDark ? 'bg-red-500/20 text-red-400 border-red-500/50' : 'bg-red-100 text-red-600 border-red-300',
        high: isDark ? 'bg-orange-500/20 text-orange-400 border-orange-500/50' : 'bg-orange-100 text-orange-600 border-orange-300',
        medium: isDark ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50' : 'bg-yellow-100 text-yellow-600 border-yellow-300',
        low: isDark ? 'bg-blue-500/20 text-blue-400 border-blue-500/50' : 'bg-blue-100 text-blue-600 border-blue-300',
    };

    const statusColors = {
        pending: isDark ? 'bg-gray-500/20 text-gray-400' : 'bg-gray-200 text-gray-600',
        active: isDark ? 'bg-cyan-500/20 text-cyan-400' : 'bg-cyan-100 text-cyan-600',
        completed: isDark ? 'bg-green-500/20 text-green-400' : 'bg-green-100 text-green-600',
        failed: isDark ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-600',
    };

    return (
        <motion.div
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            whileHover={{ scale: 1.02 }}
            className={`relative backdrop-blur-xl border rounded-xl p-5 m-2 transition-all duration-300 shadow-lg cursor-pointer
                ${isDark
                    ? 'bg-slate-800/40 border-cyan-500/20 hover:border-cyan-400/40 shadow-cyan-500/5'
                    : 'bg-white/60 border-sky-200/60 hover:border-sky-300/80 shadow-sky-500/10'
                }`}
        >
            {/* Checkbox for Mark as Complete */}
            <div className="absolute top-3 left-3 flex items-center gap-2">
                <input
                    type="checkbox"
                    checked={mission.status === 'completed'}
                    onChange={() => onToggleComplete(mission.id)}
                    className="w-5 h-5 rounded border-2 cursor-pointer"
                    style={{
                        accentColor: isDark ? '#22d3ee' : '#0891b2'
                    }}
                />
            </div>

            {/* Priority Badge */}
            <div className="absolute -top-2 -right-2">
                <span className={`px-3 py-1 text-xs font-bold uppercase rounded-full border ${priorityColors[mission.priority]}`}>
                    {mission.priority}
                </span>
            </div>

            {/* Delete Icon */}
            <button
                onClick={() => onDelete(mission.id)}
                className={`absolute top-3 right-12 p-1.5 rounded-lg transition-colors
                    ${isDark ? 'text-red-400 hover:bg-red-500/20' : 'text-red-600 hover:bg-red-100'}`}
                title="Move to Trash"
            >
                <Trash2 className="w-4 h-4" />
            </button>

            {/* Menu Button */}
            <button
                onClick={() => setShowMenu(!showMenu)}
                className={`absolute top-3 right-3 p-1 transition-colors ${isDark ? 'text-gray-400 hover:text-cyan-400' : 'text-gray-500 hover:text-cyan-600'}`}
            >
                <MoreVertical className="w-4 h-4" />
            </button>

            {/* Dropdown Menu */}
            <AnimatePresence>
                {showMenu && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className={`absolute top-10 right-3 border rounded-lg shadow-xl z-10
                            ${isDark ? 'bg-gray-800 border-gray-600' : 'bg-white border-gray-200'}`}
                    >
                        <button
                            onClick={() => { onEdit(mission); setShowMenu(false); }}
                            className={`flex items-center gap-2 px-4 py-2 text-sm w-full
                                ${isDark ? 'text-gray-300 hover:bg-gray-700' : 'text-gray-600 hover:bg-gray-100'}`}
                        >
                            <Edit className="w-4 h-4" /> Edit
                        </button>
                        <button
                            onClick={() => { onToggleComplete(mission.id); setShowMenu(false); }}
                            className={`flex items-center gap-2 px-4 py-2 text-sm w-full
                                ${mission.status === 'completed'
                                    ? isDark ? 'text-orange-400 hover:bg-gray-700' : 'text-orange-600 hover:bg-gray-100'
                                    : isDark ? 'text-green-400 hover:bg-gray-700' : 'text-green-600 hover:bg-gray-100'}`}
                        >
                            <CheckCircle className="w-4 h-4" /> {mission.status === 'completed' ? 'Mark Incomplete' : 'Mark Complete'}
                        </button>
                        <button
                            onClick={() => { onDelete(mission.id); setShowMenu(false); }}
                            className="flex items-center gap-2 px-4 py-2 text-sm text-red-400 hover:bg-gray-700 w-full"
                        >
                            <Trash2 className="w-4 h-4" /> Delete
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Status Badge */}
            <div className="mb-3">
                <span className={`px-2 py-1 text-xs font-semibold uppercase rounded ${statusColors[mission.status]}`}>
                    {mission.status}
                </span>
            </div>

            {/* Title with strikethrough for completed */}
            <h3 className={`text-lg font-bold mb-2 pr-8 pl-8 ${isDark ? 'text-white' : 'text-gray-800'} 
                ${mission.status === 'completed' ? 'line-through opacity-60' : ''}`}>
                {mission.title}
            </h3>

            {/* Description with reduced opacity for completed */}
            <p className={`text-sm mb-4 line-clamp-2 pl-8 ${isDark ? 'text-gray-400' : 'text-gray-600'}
                ${mission.status === 'completed' ? 'line-through opacity-50' : ''}`}>
                {mission.description}
            </p>

            {/* Details Grid */}
            <div className={`grid grid-cols-2 gap-3 text-xs mb-4 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                <div className="flex items-center gap-2">
                    <Calendar className={`w-4 h-4 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`} />
                    <span>Due: {formatDate(mission.dueDate)}</span>
                </div>
                <div className="flex items-center gap-2">
                    <Clock className={`w-4 h-4 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`} />
                    <span>Created: {formatDate(mission.createdAt)}</span>
                </div>
                {mission.recursion && (
                    <div className="flex items-center gap-2">
                        <RefreshCw className={`w-4 h-4 ${isDark ? 'text-purple-400' : 'text-purple-600'}`} />
                        <span>Recurs: {mission.recursion}</span>
                    </div>
                )}
                <div className="flex items-center gap-2">
                    <Flag className={`w-4 h-4 ${isDark ? 'text-orange-400' : 'text-orange-600'}`} />
                    <span>{mission.category}</span>
                </div>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-2">
                {mission.tags.map((tag, index) => (
                    <span
                        key={index}
                        className={`px-2 py-1 text-xs rounded-md border
                            ${isDark ? 'bg-gray-700/50 text-gray-300 border-gray-600' : 'bg-gray-100 text-gray-600 border-gray-200'}`}
                    >
                        #{tag}
                    </span>
                ))}
            </div>

            {/* Open Button */}
            <div className="mt-4 pt-3 border-t border-gray-300 border-opacity-30">
                <button
                    className={`w-full py-2 text-sm rounded-lg border transition-all ${
                        isDark
                            ? 'border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10'
                            : 'border-cyan-300 text-cyan-600 hover:bg-cyan-100'
                    }`}
                >
                    Open Task
                </button>
            </div>
        </motion.div>
    );
};

// AddMissionModal Component
const AddMissionModal = ({
    isOpen,
    onClose,
    onAdd,
    isDark,
    initialData,
    isEditMode = false
}: {
    isOpen: boolean;
    onClose: () => void;
    onAdd: (mission: Omit<Mission, 'id' | 'createdAt'>) => void;
    isDark: boolean;
    initialData?: Mission;
    isEditMode?: boolean;
}) => {
    const [formData, setFormData] = useState({
        title: initialData?.title || '',
        description: initialData?.description || '',
        priority: (initialData?.priority || 'medium') as Mission['priority'],
        status: (initialData?.status || 'pending') as Mission['status'],
        dueDate: initialData?.dueDate ? new Date(initialData.dueDate).toISOString().split('T')[0] : '',
        category: initialData?.category || '',
        tags: initialData?.tags ? initialData.tags.join(', ') : '',
        recursion: initialData?.recursion || '',
    });

    // Update form when initialData changes
    React.useEffect(() => {
        if (initialData) {
            setFormData({
                title: initialData.title || '',
                description: initialData.description || '',
                priority: initialData.priority || 'medium',
                status: initialData.status || 'pending',
                dueDate: initialData.dueDate ? new Date(initialData.dueDate).toISOString().split('T')[0] : '',
                category: initialData.category || '',
                tags: initialData.tags ? initialData.tags.join(', ') : '',
                recursion: initialData.recursion || '',
            });
        }
    }, [initialData]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!formData.title.trim()) return;

        onAdd({
            title: formData.title,
            description: formData.description,
            priority: formData.priority,
            status: formData.status,
            dueDate: formData.dueDate || new Date().toISOString().split('T')[0],
            category: formData.category || 'General',
            tags: formData.tags.split(',').map(t => t.trim()).filter(Boolean),
            recursion: formData.recursion || undefined,
        });

        setFormData({
            title: '',
            description: '',
            priority: 'medium',
            status: 'pending',
            dueDate: '',
            category: '',
            tags: '',
            recursion: '',
        });
    };

    if (!isOpen) return null;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={onClose}
        >
            <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className={`border rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto
                    ${isDark ? 'bg-gray-900 border-cyan-500/50' : 'bg-white border-sky-300'}`}
                onClick={(e) => e.stopPropagation()}
            >
                <div className="flex items-center justify-between mb-6">
                    <h2 className={`text-2xl font-bold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                        {isEditMode ? 'Edit Mission' : 'Initialize New Mission'}
                    </h2>
                    <button onClick={onClose} className={isDark ? 'text-gray-400 hover:text-white' : 'text-gray-500 hover:text-gray-800'}>
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Mission Title *</label>
                        <input
                            type="text"
                            value={formData.title}
                            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                            className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors
                                ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            placeholder="Enter mission title..."
                            required
                        />
                    </div>

                    <div>
                        <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Description</label>
                        <textarea
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors resize-none
                                ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            rows={3}
                            placeholder="Mission details..."
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Priority</label>
                            <select
                                value={formData.priority}
                                onChange={(e) => setFormData({ ...formData, priority: e.target.value as Mission['priority'] })}
                                className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400
                                    ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                                <option value="critical">Critical</option>
                            </select>
                        </div>

                        <div>
                            <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Status</label>
                            <select
                                value={formData.status}
                                onChange={(e) => setFormData({ ...formData, status: e.target.value as Mission['status'] })}
                                className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400
                                    ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            >
                                <option value="pending">Pending</option>
                                <option value="active">Active</option>
                                <option value="completed">Completed</option>
                            </select>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Due Date</label>
                            <input
                                type="date"
                                value={formData.dueDate}
                                onChange={(e) => setFormData({ ...formData, dueDate: e.target.value })}
                                className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400
                                    ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            />
                        </div>

                        <div>
                            <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Recursion</label>
                            <select
                                value={formData.recursion}
                                onChange={(e) => setFormData({ ...formData, recursion: e.target.value })}
                                className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400
                                    ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            >
                                <option value="">None</option>
                                <option value="Daily">Daily</option>
                                <option value="Weekly">Weekly</option>
                                <option value="Bi-weekly">Bi-weekly</option>
                                <option value="Monthly">Monthly</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Category</label>
                        <input
                            type="text"
                            value={formData.category}
                            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                            className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400
                                ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            placeholder="e.g., Infrastructure, Operations..."
                        />
                    </div>

                    <div>
                        <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Tags (comma separated)</label>
                        <input
                            type="text"
                            value={formData.tags}
                            onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                            className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400
                                ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                            placeholder="security, urgent, backend..."
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-3 rounded-lg
                                 hover:from-cyan-400 hover:to-blue-500 transition-all duration-300 transform hover:scale-[1.02]"
                    >
                        {isEditMode ? 'Save Changes' : 'Initialize Mission'}
                    </button>
                </form>
            </motion.div>
        </motion.div>
    );
};

// Main Dashboard Component
export default function Dashboard() {
    const router = useRouter();
    const { data: session, isPending } = useSession();
    const isAuthenticated = !!session?.user;

    const [missions, setMissions] = useState<Mission[]>([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedPriority, setSelectedPriority] = useState<string>('all');
    const [selectedStatus, setSelectedStatus] = useState<string>('all');
    const [selectedCategory, setSelectedCategory] = useState<string>('all'); // For category filtering
    const [showFilters, setShowFilters] = useState(false);
    const [showAddModal, setShowAddModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editingMission, setEditingMission] = useState<Mission | null>(null);
    const [isMobile, setIsMobile] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [isDark, setIsDark] = useState(() => {
        // Initialize from localStorage or default to true
        if (typeof window !== 'undefined') {
            const saved = localStorage.getItem('theme');
            return saved ? saved === 'dark' : true;
        }
        return true;
    });
    const [showShoppingList, setShowShoppingList] = useState(false);
    const [shoppingListCategory, setShoppingListCategory] = useState<string>('');
    const [newItemName, setNewItemName] = useState('');
    const [newItemPrice, setNewItemPrice] = useState(0);
    const [newItemQuantity, setNewItemQuantity] = useState(1);
    const [editingItemId, setEditingItemId] = useState<string | null>(null);
    const [editingItemMissionId, setEditingItemMissionId] = useState<string | null>(null);
    const [editingItemCategoryId, setEditingItemCategoryId] = useState<string | null>(null);
    const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({});
    const [selectedMission, setSelectedMission] = useState<Mission | null>(null);

    // Handle mission card click to expand sub-items
    const handleMissionCardClick = useCallback((mission: Mission) => {
        setSelectedMission(selectedMission?.id === mission.id ? null : mission);
        
        // Expand shopping list if it has items
        if (mission.shoppingList && mission.shoppingList.length > 0) {
            const expandedState: Record<string, boolean> = {};
            mission.shoppingList.forEach(category => {
                expandedState[category.id] = true;
            });
            setExpandedCategories(expandedState);
        }
    }, [selectedMission]);

    // Fetch tasks from API on mount
    useEffect(() => {
        const fetchTasks = async () => {
            try {
                // Wait for session check to complete
                if (isPending) {
                    console.log('Session check in progress...');
                    return;
                }

                setLoading(true);

                // Check authentication
                if (!isAuthenticated) {
                    console.log('Not authenticated - showing empty dashboard');
                    // Show empty missions when not authenticated
                    setMissions([]);
                    setLoading(false);
                    return;
                }

                // Sync user to backend
                if (session?.user) {
                    try {
                        console.log('User synced to backend');
                    } catch (error) {
                        console.error('Failed to sync user:', error);
                    }
                }

                const userId = getUserId(session);

                if (!userId || userId === 'anonymous') {
                    console.error('No userId found in session');
                    // Show empty missions if no user ID found
                    setMissions([]);
                    setLoading(false);
                    return;
                }

                const userEmail = session?.user?.email;
                const userName = session?.user?.name;

                // Try to fetch from backend, but fallback to mock data if API fails
                try {
                    const tasks = await api.tasks.list({ userId, userEmail, userName });

                    // Map backend tasks to Mission format
                    const mappedTasks: Mission[] = tasks.map((task: any) => ({
                        id: task.id.toString(),
                        title: task.title,
                        description: task.description || '',
                        priority: (task.priority || 'medium') as 'critical' | 'high' | 'medium' | 'low',
                        status: (task.status || 'pending') as 'pending' | 'active' | 'completed' | 'failed',
                        dueDate: task.dueDate || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
                        createdAt: task.createdAt,
                        tags: task.tags || [],
                        category: task.category || 'General',
                        recursion: task.recursion,
                        shoppingList: task.shopping_list || task.shoppingList || []
                    }));
                    setMissions(mappedTasks);
                } catch (apiError) {
                    console.warn('Failed to fetch tasks from backend:', apiError);
                    // Show empty missions if API fails
                    setMissions([]);
                }
            } catch (error) {
                console.error('Unexpected error in fetchTasks:', error);
                // Show empty missions on error
                setMissions([]);
            } finally {
                setLoading(false);
            }
        };

        fetchTasks();
    }, [router, isAuthenticated, session, isPending]);

    // Check for mobile on mount and resize
    useEffect(() => {
        const checkMobile = () => {
            const mobile = window.innerWidth < 768;
            setIsMobile(mobile);
        };

        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    // Toggle theme
    const toggleTheme = () => {
        const newTheme = !isDark;
        setIsDark(newTheme);
        localStorage.setItem('theme', newTheme ? 'dark' : 'light');
    };

    // Stats for cards
    const stats = {
        total: missions.length,
        active: missions.filter(m => m.status === 'active').length,
        completed: missions.filter(m => m.status === 'completed').length,
        pending: missions.filter(m => m.status === 'pending').length,
    };

    // Chart data (mock weekly data)
    const chartData = {
        completed: [3, 5, 4, 7, 6, 8, 5],
        active: [2, 3, 4, 2, 5, 3, 4],
        pending: [4, 3, 5, 4, 3, 4, 6],
    };

    // Define fixed system categories
    const systemCategories = [
        'Groceries', 'Office', 'Personal', 'Health', 'Finance', 'Projects', 'Shopping',
        'Maintenance', 'Education', 'Entertainment', 'Travel', 'Utilities'
    ];

    // Extract unique categories from missions
    const uniqueCategories = Array.from(new Set(missions.map(mission => mission.category)));

    // Show only user-created categories from missions, not system categories
    const allCategories = uniqueCategories.sort();

    // Mission tabs with dynamic counts
    const missionTabs: MissionTab[] = [
        { id: 'all', label: 'All Missions', icon: <Target className="w-5 h-5" />, count: missions.length },
        { id: 'active', label: 'Active', icon: <Clock className="w-5 h-5" />, count: stats.active },
        { id: 'pending', label: 'Pending', icon: <AlertTriangle className="w-5 h-5" />, count: stats.pending },
        { id: 'completed', label: 'Completed', icon: <CheckCircle className="w-5 h-5" />, count: stats.completed },
        { id: 'starred', label: 'Priority', icon: <Star className="w-5 h-5" />, count: missions.filter(m => m.priority === 'critical' || m.priority === 'high').length },
        { id: 'history', label: 'History', icon: <History className="w-5 h-5" />, count: 0 },
        { id: 'recursion', label: 'Recursion', icon: <Repeat className="w-5 h-5" />, count: 0 },
        { id: 'chatbot', label: 'AI Assistant', icon: <MessageSquare className="w-5 h-5" />, count: 0 },
    ];

    // Filter missions
    const filteredMissions = missions.filter((mission) => {
        if (activeTab !== 'all' && activeTab !== 'chatbot') {
            if (activeTab === 'starred') {
                if (mission.priority !== 'critical' && mission.priority !== 'high') return false;
            } else if (mission.status !== activeTab) {
                return false;
            }
        }
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            const matchesSearch =
                mission.title.toLowerCase().includes(query) ||
                mission.description.toLowerCase().includes(query) ||
                mission.tags.some(tag => tag.toLowerCase().includes(query)) ||
                mission.category.toLowerCase().includes(query);
            if (!matchesSearch) return false;
        }
        if (selectedPriority !== 'all' && mission.priority !== selectedPriority) return false;
        if (selectedStatus !== 'all' && mission.status !== selectedStatus) return false;
        if (selectedCategory !== 'all' && mission.category !== selectedCategory) return false;
        return true;
    });

    // Add new mission
    const handleAddMission = useCallback(async (missionData: Omit<Mission, 'id' | 'createdAt'>) => {
        try {
            // Get user info from session
            const userId = getUserId(session);
            const userEmail = session?.user?.email;
            const userName = session?.user?.name;

            // Create task in backend with all fields
            try {
                const task = await api.tasks.create({
                    title: missionData.title,
                    description: missionData.description,
                    priority: missionData.priority,
                    status: missionData.status,
                    dueDate: missionData.dueDate,
                    recursion: missionData.recursion,
                    category: missionData.category,
                    tags: missionData.tags,
                    shopping_list: missionData.shoppingList || [],
                    userId: userId,
                    userEmail: userEmail,
                    userName: userName
                });

                // Add to local state
                const newMission: Mission = {
                    ...missionData,
                    id: task.id.toString(),
                    createdAt: (task as any).createdAt || new Date().toISOString(),
                };
                setMissions(prev => [newMission, ...prev]);
                setShowAddModal(false);
            } catch (apiError) {
                console.warn('Failed to create task in backend, using local storage:', apiError);

                // Generate a local ID for the new task
                const localId = `local-${Date.now()}`;

                // Add to local state with local ID
                const newMission: Mission = {
                    ...missionData,
                    id: localId,
                    createdAt: new Date().toISOString(),
                };
                setMissions(prev => [newMission, ...prev]);
                setShowAddModal(false);

                // Silently save locally - no need to alert user
                console.log('Task saved locally due to API error');
            }
        } catch (error) {
            console.error('Failed to create task - Full error:', error);

            // Show more specific error message
            let errorMessage = 'Failed to create task. ';

            if (error instanceof Error) {
                if (error.message.includes('401') || error.message.includes('Unauthorized')) {
                    errorMessage += 'Please login first.';
                    // Redirect to login after a short delay
                    setTimeout(() => router.push('/auth'), 2000);
                } else if (error.message.includes('403')) {
                    errorMessage += 'You do not have permission.';
                } else if (error.message.includes('Network')) {
                    errorMessage += 'Network error. Check if backend is running.';
                } else {
                    errorMessage += error.message;
                }
            } else {
                errorMessage += 'Please try again.';
            }

            alert(errorMessage);
        }
    }, [router, session]);

    // Delete mission (move to trash)
    const handleDeleteMission = useCallback(async (id: string) => {
        try {
            // Check if this is a local-only task (never saved to backend)
            const isLocalOnly = id.startsWith('local-');

            if (isLocalOnly) {
                // For local-only tasks, just remove from state
                setMissions(prev => prev.filter(m => m.id !== id));
                if (selectedMission && selectedMission.id === id) {
                    setSelectedMission(null);
                }
                return;
            }

            const userId = getUserId(session);

            // Try to delete from backend (only for server-synced tasks)
            try {
                await api.tasks.delete(id, userId);

                setMissions(prev => prev.filter(m => m.id !== id));

                // If the deleted mission was the selected one, close the detail view
                if (selectedMission && selectedMission.id === id) {
                    setSelectedMission(null);
                }
            } catch (apiError) {
                console.warn('Failed to delete task in backend, removing locally:', apiError);

                // Remove locally anyway
                setMissions(prev => prev.filter(m => m.id !== id));

                // If the deleted mission was the selected one, close the detail view
                if (selectedMission && selectedMission.id === id) {
                    setSelectedMission(null);
                }

                // Silently remove locally - no need to alert user
                console.log('Task removed locally due to API error');
            }
        } catch (error) {
            console.error('Failed to delete task:', error);
            alert('Failed to delete task. Please try again.');
        }
    }, [session, selectedMission]);

    // Edit mission
    const handleEditMission = useCallback((mission: Mission) => {
        setEditingMission(mission);
        setShowEditModal(true);
    }, []);

    // Handle mission selection to show details
    const handleMissionClick = useCallback((mission: Mission) => {
        // Set the selected mission to show its details
        setSelectedMission(mission);
    }, []);

    // Save edited mission
    const handleSaveEdit = useCallback(async (updatedMission: Omit<Mission, 'id' | 'createdAt'>) => {
        if (!editingMission) return;

        try {
            // Check if this is a local-only task
            const isLocalOnly = editingMission.id.startsWith('local-');

            if (isLocalOnly) {
                // For local-only tasks, just update state
                setMissions(prev => prev.map(m =>
                    m.id === editingMission.id
                        ? { ...m, ...updatedMission }
                        : m
                ));
                setShowEditModal(false);
                setEditingMission(null);
                return;
            }

            const userId = getUserId(session);

            // Try to update in backend (only for server-synced tasks)
            try {
                // Ensure all required fields are present
                const taskUpdateData = {
                    title: updatedMission.title || editingMission.title,
                    description: updatedMission.description || editingMission.description || '',
                    status: updatedMission.status || editingMission.status,
                    priority: updatedMission.priority || editingMission.priority,
                    dueDate: updatedMission.dueDate || editingMission.dueDate,
                    recursion: updatedMission.recursion,
                    category: updatedMission.category || editingMission.category,
                    tags: updatedMission.tags || editingMission.tags || [],
                    shoppingList: updatedMission.shoppingList || editingMission.shoppingList || [], // Include shopping list data
                };

                await api.tasks.update(editingMission.id, taskUpdateData, userId);

                setMissions(prev => prev.map(m =>
                    m.id === editingMission.id
                        ? { ...m, ...updatedMission }
                        : m
                ));
                setShowEditModal(false);
                setEditingMission(null);
            } catch (apiError) {
                console.warn('Failed to update task in backend, updating locally:', apiError);

                // Update locally anyway
                setMissions(prev => prev.map(m =>
                    m.id === editingMission.id
                        ? { ...m, ...updatedMission }
                        : m
                ));
                setShowEditModal(false);
                setEditingMission(null);

                // Silently save locally - no need to alert user
                console.log('Changes saved locally due to API error');
            }
        } catch (error) {
            console.error('Failed to update task:', error);
            alert('Failed to update task. Please try again.');
        }
    }, [editingMission, session]);

    // Toggle mission completion
    const handleToggleComplete = useCallback(async (id: string) => {
        try {
            const mission = missions.find(m => m.id === id);
            if (!mission) return;

            const newStatus = mission.status === 'completed' ? 'pending' : 'completed';
            const isLocalOnly = id.startsWith('local-');

            if (isLocalOnly) {
                // For local-only tasks, just update state
                setMissions(prev => prev.map(m =>
                    m.id === id
                        ? { ...m, status: newStatus }
                        : m
                ));
                return;
            }

            const userId = getUserId(session);

            // Try to update in backend (only for server-synced tasks)
            try {
                // Ensure all required fields are sent to prevent validation errors
                const taskUpdateData = {
                    title: mission.title,
                    description: mission.description || '',
                    status: newStatus,
                    priority: mission.priority,
                    dueDate: mission.dueDate,
                    recursion: mission.recursion,
                    category: mission.category,
                    tags: mission.tags || [],
                    shoppingList: mission.shoppingList || [], // Include shopping list data
                };

                await api.tasks.update(id, taskUpdateData, userId);

                setMissions(prev => prev.map(m =>
                    m.id === id
                        ? { ...m, status: newStatus }
                        : m
                ));
            } catch (apiError) {
                console.warn('Failed to update task in backend, updating locally:', apiError);

                // Update locally anyway
                setMissions(prev => prev.map(m =>
                    m.id === id
                        ? { ...m, status: newStatus }
                        : m
                ));

                // Silently save locally - no need to alert user
                console.log('Changes saved locally due to API error');
            }
        } catch (error) {
            console.error('Failed to update task:', error);
            alert('Failed to update task. Please try again.');
        }
    }, [missions, session]);

    // Add or update item in shopping list
    const addItemToShoppingList = (categoryName: string) => {
        if (!newItemName.trim() || newItemPrice < 0) return;

        const newItem: Item = {
            id: editingItemId || Date.now().toString(),
            name: newItemName,
            price: newItemPrice,
            quantity: newItemQuantity,
            completed: editingItemId ? (missions
                .find(m => m.id === editingItemMissionId)?.shoppingList
                ?.find(c => c.id === editingItemCategoryId)?.items
                ?.find(i => i.id === editingItemId)?.completed || false) : false
        };

        setMissions(prevMissions => {
            // Find missions in the selected category
            const categoryMissions = prevMissions.filter(m => m.category === categoryName);

            if (categoryMissions.length === 0 && !editingItemId) {
                // If no mission exists in this category, create one
                const newMission: Mission = {
                    id: Date.now().toString(),
                    title: `${categoryName} Shopping List`,
                    description: `Shopping list for ${categoryName}`,
                    priority: 'medium',
                    status: 'active',
                    dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    createdAt: new Date().toISOString(),
                    tags: ['shopping'],
                    category: categoryName,
                    shoppingList: [{
                        id: Date.now().toString(),
                        name: categoryName,
                        items: [newItem]
                    }]
                };

                return [newMission, ...prevMissions];
            } else {
                // Update existing missions in the category or edit existing item
                return prevMissions.map(mission => {
                    if (mission.category === categoryName || mission.id === editingItemMissionId) {
                        let updatedShoppingList = [...(mission.shoppingList || [])];

                        if (editingItemId && editingItemCategoryId) {
                            // Editing existing item
                            updatedShoppingList = updatedShoppingList.map(category => {
                                if (category.id === editingItemCategoryId) {
                                    const updatedItems = category.items.map(item => {
                                        if (item.id === editingItemId) {
                                            return newItem;
                                        }
                                        return item;
                                    });
                                    return { ...category, items: updatedItems };
                                }
                                return category;
                            });
                        } else {
                            // Adding new item
                            // Find if there's already a category with this name
                            const categoryIndex = updatedShoppingList.findIndex(cat => cat.name === categoryName);

                            if (categoryIndex !== -1) {
                                // Add item to existing category
                                updatedShoppingList[categoryIndex] = {
                                    ...updatedShoppingList[categoryIndex],
                                    items: [...updatedShoppingList[categoryIndex].items, newItem]
                                };
                            } else {
                                // Create new category with the item
                                updatedShoppingList.push({
                                    id: Date.now().toString(),
                                    name: categoryName,
                                    items: [newItem]
                                });
                            }
                        }

                        return {
                            ...mission,
                            shoppingList: updatedShoppingList
                        };
                    }
                    return mission;
                });
            }
        });

        // If the selected mission is the one being updated, update the selectedMission state too
        if (selectedMission && selectedMission.id === editingItemMissionId) {
            setSelectedMission(prev => {
                if (!prev || !prev.shoppingList) return prev;

                let updatedShoppingList = [...prev.shoppingList];

                if (editingItemId && editingItemCategoryId) {
                    // Editing existing item
                    updatedShoppingList = updatedShoppingList.map(category => {
                        if (category.id === editingItemCategoryId) {
                            const updatedItems = category.items.map(item => {
                                if (item.id === editingItemId) {
                                    return newItem;
                                }
                                return item;
                            });
                            return { ...category, items: updatedItems };
                        }
                        return category;
                    });
                } else {
                    // Adding new item
                    const categoryIndex = updatedShoppingList.findIndex(cat => cat.name === categoryName);

                    if (categoryIndex !== -1) {
                        // Add item to existing category
                        updatedShoppingList[categoryIndex] = {
                            ...updatedShoppingList[categoryIndex],
                            items: [...updatedShoppingList[categoryIndex].items, newItem]
                        };
                    } else {
                        // Create new category with the item
                        updatedShoppingList.push({
                            id: Date.now().toString(),
                            name: categoryName,
                            items: [newItem]
                        });
                    }
                }

                return {
                    ...prev,
                    shoppingList: updatedShoppingList
                };
            });
        }

        // Save to backend by updating the parent task with updated shopping list
        if (editingItemMissionId) {
            setMissions(prevMissions => {
                const missionToUpdate = prevMissions.find(m => m.id === editingItemMissionId);
                if (missionToUpdate) {
                    const userId = getUserId(session);

                    const taskUpdateData = {
                        title: missionToUpdate.title,
                        description: missionToUpdate.description || '',
                        status: missionToUpdate.status,
                        priority: missionToUpdate.priority,
                        dueDate: missionToUpdate.dueDate,
                        recursion: missionToUpdate.recursion,
                        category: missionToUpdate.category,
                        tags: missionToUpdate.tags || [],
                        shoppingList: missionToUpdate.shoppingList || [], // Use updated shopping list
                    };

                    api.tasks.update(editingItemMissionId, taskUpdateData, userId)
                        .then(() => {
                            console.log('✅ Sub-item saved to database');
                        })
                        .catch(error => {
                            console.error('❌ Failed to save sub-item to backend:', error);
                        });
                }
                return prevMissions;
            });
        }

        // Reset form
        setNewItemName('');
        setNewItemPrice(0);
        setNewItemQuantity(1);
        setEditingItemId(null);
        setEditingItemMissionId(null);
        setEditingItemCategoryId(null);
    };

    // Remove item from shopping list
    const removeItemFromShoppingList = (missionId: string, categoryId: string, itemId: string) => {
        setMissions(prevMissions =>
            prevMissions.map(mission => {
                if (mission.id === missionId && mission.shoppingList) {
                    const updatedShoppingList = mission.shoppingList.map(category => {
                        if (category.id === categoryId) {
                            return {
                                ...category,
                                items: category.items.filter(item => item.id !== itemId)
                            };
                        }
                        return category;
                    }).filter(category => category.items.length > 0); // Remove empty categories

                    return {
                        ...mission,
                        shoppingList: updatedShoppingList
                    };
                }
                return mission;
            })
        );

        // If the selected mission is the one being updated, update the selectedMission state too
        if (selectedMission && selectedMission.id === missionId) {
            setSelectedMission(prev => {
                if (!prev || !prev.shoppingList) return prev;

                const updatedShoppingList = prev.shoppingList.map(category => {
                    if (category.id === categoryId) {
                        return {
                            ...category,
                            items: category.items.filter(item => item.id !== itemId)
                        };
                    }
                    return category;
                }).filter(category => category.items.length > 0); // Remove empty categories

                return {
                    ...prev,
                    shoppingList: updatedShoppingList
                };
            });
        }

        // Sync with backend by updating the parent task with updated shopping list
        setMissions(prevMissions => {
            const missionToUpdate = prevMissions.find(m => m.id === missionId);
            if (missionToUpdate) {
                const userId = getUserId(session);

                const taskUpdateData = {
                    title: missionToUpdate.title,
                    description: missionToUpdate.description || '',
                    status: missionToUpdate.status,
                    priority: missionToUpdate.priority,
                    dueDate: missionToUpdate.dueDate,
                    recursion: missionToUpdate.recursion,
                    category: missionToUpdate.category,
                    tags: missionToUpdate.tags || [],
                    shoppingList: missionToUpdate.shoppingList || [], // Use updated shopping list (item removed)
                };

                api.tasks.update(missionId, taskUpdateData, userId)
                    .then(() => {
                        console.log('✅ Sub-item deletion saved to database');
                    })
                    .catch(error => {
                        console.error('❌ Failed to save sub-item deletion to backend:', error);
                    });
            }
            return prevMissions;
        });
    };

    // Calculate total cost for a category
    const calculateCategoryTotal = (items: Item[]) => {
        return items.reduce((total, item) => total + (item.price * item.quantity), 0);
    };

    // Edit item in shopping list
    const editItemInShoppingList = (missionId: string, categoryId: string, itemId: string, updates: Partial<Item>) => {
        setMissions(prevMissions =>
            prevMissions.map(mission => {
                if (mission.id === missionId && mission.shoppingList) {
                    const updatedShoppingList = mission.shoppingList.map(category => {
                        if (category.id === categoryId) {
                            const updatedItems = category.items.map(item => {
                                if (item.id === itemId) {
                                    return { ...item, ...updates };
                                }
                                return item;
                            });

                            return {
                                ...category,
                                items: updatedItems
                            };
                        }
                        return category;
                    });

                    return {
                        ...mission,
                        shoppingList: updatedShoppingList
                    };
                }
                return mission;
            })
        );

        // If the selected mission is the one being updated, update the selectedMission state too
        if (selectedMission && selectedMission.id === missionId) {
            setSelectedMission(prev => {
                if (!prev || !prev.shoppingList) return prev;

                const updatedShoppingList = prev.shoppingList.map(category => {
                    if (category.id === categoryId) {
                        const updatedItems = category.items.map(item => {
                            if (item.id === itemId) {
                                return { ...item, ...updates };
                            }
                            return item;
                        });

                        return {
                            ...category,
                            items: updatedItems
                        };
                    }
                    return category;
                });

                return {
                    ...prev,
                    shoppingList: updatedShoppingList
                };
            });
        }

        // Sync with backend by updating the parent task with updated shopping list
        setMissions(prevMissions => {
            const missionToUpdate = prevMissions.find(m => m.id === missionId);
            if (missionToUpdate) {
                const userId = getUserId(session);

                const taskUpdateData = {
                    title: missionToUpdate.title,
                    description: missionToUpdate.description || '',
                    status: missionToUpdate.status,
                    priority: missionToUpdate.priority,
                    dueDate: missionToUpdate.dueDate,
                    recursion: missionToUpdate.recursion,
                    category: missionToUpdate.category,
                    tags: missionToUpdate.tags || [],
                    shoppingList: missionToUpdate.shoppingList || [], // Use updated shopping list (item edited)
                };

                api.tasks.update(missionId, taskUpdateData, userId)
                    .then(() => {
                        console.log('✅ Sub-item edit saved to database');
                    })
                    .catch(error => {
                        console.error('❌ Failed to save sub-item edit to backend:', error);
                    });
            }
            return prevMissions;
        });
    };

    // Toggle item completion status
    const toggleItemCompletion = (missionId: string, categoryId: string, itemId: string) => {
        setMissions(prevMissions =>
            prevMissions.map(mission => {
                if (mission.id === missionId && mission.shoppingList) {
                    const updatedShoppingList = mission.shoppingList.map(category => {
                        if (category.id === categoryId) {
                            const updatedItems = category.items.map(item => {
                                if (item.id === itemId) {
                                    return {
                                        ...item,
                                        completed: !item.completed
                                    };
                                }
                                return item;
                            });

                            return {
                                ...category,
                                items: updatedItems
                            };
                        }
                        return category;
                    });

                    return {
                        ...mission,
                        shoppingList: updatedShoppingList
                    };
                }
                return mission;
            })
        );

        // If the selected mission is the one being updated, update the selectedMission state too
        if (selectedMission && selectedMission.id === missionId) {
            setSelectedMission(prev => {
                if (!prev || !prev.shoppingList) return prev;

                const updatedShoppingList = prev.shoppingList.map(category => {
                    if (category.id === categoryId) {
                        const updatedItems = category.items.map(item => {
                            if (item.id === itemId) {
                                return {
                                    ...item,
                                    completed: !item.completed
                                };
                            }
                            return item;
                        });

                        return {
                            ...category,
                            items: updatedItems
                        };
                    }
                    return category;
                });

                return {
                    ...prev,
                    shoppingList: updatedShoppingList
                };
            });
        }

        // Sync with backend by updating the parent task with updated shopping list
        setMissions(prevMissions => {
            const missionToUpdate = prevMissions.find(m => m.id === missionId);
            if (missionToUpdate) {
                const userId = getUserId(session);

                const taskUpdateData = {
                    title: missionToUpdate.title,
                    description: missionToUpdate.description || '',
                    status: missionToUpdate.status,
                    priority: missionToUpdate.priority,
                    dueDate: missionToUpdate.dueDate,
                    recursion: missionToUpdate.recursion,
                    category: missionToUpdate.category,
                    tags: missionToUpdate.tags || [],
                    shoppingList: missionToUpdate.shoppingList || [], // Use updated shopping list (item toggled)
                };

                api.tasks.update(missionId, taskUpdateData, userId)
                    .then(() => {
                        console.log('✅ Sub-item completion status saved to database');
                    })
                    .catch(error => {
                        console.error('❌ Failed to save sub-item completion to backend:', error);
                    });
            }
            return prevMissions;
        });
    };

    // Voice command handler - FIXED to properly add tasks
    const handleVoiceCommand = useCallback((command: string): boolean => {
        const lowerCommand = command.toLowerCase().trim();
        console.log('Voice command received:', lowerCommand);

        // Add task patterns - improved matching
        const addPatterns = [
            /^add\s+(.+)/i,
            /^create\s+(.+)/i,
            /^new\s+(?:task|mission)?\s*(.+)/i,
            /^make\s+(.+)/i,
        ];

        for (const pattern of addPatterns) {
            const match = lowerCommand.match(pattern);
            if (match) {
                let title = match[1].trim();
                // Remove common words
                title = title.replace(/^(a\s+)?(task|mission)\s+(called|named|titled)?\s*/i, '').trim();
                if (!title) title = command;

                console.log('Adding mission with title:', title);
                handleAddMission({
                    title: title.charAt(0).toUpperCase() + title.slice(1),
                    description: 'Created via voice command',
                    priority: 'medium',
                    status: 'pending',
                    dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                    category: 'Voice Created',
                    tags: ['voice'],
                });
                return true;
            }
        }

        // Filter patterns
        if (lowerCommand.includes('show') || lowerCommand.includes('filter')) {
            if (lowerCommand.includes('all')) {
                setActiveTab('all');
                setSelectedPriority('all');
                setSelectedStatus('all');
                setSelectedCategory('all');
                return true;
            }
            if (lowerCommand.includes('active')) { setActiveTab('active'); return true; }
            if (lowerCommand.includes('pending')) { setActiveTab('pending'); return true; }
            if (lowerCommand.includes('completed') || lowerCommand.includes('done')) { setActiveTab('completed'); return true; }
            if (lowerCommand.includes('critical') || lowerCommand.includes('high priority')) { setSelectedPriority('critical'); return true; }
        }

        return false;
    }, [handleAddMission]);

    // Pre-defined particle data (static to avoid impure function calls during render)
    const particleData = [
        { id: 0, initialX: 100, initialY: 50, animateY: -150, duration: 8, delay: 0.5 },
        { id: 1, initialX: 200, initialY: 150, animateY: -180, duration: 10, delay: 1 },
        { id: 2, initialX: 350, initialY: 80, animateY: -120, duration: 7, delay: 2 },
        { id: 3, initialX: 500, initialY: 200, animateY: -200, duration: 12, delay: 0 },
        { id: 4, initialX: 650, initialY: 120, animateY: -160, duration: 9, delay: 3 },
        { id: 5, initialX: 800, initialY: 60, animateY: -140, duration: 11, delay: 1.5 },
        { id: 6, initialX: 900, initialY: 180, animateY: -190, duration: 8, delay: 2.5 },
        { id: 7, initialX: 150, initialY: 300, animateY: -170, duration: 10, delay: 4 },
        { id: 8, initialX: 400, initialY: 350, animateY: -130, duration: 6, delay: 0.8 },
        { id: 9, initialX: 600, initialY: 400, animateY: -210, duration: 13, delay: 1.2 },
        { id: 10, initialX: 750, initialY: 280, animateY: -145, duration: 9, delay: 3.5 },
        { id: 11, initialX: 50, initialY: 450, animateY: -185, duration: 11, delay: 2.2 },
        { id: 12, initialX: 300, initialY: 500, animateY: -155, duration: 7, delay: 4.5 },
        { id: 13, initialX: 550, initialY: 550, animateY: -175, duration: 10, delay: 0.3 },
        { id: 14, initialX: 850, initialY: 480, animateY: -195, duration: 8, delay: 1.8 },
    ];

    return (
        <div className={`min-h-screen transition-colors duration-500 relative overflow-hidden ${isDark ? 'bg-gray-950 text-white' : 'bg-gradient-to-br from-sky-50 via-indigo-50 to-purple-50 text-gray-900'}`}>

            {/* Enhanced Framer Motion Background */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                {/* Animated gradient orbs */}
                <motion.div
                    animate={{
                        x: [0, 100, -50, 0],
                        y: [0, -100, 50, 0],
                        scale: [1, 1.2, 0.9, 1],
                    }}
                    transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
                    className={`absolute -top-40 -left-40 w-80 h-80 rounded-full blur-3xl ${isDark ? 'bg-cyan-500/20' : 'bg-cyan-300/30'}`}
                />
                <motion.div
                    animate={{
                        x: [0, -100, 80, 0],
                        y: [0, 50, -100, 0],
                        scale: [1, 0.8, 1.1, 1],
                    }}
                    transition={{ duration: 25, repeat: Infinity, ease: "easeInOut" }}
                    className={`absolute -top-20 -right-40 w-96 h-96 rounded-full blur-3xl ${isDark ? 'bg-purple-500/20' : 'bg-purple-300/30'}`}
                />
                <motion.div
                    animate={{
                        x: [0, 80, -80, 0],
                        y: [0, -50, 100, 0],
                        scale: [1, 1.1, 0.9, 1],
                    }}
                    transition={{ duration: 18, repeat: Infinity, ease: "easeInOut" }}
                    className={`absolute -bottom-40 left-1/4 w-72 h-72 rounded-full blur-3xl ${isDark ? 'bg-blue-500/15' : 'bg-blue-300/30'}`}
                />
                <motion.div
                    animate={{
                        x: [0, -60, 60, 0],
                        y: [0, 80, -80, 0],
                        scale: [1, 0.9, 1.2, 1],
                    }}
                    transition={{ duration: 22, repeat: Infinity, ease: "easeInOut" }}
                    className={`absolute -bottom-20 -right-20 w-64 h-64 rounded-full blur-3xl ${isDark ? 'bg-violet-500/20' : 'bg-violet-300/30'}`}
                />

                {/* Floating particles */}
                {particleData.map((particle) => (
                    <motion.div
                        key={particle.id}
                        initial={{
                            x: particle.initialX,
                            y: particle.initialY,
                        }}
                        animate={{
                            y: [null, particle.animateY],
                            opacity: [0, 0.6, 0],
                        }}
                        transition={{
                            duration: particle.duration,
                            repeat: Infinity,
                            delay: particle.delay,
                        }}
                        className={`absolute w-1 h-1 rounded-full ${isDark ? 'bg-cyan-400' : 'bg-purple-400'}`}
                    />
                ))}
            </div>

            {/* Particles Background for dark mode */}
            {isDark && <ParticlesBackground />}

            <div className="relative z-10 flex flex-col md:flex-row">
                {/* Mobile Header with Menu Toggle */}
                <div className={`md:hidden fixed top-0 left-0 right-0 z-50 flex items-center justify-between p-4 backdrop-blur-xl border-b
                    ${isDark ? 'bg-gray-900/95 border-cyan-500/30' : 'bg-white/95 border-sky-200'}`}>
                    <button
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                        className={`p-2 rounded-lg ${isDark ? 'text-cyan-400 hover:bg-gray-800' : 'text-cyan-600 hover:bg-gray-100'}`}
                    >
                        <Menu className="w-6 h-6" />
                    </button>
                    <h1 className={`text-lg font-bold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                        Mission Control
                    </h1>
                    <button
                        onClick={() => {/* Notifications handler */}}
                        className={`relative p-2 rounded-lg ${isDark ? 'text-cyan-400 hover:bg-gray-800' : 'text-cyan-600 hover:bg-gray-100'}`}
                    >
                        <Bell className="w-5 h-5" />
                        <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                    </button>
                </div>

                {/* Mobile Overlay */}
                {sidebarOpen && (
                    <div
                        className="md:hidden fixed inset-0 bg-black/50 z-40"
                        onClick={() => setSidebarOpen(false)}
                    />
                )}

                {/* Sidebar - Hidden on mobile, visible on desktop - FIXED POSITIONING */}
                <aside
                    className={`fixed top-0 left-0 w-72 backdrop-blur-xl border-r flex flex-col h-screen z-50 transition-transform duration-300
                        ${isDark ? 'bg-gray-900/95 border-cyan-500/30' : 'bg-white/95 border-sky-200'}
                        ${isMobile ? (sidebarOpen ? 'translate-x-0' : '-translate-x-full') : 'translate-x-0'}`}
                >
                    {/* Sidebar Header with User Profile */}
                    <div className={`p-4 border-b ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
                        {/* Mobile Close Button */}
                        {isMobile && (
                            <button
                                onClick={() => setSidebarOpen(false)}
                                className={`absolute top-4 right-4 p-2 rounded-lg ${isDark ? 'text-gray-400 hover:text-white hover:bg-gray-800' : 'text-gray-500 hover:text-gray-800 hover:bg-gray-100'}`}
                            >
                                <X className="w-5 h-5" />
                            </button>
                        )}
                        {/* User Profile Section */}
                        <div className="flex items-center gap-3 mb-4">
                            {session?.user?.image ? (
                                <img
                                    src={session.user.image}
                                    alt="Profile"
                                    className="w-10 h-10 rounded-full border-2 border-cyan-500 object-cover"
                                />
                            ) : (
                                <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-lg
                                    ${isDark ? 'bg-gradient-to-br from-cyan-500 to-blue-600' : 'bg-gradient-to-br from-cyan-400 to-blue-500'}`}>
                                    {session?.user?.name?.[0]?.toUpperCase() || session?.user?.email?.[0]?.toUpperCase() || '?'}
                                </div>
                            )}
                            <div className="flex-1 min-w-0">
                                <p className={`text-sm font-semibold truncate ${isDark ? 'text-white' : 'text-gray-800'}`}>
                                    {session?.user?.name || 'User'}
                                </p>
                                <p className={`text-xs truncate ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                                    {session?.user?.email || ''}
                                </p>
                            </div>
                        </div>



                        {/* App Title */}
                        <h1 className={`text-xl font-bold ${isDark ? 'text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500' : 'text-cyan-600'}`}>
                            <Target className="inline w-5 h-5 mr-2" />
                            Mission Control
                        </h1>
                    </div>

                    {/* Mission Tabs */}
                    <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                        {missionTabs.map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all duration-200 ${activeTab === tab.id
                                    ? isDark
                                        ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/50'
                                        : 'bg-cyan-100 text-cyan-700 border border-cyan-300'
                                    : isDark
                                        ? 'text-gray-400 hover:bg-gray-800 hover:text-white'
                                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-800'
                                    }`}
                            >
                                <div className="flex items-center gap-3">
                                    {tab.icon}
                                    <span className="font-medium">{tab.label}</span>
                                </div>
                                <span className={`px-2 py-0.5 text-xs rounded-full ${activeTab === tab.id
                                    ? isDark ? 'bg-cyan-500/30' : 'bg-cyan-200'
                                    : isDark ? 'bg-gray-700' : 'bg-gray-200'
                                    }`}>
                                    {tab.count}
                                </span>
                            </button>
                        ))}
                    </nav>

                    {/* Stats */}
                    <div className={`p-4 border-t ${isDark ? 'border-gray-700' : 'border-gray-200'}`}>
                        <div className="grid grid-cols-2 gap-3">
                            <div className={`rounded-lg p-3 text-center ${isDark ? 'bg-gray-800/50' : 'bg-gray-100'}`}>
                                <p className={`text-2xl font-bold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>{missions.length}</p>
                                <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Total</p>
                            </div>
                            <div className={`rounded-lg p-3 text-center ${isDark ? 'bg-gray-800/50' : 'bg-gray-100'}`}>
                                <p className={`text-2xl font-bold ${isDark ? 'text-green-400' : 'text-green-600'}`}>{stats.completed}</p>
                                <p className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Done</p>
                            </div>
                        </div>
                    </div>
                    {/* Logout Button */}
                    <button
                        onClick={async () => {
                            await signOut();
                            router.push('/');
                        }}
                        className={`w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg transition-all
                                ${isDark
                                ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30 border border-red-500/50'
                                : 'bg-red-100 text-red-600 hover:bg-red-200 border border-red-300'}`}
                    >
                        <LogOut className="w-4 h-4" />
                        <span className="text-sm font-medium">Session Dismissed</span>
                    </button>
                </aside>

                {/* Main Content */}
                <main className={`flex-1 flex flex-col min-h-screen overflow-hidden ${isMobile ? 'pt-16' : 'md:ml-72 md:pt-0'}`}>
                    {/* Top Bar - Hidden on mobile since we have mobile header */}
                    <header className={`hidden md:block backdrop-blur-xl border-b px-4 md:px-6 py-4
                        ${isDark ? 'bg-gray-900/60 border-gray-700' : 'bg-white/60 border-gray-200'}`}>
                        <div className="flex items-center justify-between gap-4">
                            {/* Search Bar */}
                            <div className="flex-1 max-w-xl relative">
                                <Search className={`absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 ${isDark ? 'text-gray-400' : 'text-gray-500'}`} />
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder="Search missions..."
                                    className={`w-full border rounded-xl pl-12 pr-4 py-3 focus:outline-none focus:ring-1 transition-all duration-200
                                        ${isDark
                                            ? 'bg-gray-800/80 border-gray-600 text-white placeholder-gray-400 focus:border-cyan-400 focus:ring-cyan-400/50'
                                            : 'bg-white border-gray-300 text-gray-800 placeholder-gray-400 focus:border-cyan-500 focus:ring-cyan-500/50'}`}
                                />
                            </div>

                            {/* Actions */}
                            <div className="flex items-center gap-3">
                                {/* Notifications Bell Icon */}
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => {
                                        // TODO: Add notification panel logic
                                        alert('Notifications feature - coming soon!')
                                    }}
                                    className={`relative p-3 rounded-lg transition-all ${isDark ? 'bg-gray-800 text-gray-400 hover:text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                                >
                                    <Bell className="w-5 h-5" />
                                    {/* Notification badge - example for unread count */}
                                    <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center font-bold">
                                        3
                                    </span>
                                </motion.button>

                                {/* Theme Toggle */}
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={toggleTheme}
                                    className={`p-3 rounded-lg transition-all ${isDark ? 'bg-gray-800 text-yellow-400 hover:bg-gray-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                                >
                                    {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                                </motion.button>

                                {/* Filter Toggle */}
                                <button
                                    onClick={() => setShowFilters(!showFilters)}
                                    className={`p-3 rounded-lg transition-all ${showFilters
                                        ? 'bg-cyan-500/20 text-cyan-400'
                                        : isDark ? 'bg-gray-800 text-gray-400 hover:text-white' : 'bg-gray-100 text-gray-500 hover:text-gray-800'
                                        }`}
                                >
                                    <Filter className="w-5 h-5" />
                                </button>

                                {/* Voice Command */}
                                <VoiceCommandButton onCommand={handleVoiceCommand} />

                                {/* Add Mission */}
                                <button
                                    onClick={() => setShowAddModal(true)}
                                    className="flex items-center gap-2 px-4 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 
                                             text-white font-semibold rounded-lg hover:from-cyan-400 hover:to-blue-500
                                             transition-all duration-200 shadow-lg shadow-cyan-500/25"
                                >
                                    <Plus className="w-5 h-5" />
                                    <span className="hidden sm:inline">New Mission</span>
                                </button>
                            </div>
                        </div>

                        {/* Filter Panel */}
                        <AnimatePresence>
                            {showFilters && (
                                <motion.div
                                    initial={{ height: 0, opacity: 0 }}
                                    animate={{ height: 'auto', opacity: 1 }}
                                    exit={{ height: 0, opacity: 0 }}
                                    className={`mt-4 pt-4 border-t overflow-hidden ${isDark ? 'border-gray-700' : 'border-gray-200'}`}
                                >
                                    <div className="flex flex-wrap gap-4">
                                        <div className="flex items-center gap-2">
                                            <label className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Priority:</label>
                                            <select
                                                value={selectedPriority}
                                                onChange={(e) => setSelectedPriority(e.target.value)}
                                                className={`border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-cyan-400
                                                    ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'}`}
                                            >
                                                <option value="all">All</option>
                                                <option value="critical">Critical</option>
                                                <option value="high">High</option>
                                                <option value="medium">Medium</option>
                                                <option value="low">Low</option>
                                            </select>
                                        </div>

                                        <div className="flex items-center gap-2">
                                            <label className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>Status:</label>
                                            <select
                                                value={selectedStatus}
                                                onChange={(e) => setSelectedStatus(e.target.value)}
                                                className={`border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-cyan-400
                                                    ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-white border-gray-300 text-gray-800'}`}
                                            >
                                                <option value="all">All</option>
                                                <option value="pending">Pending</option>
                                                <option value="active">Active</option>
                                                <option value="completed">Completed</option>
                                            </select>
                                        </div>

                                        <button
                                            onClick={() => {
                                                setSelectedPriority('all');
                                                setSelectedStatus('all');
                                                setSearchQuery('');
                                            }}
                                            className={`text-sm transition-colors ${isDark ? 'text-cyan-400 hover:text-cyan-300' : 'text-cyan-600 hover:text-cyan-500'}`}
                                        >
                                            Clear Filters
                                        </button>
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </header>

                    {/* Dashboard Content */}
                    <div className="flex-1 overflow-y-auto p-4 md:p-6">
                        {/* Mobile Search and Actions Bar */}
                        <div className="md:hidden mb-4 space-y-3">
                            <div className="relative">
                                <Search className={`absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 ${isDark ? 'text-gray-400' : 'text-gray-500'}`} />
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder="Search missions..."
                                    className={`w-full border rounded-xl pl-12 pr-4 py-3 focus:outline-none focus:ring-1 transition-all duration-200
                                        ${isDark
                                            ? 'bg-gray-800/80 border-gray-600 text-white placeholder-gray-400 focus:border-cyan-400 focus:ring-cyan-400/50'
                                            : 'bg-white border-gray-300 text-gray-800 placeholder-gray-400 focus:border-cyan-500 focus:ring-cyan-500/50'}`}
                                />
                            </div>
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => setShowFilters(!showFilters)}
                                    className={`flex-1 flex items-center justify-center gap-2 p-3 rounded-xl transition-all
                                        ${showFilters
                                            ? 'bg-cyan-500/20 text-cyan-400'
                                            : isDark ? 'bg-gray-800 text-gray-400' : 'bg-gray-100 text-gray-600'}`}
                                >
                                    <Filter className="w-4 h-4" />
                                    <span className="text-sm">Filters</span>
                                </button>
                                <VoiceCommandButton onCommand={handleVoiceCommand} />
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => setShowAddModal(true)}
                                    className="flex-1 flex items-center justify-center gap-2 p-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 text-white"
                                >
                                    <Plus className="w-4 h-4" />
                                    <span className="text-sm">Add</span>
                                </motion.button>
                            </div>
                        </div>

                        {/* Authentication Warning Banner */}
                        {!isAuthenticated && (
                            <motion.div
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`mb-6 p-6 rounded-2xl border-2 shadow-xl ${isDark ? 'bg-gradient-to-r from-orange-500/20 to-red-500/20 border-orange-500/50 text-orange-300' : 'bg-gradient-to-r from-orange-50 to-red-50 border-orange-300 text-orange-800'}`}
                            >
                                <div className="flex items-start justify-between gap-4">
                                    <div className="flex items-start gap-3 flex-1">
                                        <AlertTriangle className="w-6 h-6 flex-shrink-0 mt-1" />
                                        <div>
                                            <h3 className="font-bold text-lg mb-1">Authentication Required</h3>
                                            <p className="text-sm opacity-90 mb-3">
                                                You need to login or create an account to save and sync your tasks across devices.
                                            </p>
                                            <div className="flex gap-3">
                                                <button
                                                    onClick={() => router.push('/auth?mode=signin')}
                                                    className={`px-6 py-2 rounded-lg font-semibold transition-all shadow-lg ${isDark ? 'bg-orange-500 hover:bg-orange-600 text-white' : 'bg-orange-600 hover:bg-orange-700 text-white'}`}
                                                >
                                                    Login
                                                </button>
                                                <button
                                                    onClick={() => router.push('/auth?mode=signup')}
                                                    className={`px-6 py-2 rounded-lg font-semibold border-2 transition-all ${isDark ? 'border-orange-500 text-orange-400 hover:bg-orange-500/20' : 'border-orange-600 text-orange-700 hover:bg-orange-100'}`}
                                                >
                                                    Sign Up
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => {
                                            // User can dismiss the banner temporarily
                                            const banner = document.querySelector('[data-auth-banner]');
                                            if (banner) banner.remove();
                                        }}
                                        className={`p-1 rounded-lg transition-colors ${isDark ? 'hover:bg-orange-500/20' : 'hover:bg-orange-200'}`}
                                        title="Dismiss"
                                    >
                                        <X className="w-5 h-5" />
                                    </button>
                                </div>
                            </motion.div>
                        )}

                        {activeTab === 'chatbot' ? (
                            <div className="h-[calc(100vh-12rem)]">
                                <ChatTab
                                    userId={getUserId(session)}
                                    isDark={isDark}
                                    onTasksUpdated={async () => {
                                        try {
                                            const userId = getUserId(session);
                                            const userEmail = session?.user?.email;
                                            const userName = session?.user?.name;
                                            if (userId) {
                                                const tasks = await api.tasks.list({ userId, userEmail, userName });
                                                const mappedTasks: Mission[] = tasks.map((task: any) => ({
                                                    id: task.id.toString(),
                                                    title: task.title,
                                                    description: task.description || '',
                                                    priority: (task.priority || 'medium') as 'critical' | 'high' | 'medium' | 'low',
                                                    status: (task.status || 'pending') as 'pending' | 'active' | 'completed' | 'failed',
                                                    dueDate: task.dueDate || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
                                                    createdAt: task.createdAt,
                                                    tags: task.tags || [],
                                                    category: task.category || 'General',
                                                    recursion: task.recursion
                                                }));
                                                setMissions(mappedTasks);
                                            }
                                        } catch (error) {
                                            console.error('Failed to refresh tasks:', error);
                                        }
                                    }}
                                />
                            </div>
                        ) : activeTab === 'recursion' ? (
                            <div className="h-[calc(100vh-12rem)]">
                                <RecursionTab isDark={isDark} />
                            </div>
                        ) : (
                            <>
                                {/* Status Cards - Mobile: 2x2 Grid, Desktop: 1x4 Grid */}
                                <div className="mb-6">
                                    <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
                                        <StatusCard
                                            title="Total"
                                            count={stats.total}
                                            icon={Target}
                                            color="cyan"
                                            trend={12}
                                            isDark={isDark}
                                        />
                                        <StatusCard
                                            title="Active"
                                            count={stats.active}
                                            icon={Activity}
                                            color="orange"
                                            trend={8}
                                            isDark={isDark}
                                        />
                                        <StatusCard
                                            title="Completed"
                                            count={stats.completed}
                                            icon={CheckCircle}
                                            color="green"
                                            trend={25}
                                            isDark={isDark}
                                        />
                                        <StatusCard
                                            title="Pending"
                                            count={stats.pending}
                                            icon={Clock}
                                            color="purple"
                                            trend={-5}
                                            isDark={isDark}
                                        />
                                    </div>
                                </div>

                                {/* Category Chips */}
                                <div className="mb-6">
                                    <h3 className={`text-lg font-semibold mb-3 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>Categories</h3>
                                    <div className="flex flex-wrap gap-2">
                                        <button
                                            onClick={() => setSelectedCategory('all')}
                                            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                                                selectedCategory === 'all'
                                                    ? isDark
                                                        ? 'bg-cyan-500 text-white'
                                                        : 'bg-cyan-500 text-white'
                                                    : isDark
                                                        ? 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                            }`}
                                        >
                                            All
                                        </button>
                                        {allCategories.map((category, index) => (
                                            <button
                                                key={index}
                                                onClick={() => setSelectedCategory(category)}
                                                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                                                    selectedCategory === category
                                                        ? isDark
                                                            ? 'bg-cyan-500 text-white'
                                                            : 'bg-cyan-500 text-white'
                                                        : isDark
                                                            ? 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                                                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                                }`}
                                            >
                                                {category}
                                            </button>
                                        ))}
                                    </div>
                                </div>

                                {/* Shopping List for Selected Category */}
                                {selectedCategory !== 'all' && (
                                    <div className={`mb-6 p-4 rounded-xl backdrop-blur-xl border ${isDark ? 'bg-slate-800/40 border-cyan-500/20' : 'bg-white/60 border-sky-200/60'}`}>
                                        <div className="flex justify-between items-center mb-4">
                                            <h3 className={`text-lg font-semibold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                                                {selectedCategory} Items
                                            </h3>
                                            <button
                                                onClick={() => {
                                                    setShoppingListCategory(selectedCategory);
                                                    setShowShoppingList(true);
                                                }}
                                                className="px-3 py-1.5 text-sm bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg hover:from-cyan-400 hover:to-blue-500 transition-all"
                                            >
                                                Add Item
                                            </button>
                                        </div>

                                        {/* Shopping List Items */}
                                        <div className="space-y-2 max-h-60 overflow-y-auto">
                                            {missions
                                                .filter(mission => mission.category === selectedCategory && mission.shoppingList)
                                                .flatMap(mission =>
                                                    mission.shoppingList?.flatMap(category =>
                                                        category.items.map(item => ({ ...item, missionId: mission.id, categoryId: category.id, missionTitle: mission.title }))
                                                    ) || []
                                                )
                                                .map((item, index) => (
                                                    <div
                                                        key={item.id}
                                                        className={`flex justify-between items-center p-2 rounded border bg-opacity-50 ${
                                                            item.completed
                                                                ? (isDark ? 'bg-gray-700/30 border-gray-600' : 'bg-gray-200/30 border-gray-300')
                                                                : (isDark ? 'border-gray-600' : 'border-gray-300')
                                                        }`}
                                                    >
                                                        <div className="flex items-center gap-2 flex-1">
                                                            <input
                                                                type="checkbox"
                                                                checked={!!item.completed}
                                                                onChange={() => toggleItemCompletion(item.missionId, item.categoryId, item.id)}
                                                                className="w-4 h-4 rounded"
                                                                style={{
                                                                    accentColor: isDark ? '#22d3ee' : '#0891b2'
                                                                }}
                                                            />
                                                            <span className={`${item.completed ? 'line-through opacity-60' : ''} ${isDark ? 'text-white' : 'text-gray-800'}`}>
                                                                {item.name}
                                                            </span>
                                                            <span className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                                                                (x{item.quantity})
                                                            </span>
                                                        </div>
                                                        <div className="flex items-center gap-2">
                                                            <span className={`${isDark ? 'text-green-400' : 'text-green-600'}`}>
                                                                ${(item.price * item.quantity).toFixed(2)}
                                                            </span>
                                                            <button
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    // Set up editing state
                                                                    setNewItemName(item.name);
                                                                    setNewItemPrice(item.price);
                                                                    setNewItemQuantity(item.quantity);
                                                                    setShoppingListCategory(selectedCategory);
                                                                    setEditingItemId(item.id);
                                                                    setEditingItemMissionId(item.missionId);
                                                                    setEditingItemCategoryId(item.categoryId);
                                                                    setShowShoppingList(true);
                                                                }}
                                                                className={`p-1 rounded ${isDark ? 'text-cyan-400 hover:bg-cyan-500/20' : 'text-cyan-600 hover:bg-cyan-100'}`}
                                                                title="Edit Item"
                                                            >
                                                                <Edit className="w-4 h-4" />
                                                            </button>
                                                            <button
                                                                onClick={() => removeItemFromShoppingList(item.missionId, item.categoryId, item.id)}
                                                                className={`p-1 rounded ${isDark ? 'text-red-400 hover:bg-red-500/20' : 'text-red-600 hover:bg-red-100'}`}
                                                                title="Remove Item"
                                                            >
                                                                <Trash2 className="w-4 h-4" />
                                                            </button>
                                                        </div>
                                                    </div>
                                                ))
                                            }
                                            {missions
                                                .filter(mission => mission.category === selectedCategory && mission.shoppingList)
                                                .flatMap(mission => mission.shoppingList || [])
                                                .flatMap(category => category.items)
                                                .length === 0 && (
                                                    <p className={`text-center py-4 ${isDark ? 'text-gray-500' : 'text-gray-400'}`}>
                                                        No items in this category
                                                    </p>
                                                )}
                                        </div>

                                        {/* Category Total */}
                                        {missions
                                            .filter(mission => mission.category === selectedCategory && mission.shoppingList)
                                            .flatMap(mission => mission.shoppingList || [])
                                            .flatMap(category => category.items)
                                            .length > 0 && (
                                                <div className={`mt-3 pt-3 border-t flex justify-between font-bold ${isDark ? 'border-gray-700 text-green-400' : 'border-gray-300 text-green-600'}`}>
                                                    <span>Total:</span>
                                                    <span>
                                                        ${calculateCategoryTotal(
                                                            missions
                                                                .filter(mission => mission.category === selectedCategory && mission.shoppingList)
                                                                .flatMap(mission => mission.shoppingList || [])
                                                                .flatMap(category => category.items)
                                                        ).toFixed(2)}
                                                    </span>
                                                </div>
                                            )}
                                    </div>
                                )}

                                {/* Mission Detail View or Grid */}
                                {selectedMission ? (
                                    // Show Mission Detail View with sub-items
                                    <div className={`backdrop-blur-xl border rounded-xl p-6 mb-6 transition-all duration-300
                                        ${isDark
                                            ? 'bg-slate-800/40 border-cyan-500/20 shadow-cyan-500/5'
                                            : 'bg-white/60 border-sky-200/60 shadow-sky-500/10'
                                        }`}>
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h2 className={`text-xl font-bold ${isDark ? 'text-white' : 'text-gray-800'}`}>
                                                    {selectedMission.title}
                                                </h2>
                                                <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                                                    {selectedMission.description}
                                                </p>
                                            </div>
                                            <button
                                                onClick={() => setSelectedMission(null)}
                                                className={`p-2 rounded-lg ${isDark ? 'text-gray-400 hover:bg-gray-700' : 'text-gray-500 hover:bg-gray-100'}`}
                                                title="Back to list"
                                            >
                                                <X className="w-5 h-5" />
                                            </button>
                                        </div>

                                        {/* Mission Details */}
                                        <div className={`grid grid-cols-2 gap-3 text-xs mb-4 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                                            <div className="flex items-center gap-2">
                                                <Flag className={`w-4 h-4 ${isDark ? 'text-orange-400' : 'text-orange-600'}`} />
                                                <span>Category: {selectedMission.category}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Calendar className={`w-4 h-4 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`} />
                                                <span>Due: {formatDate(selectedMission.dueDate)}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Clock className={`w-4 h-4 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`} />
                                                <span>Created: {formatDate(selectedMission.createdAt)}</span>
                                            </div>
                                            {selectedMission.recursion && (
                                                <div className="flex items-center gap-2">
                                                    <RefreshCw className={`w-4 h-4 ${isDark ? 'text-purple-400' : 'text-purple-600'}`} />
                                                    <span>Recurs: {selectedMission.recursion}</span>
                                                </div>
                                            )}
                                        </div>

                                        {/* Shopping List Items (Sub-items) */}
                                        {selectedMission.shoppingList && selectedMission.shoppingList.length > 0 && (
                                            <div className="mt-6">
                                                <h3 className={`text-lg font-semibold mb-3 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                                                    Sub-items
                                                </h3>
                                                <div className="space-y-2">
                                                    {selectedMission.shoppingList.flatMap(category => category.items).map((item, index) => (
                                                        <div
                                                            key={item.id}
                                                            className={`flex justify-between items-center p-3 rounded border bg-opacity-50 ${
                                                                item.completed
                                                                    ? (isDark ? 'bg-gray-700/30 border-gray-600' : 'bg-gray-200/30 border-gray-300')
                                                                    : (isDark ? 'border-gray-600' : 'border-gray-300')
                                                            }`}
                                                        >
                                                            <div className="flex items-center gap-3 flex-1">
                                                                <input
                                                                    type="checkbox"
                                                                    checked={!!item.completed}
                                                                    onChange={() => toggleItemCompletion(selectedMission.id, selectedMission.shoppingList![0].id, item.id)}
                                                                    className="w-5 h-5 rounded"
                                                                    style={{
                                                                        accentColor: isDark ? '#22d3ee' : '#0891b2'
                                                                    }}
                                                                />
                                                                <span className={`${item.completed ? 'line-through opacity-60' : ''} ${isDark ? 'text-white' : 'text-gray-800'}`}>
                                                                    {item.name}
                                                                </span>
                                                                <span className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                                                                    (x{item.quantity})
                                                                </span>
                                                            </div>
                                                            <div className="flex items-center gap-2">
                                                                <span className={`${isDark ? 'text-green-400' : 'text-green-600'}`}>
                                                                    ${(item.price * item.quantity).toFixed(2)}
                                                                </span>
                                                                <button
                                                                    onClick={(e) => {
                                                                        e.stopPropagation();
                                                                        // Set up editing state
                                                                        setNewItemName(item.name);
                                                                        setNewItemPrice(item.price);
                                                                        setNewItemQuantity(item.quantity);
                                                                        setShoppingListCategory(selectedMission.category);
                                                                        setEditingItemId(item.id);
                                                                        setEditingItemMissionId(selectedMission.id);
                                                                        setEditingItemCategoryId(selectedMission.shoppingList![0].id);
                                                                        setShowShoppingList(true);
                                                                    }}
                                                                    className={`p-1.5 rounded ${isDark ? 'text-cyan-400 hover:bg-cyan-500/20' : 'text-cyan-600 hover:bg-cyan-100'}`}
                                                                    title="Edit Item"
                                                                >
                                                                    <Edit className="w-4 h-4" />
                                                                </button>
                                                                <button
                                                                    onClick={() => removeItemFromShoppingList(selectedMission.id, selectedMission.shoppingList![0].id, item.id)}
                                                                    className={`p-1.5 rounded ${isDark ? 'text-red-400 hover:bg-red-500/20' : 'text-red-600 hover:bg-red-100'}`}
                                                                    title="Remove Item"
                                                                >
                                                                    <Trash2 className="w-4 h-4" />
                                                                </button>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>

                                                {/* Category Total */}
                                                <div className={`mt-4 pt-3 border-t flex justify-between font-bold ${isDark ? 'border-gray-700 text-green-400' : 'border-gray-300 text-green-600'}`}>
                                                    <span>Total:</span>
                                                    <span>
                                                        ${calculateCategoryTotal(selectedMission.shoppingList.flatMap(category => category.items))}
                                                    </span>
                                                </div>
                                            </div>
                                        )}

                                        {/* Add Item Button */}
                                        <div className="mt-6">
                                            <button
                                                onClick={() => {
                                                    setShoppingListCategory(selectedMission.category);
                                                    setEditingItemMissionId(selectedMission.id);
                                                    setEditingItemCategoryId(selectedMission.shoppingList && selectedMission.shoppingList.length > 0 ? selectedMission.shoppingList[0].id : Date.now().toString());
                                                    setShowShoppingList(true);
                                                }}
                                                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg hover:from-cyan-400 hover:to-blue-500 transition-all"
                                            >
                                                <Plus className="w-4 h-4" />
                                                <span>Add Sub-item</span>
                                            </button>
                                        </div>

                                        {/* Back Button */}
                                        <div className="mt-6">
                                            <button
                                                onClick={() => setSelectedMission(null)}
                                                className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-all ${
                                                    isDark
                                                        ? 'border-gray-600 text-gray-300 hover:bg-gray-700'
                                                        : 'border-gray-300 text-gray-600 hover:bg-gray-100'
                                                }`}
                                            >
                                                <ChevronLeft className="w-4 h-4" />
                                                <span>Back to missions</span>
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    // Original Mission Grid
                                    <>
                                        {(loading || isPending) ? (
                                            <div className="flex flex-col items-center justify-center h-64 text-center">
                                                <RefreshCw className={`w-16 h-16 mb-4 animate-spin ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`} />
                                                <h3 className={`text-xl font-semibold ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                                                    {isPending ? 'Checking authentication...' : 'Loading missions...'}
                                                </h3>
                                            </div>
                                        ) : filteredMissions.length === 0 ? (
                                            <div className="flex flex-col items-center justify-center h-64 text-center">
                                                <Target className={`w-16 h-16 mb-4 ${isDark ? 'text-gray-600' : 'text-gray-400'}`} />
                                                <h3 className={`text-xl font-semibold mb-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>No Missions Found</h3>
                                                <p className={`mb-6 ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>
                                                    {missions.length === 0
                                                        ? "No missions have been added yet. Click 'New Mission' to get started!"
                                                        : "Try adjusting your filters or search query"}
                                                </p>
                                                <button
                                                    onClick={() => setShowAddModal(true)}
                                                    className={`flex items-center gap-2 px-6 py-3 rounded-lg border transition-all
                                                ${isDark
                                                            ? 'bg-cyan-500/20 text-cyan-400 border-cyan-500/50 hover:bg-cyan-500/30'
                                                            : 'bg-cyan-100 text-cyan-600 border-cyan-300 hover:bg-cyan-200'}`}
                                                >
                                                    <Plus className="w-5 h-5" />
                                                    Initialize First Mission
                                                </button>
                                            </div>
                                        ) : (
                                            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                                                <AnimatePresence>
                                                    {filteredMissions.map((mission) => (
                                                        <div key={mission.id}>
                                                            <MissionCard
                                                                mission={mission}
                                                                onEdit={handleEditMission}
                                                                onDelete={handleDeleteMission}
                                                                onToggleComplete={handleToggleComplete}
                                                                isDark={isDark}
                                                            />
                                                            
                                                            {/* Expanded Sub-items View */}
                                                            <AnimatePresence>
                                                                {selectedMission && (selectedMission as Mission).id === mission.id && mission.shoppingList && mission.shoppingList.length > 0 && (
                                                                    <motion.div
                                                                        initial={{ opacity: 0, height: 0 }}
                                                                        animate={{ opacity: 1, height: 'auto' }}
                                                                        exit={{ opacity: 0, height: 0 }}
                                                                        className={`mt-4 p-4 rounded-lg border backdrop-blur-xl ${
                                                                            isDark
                                                                                ? 'bg-slate-800/40 border-cyan-500/30'
                                                                                : 'bg-white/60 border-sky-200/60'
                                                                        }`}
                                                                    >
                                                                        <h4 className={`font-semibold mb-3 flex items-center gap-2 ${isDark ? 'text-cyan-300' : 'text-cyan-600'}`}>
                                                                            <ChevronLeft className="w-4 h-4" /> Sub-items
                                                                        </h4>
                                                                        <div className="space-y-2">
                                                                            {mission.shoppingList.map((category) => (
                                                                                <div key={category.id}>
                                                                                    <button
                                                                                        onClick={() => setExpandedCategories(prev => ({
                                                                                            ...prev,
                                                                                            [category.id]: !prev[category.id]
                                                                                        }))}
                                                                                        className={`flex items-center gap-2 w-full p-2 rounded transition-colors ${
                                                                                            isDark
                                                                                                ? 'hover:bg-cyan-500/10 text-cyan-300'
                                                                                                : 'hover:bg-sky-100 text-sky-600'
                                                                                        }`}
                                                                                    >
                                                                                        <ChevronLeft className={`w-4 h-4 transition-transform ${expandedCategories[category.id] ? 'rotate-90' : ''}`} />
                                                                                        <span className="font-medium">{category.name}</span>
                                                                                    </button>
                                                                                    
                                                                                    <AnimatePresence>
                                                                                        {expandedCategories[category.id] && (
                                                                                            <motion.div
                                                                                                initial={{ opacity: 0, height: 0 }}
                                                                                                animate={{ opacity: 1, height: 'auto' }}
                                                                                                exit={{ opacity: 0, height: 0 }}
                                                                                                className="ml-4 space-y-2 mt-2"
                                                                                            >
                                                                                                {category.items.map((item) => (
                                                                                                    <div
                                                                                                        key={item.id}
                                                                                                        className={`p-2 rounded border flex justify-between items-center text-sm ${
                                                                                                            isDark
                                                                                                                ? 'bg-gray-700/50 border-gray-600 text-gray-300'
                                                                                                                : 'bg-gray-100 border-gray-200 text-gray-700'
                                                                                                        }`}
                                                                                                    >
                                                                                                        <div className="flex-1">
                                                                                                            <div className={item.completed ? 'line-through opacity-50' : ''}>
                                                                                                                {item.name}
                                                                                                            </div>
                                                                                                            <div className={`text-xs ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                                                                                                                {item.quantity}x @ ${item.price.toFixed(2)}
                                                                                                            </div>
                                                                                                        </div>
                                                                                                        <input
                                                                                                            type="checkbox"
                                                                                                            checked={item.completed || false}
                                                                                                            className="w-4 h-4"
                                                                                                        />
                                                                                                    </div>
                                                                                                ))}
                                                                                            </motion.div>
                                                                                        )}
                                                                                    </AnimatePresence>
                                                                                </div>
                                                                            ))}
                                                                        </div>
                                                                    </motion.div>
                                                                )}
                                                            </AnimatePresence>
                                                        </div>
                                                    ))}
                                                </AnimatePresence>
                                            </div>
                                        )}
                                    </>
                                )}
                            </>
                        )}
                    </div>
                </main>
            </div>

            {/* Add Mission Modal */}
            <AnimatePresence>
                {showAddModal && (
                    <AddMissionModal
                        isOpen={showAddModal}
                        onClose={() => setShowAddModal(false)}
                        onAdd={handleAddMission}
                        isDark={isDark}
                    />
                )}
                {showEditModal && editingMission && (
                    <AddMissionModal
                        isOpen={showEditModal}
                        onClose={() => {
                            setShowEditModal(false);
                            setEditingMission(null);
                        }}
                        onAdd={handleSaveEdit}
                        isDark={isDark}
                        initialData={editingMission}
                        isEditMode={true}
                    />
                )}
            </AnimatePresence>

            {/* Add Item to Shopping List Modal */}
            <AnimatePresence>
            {showShoppingList && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
                    onClick={() => {
                        setShowShoppingList(false);
                        setNewItemName('');
                        setNewItemPrice(0);
                        setNewItemQuantity(1);
                        setEditingItemId(null);
                        setEditingItemMissionId(null);
                        setEditingItemCategoryId(null);
                    }}
                >
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                        className={`border rounded-2xl p-6 w-full max-w-md ${isDark ? 'bg-gray-900 border-cyan-500/50' : 'bg-white border-sky-300'}`}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="flex items-center justify-between mb-6">
                            <h2 className={`text-2xl font-bold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                                Add Item to Shopping List
                            </h2>
                            <button
                                onClick={() => {
                                    setShowShoppingList(false);
                                    setNewItemName('');
                                    setNewItemPrice(0);
                                    setNewItemQuantity(1);
                                }}
                                className={isDark ? 'text-gray-400 hover:text-white' : 'text-gray-500 hover:text-gray-800'}
                            >
                                <X className="w-6 h-6" />
                            </button>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Item Name *</label>
                                <input
                                    type="text"
                                    value={newItemName}
                                    onChange={(e) => setNewItemName(e.target.value)}
                                    className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors
                                        ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                                    placeholder="Item name..."
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Price ($)</label>
                                    <input
                                        type="number"
                                        value={newItemPrice}
                                        onChange={(e) => setNewItemPrice(parseFloat(e.target.value) || 0)}
                                        className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors
                                            ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                                        min="0"
                                        step="0.01"
                                    />
                                </div>

                                <div>
                                    <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Quantity</label>
                                    <input
                                        type="number"
                                        value={newItemQuantity}
                                        onChange={(e) => setNewItemQuantity(parseInt(e.target.value) || 1)}
                                        className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors
                                            ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                                        min="1"
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={() => {
                                    addItemToShoppingList(shoppingListCategory);
                                    setShowShoppingList(false);
                                }}
                                className="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-3 rounded-lg
                                    hover:from-cyan-400 hover:to-blue-500 transition-all"
                            >
                                {editingItemId ? 'Update Item' : 'Add Item'}
                            </button>
                            <button
                                onClick={() => {
                                    setShowShoppingList(false);
                                    setNewItemName('');
                                    setNewItemPrice(0);
                                    setNewItemQuantity(1);
                                    setEditingItemId(null);
                                    setEditingItemMissionId(null);
                                    setEditingItemCategoryId(null);
                                }}
                                className={`flex-1 py-3 rounded-lg border font-bold transition-colors
                                    ${isDark ? 'border-gray-600 text-gray-300 hover:bg-gray-800' : 'border-gray-300 text-gray-600 hover:bg-gray-100'}`}
                            >
                                Cancel
                            </button>
                        </div>
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>

        </div >
    );
}
