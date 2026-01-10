'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    BarChart3,
    CheckCircle,
    Activity,
    Clock,
    ArrowLeft,
    TrendingUp,
    Zap,
    Target,
    AlertTriangle,
} from 'lucide-react';
import { useRouter } from 'next/navigation';

interface Mission {
    id: string;
    title: string;
    priority: 'critical' | 'high' | 'medium' | 'low';
    status: 'pending' | 'active' | 'completed' | 'failed';
    dueDate: string;
}

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

export default function AnalyticsPage() {
    const router = useRouter();
    const [isDark, setIsDark] = useState(true);
    const [missions, setMissions] = useState<Mission[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const theme = localStorage.getItem('theme');
        setIsDark(theme === 'dark' || theme === null);
    }, []);

    useEffect(() => {
        const fetchMissions = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    router.push('/auth');
                    return;
                }

                const response = await fetch('http://localhost:8000/tasks/', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setMissions(data);
                }
            } catch (error) {
                console.error('Failed to fetch missions:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchMissions();
    }, [router]);

    const stats = {
        total: missions.length,
        active: missions.filter((m) => m.status === 'active').length,
        completed: missions.filter((m) => m.status === 'completed').length,
        pending: missions.filter((m) => m.status === 'pending').length,
        failed: missions.filter((m) => m.status === 'failed').length,
    };

    const chartData = {
        completed: [12, 19, 15, 22, 18, 25, 28],
        active: [8, 12, 10, 15, 14, 18, 16],
        pending: [5, 8, 6, 10, 9, 12, 11],
    };

    if (loading) {
        return (
            <div className={`min-h-screen flex items-center justify-center ${isDark ? 'bg-gray-900' : 'bg-gray-50'}`}>
                <div className={`text-xl ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Loading analytics...</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-gray-900">
            {/* Animated background particles */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(168,85,247,0.1),transparent_50%)]"></div>
                {[...Array(20)].map((_, i) => (
                    <motion.div
                        key={i}
                        className="absolute w-1 h-1 bg-purple-500/30 rounded-full"
                        style={{
                            left: `${Math.random() * 100}%`,
                            top: `${Math.random() * 100}%`,
                        }}
                        animate={{
                            y: [0, -30, 0],
                            opacity: [0.2, 0.5, 0.2],
                        }}
                        transition={{
                            duration: 3 + Math.random() * 2,
                            repeat: Infinity,
                            delay: Math.random() * 2,
                        }}
                    />
                ))}
            </div>

            {/* Header */}
            <div className="sticky top-0 z-10 backdrop-blur-xl border-b bg-gray-900/90 border-purple-500/20">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <button
                                onClick={() => router.push('/dashboard')}
                                className="p-2 rounded-lg transition-all hover:bg-purple-500/20 text-purple-400 hover:text-purple-300"
                            >
                                <ArrowLeft className="w-5 h-5" />
                            </button>
                            <div className="flex items-center gap-3">
                                <div className="p-2 rounded-lg bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30">
                                    <BarChart3 className="w-6 h-6 text-purple-400" />
                                </div>
                                <div>
                                    <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Analytics Dashboard</h1>
                                    <p className="text-sm text-gray-400">Mission Performance & Insights</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Content */}
            <div className="container mx-auto px-6 py-8 relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-8"
                >
                    {/* Summary Cards */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.1 }}
                            className="p-6 rounded-2xl text-center backdrop-blur-xl bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-500/20 shadow-[0_0_15px_rgba(6,182,212,0.1)]"
                        >
                            <Target className="w-10 h-10 mx-auto mb-3 text-cyan-400 drop-shadow-[0_0_8px_rgba(6,182,212,0.6)]" />
                            <p className="text-5xl font-bold mb-2 text-cyan-400">{stats.total}</p>
                            <p className="text-sm text-cyan-300/70">Total Missions</p>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.2 }}
                            className="p-6 rounded-2xl text-center backdrop-blur-xl bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 shadow-[0_0_15px_rgba(251,146,60,0.1)]"
                        >
                            <Zap className="w-10 h-10 mx-auto mb-3 text-orange-400 drop-shadow-[0_0_8px_rgba(251,146,60,0.6)]" />
                            <p className="text-5xl font-bold mb-2 text-orange-400">{stats.active}</p>
                            <p className="text-sm text-orange-300/70">Active</p>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.3 }}
                            className="p-6 rounded-2xl text-center backdrop-blur-xl bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 shadow-[0_0_15px_rgba(34,197,94,0.1)]"
                        >
                            <CheckCircle className="w-10 h-10 mx-auto mb-3 text-green-400 drop-shadow-[0_0_8px_rgba(34,197,94,0.6)]" />
                            <p className="text-5xl font-bold mb-2 text-green-400">{stats.completed}</p>
                            <p className="text-sm text-green-300/70">Completed</p>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.4 }}
                            className="p-6 rounded-2xl text-center backdrop-blur-xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20 shadow-[0_0_15px_rgba(168,85,247,0.1)]"
                        >
                            <Clock className="w-10 h-10 mx-auto mb-3 text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.6)]" />
                            <p className="text-5xl font-bold mb-2 text-purple-400">{stats.pending}</p>
                            <p className="text-sm text-purple-300/70">Pending</p>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.5 }}
                            className="p-6 rounded-2xl text-center backdrop-blur-xl bg-gradient-to-br from-red-500/10 to-rose-500/10 border border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.1)]"
                        >
                            <AlertTriangle className="w-10 h-10 mx-auto mb-3 text-red-400 drop-shadow-[0_0_8px_rgba(239,68,68,0.6)]" />
                            <p className="text-5xl font-bold mb-2 text-red-400">{stats.failed}</p>
                            <p className="text-sm text-red-300/70">Failed</p>
                        </motion.div>
                    </div>

                    {/* Chart Sections */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.6 }}
                            className="backdrop-blur-xl bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-2xl p-8 shadow-[0_0_20px_rgba(34,197,94,0.1)]"
                        >
                            <h3 className="font-semibold text-lg mb-6 flex items-center gap-2 text-green-400">
                                <CheckCircle className="w-6 h-6" /> Completed Tasks
                            </h3>
                            <div className="h-40 mb-4">
                                <MiniChart data={chartData.completed} color="green" isDark={isDark} />
                            </div>
                            <p className="text-xs text-center text-green-300/70">Last 7 days trend</p>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.7 }}
                            className="backdrop-blur-xl bg-gradient-to-br from-orange-500/10 to-red-500/10 border border-orange-500/20 rounded-2xl p-8 shadow-[0_0_20px_rgba(251,146,60,0.1)]"
                        >
                            <h3 className="font-semibold text-lg mb-6 flex items-center gap-2 text-orange-400">
                                <Activity className="w-6 h-6" /> Active Tasks
                            </h3>
                            <div className="h-40 mb-4">
                                <MiniChart data={chartData.active} color="orange" isDark={isDark} />
                            </div>
                            <p className="text-xs text-center text-orange-300/70">Last 7 days trend</p>
                        </motion.div>
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.8 }}
                            className="backdrop-blur-xl bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/20 rounded-2xl p-8 shadow-[0_0_20px_rgba(168,85,247,0.1)]"
                        >
                            <h3 className="font-semibold text-lg mb-6 flex items-center gap-2 text-purple-400">
                                <Clock className="w-6 h-6" /> Pending Tasks
                            </h3>
                            <div className="h-40 mb-4">
                                <MiniChart data={chartData.pending} color="purple" isDark={isDark} />
                            </div>
                            <p className="text-xs text-center text-purple-300/70">Last 7 days trend</p>
                        </motion.div>
                    </div>

                    {/* Priority Distribution */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.9 }}
                        className="backdrop-blur-xl bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-500/20 rounded-2xl p-8 shadow-[0_0_20px_rgba(6,182,212,0.1)]"
                    >
                        <h3 className="font-semibold text-xl mb-6 flex items-center gap-2 text-cyan-400">
                            <TrendingUp className="w-6 h-6" /> Priority Distribution
                        </h3>
                        <div className="space-y-6">
                            {['critical', 'high', 'medium', 'low'].map((priority, index) => {
                                const count = missions.filter(m => m.priority === priority).length;
                                const percentage = missions.length > 0 ? (count / missions.length) * 100 : 0;
                                const colors: Record<string, { bg: string; text: string; glow: string }> = {
                                    critical: { bg: 'bg-gradient-to-r from-red-500 to-rose-500', text: 'text-red-400', glow: 'shadow-[0_0_10px_rgba(239,68,68,0.4)]' },
                                    high: { bg: 'bg-gradient-to-r from-orange-500 to-red-500', text: 'text-orange-400', glow: 'shadow-[0_0_10px_rgba(251,146,60,0.4)]' },
                                    medium: { bg: 'bg-gradient-to-r from-yellow-500 to-orange-500', text: 'text-yellow-400', glow: 'shadow-[0_0_10px_rgba(234,179,8,0.4)]' },
                                    low: { bg: 'bg-gradient-to-r from-blue-500 to-cyan-500', text: 'text-blue-400', glow: 'shadow-[0_0_10px_rgba(59,130,246,0.4)]' },
                                };
                                return (
                                    <div key={priority}>
                                        <div className="flex items-center justify-between mb-2">
                                            <span className={`text-sm font-medium capitalize ${colors[priority].text}`}>{priority} Priority</span>
                                            <span className="text-sm font-bold text-gray-300">
                                                {count} tasks ({percentage.toFixed(1)}%)
                                            </span>
                                        </div>
                                        <div className="h-4 rounded-full overflow-hidden bg-gray-800/50 border border-gray-700/50">
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${percentage}%` }}
                                                transition={{ duration: 1, delay: 0.2 * index }}
                                                className={`h-full rounded-full ${colors[priority].bg} ${colors[priority].glow}`}
                                            />
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </motion.div>
                </motion.div>
            </div>
        </div>
    );
}
