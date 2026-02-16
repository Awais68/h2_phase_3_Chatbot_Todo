/**
 * Mission/Task Synchronization Utilities
 * Provides atomic, retry-enabled sync for shopping list items
 */

import { Mission, Category, Item } from '@/types';

/**
 * Deep clone an object to prevent reference mutations
 * More reliable than JSON.parse(JSON.stringify()) for dates/functions
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime()) as any;
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as any;
  
  const clonedObj = {} as T;
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      clonedObj[key] = deepClone(obj[key]);
    }
  }
  return clonedObj;
}

/**
 * Retry configuration for API calls
 */
interface RetryConfig {
  maxRetries: number;
  retryDelay: number; // milliseconds
  backoffMultiplier: number;
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  retryDelay: 1000,
  backoffMultiplier: 2,
};

/**
 * Retry wrapper for async functions with exponential backoff
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY_CONFIG,
  context: string = 'Operation'
): Promise<T> {
  let lastError: Error | null = null;
  
  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      const result = await fn();
      if (attempt > 0) {
        console.log(`✅ ${context} succeeded on retry ${attempt}`);
      }
      return result;
    } catch (error) {
      lastError = error as Error;
      
      if (attempt < config.maxRetries) {
        const delay = config.retryDelay * Math.pow(config.backoffMultiplier, attempt);
        console.warn(
          `⚠️ ${context} failed (attempt ${attempt + 1}/${config.maxRetries + 1}). Retrying in ${delay}ms...`,
          error
        );
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  console.error(`❌ ${context} failed after ${config.maxRetries} retries`, lastError);
  throw lastError;
}

/**
 * Validate shopping list structure before saving
 */
export function validateShoppingList(shoppingList: Category[] | undefined): {
  isValid: boolean;
  errors: string[];
  sanitized: Category[];
} {
  const errors: string[] = [];
  
  if (!shoppingList || !Array.isArray(shoppingList)) {
    return { isValid: true, errors: [], sanitized: [] };
  }
  
  const sanitized = shoppingList
    .filter(category => {
      // Validate category structure
      if (!category.id || !category.name) {
        errors.push(`Invalid category: missing id or name`);
        return false;
      }
      
      // Ensure items array exists
      if (!Array.isArray(category.items)) {
        errors.push(`Category "${category.name}" has invalid items array`);
        return false;
      }
      
      return true;
    })
    .map(category => ({
      ...category,
      items: category.items.filter(item => {
        // Validate item structure
        if (!item.id || !item.name) {
          errors.push(`Invalid item in category "${category.name}": missing id or name`);
          return false;
        }
        
        // Ensure numeric fields
        if (typeof item.price !== 'number' || item.price < 0) {
          errors.push(`Invalid price for item "${item.name}"`);
          return false;
        }
        
        if (typeof item.quantity !== 'number' || item.quantity < 0) {
          errors.push(`Invalid quantity for item "${item.name}"`);
          return false;
        }
        
        return true;
      }),
    }))
    .filter(category => category.items.length > 0); // Remove empty categories
  
  return { 
    isValid: errors.length === 0, 
    errors, 
    sanitized 
  };
}

/**
 * Create task update payload with proper structure
 */
export function createTaskUpdatePayload(mission: Mission) {
  // Validate and sanitize shopping list
  const { sanitized, errors } = validateShoppingList(mission.shoppingList);
  
  if (errors.length > 0) {
    console.warn('⚠️ Shopping list validation warnings:', errors);
  }
  
  return {
    title: mission.title,
    description: mission.description || '',
    status: mission.status,
    priority: mission.priority,
    dueDate: mission.dueDate,
    recursion: mission.recursion,
    category: mission.category,
    tags: mission.tags || [],
    shoppingList: sanitized, // Always use sanitized data
  };
}

/**
 * Atomic shopping list operation
 * Ensures state and DB are updated together or both fail
 */
export interface ShoppingListOperation {
  missionId: string;
  updatedMission: Mission;
  onSuccess?: (mission: Mission) => void;
  onError?: (error: Error) => void;
}

/**
 * Log shopping list sync for debugging
 */
export function logShoppingListSync(
  missionId: string,
  operation: string,
  success: boolean,
  details?: any
) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    missionId,
    operation,
    success,
    details,
  };
  
  // Log to console
  if (success) {
    console.log(`✅ [${timestamp}] Shopping List Sync: ${operation}`, logEntry);
  } else {
    console.error(`❌ [${timestamp}] Shopping List Sync Failed: ${operation}`, logEntry);
  }
  
  // Store in localStorage for debugging (keep last 50 logs)
  try {
    const logs = JSON.parse(localStorage.getItem('shoppingListSyncLogs') || '[]');
    logs.push(logEntry);
    if (logs.length > 50) logs.shift();
    localStorage.setItem('shoppingListSyncLogs', JSON.stringify(logs));
  } catch (e) {
    console.warn('Failed to store sync log', e);
  }
}

/**
 * Check if mission data is consistent
 */
export function validateMissionConsistency(
  localMission: Mission,
  serverMission: Mission
): { consistent: boolean; differences: string[] } {
  const differences: string[] = [];
  
  // Compare shopping list lengths
  const localListLength = localMission.shoppingList?.length || 0;
  const serverListLength = serverMission.shoppingList?.length || 0;
  
  if (localListLength !== serverListLength) {
    differences.push(
      `Shopping list length mismatch: local=${localListLength}, server=${serverListLength}`
    );
  }
  
  // Compare item counts
  const localItemCount = localMission.shoppingList?.reduce(
    (sum, cat) => sum + cat.items.length,
    0
  ) || 0;
  const serverItemCount = serverMission.shoppingList?.reduce(
    (sum, cat) => sum + cat.items.length,
    0
  ) || 0;
  
  if (localItemCount !== serverItemCount) {
    differences.push(
      `Item count mismatch: local=${localItemCount}, server=${serverItemCount}`
    );
  }
  
  return {
    consistent: differences.length === 0,
    differences,
  };
}
