'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Edit, CheckCircle, Calendar, Flag, Trash2, Plus } from 'lucide-react';
import { Mission } from '@/types';

interface HistoryTabProps {
    missions: Mission[];
    isDark: boolean;
    onEdit: (mission: Mission) => void;
}

const HistoryTab: React.FC<HistoryTabProps> = ({ missions, isDark, onEdit }) => {
    const completedMissions = missions.filter(mission => mission.status === 'completed');

    return (
        <div className="p-6">
            <h2 className={`text-2xl font-bold mb-6 ${isDark ? 'text-white' : 'text-gray-900'}`}>Task History</h2>

            <div className="mb-6">
                <h3 className={`text-lg font-semibold mb-3 ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>Recently Completed</h3>

                {completedMissions.length > 0 ? (
                    <div className="space-y-4">
                        {completedMissions.map((mission) => (
                            <motion.div
                                key={mission.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`p-4 rounded-xl border ${
                                    isDark
                                        ? 'bg-gray-800/50 border-gray-700 text-gray-200'
                                        : 'bg-white border-gray-200 text-gray-700'
                                }`}
                            >
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h4 className={`font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>{mission.title}</h4>
                                        <p className="text-sm mt-1">{mission.description}</p>
                                        <div className="flex items-center gap-4 mt-2 text-xs">
                                            <span className={`px-2 py-1 rounded ${isDark ? 'bg-gray-700' : 'bg-gray-100'}`}>
                                                Priority: {mission.priority}
                                            </span>
                                            <span className={`px-2 py-1 rounded ${isDark ? 'bg-green-900/30 text-green-400' : 'bg-green-100 text-green-700'}`}>
                                                Completed
                                            </span>
                                            <span className={`px-2 py-1 rounded ${isDark ? 'bg-gray-700' : 'bg-gray-100'}`}>
                                                {new Date(mission.dueDate).toLocaleDateString()}
                                            </span>
                                            <span className={`px-2 py-1 rounded ${isDark ? 'bg-gray-700' : 'bg-gray-100'}`}>
                                                Category: {mission.category}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => onEdit(mission)}
                                            className={`p-2 rounded-lg transition-colors ${isDark ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}
                                            title="Edit"
                                        >
                                            <Edit className="w-4 h-4" />
                                        </button>
                                    </div>
                                </div>

                                {/* Display tags if they exist */}
                                {mission.tags && mission.tags.length > 0 && (
                                    <div className="mt-3 flex flex-wrap gap-2">
                                        {mission.tags.map((tag, index) => (
                                            <span
                                                key={index}
                                                className={`text-xs px-2 py-1 rounded-full ${
                                                    isDark
                                                        ? 'bg-cyan-900/30 text-cyan-300 border border-cyan-700/50'
                                                        : 'bg-cyan-100 text-cyan-700 border border-cyan-300'
                                                }`}
                                            >
                                                {tag}
                                            </span>
                                        ))}
                                    </div>
                                )}

                                {/* Display shopping list items if they exist */}
                                {mission.shoppingList && mission.shoppingList.length > 0 && (
                                    <div className="mt-3 space-y-2">
                                        <h5 className={`text-sm font-medium ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Shopping List:</h5>
                                        {mission.shoppingList.map((category, catIndex) => (
                                            <div key={catIndex} className="ml-2">
                                                <h6 className={`text-xs font-semibold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>{category.name}</h6>
                                                <div className="space-y-1">
                                                    {category.items.map((item, itemIndex) => (
                                                        <div
                                                            key={itemIndex}
                                                            className={`text-xs flex justify-between pl-2 ${item.completed ? 'line-through opacity-60' : ''}`}
                                                        >
                                                            <span>{item.name} (x{item.quantity})</span>
                                                            <span>${item.price.toFixed(2)}</span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <div className={`p-8 text-center rounded-xl border ${
                        isDark ? 'bg-gray-800/30 border-gray-700 text-gray-400' : 'bg-gray-50 border-gray-200 text-gray-500'
                    }`}>
                        <CheckCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                        <p>No completed tasks yet.</p>
                        <p className="text-sm mt-1">Your completed tasks will appear here.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HistoryTab;