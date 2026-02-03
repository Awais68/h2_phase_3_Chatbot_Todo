'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Trash2, Edit, Calculator, Package, Tag, DollarSign, Calendar, Clock } from 'lucide-react';

interface Item {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface Category {
  id: string;
  name: string;
  items: Item[];
}

interface RecurringTask {
  id: string;
  title: string;
  description: string;
  category: string;
  nextOccurrence: string;
  recurrencePattern: string;
  totalCost: number;
  categories: Category[];
}

const RecursionTab = ({ isDark }: { isDark: boolean }) => {
  const [recurringTasks, setRecurringTasks] = useState<RecurringTask[]>([]);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    category: '',
    recurrencePattern: 'monthly'
  });
  const [editingTask, setEditingTask] = useState<RecurringTask | null>(null);
  const [showAddTask, setShowAddTask] = useState(false);
  const [showAddItem, setShowAddItem] = useState<{ taskId: string; categoryId?: string } | null>(null);
  const [newItem, setNewItem] = useState({ name: '', price: 0, quantity: 1 });

  // Load recurring tasks from localStorage on mount
  useEffect(() => {
    const storedTasks = localStorage.getItem('recurringTasks');
    if (storedTasks) {
      try {
        const parsedTasks = JSON.parse(storedTasks);
        // Filter tasks to show only those occurring in the next week
        const nextWeek = new Date();
        nextWeek.setDate(nextWeek.getDate() + 7);

        const filteredTasks = parsedTasks.filter((task: RecurringTask) => {
          const nextDate = new Date(task.nextOccurrence);
          return nextDate <= nextWeek;
        });

        setRecurringTasks(filteredTasks);
      } catch (e) {
        console.error('Error parsing recurring tasks:', e);
      }
    } else {
      // Initialize with sample data
      const sampleTasks: RecurringTask[] = [
        {
          id: '1',
          title: 'Grocery Shopping',
          description: 'Monthly grocery shopping trip',
          category: 'Shopping',
          nextOccurrence: new Date(Date.now() + 6 * 24 * 60 * 60 * 1000).toISOString(), // 6 days from now
          recurrencePattern: 'monthly',
          totalCost: 125.50,
          categories: [
            {
              id: '1',
              name: 'Groceries',
              items: [
                { id: '1', name: 'Flour', price: 2.50, quantity: 2 },
                { id: '2', name: 'Surf', price: 3.20, quantity: 1 },
                { id: '3', name: 'Soap', price: 1.80, quantity: 3 },
                { id: '4', name: 'Match Box', price: 0.50, quantity: 2 },
              ]
            }
          ]
        },
        {
          id: '2',
          title: 'Rent Payment',
          description: 'Monthly rent payment',
          category: 'Bills',
          nextOccurrence: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days from now
          recurrencePattern: 'monthly',
          totalCost: 1200,
          categories: [
            {
              id: '2',
              name: 'Housing',
              items: [
                { id: '5', name: 'Monthly Rent', price: 1200, quantity: 1 },
              ]
            }
          ]
        }
      ];
      setRecurringTasks(sampleTasks);
      localStorage.setItem('recurringTasks', JSON.stringify(sampleTasks));
    }
  }, []);

  // Save to localStorage whenever recurringTasks changes
  useEffect(() => {
    localStorage.setItem('recurringTasks', JSON.stringify(recurringTasks));
  }, [recurringTasks]);

  const calculateTotalCost = (categories: Category[]) => {
    let total = 0;
    categories.forEach(category => {
      category.items.forEach(item => {
        total += item.price * item.quantity;
      });
    });
    return total;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const addTask = () => {
    if (!newTask.title.trim()) return;

    const nextOccurrence = new Date();
    if (newTask.recurrencePattern === 'monthly') {
      nextOccurrence.setMonth(nextOccurrence.getMonth() + 1);
    } else if (newTask.recurrencePattern === 'weekly') {
      nextOccurrence.setDate(nextOccurrence.getDate() + 7);
    } else {
      nextOccurrence.setDate(nextOccurrence.getDate() + 1);
    }

    const task: RecurringTask = {
      id: Date.now().toString(),
      title: newTask.title,
      description: newTask.description,
      category: newTask.category || 'General',
      nextOccurrence: nextOccurrence.toISOString(),
      recurrencePattern: newTask.recurrencePattern,
      totalCost: 0,
      categories: []
    };

    setRecurringTasks([...recurringTasks, task]);
    setNewTask({ title: '', description: '', category: '', recurrencePattern: 'monthly' });
    setShowAddTask(false);
  };

  const deleteTask = (taskId: string) => {
    setRecurringTasks(recurringTasks.filter(task => task.id !== taskId));
  };

  const addItemToCategory = (taskId: string, categoryId?: string) => {
    if (!newItem.name.trim() || newItem.price <= 0) return;

    const item: Item = {
      id: Date.now().toString(),
      name: newItem.name,
      price: newItem.price,
      quantity: newItem.quantity
    };

    setRecurringTasks(prevTasks =>
      prevTasks.map(task => {
        if (task.id === taskId) {
          if (categoryId) {
            // Add to existing category
            const updatedCategories = task.categories.map(cat => {
              if (cat.id === categoryId) {
                return {
                  ...cat,
                  items: [...cat.items, item]
                };
              }
              return cat;
            });

            const newTotalCost = calculateTotalCost(updatedCategories);
            return { ...task, categories: updatedCategories, totalCost: newTotalCost };
          } else {
            // Create new category with item
            const newCategory: Category = {
              id: Date.now().toString(),
              name: task.title,
              items: [item]
            };

            const updatedCategories = [...task.categories, newCategory];
            const newTotalCost = calculateTotalCost(updatedCategories);
            return { ...task, categories: updatedCategories, totalCost: newTotalCost };
          }
        }
        return task;
      })
    );

    setNewItem({ name: '', price: 0, quantity: 1 });
    setShowAddItem(null);
  };

  const deleteItem = (taskId: string, categoryId: string, itemId: string) => {
    setRecurringTasks(prevTasks =>
      prevTasks.map(task => {
        if (task.id === taskId) {
          const updatedCategories = task.categories.map(cat => {
            if (cat.id === categoryId) {
              const filteredItems = cat.items.filter(item => item.id !== itemId);
              return { ...cat, items: filteredItems };
            }
            return cat;
          }).filter(cat => cat.items.length > 0); // Remove empty categories

          const newTotalCost = calculateTotalCost(updatedCategories);
          return { ...task, categories: updatedCategories, totalCost: newTotalCost };
        }
        return task;
      })
    );
  };

  const addCategory = (taskId: string) => {
    const newCategory: Category = {
      id: Date.now().toString(),
      name: `Category ${Date.now()}`,
      items: []
    };

    setRecurringTasks(prevTasks =>
      prevTasks.map(task => {
        if (task.id === taskId) {
          const updatedCategories = [...task.categories, newCategory];
          return { ...task, categories: updatedCategories };
        }
        return task;
      })
    );
  };

  const deleteCategory = (taskId: string, categoryId: string) => {
    setRecurringTasks(prevTasks =>
      prevTasks.map(task => {
        if (task.id === taskId) {
          const updatedCategories = task.categories.filter(cat => cat.id !== categoryId);
          const newTotalCost = calculateTotalCost(updatedCategories);
          return { ...task, categories: updatedCategories, totalCost: newTotalCost };
        }
        return task;
      })
    );
  };

  const daysUntilOccurrence = (dateString: string) => {
    const today = new Date();
    const nextDate = new Date(dateString);
    const diffTime = nextDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  return (
    <div className={`p-4 md:p-6 h-full overflow-y-auto ${isDark ? 'text-white' : 'text-gray-900'}`}>
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-6 gap-4">
        <div>
          <h2 className={`text-2xl font-bold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
            Recursion Manager
          </h2>
          <p className={`mt-1 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Manage recurring tasks and category-based shopping lists
          </p>
        </div>
        <button
          onClick={() => setShowAddTask(true)}
          className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg hover:from-cyan-400 hover:to-blue-500 transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>Add Recurring Task</span>
        </button>
      </div>

      {/* Add Task Modal */}
      <AnimatePresence>
        {showAddTask && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowAddTask(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className={`border rounded-2xl p-6 w-full max-w-md ${isDark ? 'bg-gray-900 border-cyan-500/50' : 'bg-white border-sky-300'}`}
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className={`text-xl font-bold mb-4 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                Add Recurring Task
              </h3>

              <div className="space-y-4">
                <div>
                  <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Title *</label>
                  <input
                    type="text"
                    value={newTask.title}
                    onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                    className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors
                      ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                    placeholder="Task title..."
                  />
                </div>

                <div>
                  <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Description</label>
                  <textarea
                    value={newTask.description}
                    onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                    className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors resize-none
                      ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                    rows={3}
                    placeholder="Task description..."
                  />
                </div>

                <div>
                  <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Category</label>
                  <input
                    type="text"
                    value={newTask.category}
                    onChange={(e) => setNewTask({...newTask, category: e.target.value})}
                    className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors
                      ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                    placeholder="Category name..."
                  />
                </div>

                <div>
                  <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Recurrence Pattern</label>
                  <select
                    value={newTask.recurrencePattern}
                    onChange={(e) => setNewTask({...newTask, recurrencePattern: e.target.value})}
                    className={`w-full border rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 transition-colors
                      ${isDark ? 'bg-gray-800 border-gray-600 text-white' : 'bg-gray-50 border-gray-300 text-gray-800'}`}
                  >
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={addTask}
                  className="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-3 rounded-lg
                    hover:from-cyan-400 hover:to-blue-500 transition-all"
                >
                  Add Task
                </button>
                <button
                  onClick={() => setShowAddTask(false)}
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

      {/* Add Item Modal */}
      <AnimatePresence>
        {showAddItem && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setShowAddItem(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className={`border rounded-2xl p-6 w-full max-w-md ${isDark ? 'bg-gray-900 border-cyan-500/50' : 'bg-white border-sky-300'}`}
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className={`text-xl font-bold mb-4 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                Add Item to Category
              </h3>

              <div className="space-y-4">
                <div>
                  <label className={`block text-sm mb-2 ${isDark ? 'text-gray-300' : 'text-gray-600'}`}>Item Name *</label>
                  <input
                    type="text"
                    value={newItem.name}
                    onChange={(e) => setNewItem({...newItem, name: e.target.value})}
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
                      value={newItem.price}
                      onChange={(e) => setNewItem({...newItem, price: parseFloat(e.target.value) || 0})}
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
                      value={newItem.quantity}
                      onChange={(e) => setNewItem({...newItem, quantity: parseInt(e.target.value) || 1})}
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
                    if (showAddItem) {
                      addItemToCategory(showAddItem.taskId, showAddItem.categoryId);
                    }
                  }}
                  className="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-3 rounded-lg
                    hover:from-cyan-400 hover:to-blue-500 transition-all"
                >
                  Add Item
                </button>
                <button
                  onClick={() => setShowAddItem(null)}
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

      {/* Recurring Tasks List */}
      {recurringTasks.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-64 text-center">
          <Package className={`w-16 h-16 mb-4 ${isDark ? 'text-gray-600' : 'text-gray-400'}`} />
          <h3 className={`text-xl font-semibold mb-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>No Recurring Tasks</h3>
          <p className={`mb-6 ${isDark ? 'text-gray-500' : 'text-gray-500'}`}>
            Create your first recurring task to get started
          </p>
          <button
            onClick={() => setShowAddTask(true)}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg border transition-all
              ${isDark
                ? 'bg-cyan-500/20 text-cyan-400 border-cyan-500/50 hover:bg-cyan-500/30'
                : 'bg-cyan-100 text-cyan-600 border-cyan-300 hover:bg-cyan-200'}`}
          >
            <Plus className="w-5 h-5" />
            Add First Task
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recurringTasks.map((task) => (
            <motion.div
              key={task.id}
              layout
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className={`backdrop-blur-xl border rounded-xl p-5 transition-all duration-300 shadow-lg
                ${isDark
                  ? 'bg-slate-800/40 border-cyan-500/20 hover:border-cyan-400/40 shadow-cyan-500/5'
                  : 'bg-white/60 border-sky-200/60 hover:border-sky-300/80 shadow-sky-500/10'
                }`}
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className={`text-lg font-bold ${isDark ? 'text-white' : 'text-gray-800'}`}>
                    {task.title}
                  </h3>
                  <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                    {task.description}
                  </p>
                </div>
                <button
                  onClick={() => deleteTask(task.id)}
                  className={`p-1.5 rounded-lg transition-colors
                    ${isDark ? 'text-red-400 hover:bg-red-500/20' : 'text-red-600 hover:bg-red-100'}`}
                  title="Delete Task"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              <div className={`grid grid-cols-2 gap-3 text-xs mb-4 ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                <div className="flex items-center gap-2">
                  <Calendar className={`w-4 h-4 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`} />
                  <span>Next: {formatDate(task.nextOccurrence)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className={`w-4 h-4 ${isDark ? 'text-purple-400' : 'text-purple-600'}`} />
                  <span>{task.recurrencePattern}</span>
                </div>
                <div className="flex items-center gap-2 col-span-2">
                  <Tag className={`w-4 h-4 ${isDark ? 'text-orange-400' : 'text-orange-600'}`} />
                  <span>{task.category}</span>
                </div>
              </div>

              {/* Categories and Items */}
              <div className="space-y-3 mb-4">
                {task.categories.map((category) => (
                  <div key={category.id} className="border-l-2 border-cyan-500 pl-3">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className={`font-semibold text-sm ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                        {category.name}
                      </h4>
                      <button
                        onClick={() => deleteCategory(task.id, category.id)}
                        className={`p-1 rounded ${isDark ? 'text-red-400 hover:bg-red-500/20' : 'text-red-600 hover:bg-red-100'}`}
                        title="Delete Category"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </div>

                    <div className="space-y-2">
                      {category.items.map((item) => (
                        <div key={item.id} className="flex justify-between items-center text-sm">
                          <div className="flex items-center gap-2">
                            <span>{item.name}</span>
                            <span className={`${isDark ? 'text-gray-500' : 'text-gray-400'}`}>
                              (x{item.quantity})
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className={`${isDark ? 'text-green-400' : 'text-green-600'}`}>
                              ${(item.price * item.quantity).toFixed(2)}
                            </span>
                            <button
                              onClick={() => deleteItem(task.id, category.id, item.id)}
                              className={`p-0.5 rounded ${isDark ? 'text-red-400 hover:bg-red-500/20' : 'text-red-600 hover:bg-red-100'}`}
                              title="Delete Item"
                            >
                              <Trash2 className="w-3 h-3" />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>

                    <button
                      onClick={() => setShowAddItem({ taskId: task.id, categoryId: category.id })}
                      className={`mt-2 text-xs flex items-center gap-1 ${isDark ? 'text-cyan-400 hover:text-cyan-300' : 'text-cyan-600 hover:text-cyan-700'}`}
                    >
                      <Plus className="w-3 h-3" />
                      Add Item
                    </button>
                  </div>
                ))}

                {task.categories.length === 0 && (
                  <button
                    onClick={() => setShowAddItem({ taskId: task.id })}
                    className={`w-full py-2 text-center text-sm rounded border ${isDark ? 'border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10' : 'border-cyan-300 text-cyan-600 hover:bg-cyan-100'}`}
                  >
                    Add First Category & Item
                  </button>
                )}
              </div>

              {/* Add Category Button */}
              <button
                onClick={() => addCategory(task.id)}
                className={`w-full py-2 text-center text-sm rounded border ${isDark ? 'border-gray-600 text-gray-400 hover:bg-gray-700' : 'border-gray-300 text-gray-600 hover:bg-gray-100'}`}
              >
                + Add Category
              </button>

              {/* Total Cost */}
              <div className={`mt-4 pt-3 border-t flex justify-between items-center font-bold ${isDark ? 'border-gray-700 text-green-400' : 'border-gray-300 text-green-600'}`}>
                <span>Total Cost:</span>
                <span className="flex items-center gap-1">
                  <Calculator className="w-4 h-4" />
                  ${task.totalCost.toFixed(2)}
                </span>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Summary Stats */}
      {recurringTasks.length > 0 && (
        <div className={`mt-6 p-4 rounded-xl backdrop-blur-xl border ${isDark ? 'bg-slate-800/40 border-cyan-500/20' : 'bg-white/60 border-sky-200/60'}`}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className={`text-center p-3 rounded-lg ${isDark ? 'bg-gray-800/50' : 'bg-gray-100'}`}>
              <div className={`text-2xl font-bold ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>
                {recurringTasks.length}
              </div>
              <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Recurring Tasks</div>
            </div>
            <div className={`text-center p-3 rounded-lg ${isDark ? 'bg-gray-800/50' : 'bg-gray-100'}`}>
              <div className={`text-2xl font-bold ${isDark ? 'text-purple-400' : 'text-purple-600'}`}>
                {recurringTasks.reduce((acc, task) => acc + task.categories.length, 0)}
              </div>
              <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Categories</div>
            </div>
            <div className={`text-center p-3 rounded-lg ${isDark ? 'bg-gray-800/50' : 'bg-gray-100'}`}>
              <div className={`text-2xl font-bold ${isDark ? 'text-green-400' : 'text-green-600'}`}>
                ${recurringTasks.reduce((acc, task) => acc + task.totalCost, 0).toFixed(2)}
              </div>
              <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>Total Estimated</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecursionTab;