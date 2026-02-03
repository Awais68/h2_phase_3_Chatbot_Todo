# Recursion Feature Documentation

## Overview
The Recursion feature adds a new tab to the dashboard for managing recurring tasks with category-wise item lists and price tracking. This feature addresses the requirement to create a system where users can:

1. Manage recurring tasks that occur monthly
2. View upcoming tasks one week in advance
3. Organize items by categories (e.g., groceries with flour, surf, soap, match boxes)
4. Track prices for individual items
5. Calculate totals automatically

## Key Features Implemented

### 1. Recursion Tab in Sidebar
- Added a new "Recursion" tab to the sidebar navigation
- Uses the `Repeat` icon from Lucide React
- Shows a count of recurring tasks (currently hardcoded as 0)

### 2. Recurring Task Management
- Create new recurring tasks with title, description, category, and recurrence pattern
- Tasks can be daily, weekly, or monthly recurring
- Automatic calculation of next occurrence based on pattern
- Deletion capability for unwanted tasks

### 3. Category-Based Organization
- Each recurring task can have multiple categories
- Items are organized within their respective categories
- Ability to add/delete categories within tasks
- Visual hierarchy showing categories and their items

### 4. Item Management
- Add items with name, price, and quantity
- Real-time calculation of item totals (price × quantity)
- Delete individual items from categories
- Price tracking for budgeting purposes

### 5. Automatic Calculations
- Per-item cost calculation (price × quantity)
- Per-category total calculation
- Overall task total calculation
- Summary statistics showing total recurring tasks, categories, and estimated costs

### 6. Advanced Visibility Logic
- Tasks are filtered to show only those occurring within the next 7 days
- Date formatting for better readability
- Days-until-occurrence indicator

### 7. Data Persistence
- Uses localStorage to persist recurring tasks between sessions
- Sample data initialization for new users
- Automatic saving on changes

## Technical Implementation Details

### Components
- `RecursionTab.tsx`: Main component for the recursion feature
- Located in `frontend/src/components/RecursionTab.tsx`
- Uses React hooks (useState, useEffect) for state management
- Implements framer-motion for smooth animations

### Data Structures
```typescript
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
```

### UI Elements
- Modal dialogs for adding tasks and items
- Responsive grid layout for task cards
- Color-coded elements for different sections
- Interactive buttons for all CRUD operations
- Summary statistics cards at the bottom

### Styling
- Consistent with the existing theme (dark/light mode support)
- Uses the same backdrop-blur and border styles as other components
- Same color scheme with cyan/blue gradients
- Responsive design for mobile and desktop

## Usage Instructions

### Adding a Recurring Task
1. Click the "Add Recurring Task" button
2. Fill in the task details (title, description, category, recurrence pattern)
3. Click "Add Task" to save

### Managing Categories
1. Click "Add Category" on a task to create a new category
2. Or add the first item to automatically create a category
3. Use the trash icon to delete categories (empty categories are automatically removed)

### Adding Items
1. Click "Add Item" in a category section
2. Fill in the item details (name, price, quantity)
3. Click "Add Item" to save
4. Items are automatically calculated in the totals

### Viewing Upcoming Tasks
- The system automatically filters to show only tasks occurring within the next 7 days
- This ensures users see only relevant upcoming recurring tasks

## Future Enhancements

Potential improvements could include:
- Integration with the backend API for recurring tasks
- More sophisticated recurrence patterns (e.g., "every 2 weeks", "last Monday of month")
- Export functionality for shopping lists
- Reminders and notifications for upcoming tasks
- Bulk import/export of item lists
- Integration with calendar apps

## Known Limitations

- Currently uses localStorage for data persistence (not suitable for multi-device sync)
- No integration with the backend recurring task API yet
- Date calculations are basic and may not handle all edge cases (leap years, etc.)

## File Locations

- Frontend Component: `frontend/src/components/RecursionTab.tsx`
- Updated Dashboard: `frontend/src/components/Dashboard.tsx`
- Icons: Added `Repeat` icon from Lucide React

The feature is fully integrated into the existing dashboard and maintains consistency with the current UI/UX patterns.