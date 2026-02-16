/**
 * Custom hook for shopping list synchronization
 * Provides atomic operations for adding/updating/deleting shopping list items
 */

import { useState, useCallback, useRef } from 'react';
import { Mission, Category, Item } from '@/types';
import { 
  deepClone, 
  withRetry, 
  validateShoppingList, 
  createTaskUpdatePayload,
  logShoppingListSync 
} from '@/utils/missionSync';

interface UseShoppingListSyncProps {
  api: any; // Your API client
  getUserId: (session: any) => string;
  session: any;
}

export function useShoppingListSync({ api, getUserId, session }: UseShoppingListSyncProps) {
  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSyncError, setLastSyncError] = useState<Error | null>(null);
  
  // Track in-progress operations to prevent duplicates
  const syncingOperations = useRef<Set<string>>(new Set());

  /**
   * Atomic add/update item operation
   * Ensures DB is updated BEFORE state is changed
   */
  const addOrUpdateItem = useCallback(
    async (
      missionId: string,
      categoryName: string,
      item: Item,
      missions: Mission[],
      setMissions: React.Dispatch<React.SetStateAction<Mission[]>>,
      setSelectedMission?: React.Dispatch<React.SetStateAction<Mission | null>>
    ): Promise<{ success: boolean; error?: Error }> => {
      const operationKey = `${missionId}-${item.id}`;
      
      // Prevent duplicate operations
      if (syncingOperations.current.has(operationKey)) {
        console.warn('⚠️ Operation already in progress:', operationKey);
        return { success: false, error: new Error('Operation in progress') };
      }
      
      syncingOperations.current.add(operationKey);
      setIsSyncing(true);
      setLastSyncError(null);
      
      try {
        // Step 1: Get current mission state (DEEP CLONE to prevent mutations)
        const currentMission = deepClone(missions.find(m => m.id === missionId));
        
        if (!currentMission) {
          throw new Error(`Mission ${missionId} not found`);
        }
        
        // Step 2: Update shopping list in cloned mission
        const updatedShoppingList = deepClone(currentMission.shoppingList || []);
        const categoryIndex = updatedShoppingList.findIndex(
          cat => cat.name === categoryName || cat.id === item.id
        );
        
        if (categoryIndex !== -1) {
          // Category exists - add/update item
          const existingItemIndex = updatedShoppingList[categoryIndex].items.findIndex(
            i => i.id === item.id
          );
          
          if (existingItemIndex !== -1) {
            // Update existing item
            updatedShoppingList[categoryIndex].items[existingItemIndex] = item;
            logShoppingListSync(missionId, `Update item ${item.name}`, true, { item });
          } else {
            // Add new item
            updatedShoppingList[categoryIndex].items.push(item);
            logShoppingListSync(missionId, `Add item ${item.name}`, true, { item });
          }
        } else {
          // Create new category with item
          updatedShoppingList.push({
            id: Date.now().toString(),
            name: categoryName,
            items: [item],
          });
          logShoppingListSync(missionId, `Create category ${categoryName} with item`, true, { 
            categoryName, 
            item 
          });
        }
        
        // Step 3: Validate shopping list
        const { isValid, errors, sanitized } = validateShoppingList(updatedShoppingList);
        
        if (!isValid) {
          console.warn('⚠️ Shopping list validation failed:', errors);
        }
        
        // Update mission with sanitized shopping list
        const updatedMission: Mission = {
          ...currentMission,
          shoppingList: sanitized,
        };
        
        // Step 4: Save to backend FIRST (with retry)
        const userId = getUserId(session);
        const taskUpdateData = createTaskUpdatePayload(updatedMission);
        
        await withRetry(
          () => api.tasks.update(missionId, taskUpdateData, userId),
          { maxRetries: 3, retryDelay: 1000, backoffMultiplier: 2 },
          `Save shopping list for mission ${missionId}`
        );
        
        logShoppingListSync(missionId, 'Backend save', true, { 
          itemCount: sanitized.reduce((sum, cat) => sum + cat.items.length, 0) 
        });
        
        // Step 5: Update local state ONLY after successful backend save
        setMissions(prevMissions =>
          prevMissions.map(m =>
            m.id === missionId
              ? { ...m, shoppingList: sanitized }
              : m
          )
        );
        
        // Update selected mission if applicable
        if (setSelectedMission) {
          setSelectedMission(prev =>
            prev && prev.id === missionId
              ? { ...prev, shoppingList: sanitized }
              : prev
          );
        }
        
        console.log('✅ Shopping list item saved successfully:', item.name);
        return { success: true };
        
      } catch (error) {
        const err = error as Error;
        setLastSyncError(err);
        
        logShoppingListSync(missionId, 'Failed to save item', false, { 
          error: err.message,
          item 
        });
        
        console.error('❌ Failed to save shopping list item:', err);
        return { success: false, error: err };
        
      } finally {
        syncingOperations.current.delete(operationKey);
        setIsSyncing(false);
      }
    },
    [api, getUserId, session]
  );

  /**
   * Atomic delete item operation
   */
  const deleteItem = useCallback(
    async (
      missionId: string,
      categoryId: string,
      itemId: string,
      missions: Mission[],
      setMissions: React.Dispatch<React.SetStateAction<Mission[]>>,
      setSelectedMission?: React.Dispatch<React.SetStateAction<Mission | null>>
    ): Promise<{ success: boolean; error?: Error }> => {
      const operationKey = `${missionId}-delete-${itemId}`;
      
      if (syncingOperations.current.has(operationKey)) {
        return { success: false, error: new Error('Delete operation in progress') };
      }
      
      syncingOperations.current.add(operationKey);
      setIsSyncing(true);
      
      try {
        const currentMission = deepClone(missions.find(m => m.id === missionId));
        
        if (!currentMission) {
          throw new Error(`Mission ${missionId} not found`);
        }
        
        // Remove item from shopping list
        const updatedShoppingList = (currentMission.shoppingList || [])
          .map(category => {
            if (category.id === categoryId) {
              return {
                ...category,
                items: category.items.filter(item => item.id !== itemId),
              };
            }
            return category;
          })
          .filter(category => category.items.length > 0); // Remove empty categories
        
        const updatedMission: Mission = {
          ...currentMission,
          shoppingList: updatedShoppingList,
        };
        
        // Save to backend first
        const userId = getUserId(session);
        const taskUpdateData = createTaskUpdatePayload(updatedMission);
        
        await withRetry(
          () => api.tasks.update(missionId, taskUpdateData, userId),
          { maxRetries: 3, retryDelay: 1000, backoffMultiplier: 2 },
          `Delete item from mission ${missionId}`
        );
        
        logShoppingListSync(missionId, 'Delete item', true, { itemId });
        
        // Update local state
        setMissions(prevMissions =>
          prevMissions.map(m =>
            m.id === missionId
              ? { ...m, shoppingList: updatedShoppingList }
              : m
          )
        );
        
        if (setSelectedMission) {
          setSelectedMission(prev =>
            prev && prev.id === missionId
              ? { ...prev, shoppingList: updatedShoppingList }
              : prev
          );
        }
        
        return { success: true };
        
      } catch (error) {
        const err = error as Error;
        setLastSyncError(err);
        logShoppingListSync(missionId, 'Failed to delete item', false, { error: err.message });
        return { success: false, error: err };
        
      } finally {
        syncingOperations.current.delete(operationKey);
        setIsSyncing(false);
      }
    },
    [api, getUserId, session]
  );

  /**
   * Toggle item completion
   */
  const toggleItemCompletion = useCallback(
    async (
      missionId: string,
      categoryId: string,
      itemId: string,
      missions: Mission[],
      setMissions: React.Dispatch<React.SetStateAction<Mission[]>>,
      setSelectedMission?: React.Dispatch<React.SetStateAction<Mission | null>>
    ): Promise<{ success: boolean; error?: Error }> => {
      const operationKey = `${missionId}-toggle-${itemId}`;
      
      if (syncingOperations.current.has(operationKey)) {
        return { success: false, error: new Error('Toggle operation in progress') };
      }
      
      syncingOperations.current.add(operationKey);
      setIsSyncing(true);
      
      try {
        const currentMission = deepClone(missions.find(m => m.id === missionId));
        
        if (!currentMission) {
          throw new Error(`Mission ${missionId} not found`);
        }
        
        // Toggle item completion
        const updatedShoppingList = (currentMission.shoppingList || []).map(category => {
          if (category.id === categoryId) {
            return {
              ...category,
              items: category.items.map(item => {
                if (item.id === itemId) {
                  return { ...item, completed: !item.completed };
                }
                return item;
              }),
            };
          }
          return category;
        });
        
        const updatedMission: Mission = {
          ...currentMission,
          shoppingList: updatedShoppingList,
        };
        
        // Save to backend first
        const userId = getUserId(session);
        const taskUpdateData = createTaskUpdatePayload(updatedMission);
        
        await withRetry(
          () => api.tasks.update(missionId, taskUpdateData, userId),
          { maxRetries: 2, retryDelay: 500, backoffMultiplier: 1.5 }, // Faster for toggle
          `Toggle item completion for mission ${missionId}`
        );
        
        // Update local state
        setMissions(prevMissions =>
          prevMissions.map(m =>
            m.id === missionId
              ? { ...m, shoppingList: updatedShoppingList }
              : m
          )
        );
        
        if (setSelectedMission) {
          setSelectedMission(prev =>
            prev && prev.id === missionId
              ? { ...prev, shoppingList: updatedShoppingList }
              : prev
          );
        }
        
        return { success: true };
        
      } catch (error) {
        const err = error as Error;
        setLastSyncError(err);
        console.error('Failed to toggle item completion:', err);
        return { success: false, error: err };
        
      } finally {
        syncingOperations.current.delete(operationKey);
        setIsSyncing(false);
      }
    },
    [api, getUserId, session]
  );

  return {
    addOrUpdateItem,
    deleteItem,
    toggleItemCompletion,
    isSyncing,
    lastSyncError,
  };
}
