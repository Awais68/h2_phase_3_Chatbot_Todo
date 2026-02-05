/**
 * Formatters for Task Data Display
 * Includes due date formatting in user's timezone
 */

import { formatDateLocal, formatDateShort, formatRelativeTime, parseDate } from './dateUtils';

/**
 * Format task title with truncation
 */
export function formatTaskTitle(title: string, maxLength: number = 50): string {
  if (title.length <= maxLength) return title;
  return `${title.substring(0, maxLength)}...`;
}

/**
 * Format task description with truncation
 */
export function formatTaskDescription(description: string | undefined, maxLength: number = 100): string {
  if (!description) return '';
  if (description.length <= maxLength) return description;
  return `${description.substring(0, maxLength)}...`;
}

/**
 * Format due date in user's timezone with fallback
 */
export function formatDueDate(
  dueDate: string | null | undefined,
  format: 'full' | 'short' | 'relative' = 'full'
): string {
  if (!dueDate) return 'No due date';

  const parsedDate = parseDate(dueDate);
  if (!parsedDate) return 'Invalid date';

  switch (format) {
    case 'short':
      return formatDateShort(parsedDate);
    case 'relative':
      return formatRelativeTime(parsedDate);
    case 'full':
    default:
      return formatDateLocal(parsedDate);
  }
}

/**
 * Format recurrence pattern for display
 */
export function formatRecurrencePattern(pattern: string | null | undefined): string {
  if (!pattern) return '';

  const patterns: Record<string, string> = {
    daily: 'Daily',
    weekly: 'Weekly',
    'bi-weekly': 'Bi-weekly',
    monthly: 'Monthly',
    yearly: 'Yearly',
  };

  return patterns[pattern.toLowerCase()] || pattern;
}

/**
 * Format reminder time before due date
 */
export function formatReminderTime(minutes: number | null | undefined): string {
  if (!minutes) return 'No reminder';

  if (minutes < 60) {
    return `${minutes} min before`;
  }

  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  if (remainingMinutes === 0) {
    return `${hours} hr before`;
  }

  return `${hours} hr ${remainingMinutes} min before`;
}

/**
 * Format timestamp to relative time or date
 */
export function formatTimestamp(timestamp: string | Date | null | undefined): string {
  if (!timestamp) return '';

  const date = typeof timestamp === 'string' ? parseDate(timestamp) : timestamp;
  if (!date) return '';

  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMinutes = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  // Less than 1 minute
  if (diffMinutes < 1) return 'Just now';

  // Less than 1 hour
  if (diffMinutes < 60) return `${diffMinutes} min ago`;

  // Less than 1 day
  if (diffHours < 24) return `${diffHours} hr ago`;

  // Less than 7 days
  if (diffDays < 7) return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`;

  // More than 7 days - show date
  return formatDateShort(date);
}

/**
 * Format priority level for display
 */
export function formatPriority(priority: string | undefined): string {
  if (!priority) return 'Normal';

  const priorities: Record<string, string> = {
    low: 'Low',
    normal: 'Normal',
    medium: 'Medium',
    high: 'High',
    critical: 'Critical',
  };

  return priorities[priority.toLowerCase()] || priority;
}

/**
 * Format status for display
 */
export function formatStatus(status: string | undefined): string {
  if (!status) return 'Pending';

  const statuses: Record<string, string> = {
    pending: 'Pending',
    active: 'Active',
    'in-progress': 'In Progress',
    completed: 'Completed',
    failed: 'Failed',
    blocked: 'Blocked',
  };

  return statuses[status.toLowerCase()] || status;
}

/**
 * Format tags array for display
 */
export function formatTags(tags: string[] | undefined, maxTags: number = 3): string {
  if (!tags || tags.length === 0) return '';

  const displayTags = tags.slice(0, maxTags);
  const remaining = tags.length - maxTags;

  let result = displayTags.join(', ');
  if (remaining > 0) {
    result += ` +${remaining} more`;
  }

  return result;
}

/**
 * Format completion percentage
 */
export function formatPercentage(value: number | undefined): string {
  if (value === undefined || value === null) return '0%';
  return `${Math.round(value)}%`;
}

/**
 * Format task count with label
 */
export function formatTaskCount(count: number, singular: string = 'task', plural?: string): string {
  const pluralForm = plural || `${singular}s`;
  return `${count} ${count === 1 ? singular : pluralForm}`;
}

/**
 * Format file size
 */
export function formatFileSize(bytes: number | undefined): string {
  if (!bytes || bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}

/**
 * Format currency
 */
export function formatCurrency(amount: number | undefined, currency: string = 'USD'): string {
  if (amount === undefined || amount === null) return '$0.00';

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}
