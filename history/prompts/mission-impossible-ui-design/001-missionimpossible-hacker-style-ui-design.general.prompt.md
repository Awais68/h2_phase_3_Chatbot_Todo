---
id: "001"
title: "MissionImpossible Hacker-Style UI Design"
stage: "general"
date: "2026-01-03"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "011-phase2-deploy"
user: "Claude Code User"
command: "Design a hacker-style UI for a MissionImpossible todo/mission management web application"
labels: ["ui-design","cyberpunk","tailwind-css","accessibility","animation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "/media/data/hackathon series/hackathon-2/phase-ii_Web_App_Full Stack/specs/mission-impossible-ui-design.md"
tests: []
---

## Prompt

Design a hacker-style UI for a "MissionImpossible" todo/mission management web application:

**Design Language:**
- Background: dark-blue-900 (#0a0f1c or similar)
- Primary text: cyan (#00ffff or similar hacker green/cyan)
- Accent colors: neon green, electric blue, magenta
- Typography: Google Fonts (Orbitron, Roboto Mono, or similar tech font)
- Style: Cyberpunk/hacker aesthetic with terminal-like elements

**Required Pages/Sections:**

1. **Landing Page:**
   - Navbar: "Space", "Protocol", "Login", "Start for Free" menu items
   - Hero: "MissionImpossible" heading, tagline, CTA buttons
   - Features: 3-5 key features with icons
   - How It Works: 3-step visual guide
   - Footer: Links and newsletter

2. **Auth Pages (with clippath transition):**
   - Sign up page
   - Sign in page with "Add Secrets" instead of username
   - Terminal-style input fields
   - Smooth clippath transitions

3. **Dashboard:**
   - Left sidebar with mission tabs
   - Task cards with colorful glowing shadows
   - "Initilize" button for adding tasks
   - Search and filter controls
   - Charts for status visualization
   - Particles.js animated background

**UI Elements:**
- Hover effects: subtle glow, color shifts
- Loading state: "Initilizing Missions..." text
- Voice command indicator
- Mobile-responsive design

Please provide:
- Color palette with hex codes
- Typography recommendations
- Component design specifications
- Animation timing recommendations
- Layout grid specifications

Return a comprehensive design guide with specific Tailwind classes and design tokens.

## Response snapshot

Created comprehensive design guide at `/media/data/hackathon series/hackathon-2/phase-ii_Web_App_Full Stack/specs/mission-impossible-ui-design.md` containing:

1. **Color Palette (RGB format for Tailwind):**
   - Background: `rgb(var(--background-primary) / <alpha-value>)` = #0A0F1C
   - Cyan (primary): `#00FFFF` (0, 255, 255)
   - Neon Green: `#39FF14` (57, 255, 20)
   - Magenta: `#FF0080` (255, 0, 128)
   - Text colors, border colors, glow colors

2. **Typography System:**
   - Orbitron (display), Roboto Mono (code), Inter (body)
   - Fluid typography with clamp()
   - Type scale table

3. **Design Tokens:**
   - Spacing scale, border radius, transitions, z-index

4. **Layout Grid:**
   - Mobile-first breakpoints (xs to 3xl)
   - Container classes, grid layouts, flex utilities

5. **Component Specifications:**
   - Button (primary/secondary/ghost variants)
   - Terminal-style Input with cursor animation
   - Card with glowing corner accent
   - Navbar with animated nav links
   - Dashboard sidebar
   - Modal (terminal-style)
   - Badge/Tag components
   - Loading states (skeleton, terminal text, spinner)
   - Voice command indicator with animated waves

6. **Animation System:**
   - CSS keyframes (pulse-glow, scan-line, glitch, typewriter, float, matrix-rain)
   - Hover effects with glow transitions
   - Clippath transition for auth pages
   - Particles.js configuration

7. **Page Specifications:**
   - Landing Page with hero, features, how it works sections
   - Auth pages with Framer Motion clippath transitions
   - Dashboard with sidebar, stats grid, mission cards

8. **Accessibility Guidelines:**
   - Color contrast requirements (4.5:1, 3:1)
   - Focus states with ring utilities
   - ARIA attributes for buttons, modals, status badges
   - Touch target minimums (44x44px)
   - Screen reader support (sr-only, aria-live)

## Outcome

- ✅ Impact: Created production-ready design guide for hacker/cyberpunk themed mission management UI
- 🧪 Tests: No tests required (design specification)
- 📁 Files: 1 spec file created with ~600 lines of comprehensive design documentation
- 🔁 Next prompts: Component implementation, frontend page creation
- 🧠 Reflection: Design follows mobile-first approach with Tailwind CSS v4 pattern. Included full Tailwind config extension with custom colors, shadows, animations, and font families. All components include accessibility considerations.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (design spec)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create component library with actual React components implementing these designs
