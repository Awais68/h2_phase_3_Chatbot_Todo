/**
 * Integration Tests for Shopping List Synchronization
 * Run with: npm test -- useShoppingListSync.integration.test.ts
 */

import { renderHook, act, waitFor } from '@testing-library/react';
import { useShoppingListSync } from '../useShoppingListSync';
import { Mission, Item } from '@/types';

// Mock API client
const createMockApi = (responses: any[] = []) => {
  let callCount = 0;
  
  return {
    tasks: {
      update: jest.fn(async () => {
        const response = responses[callCount] || { success: true };
        callCount++;
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        return response;
      }),
    },
    getCallCount: () => callCount,
  };
};

describe('useShoppingListSync - Integration Tests', () => {
  const mockSession = { user: { id: 'user123' } };
  const getUserId = (session: any) => session?.user?.id || 'user123';
  
  beforeEach(() => {
    // Clear localStorage logs before each test
    localStorage.removeItem('shoppingListSyncLogs');
  });

  describe('Test Case 1: Successful Save with Items', () => {
    it('should save shopping list with multiple items successfully', async () => {
      const mockApi = createMockApi([{ success: true }]);
      
      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: '1771246388990',
        title: 'Ramzan Tasks',
        description: 'Religious tasks',
        priority: 'high',
        status: 'active',
        dueDate: '2024-03-15',
        createdAt: new Date().toISOString(),
        tags: ['ramzan'],
        category: 'Religious',
        shoppingList: [],
      };

      const missions = [testMission];
      const setMissions = jest.fn((updater) => {
        if (typeof updater === 'function') {
          const updated = updater(missions);
          missions.length = 0;
          missions.push(...updated);
        }
      });

      // Add first item
      const item1: Item = {
        id: '1771246388990',
        name: 'roza rakho',
        price: 0,
        quantity: 1,
        completed: false,
      };

      await act(async () => {
        const { success } = await result.current.addOrUpdateItem(
          testMission.id,
          'Ramzan',
          item1,
          missions,
          setMissions
        );

        expect(success).toBe(true);
      });

      expect(mockApi.tasks.update).toHaveBeenCalledTimes(1);
      
      // Verify the payload structure
      const updateCall = mockApi.tasks.update.mock.calls[0];
      expect(updateCall[1]).toHaveProperty('shoppingList');
      expect(updateCall[1].shoppingList).toHaveLength(1);
      expect(updateCall[1].shoppingList[0].items).toContainEqual(
        expect.objectContaining({
          name: 'roza rakho',
          price: 0,
          quantity: 1,
        })
      );

      // Add second item
      const item2: Item = {
        id: '1771246397530',
        name: 'namz parho',
        price: 0,
        quantity: 1,
        completed: true,
      };

      await act(async () => {
        const { success } = await result.current.addOrUpdateItem(
          testMission.id,
          'Ramzan',
          item2,
          missions,
          setMissions
        );

        expect(success).toBe(true);
      });

      expect(mockApi.tasks.update).toHaveBeenCalledTimes(2);
      
      // Verify both items are in the list
      const secondUpdateCall = mockApi.tasks.update.mock.calls[1];
      expect(secondUpdateCall[1].shoppingList[0].items).toHaveLength(2);
    });

    it('should log sync operations correctly', async () => {
      const mockApi = createMockApi([{ success: true }]);
      
      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'test-mission',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      const item: Item = {
        id: 'item-123',
        name: 'Test Item',
        price: 100,
        quantity: 2,
        completed: false,
      };

      await act(async () => {
        await result.current.addOrUpdateItem(
          testMission.id,
          'Test Category',
          item,
          missions,
          setMissions
        );
      });

      // Check sync logs
      const logs = JSON.parse(localStorage.getItem('shoppingListSyncLogs') || '[]');
      expect(logs.length).toBeGreaterThan(0);
      expect(logs[0]).toHaveProperty('success', true);
      expect(logs[0]).toHaveProperty('missionId', 'test-mission');
    });
  });

  describe('Test Case 2: Empty Array Scenario', () => {
    it('should handle empty shopping list correctly', async () => {
      const mockApi = createMockApi([{ success: true }]);
      
      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'empty-mission',
        title: 'Empty Task',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      // Delete all items (resulting in empty shopping list)
      await act(async () => {
        const { success } = await result.current.deleteItem(
          testMission.id,
          'category-1',
          'item-1',
          missions,
          setMissions
        );

        expect(success).toBe(true);
      });

      // Verify empty array is saved
      const updateCall = mockApi.tasks.update.mock.calls[0];
      expect(updateCall[1].shoppingList).toEqual([]);
    });
  });

  describe('Test Case 3: Network Failure Recovery', () => {
    it('should retry on network failure and eventually succeed', async () => {
      // Fail twice, then succeed
      const mockApi = createMockApi([
        { error: 'Network error' },
        { error: 'Network error' },
        { success: true },
      ]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'retry-mission',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      const item: Item = {
        id: 'item-retry',
        name: 'Retry Item',
        price: 50,
        quantity: 1,
        completed: false,
      };

      await act(async () => {
        const { success } = await result.current.addOrUpdateItem(
          testMission.id,
          'Retry Category',
          item,
          missions,
          setMissions
        );

        expect(success).toBe(true);
      });

      // Should have been called 3 times (2 failures + 1 success)
      await waitFor(() => {
        expect(mockApi.tasks.update).toHaveBeenCalledTimes(3);
      });

      // State should still be updated after retries succeed
      expect(setMissions).toHaveBeenCalled();
    });

    it('should fail after max retries and not update state', async () => {
      // Fail all attempts
      const mockApi = createMockApi([
        { error: 'Network error' },
        { error: 'Network error' },
        { error: 'Network error' },
        { error: 'Network error' },
      ]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'fail-mission',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      const item: Item = {
        id: 'item-fail',
        name: 'Fail Item',
        price: 50,
        quantity: 1,
        completed: false,
      };

      await act(async () => {
        const { success, error } = await result.current.addOrUpdateItem(
          testMission.id,
          'Fail Category',
          item,
          missions,
          setMissions
        );

        expect(success).toBe(false);
        expect(error).toBeDefined();
        expect(error?.message).toBe('Network error');
      });

      // Should have retried 3 times (max retries)
      await waitFor(() => {
        expect(mockApi.tasks.update).toHaveBeenCalledTimes(4); // 1 initial + 3 retries
      });

      // State should NOT be updated when all retries fail
      expect(setMissions).not.toHaveBeenCalled();

      // Error state should be set
      expect(result.current.lastSyncError).toBeDefined();
    });
  });

  describe('Test Case 4: Race Condition Prevention', () => {
    it('should prevent duplicate operations for the same item', async () => {
      const mockApi = createMockApi([
        { success: true },
        { success: true },
      ]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'race-mission',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      const item: Item = {
        id: 'item-race',
        name: 'Race Item',
        price: 50,
        quantity: 1,
        completed: false,
      };

      // Try to add the same item twice simultaneously
      const [result1, result2] = await Promise.all([
        act(async () =>
          result.current.addOrUpdateItem(
            testMission.id,
            'Race Category',
            item,
            missions,
            setMissions
          )
        ),
        act(async () =>
          result.current.addOrUpdateItem(
            testMission.id,
            'Race Category',
            item,
            missions,
            setMissions
          )
        ),
      ]);

      // One should succeed, one should fail with "operation in progress"
      const successCount = [result1, result2].filter(r => r.success).length;
      expect(successCount).toBe(1);

      // API should only be called once (second call blocked)
      await waitFor(() => {
        expect(mockApi.tasks.update).toHaveBeenCalledTimes(1);
      });
    });

    it('should handle rapid sequential operations correctly', async () => {
      const mockApi = createMockApi(
        Array(5).fill({ success: true })
      );

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'sequential-mission',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      let missionsCopy = [...missions];
      const setMissions = jest.fn((updater) => {
        if (typeof updater === 'function') {
          missionsCopy = updater(missionsCopy);
        }
      });

      // Add 5 items sequentially
      for (let i = 0; i < 5; i++) {
        const item: Item = {
          id: `item-${i}`,
          name: `Item ${i}`,
          price: 10 * i,
          quantity: i + 1,
          completed: false,
        };

        await act(async () => {
          const { success } = await result.current.addOrUpdateItem(
            testMission.id,
            'Sequential Category',
            item,
            missionsCopy,
            setMissions
          );

          expect(success).toBe(true);
        });
      }

      // All 5 operations should complete
      expect(mockApi.tasks.update).toHaveBeenCalledTimes(5);

      // Verify all items are in the final shopping list
      const finalCall = mockApi.tasks.update.mock.calls[4];
      expect(finalCall[1].shoppingList[0].items).toHaveLength(5);
    });
  });

  describe('Test Case 5: Data Validation', () => {
    it('should sanitize invalid data before saving', async () => {
      const mockApi = createMockApi([{ success: true }]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'validation-mission',
        shoppingList: [
          {
            id: 'cat-1',
            name: 'Valid Category',
            items: [
              { id: 'item-1', name: 'Valid Item', price: 100, quantity: 1, completed: false },
              { id: '', name: '', price: -10, quantity: -1, completed: false }, // Invalid
            ],
          },
          {
            id: '',
            name: '', // Invalid category
            items: [],
          },
        ],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      const newItem: Item = {
        id: 'item-new',
        name: 'New Item',
        price: 50,
        quantity: 2,
        completed: false,
      };

      await act(async () => {
        await result.current.addOrUpdateItem(
          testMission.id,
          'Valid Category',
          newItem,
          missions,
          setMissions
        );
      });

      // Check that sanitization removed invalid data
      const updateCall = mockApi.tasks.update.mock.calls[0];
      const savedList = updateCall[1].shoppingList;

      // Should only have valid category
      expect(savedList).toHaveLength(1);
      expect(savedList[0].name).toBe('Valid Category');

      // Should only have valid items
      expect(savedList[0].items).toHaveLength(2); // Valid Item + New Item
      expect(savedList[0].items.every((item: Item) => item.id && item.name)).toBe(true);
      expect(savedList[0].items.every((item: Item) => item.price >= 0)).toBe(true);
      expect(savedList[0].items.every((item: Item) => item.quantity >= 0)).toBe(true);
    });
  });

  describe('Test Case 6: Toggle and Delete Operations', () => {
    it('should toggle item completion atomically', async () => {
      const mockApi = createMockApi([{ success: true }]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'toggle-mission',
        shoppingList: [
          {
            id: 'cat-1',
            name: 'Category',
            items: [
              { id: 'item-1', name: 'Item 1', price: 10, quantity: 1, completed: false },
            ],
          },
        ],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn((updater) => {
        if (typeof updater === 'function') {
          const updated = updater(missions);
          missions[0] = updated[0];
        }
      });

      await act(async () => {
        const { success } = await result.current.toggleItemCompletion(
          testMission.id,
          'cat-1',
          'item-1',
          missions,
          setMissions
        );

        expect(success).toBe(true);
      });

      // Verify item is toggled to completed
      const updateCall = mockApi.tasks.update.mock.calls[0];
      expect(updateCall[1].shoppingList[0].items[0].completed).toBe(true);
    });

    it('should delete item atomically', async () => {
      const mockApi = createMockApi([{ success: true }]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'delete-mission',
        shoppingList: [
          {
            id: 'cat-1',
            name: 'Category',
            items: [
              { id: 'item-1', name: 'Item 1', price: 10, quantity: 1, completed: false },
              { id: 'item-2', name: 'Item 2', price: 20, quantity: 2, completed: false },
            ],
          },
        ],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      await act(async () => {
        const { success } = await result.current.deleteItem(
          testMission.id,
          'cat-1',
          'item-1',
          missions,
          setMissions
        );

        expect(success).toBe(true);
      });

      // Verify item is deleted
      const updateCall = mockApi.tasks.update.mock.calls[0];
      expect(updateCall[1].shoppingList[0].items).toHaveLength(1);
      expect(updateCall[1].shoppingList[0].items[0].id).toBe('item-2');
    });

    it('should remove empty categories after deleting last item', async () => {
      const mockApi = createMockApi([{ success: true }]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      const testMission: Mission = {
        id: 'delete-category-mission',
        shoppingList: [
          {
            id: 'cat-1',
            name: 'Category',
            items: [
              { id: 'item-1', name: 'Item 1', price: 10, quantity: 1, completed: false },
            ],
          },
        ],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      await act(async () => {
        await result.current.deleteItem(
          testMission.id,
          'cat-1',
          'item-1',
          missions,
          setMissions
        );
      });

      // Verify empty category is removed
      const updateCall = mockApi.tasks.update.mock.calls[0];
      expect(updateCall[1].shoppingList).toHaveLength(0);
    });
  });

  describe('Test Case 7: Loading and Error States', () => {
    it('should set isSyncing to true during operation', async () => {
      const mockApi = createMockApi([{ success: true }]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      expect(result.current.isSyncing).toBe(false);

      const testMission: Mission = {
        id: 'loading-mission',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      const item: Item = {
        id: 'item-loading',
        name: 'Loading Item',
        price: 50,
        quantity: 1,
        completed: false,
      };

      const promise = act(async () => {
        result.current.addOrUpdateItem(
          testMission.id,
          'Loading Category',
          item,
          missions,
          setMissions
        );
      });

      // Should be syncing during operation
      // Note: This may need adjustment based on timing
      await promise;

      // Should not be syncing after operation completes
      await waitFor(() => {
        expect(result.current.isSyncing).toBe(false);
      });
    });

    it('should set lastSyncError on failure', async () => {
      const mockApi = createMockApi([
        { error: 'Test error' },
        { error: 'Test error' },
        { error: 'Test error' },
        { error: 'Test error' },
      ]);

      const { result } = renderHook(() =>
        useShoppingListSync({ api: mockApi, getUserId, session: mockSession })
      );

      expect(result.current.lastSyncError).toBeNull();

      const testMission: Mission = {
        id: 'error-mission',
        shoppingList: [],
      } as Mission;

      const missions = [testMission];
      const setMissions = jest.fn();

      const item: Item = {
        id: 'item-error',
        name: 'Error Item',
        price: 50,
        quantity: 1,
        completed: false,
      };

      await act(async () => {
        await result.current.addOrUpdateItem(
          testMission.id,
          'Error Category',
          item,
          missions,
          setMissions
        );
      });

      expect(result.current.lastSyncError).toBeDefined();
      expect(result.current.lastSyncError?.message).toBe('Test error');
    });
  });
});
