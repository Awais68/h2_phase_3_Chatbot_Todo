# Phase 1: Enhanced CLI Demo Script

**Duration**: 2 minutes
**Target Audience**: Hackathon judges, developers
**Goal**: Showcase colorful CLI with ASCII art, themes, and rich formatting

---

## Setup (Before Recording)

- Terminal: iTerm2 or Windows Terminal with dark background
- Font: Fira Code or JetBrains Mono (for ligatures)
- Resolution: 1920x1080
- Clear terminal history
- Pre-create 2 sample tasks for demo

---

## Script

### [00:00-00:15] Opening + ASCII Art (15 seconds)

**Narration:**
> "Welcome to Todo Evolution Phase 1. This is an enhanced command-line task manager built with Python, demonstrating spec-driven development with Claude Code."

**Actions:**
1. Open terminal
2. `cd` to project directory
3. Run: `python main.py`
4. **Show**: ASCII art banner appears with "TODO EVOLUTION" title
5. **Show**: Colored welcome panel with app version
6. **Show**: Task statistics at top (0 tasks initially)

**Visual**:
- ASCII art in cyan/magenta gradient
- Rich panel with rounded borders
- Statistics in yellow

---

### [00:15-00:45] Adding Tasks with Rich UI (30 seconds)

**Narration:**
> "Let's add some tasks. Notice the emoji indicators, loading animations, and color-coded feedback."

**Actions:**
1. Select option "1. Add new task" (use arrow keys)
2. Enter title: "Complete hackathon demo"
3. Enter description: "Record all 5 phase demonstrations"
4. **Show**: Loading spinner with "Creating task..." animation
5. **Show**: Success message with ✓ emoji in green
6. **Repeat**: Add second task - "Prepare deployment"
7. **Show**: Task count updates to "2 tasks (0 done, 2 pending)"

**Visual**:
- Questionary arrow key navigation (▸ indicator)
- Loading animation with spinning cursor
- Green success notification
- Updated statistics in yellow

---

### [00:45-01:15] Viewing Tasks with Rich Tables (30 seconds)

**Narration:**
> "Phase 1 transforms the task list into a beautiful, color-coded Rich table with status indicators and formatting."

**Actions:**
1. Select option "2. View all tasks"
2. **Show**: Rich table appears with:
   - Column headers: ID, Status, Title, Created
   - Task 1: • (yellow pending indicator) "Complete hackathon demo"
   - Task 2: • (yellow pending indicator) "Prepare deployment"
   - Table borders in cyan
   - Alternating row colors for readability
3. **Pause**: Let viewers see the table for 3 seconds

**Visual**:
- Rich Table with rounded borders
- Status column: • (yellow) for pending, ✓ (green) for complete
- Timestamps formatted nicely
- Emojis render correctly

---

### [01:15-01:35] Theme Switching (20 seconds)

**Narration:**
> "Phase 1 includes theme switching. Watch as we switch from dark to hacker mode."

**Actions:**
1. Return to main menu (if not there)
2. Access theme menu (if implemented)
3. Switch to "Hacker" theme
4. **Show**: Interface changes to:
   - Green-on-black color scheme
   - Matrix-style ASCII art
   - Green status indicators
   - Monospace aesthetic
5. View task list again to show themed table

**Visual**:
- Instant theme change
- Green text on black background
- All UI elements re-colored consistently

---

### [01:35-01:50] Completing & Deleting Tasks (15 seconds)

**Narration:**
> "Let's complete a task. Notice the progress bar and visual feedback."

**Actions:**
1. Select option "5. Mark task complete/incomplete"
2. Enter task ID: 1
3. **Show**: Progress bar animation
4. **Show**: Success message: "✓ Task marked as complete!"
5. View task list again
6. **Show**: Task 1 now has ✓ (green) status indicator
7. **Show**: Statistics update: "2 tasks (1 done, 1 pending)"

**Visual**:
- Progress bar fills from left to right (Rich Progress)
- Status changes from • (yellow) to ✓ (green)
- Statistics update in real-time

---

### [01:50-02:00] Closing (10 seconds)

**Narration:**
> "Phase 1 demonstrates how spec-driven development with Claude Code can transform a basic CLI into a beautiful, colorful user experience. All code was generated from specifications—no manual coding. Next, we'll see Phase 2's mobile-first PWA."

**Actions:**
1. Select option "6. Exit"
2. **Show**: Graceful exit message: "Thanks for using Todo Evolution!"
3. Terminal returns to prompt

**Visual**:
- Clean exit
- Farewell message in cyan

---

## Post-Production Notes

### Text Overlays:
- [00:05] "Phase 1: Enhanced CLI"
- [00:20] "✓ ASCII Art Title"
- [00:25] "✓ Emoji Indicators"
- [00:50] "✓ Rich Table Formatting"
- [01:20] "✓ Theme Switching"
- [01:45] "✓ Progress Animations"

### Background Music:
- Upbeat, techy instrumental
- Low volume (30%)
- Fade out at end

### Transitions:
- Quick fade between major sections
- Zoom in slightly on key visual elements (table, ASCII art)

### Final Frame:
- Text: "Phase 1 Complete - 100 points"
- Text: "Built with Claude Code + Spec-Driven Development"
- Text: "Next: Phase 2 - Mobile PWA"

---

## Troubleshooting

**If ASCII art doesn't render:**
- Ensure terminal supports UTF-8 encoding
- Check font supports box-drawing characters
- Fallback: Show simple text title

**If colors don't show:**
- Verify terminal supports 256 colors: `echo $TERM`
- Should be `xterm-256color` or similar
- Rich library handles fallback automatically

**If animations stutter:**
- Record at 60fps
- Use screen recording software that handles terminal animations (Asciinema or OBS)
- Edit video to smooth out any hiccups

---

## Key Metrics to Mention (Optional)

- **Startup Time**: <500ms
- **Menu Response**: <50ms
- **Lines of Code**: ~800 (all Claude Code generated)
- **Libraries Used**: Rich, Art, Questionary, Emoji
- **Python Version**: 3.13+

---

## Backup Plan

If live demo fails, have these ready:
1. Pre-recorded GIF of CLI in action
2. Screenshots of key features (ASCII art, table, themes)
3. Code snippets showing Rich library usage

---

## Call to Action (End of Video)

> "Phase 1 shows what's possible when you combine thoughtful specifications with AI-powered code generation. Every feature you saw was specified in detail, then generated by Claude Code. Let's see what happens when we take this to the web in Phase 2."

**URL on screen**: github.com/[your-repo]/todo-evolution
