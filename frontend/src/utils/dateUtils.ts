/**
 * Date Utilities for Due Date Display and Status Calculation
 * Handles timezone conversions and due date status indicators
 */

export type DueDateStatus = 'overdue' | 'due_today' | 'upcoming' | null;

export interface DueDateInfo {
  status: DueDateStatus;
  displayText: string;
  color: string;
  bgColor: string;
  borderColor: string;
}

/**
 * Parse ISO date string to Date object
 */
export function parseDate(dateString: string | null | undefined): Date | null {
  if (!dateString) return null;
  try {
    return new Date(dateString);
  } catch {
    return null;
  }
}

/**
 * Format date to user's local timezone
 */
export function formatDateLocal(date: Date | string | null | undefined): string {
  const parsedDate = typeof date === 'string' ? parseDate(date) : date;
  if (!parsedDate) return '';

  return parsedDate.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Format date to short format (e.g., "Jan 20, 3:00 PM")
 */
export function formatDateShort(date: Date | string | null | undefined): string {
  const parsedDate = typeof date === 'string' ? parseDate(date) : date;
  if (!parsedDate) return '';

  return parsedDate.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Format relative time (e.g., "in 2 hours", "2 days ago")
 */
export function formatRelativeTime(date: Date | string | null | undefined): string {
  const parsedDate = typeof date === 'string' ? parseDate(date) : date;
  if (!parsedDate) return '';

  const now = new Date();
  const diffMs = parsedDate.getTime() - now.getTime();
  const diffMinutes = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMinutes < 0) {
    const absDiffMinutes = Math.abs(diffMinutes);
    if (absDiffMinutes < 60) return `${absDiffMinutes} min ago`;
    if (absDiffMinutes < 1440) return `${Math.abs(diffHours)} hr ago`;
    return `${Math.abs(diffDays)} day${Math.abs(diffDays) === 1 ? '' : 's'} ago`;
  }

  if (diffMinutes < 60) return `in ${diffMinutes} min`;
  if (diffMinutes < 1440) return `in ${diffHours} hr`;
  return `in ${diffDays} day${diffDays === 1 ? '' : 's'}`;
}

/**
 * Check if a date is today
 */
export function isToday(date: Date | string | null | undefined): boolean {
  const parsedDate = typeof date === 'string' ? parseDate(date) : date;
  if (!parsedDate) return false;

  const today = new Date();
  return (
    parsedDate.getDate() === today.getDate() &&
    parsedDate.getMonth() === today.getMonth() &&
    parsedDate.getFullYear() === today.getFullYear()
  );
}

/**
 * Check if a date is in the past (overdue)
 */
export function isOverdue(date: Date | string | null | undefined): boolean {
  const parsedDate = typeof date === 'string' ? parseDate(date) : date;
  if (!parsedDate) return false;

  return parsedDate.getTime() < new Date().getTime();
}

/**
 * Check if a date is upcoming (within next 7 days)
 */
export function isUpcoming(date: Date | string | null | undefined): boolean {
  const parsedDate = typeof date === 'string' ? parseDate(date) : date;
  if (!parsedDate) return false;

  const now = new Date();
  const sevenDaysFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);

  return parsedDate.getTime() > now.getTime() && parsedDate.getTime() <= sevenDaysFromNow.getTime();
}

/**
 * Calculate due date status with styling information
 */
export function getDueDateStatus(dueDate: string | null | undefined): DueDateInfo {
  if (!dueDate) {
    return {
      status: null,
      displayText: '',
      color: '',
      bgColor: '',
      borderColor: '',
    };
  }

  const parsedDate = parseDate(dueDate);
  if (!parsedDate) {
    return {
      status: null,
      displayText: '',
      color: '',
      bgColor: '',
      borderColor: '',
    };
  }

  // Check if overdue
  if (isOverdue(parsedDate) && !isToday(parsedDate)) {
    return {
      status: 'overdue',
      displayText: `Overdue (${formatRelativeTime(parsedDate)})`,
      color: 'text-red-600 dark:text-red-400',
      bgColor: 'bg-red-50 dark:bg-red-900/20',
      borderColor: 'border-red-200 dark:border-red-800',
    };
  }

  // Check if due today
  if (isToday(parsedDate)) {
    return {
      status: 'due_today',
      displayText: `Due today at ${parsedDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`,
      color: 'text-yellow-600 dark:text-yellow-400',
      bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
      borderColor: 'border-yellow-200 dark:border-yellow-800',
    };
  }

  // Check if upcoming
  if (isUpcoming(parsedDate)) {
    return {
      status: 'upcoming',
      displayText: `Due ${formatRelativeTime(parsedDate)}`,
      color: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      borderColor: 'border-blue-200 dark:border-blue-800',
    };
  }

  // Future date (more than 7 days away)
  return {
    status: 'upcoming',
    displayText: `Due ${formatDateShort(parsedDate)}`,
    color: 'text-gray-600 dark:text-gray-400',
    bgColor: 'bg-gray-50 dark:bg-gray-900/20',
    borderColor: 'border-gray-200 dark:border-gray-800',
  };
}

/**
 * Get timezone abbreviation (e.g., "PST", "EST")
 */
export function getTimezoneAbbreviation(): string {
  const date = new Date();
  const timeZoneString = date.toLocaleTimeString('en-US', { timeZoneName: 'short' });
  const match = timeZoneString.match(/\b[A-Z]{3,4}\b/);
  return match ? match[0] : '';
}

/**
 * Get full timezone name (e.g., "America/Los_Angeles")
 */
export function getTimezoneName(): string {
  return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

/**
 * Format due date for display in chat responses
 */
export function formatDueDateForChat(dueDate: string | null | undefined): string {
  if (!dueDate) return '';

  const info = getDueDateStatus(dueDate);
  if (!info.status) return '';

  const parsedDate = parseDate(dueDate);
  if (!parsedDate) return '';

  const fullDate = formatDateLocal(parsedDate);
  const timezone = getTimezoneAbbreviation();

  return `${info.displayText} (${fullDate} ${timezone})`;
}
