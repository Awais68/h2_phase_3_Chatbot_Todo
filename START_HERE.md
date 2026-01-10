# Phase I Complete Task Management System - Quick Start

## 🚀 How to Run the Application

### Simple Command (Copy & Paste):

```bash
cd "/media/data/hackathon series/hackathon-2/hackathon-2/sp-1"
source .venv/bin/activate
python phase1_complete_cli.py
```

### Or use the shortcut:

```bash
cd "/media/data/hackathon series/hackathon-2/hackathon-2/sp-1"
./run_app.sh
```

---

## ✅ All Features Working:

1. ✅ **Priority Levels** - High (🔴), Medium (🟡), Low (🟢)
2. ✅ **Due Dates** - Natural language ("tomorrow", "next week") or ISO format
3. ✅ **Tags** - Add multiple tags (personal, work, health, shopping, etc.)
4. ✅ **Recurring Tasks** - Daily, Weekly, Monthly, Yearly (auto-creates next)
5. ✅ **Status Tracking** - Pending (⏳Green), Completed (✅Blue), Overdue (⚠️Red)
6. ✅ **Filtering** - By status, priority, tags, or date range
7. ✅ **Search** - Keyword search in title and description
8. ✅ **Sorting** - By priority, due date, created date, or tags
9. ✅ **Theme Changing** - Dark (cyan), Light (blue), Hacker (green)
10. ✅ **Voice Commands** - Optional voice input for all operations

---

## 📋 Menu Options:

```
1. ➕ Add new task (with priority, due date, tags, recurrence)
2. ✏️  Update task (edit any field)
3. 🗑️  Delete task (with confirmation)
4. ✓ Toggle task completion (auto-creates recurring)
5. 🔍 Filter / Search tasks
6. 📊 Sort tasks
7. 🎨 Change theme
8. 🎤 Voice Commands (requires microphone)
9. ❌ Exit (auto-saves)
```

---

## 💡 Quick Examples:

### Add a High Priority Task:
1. Run the app
2. Choose option `1` (Add new task)
3. Title: "Complete project"
4. Description: "Finish Phase I"
5. Priority: Choose `High`
6. Due date: Type "tomorrow"
7. Tags: Type "work urgent"
8. Recurrence: Choose `None`
9. Task created! ✓

### Filter by Completed Tasks:
1. Choose option `5` (Filter / Search)
2. Select "Filter by Status"
3. Choose "Completed"
4. See only completed tasks ✓

### Change Theme to Hacker (Green):
1. Choose option `7` (Change theme)
2. Select "Hacker Theme"
3. Colors change to green ✓

### Create Yearly Recurring Task:
1. Choose option `1` (Add task)
2. Title: "Annual review"
3. Due date: "2025-12-31"
4. Recurrence: Choose `Yearly`
5. When you complete it, next year's task auto-creates! ✓

---

## 🎤 Voice Commands (Optional):

To use voice commands:
1. Install dependencies: `pip install SpeechRecognition PyAudio`
2. Choose option `8` (Voice Commands)
3. Speak naturally: "Add task buy milk high priority tomorrow tags personal shopping"
4. System parses and executes command ✓

**Note**: Voice is optional. All features work perfectly without it!

---

## 🐛 Known Issues: **ALL FIXED!**

- ✅ Rich markup error - Fixed
- ✅ Filter not showing results - Fixed
- ✅ Theme not changing - Fixed
- ✅ Voice commands crashing - Fixed

---

## 📊 What You'll See:

**Enhanced Table:**
```
╭───┬────┬─────────────────┬──────────┬──────────┬──────────────┬──────────────╮
│ # │ ID │ Title           │ Priority │ Due Date │ Tags         │ Status       │
├───┼────┼─────────────────┼──────────┼──────────┼──────────────┼──────────────┤
│ 1 │ 5  │ Update docs     │ 🔴 High  │ 2025-12-25│ 🏷️work 🏷️docs│ ⚠️ Overdue   │
│ 2 │ 3  │ Buy groceries   │ 🟢 Low   │ -        │ 🏷️personal   │ ✅ Done      │
│ 3 │ 2  │ Team meeting    │ 🟡 Medium│ 2026-01-02│ 🏷️work       │ ⏳ Pending   │
╰───┴────┴─────────────────┴──────────┴──────────┴──────────────┴──────────────╯
```

**Status Overview Panel:**
```
╭──────────────────────────────── Status Overview ─────────────────────────────╮
│ Completed: 1   Pending: 2   Overdue: 1   Total: 4                            │
╰───────────────────────────────────────────────────────────────────────────────╯
```

**Themes:**
- **Dark Theme** - Cyan colors (default)
- **Light Theme** - Blue colors
- **Hacker Theme** - Green colors (Matrix style!)

---

## ✨ Status: **PRODUCTION READY!**

All bugs fixed. All features working. Ready for real-world use!

**Just run**: `python phase1_complete_cli.py`
