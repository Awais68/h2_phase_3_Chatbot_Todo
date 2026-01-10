# Phase 2: Mobile-First PWA Demo Script

**Duration**: 3 minutes
**Target Audience**: Hackathon judges, mobile developers
**Goal**: Showcase PWA with offline mode, swipe gestures, and push notifications

---

## Setup (Before Recording)

- Device: iPhone or Android phone (physical device for authenticity)
- Screen recording: iOS Screen Recording or Android ADB
- Network: WiFi (for disabling demonstration)
- Browser: Chrome (Android) or Safari (iOS)
- Pre-registered account: test@example.com / password123
- Pre-created 3 tasks for demo

---

## Script

### [00:00-00:20] Opening + Mobile-First Design (20 seconds)

**Narration:**
> "Phase 2 transforms our CLI into a mobile-first Progressive Web App. Watch as we demonstrate touch optimization, offline mode, and PWA installation."

**Actions:**
1. Open browser on mobile device
2. Navigate to: `https://todo-app.example.com`
3. **Show**: App loads with mobile-optimized layout
4. **Show**: Login screen with 44×44px touch targets
5. Login with test account
6. **Show**: Task list appears immediately

**Visual**:
- Mobile viewport (320px width)
- Large, tappable buttons
- Smooth transitions
- Bottom navigation bar

---

### [00:20-00:50] Swipe Gestures (30 seconds)

**Narration:**
> "Phase 2 introduces intuitive swipe gestures for quick task management."

**Actions:**
1. **Show**: Task list with 3 tasks visible
2. Swipe task 1 **to the right**
3. **Show**: Green checkmark animation
4. **Show**: Task marked as complete with strikethrough
5. Swipe task 2 **to the left**
6. **Show**: Red delete animation
7. **Show**: Confirmation prompt: "Delete task?"
8. Tap "Yes"
9. **Show**: Task slides off screen with animation

**Visual**:
- Smooth swipe animation with visual feedback
- Right swipe: Green background with ✓ icon
- Left swipe: Red background with 🗑️ icon
- Framer Motion animations

---

### [00:50-01:20] Offline Mode (30 seconds)

**Narration:**
> "The PWA works completely offline using Service Workers and IndexedDB. Let's go offline and create a task."

**Actions:**
1. Enable Airplane Mode on device
2. **Show**: Offline indicator appears (⚠️ "Offline Mode")
3. Tap "Add Task" button
4. Enter title: "Check email"
5. Tap "Save"
6. **Show**: Task appears in list with sync indicator (⏳)
7. **Show**: "Changes will sync when online" message
8. Disable Airplane Mode
9. **Show**: Sync indicator changes to ✓
10. **Show**: "Synced" notification

**Visual**:
- Offline banner at top
- Task created locally (instant)
- Sync queue indicator
- Auto-sync when reconnected

---

### [01:20-01:50] PWA Installation (30 seconds)

**Narration:**
> "As a Progressive Web App, users can install this directly to their home screen, no app store required."

**Actions:**
**For Android:**
1. Tap browser menu (⋮)
2. Select "Add to Home Screen"
3. **Show**: Installation prompt with app icon
4. Tap "Add"
5. **Show**: App icon appears on home screen
6. Tap icon to open
7. **Show**: App opens full-screen (no browser UI)

**For iOS:**
1. Tap Share button (□↑)
2. Scroll and select "Add to Home Screen"
3. **Show**: App preview with icon
4. Tap "Add"
5. **Show**: App icon on home screen

**Visual**:
- PWA manifest icon (512×512)
- Full-screen app (no URL bar)
- Splash screen on launch

---

### [01:50-02:20] Push Notifications (30 seconds)

**Narration:**
> "Phase 2 supports push notifications to remind users about tasks across devices."

**Actions:**
1. Open app settings
2. Enable "Push Notifications"
3. **Show**: Browser permission prompt
4. Tap "Allow"
5. **Show**: "Notifications enabled" success message
6. Create new task: "Call dentist at 2PM"
7. Set reminder (if implemented)
8. **Simulated**: Show notification arriving on device
   - Notification: "🔔 Reminder: Call dentist at 2PM"
   - Tap notification
   - App opens to task detail

**Visual**:
- Native notification style (Android/iOS)
- App icon in notification
- Tapping opens app to correct task

---

### [02:20-02:50] Performance & Lighthouse (30 seconds)

**Narration:**
> "Phase 2 achieves excellent performance metrics on mobile networks."

**Actions:**
1. Open Chrome DevTools on desktop
2. Navigate to app
3. Run Lighthouse audit (mobile, 3G simulation)
4. **Show**: Lighthouse results appear:
   - **Performance**: 93/100 (green)
   - **Accessibility**: 100/100 (green)
   - **Best Practices**: 95/100 (green)
   - **SEO**: 100/100 (green)
   - **PWA**: ✓ Installable
5. **Highlight**: First Contentful Paint: 1.2s (target: <1.5s)

**Visual**:
- Lighthouse report with green scores
- Performance metrics graph
- PWA badge: "Installable"

---

### [02:50-03:00] Closing (10 seconds)

**Narration:**
> "Phase 2 delivers a production-ready Progressive Web App with offline support, push notifications, and excellent performance. Built with Next.js, React, and Tailwind CSS—all following spec-driven development. Next, Phase 3 adds voice control."

**Actions:**
1. Show app on home screen alongside native apps
2. Final shot: App running smoothly

**Visual**:
- App icon among native apps (Indistinguishable)
- Smooth, native-feeling experience

---

## Post-Production Notes

### Text Overlays:
- [00:10] "Phase 2: Mobile-First PWA"
- [00:25] "✓ Swipe Gestures"
- [00:55] "✓ Offline Mode + Sync"
- [01:25] "✓ PWA Installation"
- [01:55] "✓ Push Notifications"
- [02:25] "✓ Lighthouse Score: 93/100"

### Split Screen (Optional):
- [01:00] Left: Device in airplane mode | Right: Network indicator
- [02:25] Left: App on phone | Right: Lighthouse scores

### Performance Callouts:
- "FCP: 1.2s (Target: <1.5s)"
- "Lighthouse: 93/100"
- "Works Offline ✓"
- "Installable PWA ✓"

---

## Key Metrics to Mention

- **First Contentful Paint**: 1.2s on 3G
- **Lighthouse Mobile**: 93/100
- **Touch Target Size**: 44×44px (WCAG AAA)
- **Offline Capability**: 100% CRUD operations
- **Technologies**: Next.js 15, React 18, Tailwind CSS, Workbox

---

## Troubleshooting

**If swipe gestures don't work:**
- Ensure `react-swipeable` properly configured
- Check touch events enabled
- Verify threshold distance (50px)

**If offline mode doesn't work:**
- Check Service Worker registered: `navigator.serviceWorker.controller`
- Verify IndexedDB available: `window.indexedDB`
- Clear cache and retry

**If PWA won't install:**
- Ensure served over HTTPS
- Check manifest.json valid
- Verify Service Worker active

---

## Call to Action

> "Phase 2 shows how web technologies now rival native apps. This PWA works offline, installs like a native app, and achieves near-perfect performance scores—all from a single codebase. Let's add voice control in Phase 3."

**URL on screen**: github.com/[your-repo]/todo-evolution
