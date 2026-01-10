# MissionImpossible - Hacker-Style UI Design Guide

A comprehensive design specification for the cyberpunk/hacker-themed mission management application.

---

## Table of Contents

1. [Color Palette](#1-color-palette)
2. [Typography System](#2-typography-system)
3. [Design Tokens](#3-design-tokens)
4. [Layout Grid System](#4-layout-grid-system)
5. [Component Specifications](#5-component-specifications)
6. [Animation System](#6-animation-system)
7. [Page Specifications](#7-page-specifications)
8. [Accessibility Guidelines](#8-accessibility-guidelines)

---

## 1. Color Palette

### 1.1 Base Colors (RGB Format for Tailwind)

```css
:root {
  /* ========================================
     HACKER THEME - DARK CYBERPUNK PALETTE
     ======================================== */

  /* Primary Background - Deep Navy/Black */
  --background-primary: 10 15 28;        /* #0A0F1C */
  --background-secondary: 12 20 36;      /* #0C1424 */
  --background-tertiary: 15 25 45;       /* #0F192D */

  /* Surface Colors */
  --surface-elevated: 20 30 55;         /* #141E37 */
  --surface-card: 17 26 46;             /* #111A2E */
  --surface-glass: 10 15 28 0.8;        /* rgba(10, 15, 28, 0.8) */

  /* ========================================
     PRIMARY ACCENT - CYAN/ELECTRIC BLUE
     ======================================== */
  --cyan-50: 224 242 254;
  --cyan-100: 186 230 253;
  --cyan-200: 125 211 252;
  --cyan-300: 56 189 248;
  --cyan-400: 14 165 233;
  --cyan-500: 0 255 255;                /* #00FFFF - Primary Brand */
  --cyan-400-glow: 34 211 238;
  --cyan-300-glow: 56 189 248;

  /* ========================================
     SECONDARY ACCENT - NEON GREEN
     ======================================== */
  --neon-green-50: 240 253 244;
  --neon-green-100: 220 252 231;
  --neon-green-200: 187 247 208;
  --neon-green-300: 134 239 172;
  --neon-green-400: 74 222 128;
  --neon-green-500: 57 255 20;          /* #39FF14 - Neon Green */
  --neon-green-glow: 132 255 89;

  /* ========================================
     TERTIARY ACCENT - MAGENTA/PINK
     ======================================== */
  --magenta-50: 253 242 248;
  --magenta-100: 252 231 243;
  --magenta-200: 251 207 232;
  --magenta-300: 249 168 212;
  --magenta-400: 244 114 182;
  --magenta-500: 255 0 128;             /* #FF0080 - Magenta */
  --magenta-glow: 255 55 158;

  /* ========================================
     SEMANTIC COLORS
     ======================================== */
  --success: 34 197 94;                 /* Green */
  --warning: 245 158 11;                /* Amber */
  --error: 239 68 68;                   /* Red */
  --info: 59 130 246;                   /* Blue */

  /* ========================================
     TEXT COLORS
     ======================================== */
  --text-primary: 240 240 245;          /* Nearly white */
  --text-secondary: 160 170 200;        /* Muted cyan-gray */
  --text-muted: 100 110 140;            /* Dimmed */
  --text-accent: 0 255 255;             /* Cyan accent */

  /* ========================================
     BORDER COLORS
     ======================================== */
  --border-subtle: 40 50 80;
  --border-default: 60 80 120;
  --border-accent: 0 255 255;
  --border-glow: 0 255 255 0.5;

  /* ========================================
     GLOW COLORS
     ======================================== */
  --glow-cyan: 0 255 255;
  --glow-green: 57 255 20;
  --glow-magenta: 255 0 128;
  --glow-blue: 59 130 246;
}
```

### 1.2 Tailwind Color Configuration

```typescript
// tailwind.config.ts (CSS-based approach in globals.css)
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Hacker/Cyberpunk Theme
        hacker: {
          bg: {
            primary: "rgb(var(--background-primary) / <alpha-value>)",
            secondary: "rgb(var(--background-secondary) / <alpha-value>)",
            tertiary: "rgb(var(--background-tertiary) / <alpha-value>)",
          },
          surface: {
            elevated: "rgb(var(--surface-elevated) / <alpha-value>)",
            card: "rgb(var(--surface-card) / <alpha-value>)",
            glass: "rgb(var(--surface-glass) / <alpha-value>)",
          },
          cyan: {
            DEFAULT: "rgb(var(--cyan-500) / <alpha-value>)",
            glow: "rgb(var(--cyan-400-glow) / <alpha-value>)",
            subtle: "rgb(var(--cyan-300) / <alpha-value>)",
          },
          neon: {
            green: "rgb(var(--neon-green-500) / <alpha-value>)",
            glow: "rgb(var(--neon-green-glow) / <alpha-value>)",
          },
          magenta: {
            DEFAULT: "rgb(var(--magenta-500) / <alpha-value>)",
            glow: "rgb(var(--magenta-glow) / <alpha-value>)",
          },
          text: {
            primary: "rgb(var(--text-primary) / <alpha-value>)",
            secondary: "rgb(var(--text-secondary) / <alpha-value>)",
            muted: "rgb(var(--text-muted) / <alpha-value>)",
            accent: "rgb(var(--text-accent) / <alpha-value>)",
          },
          border: {
            subtle: "rgb(var(--border-subtle) / <alpha-value>)",
            default: "rgb(var(--border-default) / <alpha-value>)",
            accent: "rgb(var(--border-accent) / <alpha-value>)",
          },
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["var(--font-roboto-mono)", "monospace"],
        display: ["var(--font-orbitron)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        "glow-cyan": "0 0 20px rgba(0, 255, 255, 0.4), 0 0 40px rgba(0, 255, 255, 0.2)",
        "glow-green": "0 0 20px rgba(57, 255, 20, 0.4), 0 0 40px rgba(57, 255, 20, 0.2)",
        "glow-magenta": "0 0 20px rgba(255, 0, 128, 0.4), 0 0 40px rgba(255, 0, 128, 0.2)",
        "glow-blue": "0 0 20px rgba(59, 130, 246, 0.4), 0 0 40px rgba(59, 130, 246, 0.2)",
        "inner-glow": "inset 0 0 20px rgba(0, 255, 255, 0.1)",
      },
      animation: {
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "scan-line": "scan-line 3s linear infinite",
        "glitch": "glitch 1s linear infinite",
        "typewriter": "typewriter 2s steps(40, end)",
        "float": "float 6s ease-in-out infinite",
        "matrix-rain": "matrix-rain 0.5s linear infinite",
      },
      keyframes: {
        "pulse-glow": {
          "0%, 100%": { boxShadow: "0 0 20px rgba(0, 255, 255, 0.4)" },
          "50%": { boxShadow: "0 0 40px rgba(0, 255, 255, 0.8)" },
        },
        "scan-line": {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
        "glitch": {
          "2%, 64%": { transform: "translate(2px,0) skew(0deg)" },
          "4%, 60%": { transform: "translate(-2px,0) skew(0deg)" },
          "62%": { transform: "translate(0,0) skew(5deg)" },
        },
        "typewriter": {
          "from": { width: "0" },
          "to": { width: "100%" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "matrix-rain": {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
```

### 1.3 Color Usage Examples

```tsx
// Background applications
<div className="bg-hacker-bg-primary">...</div>
<div className="bg-hacker-bg-secondary">...</div>
<div className="bg-hacker-surface-card">...</div>

// Text applications
<p className="text-hacker-text-primary">...</p>
<p className="text-hacker-text-secondary">...</p>
<p className="text-hacker-text-accent">...</p>

// Border applications
<div className="border border-hacker-border-default">...</div>
<div className="border border-hacker-border-accent">...</div>

// Glow effects
<button className="shadow-glow-cyan">...</button>
<div className="shadow-glow-green">...</div>
```

---

## 2. Typography System

### 2.1 Google Fonts Configuration

```css
/* In app/layout.tsx or globals.css import */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Roboto+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
```

### 2.2 Font Variables

```css
:root {
  /* Display Font - Headings */
  --font-orbitron: 'Orbitron', system-ui, sans-serif;

  /* Monospace Font - Code, Terminal, Data */
  --font-roboto-mono: 'Roboto Mono', 'Fira Code', monospace;

  /* Body Font - Readable UI text */
  --font-inter: 'Inter', system-ui, -apple-system, sans-serif;

  /* Font Sizes - Fluid typography with clamp */
  --font-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --font-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --font-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --font-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --font-2xl: clamp(1.5rem, 1.3rem + 1vw, 1.875rem);
  --font-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --font-4xl: clamp(2.25rem, 1.8rem + 2.25vw, 3.125rem);
  --font-5xl: clamp(3rem, 2.2rem + 4vw, 4rem);

  /* Line Heights */
  --leading-tight: 1.1;
  --leading-snug: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;

  /* Letter Spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
  --tracking-widest: 0.1em;
}
```

### 2.3 Typography Classes

```tsx
// Display typography (Orbitron)
<h1 className="font-display text-4xl font-bold tracking-wider text-hacker-cyan">MissionImpossible</h1>
<h2 className="font-display text-3xl font-semibold text-hacker-text-primary">Initialize Protocol</h2>
<h3 className="font-display text-2xl font-medium text-hacker-text-secondary">Task Overview</h3>

// Monospace typography (Roboto Mono)
<code className="font-mono text-sm text-hacker-neon-green">const mission = "complete"</code>
<p className="font-mono text-xs text-hacker-text-muted">$ ./execute --force</p>
<div className="font-mono text-lg text-hacker-cyan">> Initializing...</div>

// Body typography (Inter)
<p className="font-sans text-base leading-relaxed text-hacker-text-primary">Task content goes here</p>
<span className="font-sans text-sm font-medium text-hacker-text-secondary">Status: Active</span>
```

### 2.4 Type Scale

| Element | Size | Weight | Line Height | Letter Spacing |
|---------|------|--------|-------------|----------------|
| Display (H1) | 3-4rem | 800 | tight | wider |
| Heading (H2) | 2-2.5rem | 700 | tight | wide |
| Heading (H3) | 1.5-1.875rem | 600 | snugh | normal |
| Heading (H4) | 1.25-1.5rem | 600 | normal | normal |
| Body Large | 1.125rem | 500 | relaxed | normal |
| Body | 1rem | 400 | normal | normal |
| Body Small | 0.875rem | 400 | normal | normal |
| Caption | 0.75rem | 400 | normal | wide |
| Code | 0.875rem | 500 | normal | tighter |

---

## 3. Design Tokens

### 3.1 Spacing System

```css
:root {
  /* Standard spacing scale */
  --space-0: 0;
  --space-1: 0.25rem;    /* 4px */
  --space-2: 0.5rem;     /* 8px */
  --space-3: 0.75rem;    /* 12px */
  --space-4: 1rem;       /* 16px */
  --space-5: 1.25rem;    /* 20px */
  --space-6: 1.5rem;     /* 24px */
  --space-8: 2rem;       /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */

  /* Special spacing for hacker theme */
  --space-terminal: 1rem;
  --space-glow: 0.25rem;
  --space-card-padding: 1.5rem;
  --space-section: 4rem;
}
```

### 3.2 Border Radius

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-3xl: 1.5rem;
  --radius-full: 9999px;

  /* Hacker-specific */
  --radius-terminal: 0.25rem;
  --radius-card: 0.5rem;
  --radius-button: 0.375rem;
  --radius-input: 0.25rem;
}
```

### 3.3 Transitions

```css
:root {
  /* Transition durations */
  --duration-fast: 75ms;
  --duration-normal: 150ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;
  --duration-slowest: 750ms;

  /* Transition easings */
  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

  /* Common transition utilities */
  --transition-fast: var(--duration-fast) var(--ease-linear);
  --transition-normal: var(--duration-normal) var(--ease-out);
  --transition-slow: var(--duration-slow) var(--ease-in-out);
  --transition-glow: var(--duration-slow) var(--ease-in-out);
}
```

### 3.4 Z-Index Scale

```css
:root {
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
  --z-toast: 1080;
  --z-loading-overlay: 1090;
}
```

---

## 4. Layout Grid System

### 4.1 Breakpoint Configuration

```typescript
// Mobile-first breakpoints
const breakpoints = {
  xs: "475px",    // Extra small phones
  sm: "640px",    // Small phones + (iPhone SE, etc.)
  md: "768px",    // Tablets (iPad vertical)
  lg: "1024px",   // Tablets (iPad horizontal) + Small desktops
  xl: "1280px",   // Desktops
  "2xl": "1536px", // Large screens
  "3xl": "1920px", // Extra large screens
};
```

### 4.2 Container Classes

```tsx
// Mobile-first container
<div className="w-full mx-auto px-4 sm:px-6 md:px-8 lg:px-12 max-w-screen-2xl">
  {/* Content */}
</div>

// Full-width sections
<section className="w-full min-h-screen bg-hacker-bg-primary">
  <div className="container mx-auto px-4">...</div>
</section>

// Centered card container
<div className="min-h-screen flex items-center justify-center p-4">
  <div className="w-full max-w-md">...</div>
</section>
```

### 4.3 Grid Layouts

```tsx
// Auto-fit responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
  {/* Cards */}
</div>

// Dashboard sidebar layout
<div className="flex min-h-screen">
  <aside className="w-64 hidden lg:block flex-shrink-0">
    <Sidebar />
  </aside>
  <main className="flex-1 min-w-0">
    <Dashboard />
  </main>
</div>

// Mobile drawer navigation
<div className="flex">
  <nav className="fixed inset-y-0 left-0 w-64 transform -translate-x-full lg:translate-x-0 transition-transform">
    <Sidebar />
  </nav>
  <main className="flex-1 lg:ml-64">
    <Dashboard />
  </main>
</div>
```

### 4.4 Flex Utilities

```tsx
// Flex center
<div className="flex items-center justify-center min-h-screen">...</div>

// Flex between
<div className="flex items-center justify-between">...</div>

// Flex column mobile, row desktop
<div className="flex flex-col md:flex-row gap-4">...</div>

// Sticky header
<header className="sticky top-0 z-50 bg-hacker-bg-primary/95 backdrop-blur">...</header>
```

---

## 5. Component Specifications

### 5.1 Button Component

```tsx
interface ButtonProps {
  variant: "primary" | "secondary" | "ghost" | "danger";
  size: "sm" | "md" | "lg";
  loading?: boolean;
  disabled?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}

// Primary Button - Cyan glow effect
<button
  className="
    font-display font-medium tracking-wide
    px-6 py-3
    bg-hacker-cyan text-hacker-bg-primary
    rounded-lg
    border border-hacker-cyan
    shadow-glow-cyan
    hover:bg-hacker-cyan/90 hover:shadow-glow-cyan hover:scale-105
    active:scale-95
    transition-all duration-300
    focus:outline-none focus:ring-2 focus:ring-hacker-cyan focus:ring-offset-2 focus:ring-offset-hacker-bg-primary
    disabled:opacity-50 disabled:cursor-not-allowed
  "
>
  Initialize Mission
</button>

// Secondary Button - Neon green outline
<button
  className="
    font-display font-medium
    px-6 py-3
    bg-transparent
    text-hacker-neon-green
    rounded-lg
    border border-hacker-neon-green
    shadow-glow-green
    hover:bg-hacker-neon-green/10 hover:shadow-glow-green
    transition-all duration-300
  "
>
  Execute
</button>

// Ghost Button - Subtle
<button
  className="
    font-sans font-medium
    px-4 py-2
    bg-transparent
    text-hacker-text-secondary
    rounded-md
    hover:bg-hacker-surface-card hover:text-hacker-text-primary
    transition-all duration-200
  "
>
  Cancel
</button>

// Loading state
<button
  className="
    px-6 py-3
    bg-hacker-cyan/50 text-hacker-bg-primary
    rounded-lg
    cursor-wait
    flex items-center gap-2
  "
>
  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
  </svg>
  <span>Initializing...</span>
</button>
```

### 5.2 Input Component (Terminal Style)

```tsx
interface InputProps {
  label?: string;
  placeholder?: string;
  type?: "text" | "email" | "password" | "search";
  error?: string;
  hint?: string;
  leftElement?: React.ReactNode;
  rightElement?: React.ReactNode;
}

// Terminal-style input
<div className="space-y-2">
  <label className="block font-mono text-sm text-hacker-cyan">
    <span className="text-hacker-neon-green">$</span> Add Secrets
  </label>
  <div className="relative">
    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <span className="text-hacker-neon-green font-mono">{'>'}</span>
    </div>
    <input
      type="text"
      placeholder="Enter your secrets..."
      className="
        w-full
        pl-8 pr-4 py-3
        bg-hacker-surface-card
        text-hacker-text-primary
        font-mono text-sm
        rounded-lg
        border border-hacker-border-subtle
        placeholder:text-hacker-text-muted
        focus:outline-none
        focus:border-hacker-cyan
        focus:ring-1 focus:ring-hacker-cyan
        focus:shadow-glow-cyan
        transition-all duration-300
      "
    />
    <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
      <span className="animate-pulse w-2 h-4 bg-hacker-cyan"></span>
    </div>
  </div>
  {error && (
    <p className="text-sm text-red-400 font-mono">
      <span className="text-red-500">[ERROR]</span> {error}
    </p>
  )}
</div>

// Search input with icon
<div className="relative">
  <input
    type="search"
    className="
      w-full
      px-4 py-3 pl-10
      bg-hacker-surface-card
      border border-hacker-border-default
      rounded-lg
      text-hacker-text-primary
      placeholder:text-hacker-text-muted
      focus:border-hacker-cyan focus:ring-1 focus:ring-hacker-cyan
      transition-all duration-300
    "
  />
  <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-hacker-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
</div>
```

### 5.3 Card Component

```tsx
interface CardProps {
  title?: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  glowColor?: "cyan" | "green" | "magenta" | "none";
}

// Mission task card with glowing border
<div
  className="
    relative
    p-6
    bg-hacker-surface-card
    rounded-xl
    border border-hacker-border-subtle
    hover:border-hacker-border-default
    transition-all duration-300
    group
  "
>
  {/* Glowing corner accent */}
  <div className="absolute top-0 right-0 w-2 h-2 bg-hacker-cyan rounded-full shadow-glow-cyan" />

  {/* Card header */}
  <div className="flex items-start justify-between mb-4">
    <div>
      <h3 className="font-display text-lg font-semibold text-hacker-text-primary">
        {title}
      </h3>
      {subtitle && (
        <p className="font-mono text-xs text-hacker-text-muted mt-1">
          {subtitle}
        </p>
      )}
    </div>
    <span className="px-2 py-1 text-xs font-mono rounded bg-hacker-cyan/10 text-hacker-cyan border border-hacker-cyan/20">
      ACTIVE
    </span>
  </div>

  {/* Card content */}
  <div className="space-y-3">
    {children}
  </div>

  {/* Card footer */}
  {footer && (
    <div className="mt-4 pt-4 border-t border-hacker-border-subtle">
      {footer}
    </div>
  )}
</div>
```

### 5.4 Navigation (Navbar)

```tsx
// Navbar component
<nav className="sticky top-0 z-50 bg-hacker-bg-primary/95 backdrop-blur-md border-b border-hacker-border-subtle">
  <div className="container mx-auto px-4">
    <div className="flex items-center justify-between h-16">
      {/* Logo */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-hacker-cyan rounded flex items-center justify-center shadow-glow-cyan">
          <span className="text-hacker-bg-primary font-display font-bold text-lg">M</span>
        </div>
        <span className="font-display text-xl font-bold text-hacker-text-primary tracking-wider">
          Mission<span className="text-hacker-cyan">Impossible</span>
        </span>
      </div>

      {/* Desktop Navigation */}
      <div className="hidden md:flex items-center gap-8">
        <a href="/space" className="nav-link">Space</a>
        <a href="/protocol" className="nav-link">Protocol</a>
        <a href="/login" className="nav-link">Login</a>
        <button className="btn-primary">
          Start for Free
        </button>
      </div>

      {/* Mobile Menu Toggle */}
      <button className="md:hidden p-2 text-hacker-text-secondary hover:text-hacker-text-primary">
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>
  </div>
</nav>

// Nav link styles
<style jsx>{`
  .nav-link {
    @apply font-sans text-sm font-medium text-hacker-text-secondary hover:text-hacker-cyan transition-colors duration-200 relative;
  }
  .nav-link::after {
    content: '';
    @apply absolute -bottom-1 left-0 w-0 h-0.5 bg-hacker-cyan transition-all duration-300;
  }
  .nav-link:hover::after {
    @apply w-full;
  }
`}</style>
```

### 5.5 Sidebar (Dashboard)

```tsx
// Dashboard sidebar
<aside className="w-64 h-screen bg-hacker-bg-secondary border-r border-hacker-border-subtle flex flex-col">
  {/* Logo section */}
  <div className="p-4 border-b border-hacker-border-subtle">
    <div className="flex items-center gap-2">
      <div className="w-8 h-8 bg-hacker-cyan rounded flex items-center justify-center">
        <span className="text-hacker-bg-primary font-display font-bold">M</span>
      </div>
      <span className="font-display font-bold text-hacker-text-primary">Mission</span>
    </div>
  </div>

  {/* Navigation links */}
  <nav className="flex-1 p-4 space-y-2">
    {['All Missions', 'Active', 'Completed', 'Archived'].map((item, index) => (
      <a
        key={item}
        href="#"
        className={`
          flex items-center gap-3 px-4 py-3 rounded-lg
          font-sans text-sm font-medium
          transition-all duration-200
          ${index === 0
            ? 'bg-hacker-surface-card text-hacker-cyan border border-hacker-cyan/30'
            : 'text-hacker-text-secondary hover:text-hacker-text-primary hover:bg-hacker-surface-card'
          }
        `}
      >
        <span className="w-2 h-2 rounded-full bg-current" />
        {item}
      </a>
    ))}
  </nav>

  {/* User section */}
  <div className="p-4 border-t border-hacker-border-subtle">
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-hacker-cyan to-hacker-neon-green flex items-center justify-center">
        <span className="text-hacker-bg-primary font-mono font-bold">A</span>
      </div>
      <div>
        <p className="font-sans text-sm font-medium text-hacker-text-primary">Agent</p>
        <p className="font-mono text-xs text-hacker-text-muted">Level 5</p>
      </div>
    </div>
  </div>
</aside>
```

### 5.6 Modal/Dialog

```tsx
// Terminal-style modal
<div className="fixed inset-0 z-50 flex items-center justify-center p-4">
  {/* Backdrop */}
  <div className="absolute inset-0 bg-hacker-bg-primary/80 backdrop-blur-sm" />

  {/* Modal content */}
  <div className="relative w-full max-w-md bg-hacker-surface-card rounded-xl border border-hacker-border-default shadow-2xl overflow-hidden">
    {/* Header */}
    <div className="flex items-center justify-between px-4 py-3 border-b border-hacker-border-subtle bg-hacker-bg-tertiary">
      <div className="flex items-center gap-2">
        <span className="flex gap-1.5">
          <span className="w-3 h-3 rounded-full bg-red-500" />
          <span className="w-3 h-3 rounded-full bg-yellow-500" />
          <span className="w-3 h-3 rounded-full bg-green-500" />
        </span>
      </div>
      <span className="font-mono text-xs text-hacker-text-muted">new_mission.exe</span>
      <button className="p-1 text-hacker-text-muted hover:text-hacker-text-primary transition-colors">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    {/* Body */}
    <div className="p-6">
      <h2 className="font-display text-xl font-bold text-hacker-text-primary mb-4">
        Initialize New Mission
      </h2>
      {/* Form content */}
    </div>

    {/* Footer */}
    <div className="flex justify-end gap-3 px-6 py-4 border-t border-hacker-border-subtle">
      <button className="btn-ghost">Cancel</button>
      <button className="btn-primary">Initialize</button>
    </div>
  </div>
</div>
```

### 5.7 Badge/Tag Component

```tsx
// Status badge
<span className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-mono bg-hacker-neon-green/10 text-hacker-neon-green border border-hacker-neon-green/30">
  <span className="w-1.5 h-1.5 rounded-full bg-hacker-neon-green animate-pulse" />
  COMPLETED
</span>

// Priority badge
<span className="inline-flex items-center px-2 py-1 rounded text-xs font-mono bg-hacker-magenta/10 text-hacker-magenta border border-hacker-magenta/30">
  CRITICAL
</span>

// Category tag
<span className="inline-flex items-center px-2 py-1 rounded text-xs font-mono bg-hacker-cyan/10 text-hacker-cyan border border-hacker-cyan/30">
  DEVELOPMENT
</span>
```

### 5.8 Loading States

```tsx
// Loading skeleton
<div className="space-y-4 animate-pulse">
  <div className="h-6 bg-hacker-surface-card rounded w-1/3" />
  <div className="h-4 bg-hacker-surface-card rounded w-full" />
  <div className="h-4 bg-hacker-surface-card rounded w-2/3" />
</div>

// Terminal loading text
<div className="font-mono text-sm text-hacker-cyan">
  <span className="animate-pulse">Initializing Missions</span>
  <span className="animate-pulse delay-75">.</span>
  <span className="animate-pulse delay-100">.</span>
  <span className="animate-pulse delay-150">.</span>
</div>

// Spinner
<div className="flex items-center justify-center gap-2">
  <div className="w-6 h-6 border-2 border-hacker-cyan/30 border-t-hacker-cyan rounded-full animate-spin" />
  <span className="font-mono text-sm text-hacker-cyan">Loading...</span>
</div>
```

### 5.9 Voice Command Indicator

```tsx
// Voice command active indicator
<div className="fixed bottom-6 right-6 z-40">
  <div className="flex items-center gap-3 px-4 py-3 bg-hacker-surface-card rounded-full border border-hacker-neon-green shadow-glow-green">
    {/* Animated voice waves */}
    <div className="flex items-end gap-0.5 h-6">
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className="w-1 bg-hacker-neon-green rounded-full animate-pulse"
          style={{
            height: `${Math.random() * 100}%`,
            animationDelay: `${i * 0.1}s`,
          }}
        />
      ))}
    </div>
    <span className="font-mono text-sm text-hacker-neon-green">Listening...</span>
  </div>
</div>
```

---

## 6. Animation System

### 6.1 Animation Timing

```css
:root {
  /* CSS Custom Properties for animations */
  --animation-duration-fast: 150ms;
  --animation-duration-normal: 300ms;
  --animation-duration-slow: 500ms;
  --animation-duration-slower: 750ms;

  --animation-ease-linear: linear;
  --animation-ease-ease: ease;
  --animation-ease-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --animation-ease-ease-out: cubic-bezier(0, 0, 0.2, 1);
  --animation-ease-ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --animation-ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### 6.2 Animation Classes

```tsx
// Fade in
<div className="animate-fade-in">...</div>

// Fade out
<div className="animate-fade-out">...</div>

// Slide up
<div className="animate-slide-up">...</div>

// Slide down
<div className="animate-slide-down">...</div>

// Scale in
<div className="animate-scale-in">...</div>

// Glitch effect (for headings)
<h1 className="animate-glitch">MissionImpossible</h1>

// Pulse glow (for important elements)
<div className="animate-pulse-glow">...</div>

// Scan line (for terminal backgrounds)
<div className="animate-scan-line">...</div>

// Float (for cards/icons)
<div className="animate-float">...</div>
```

### 6.3 Clippath Transition (Auth Pages)

```tsx
// Clippath transition animation
const clipPathVariants = {
  initial: {
    clipPath: "polygon(0 0, 100% 0, 100% 0, 0 0)",
  },
  animate: {
    clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)",
  },
  exit: {
    clipPath: "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)",
  },
};

// Usage in Framer Motion
<motion.div
  variants={clipPathVariants}
  initial="initial"
  animate="animate"
  exit="exit"
  transition={{ duration: 0.5, ease: "easeInOut" }}
  className="absolute inset-0 bg-hacker-surface-card"
>
  {/* Content */}
</motion.div>
```

### 6.4 Hover Effects

```tsx
// Card hover with glow
<div className="
  p-6
  bg-hacker-surface-card
  border border-hacker-border-subtle
  rounded-xl
  transition-all duration-300
  hover:border-hacker-cyan/50
  hover:shadow-glow-cyan
  hover:-translate-y-1
">

// Button hover scale
<button className="
  px-6 py-3
  bg-hacker-cyan text-hacker-bg-primary
  rounded-lg
  transition-all duration-300
  hover:scale-105
  hover:shadow-glow-cyan
  active:scale-95
">

// Input focus glow
<input className="
  w-full px-4 py-3
  bg-hacker-surface-card
  border border-hacker-border-subtle
  rounded-lg
  transition-all duration-300
  focus:border-hacker-cyan
  focus:ring-1 focus:ring-hacker-cyan
  focus:shadow-glow-cyan
">

// Icon button with ripple
<button className="
  p-3
  rounded-full
  text-hacker-text-secondary
  hover:text-hacker-cyan
  hover:bg-hacker-surface-card
  transition-all duration-300
  hover:shadow-glow-cyan
">
```

### 6.5 Particles.js Background Configuration

```tsx
// Particles configuration for cyberpunk effect
const particlesConfig = {
  particles: {
    number: {
      value: 80,
      density: {
        enable: true,
        value_area: 800,
      },
    },
    color: {
      value: "#00ffff",
    },
    shape: {
      type: "circle",
    },
    opacity: {
      value: 0.5,
      random: true,
      anim: {
        enable: true,
        speed: 1,
        opacity_min: 0.1,
        sync: false,
      },
    },
    size: {
      value: 3,
      random: true,
      anim: {
        enable: true,
        speed: 2,
        size_min: 0.1,
        sync: false,
      },
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#00ffff",
      opacity: 0.2,
      width: 1,
    },
    move: {
      enable: true,
      speed: 2,
      direction: "none",
      random: true,
      straight: false,
      out_mode: "out",
      bounce: false,
      attract: {
        enable: false,
        rotateX: 600,
        rotateY: 1200,
      },
    },
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "repulse",
      },
      onclick: {
        enable: true,
        mode: "push",
      },
      resize: true,
    },
    modes: {
      repulse: {
        distance: 100,
        duration: 0.4,
      },
      push: {
        particles_nb: 4,
      },
    },
  },
  retina_detect: true,
};
```

---

## 7. Page Specifications

### 7.1 Landing Page

```tsx
// app/page.tsx - Landing Page
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-hacker-bg-primary">
      {/* Navbar */}
      <Navbar />

      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
        {/* Animated background grid */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,255,0.03)_1px,transparent_1px)] bg-[size:50px_50px]" />

        {/* Gradient orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-hacker-cyan/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-hacker-neon-green/10 rounded-full blur-3xl animate-pulse delay-1000" />

        {/* Hero content */}
        <div className="relative z-10 container mx-auto px-4 text-center">
          <h1 className="font-display text-4xl sm:text-5xl lg:text-7xl font-bold text-hacker-text-primary mb-6 tracking-tight">
            Mission<span className="text-hacker-cyan">Impossible</span>
          </h1>
          <p className="font-sans text-lg sm:text-xl text-hacker-text-secondary max-w-2xl mx-auto mb-8">
            The ultimate mission management system for elite operatives.
            Track, execute, and complete missions with precision.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="btn-primary text-lg px-8 py-4">
              Start for Free
            </button>
            <button className="btn-secondary text-lg px-8 py-4">
              View Protocol
            </button>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <svg className="w-6 h-6 text-hacker-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-hacker-bg-secondary">
        <div className="container mx-auto px-4">
          <h2 className="font-display text-3xl sm:text-4xl font-bold text-hacker-text-primary text-center mb-16">
            System <span className="text-hacker-cyan">Capabilities</span>
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature cards */}
            {features.map((feature) => (
              <div className="card-glow-cyan p-8">
                <div className="w-12 h-12 bg-hacker-cyan/10 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-hacker-cyan" />
                </div>
                <h3 className="font-display text-xl font-semibold text-hacker-text-primary mb-2">
                  {feature.title}
                </h3>
                <p className="font-sans text-hacker-text-secondary">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 bg-hacker-bg-primary">
        <div className="container mx-auto px-4">
          <h2 className="font-display text-3xl sm:text-4xl font-bold text-hacker-text-primary text-center mb-16">
            Operational <span className="text-hacker-neon-green">Protocol</span>
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Steps */}
            {steps.map((step, index) => (
              <div className="relative text-center">
                {/* Step number */}
                <div className="w-16 h-16 mx-auto mb-6 bg-hacker-surface-card rounded-full flex items-center justify-center border border-hacker-neon-green/30 shadow-glow-green">
                  <span className="font-display text-2xl font-bold text-hacker-neon-green">
                    {index + 1}
                  </span>
                </div>
                <h3 className="font-display text-xl font-semibold text-hacker-text-primary mb-2">
                  {step.title}
                </h3>
                <p className="font-sans text-hacker-text-secondary">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-hacker-bg-secondary border-t border-hacker-border-subtle">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {/* Footer links */}
          </div>
          <div className="mt-12 pt-8 border-t border-hacker-border-subtle text-center">
            <p className="font-mono text-sm text-hacker-text-muted">
              2024 MissionImpossible. All systems operational.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
```

### 7.2 Authentication Pages

```tsx
// app/auth/signin/page.tsx - Sign In with clippath transition
"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function SignInPage() {
  const [isSignUp, setIsSignUp] = useState(false);

  return (
    <div className="min-h-screen bg-hacker-bg-primary flex items-center justify-center p-4">
      {/* Background effects */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,255,0.02)_1px,transparent_1px)] bg-[size:100px_100px]" />

      {/* Toggle container */}
      <div className="relative w-full max-w-4xl h-[600px] bg-hacker-surface-card/50 rounded-2xl border border-hacker-border-default overflow-hidden">
        {/* Clippath transition container */}
        <AnimatePresence mode="wait">
          {isSignUp ? (
            <motion.div
              key="signup"
              initial={{ clipPath: "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)" }}
              animate={{ clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)" }}
              exit={{ clipPath: "polygon(0 0, 0 0, 0 100%, 0 100%)" }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className="absolute inset-0 flex"
            >
              {/* Sign Up Form */}
              <div className="w-full lg:w-1/2 p-12 flex flex-col justify-center">
                <h2 className="font-display text-3xl font-bold text-hacker-text-primary mb-2">
                  Initialize Protocol
                </h2>
                <p className="font-sans text-hacker-text-secondary mb-8">
                  Create your operative account
                </p>

                <form className="space-y-6">
                  <Input label="Agent Name" placeholder="Enter your codename" />
                  <Input label="Add Secrets" type="password" placeholder="Create password" />
                  <Input label="Confirm Secrets" type="password" placeholder="Confirm password" />
                  <button type="submit" className="btn-primary w-full">
                    Initialize
                  </button>
                </form>
              </div>

              {/* Overlay panel */}
              <div className="hidden lg:flex w-1/2 bg-hacker-cyan/10 flex-col justify-center items-center p-12 border-l border-hacker-cyan/20">
                <h3 className="font-display text-2xl font-bold text-hacker-text-primary mb-4">
                  Welcome Back
                </h3>
                <p className="font-sans text-hacker-text-secondary text-center mb-8">
                  Already have an account? Sign in to access your missions.
                </p>
                <button
                  onClick={() => setIsSignUp(false)}
                  className="btn-secondary"
                >
                  Access System
                </button>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="signin"
              initial={{ clipPath: "polygon(0 0, 0 0, 0 100%, 0 100%)" }}
              animate={{ clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)" }}
              exit={{ clipPath: "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)" }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              className="absolute inset-0 flex"
            >
              {/* Sign In Form */}
              <div className="w-full lg:w-1/2 p-12 flex flex-col justify-center">
                <h2 className="font-display text-3xl font-bold text-hacker-text-primary mb-2">
                  Access System
                </h2>
                <p className="font-sans text-hacker-text-secondary mb-8">
                  Enter your credentials to continue
                </p>

                <form className="space-y-6">
                  <Input label="Agent Name" placeholder="Enter your codename" />
                  <Input label="Add Secrets" type="password" placeholder="Enter password" />
                  <div className="flex items-center justify-between">
                    <label className="flex items-center gap-2">
                      <input type="checkbox" className="w-4 h-4 rounded border-hacker-border-default bg-hacker-surface-card text-hacker-cyan focus:ring-hacker-cyan" />
                      <span className="font-sans text-sm text-hacker-text-secondary">Remember me</span>
                    </label>
                    <a href="#" className="font-sans text-sm text-hacker-cyan hover:underline">
                      Forgot secrets?
                    </a>
                  </div>
                  <button type="submit" className="btn-primary w-full">
                    Access System
                  </button>
                </form>
              </div>

              {/* Overlay panel */}
              <div className="hidden lg:flex w-1/2 bg-hacker-neon-green/10 flex-col justify-center items-center p-12 border-l border-hacker-neon-green/20">
                <h3 className="font-display text-2xl font-bold text-hacker-text-primary mb-4">
                  New Operation?
                </h3>
                <p className="font-sans text-hacker-text-secondary text-center mb-8">
                  Register as a new operative to start your first mission.
                </p>
                <button
                  onClick={() => setIsSignUp(true)}
                  className="btn-secondary"
                >
                  Initialize Protocol
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Mobile toggle buttons */}
        <div className="lg:hidden absolute bottom-4 left-0 right-0 flex justify-center gap-4">
          <button
            onClick={() => setIsSignUp(false)}
            className={`px-4 py-2 rounded-lg font-sans text-sm transition-colors ${
              !isSignUp ? "bg-hacker-cyan text-hacker-bg-primary" : "text-hacker-text-secondary"
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => setIsSignUp(true)}
            className={`px-4 py-2 rounded-lg font-sans text-sm transition-colors ${
              isSignUp ? "bg-hacker-cyan text-hacker-bg-primary" : "text-hacker-text-secondary"
            }`}
          >
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}
```

### 7.3 Dashboard Page

```tsx
// app/dashboard/page.tsx - Main Dashboard
export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-hacker-bg-primary flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        {/* Header */}
        <header className="sticky top-0 z-40 bg-hacker-bg-primary/95 backdrop-blur border-b border-hacker-border-subtle px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-display text-2xl font-bold text-hacker-text-primary">
                Mission Control
              </h1>
              <p className="font-mono text-sm text-hacker-text-muted">
                Active Operations: 7
              </p>
            </div>

            <div className="flex items-center gap-4">
              {/* Search */}
              <div className="relative hidden sm:block">
                <input
                  type="search"
                  placeholder="Search missions..."
                  className="w-64 pl-10 pr-4 py-2 bg-hacker-surface-card border border-hacker-border-subtle rounded-lg text-sm text-hacker-text-primary placeholder:text-hacker-text-muted focus:border-hacker-cyan focus:outline-none"
                />
                <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-hacker-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>

              {/* Voice command */}
              <button className="p-2 rounded-lg bg-hacker-surface-card border border-hacker-border-subtle hover:border-hacker-neon-green transition-colors group">
                <svg className="w-5 h-5 text-hacker-text-secondary group-hover:text-hacker-neon-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              </button>

              {/* Add mission button */}
              <button className="btn-primary flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span className="hidden sm:inline">Initilize</span>
              </button>
            </div>
          </div>
        </header>

        {/* Dashboard content */}
        <div className="p-6">
          {/* Stats grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <StatCard
              label="Total Missions"
              value="42"
              trend="+12%"
              trendUp={true}
            />
            <StatCard
              label="Active"
              value="7"
              trend="+2"
              trendUp={true}
            />
            <StatCard
              label="Completed"
              value="31"
              trend="+8"
              trendUp={true}
            />
            <StatCard
              label="Success Rate"
              value="98%"
              trend="+2.5%"
              trendUp={true}
            />
          </div>

          {/* Missions grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {missions.map((mission) => (
              <MissionCard key={mission.id} mission={mission} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

// Stat Card Component
function StatCard({ label, value, trend, trendUp }: StatCardProps) {
  return (
    <div className="p-6 bg-hacker-surface-card rounded-xl border border-hacker-border-subtle hover:border-hacker-cyan/50 transition-all duration-300">
      <p className="font-mono text-xs text-hacker-text-muted uppercase tracking-wider">
        {label}
      </p>
      <p className="font-display text-3xl font-bold text-hacker-text-primary mt-2">
        {value}
      </p>
      <div className="flex items-center gap-1 mt-2">
        <span className={`text-sm ${trendUp ? "text-hacker-neon-green" : "text-red-400"}`}>
          {trendUp ? "↑" : "↓"}
        </span>
        <span className={`text-sm ${trendUp ? "text-hacker-neon-green" : "text-red-400"}`}>
          {trend}
        </span>
        <span className="font-mono text-xs text-hacker-text-muted">vs last week</span>
      </div>
    </div>
  );
}

// Mission Card Component
function MissionCard({ mission }: MissionCardProps) {
  return (
    <div className="
      p-6
      bg-hacker-surface-card
      rounded-xl
      border border-hacker-border-subtle
      hover:border-hacker-cyan/50
      transition-all duration-300
      group
    ">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-display text-lg font-semibold text-hacker-text-primary group-hover:text-hacker-cyan transition-colors">
            {mission.title}
          </h3>
          <p className="font-mono text-xs text-hacker-text-muted mt-1">
            {mission.id}
          </p>
        </div>
        <Badge status={mission.status} />
      </div>

      {/* Description */}
      <p className="font-sans text-sm text-hacker-text-secondary mb-4 line-clamp-2">
        {mission.description}
      </p>

      {/* Progress */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="font-mono text-xs text-hacker-text-muted">Progress</span>
          <span className="font-mono text-xs text-hacker-cyan">{mission.progress}%</span>
        </div>
        <div className="h-1 bg-hacker-bg-tertiary rounded-full overflow-hidden">
          <div
            className="h-full bg-hacker-cyan rounded-full transition-all duration-500"
            style={{ width: `${mission.progress}%` }}
          />
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-hacker-border-subtle">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-hacker-cyan to-hacker-neon-green flex items-center justify-center">
            <span className="text-hacker-bg-primary font-mono text-xs font-bold">
              {mission.assignee.charAt(0)}
            </span>
          </div>
          <span className="font-sans text-sm text-hacker-text-secondary">
            {mission.assignee}
          </span>
        </div>
        <span className="font-mono text-xs text-hacker-text-muted">
          Due: {mission.dueDate}
        </span>
      </div>
    </div>
  );
}
```

---

## 8. Accessibility Guidelines

### 8.1 Color Contrast Requirements

| Text Size | Minimum Contrast | Example |
|-----------|------------------|---------|
| Normal text (≤18px) | 4.5:1 | Body text, labels |
| Large text (>18px) | 3:1 | Headings, emphasis |
| UI components | 3:1 | Borders, icons, buttons |
| Decorative | No requirement | Background elements |

### 8.2 Focus States

```tsx
// Visible focus indicator
<button
  className="
    px-4 py-2
    bg-hacker-cyan text-hacker-bg-primary
    rounded-lg
    focus:outline-none
    focus:ring-2
    focus:ring-hacker-cyan
    focus:ring-offset-2
    focus:ring-offset-hacker-bg-primary
  "
>
  Accessible Button
</button>

// Skip link
<a
  href="#main-content"
  className="
    sr-only
    focus:not-sr-only
    focus:fixed
    focus:top-4
    focus:left-4
    focus:z-50
    focus:px-4
    focus:py-2
    focus:bg-hacker-cyan
    focus:text-hacker-bg-primary
    focus:font-display
  "
>
  Skip to main content
</a>
```

### 8.3 ARIA Attributes

```tsx
// Button with loading state
<button
  aria-busy={loading}
  aria-disabled={disabled}
  disabled={disabled || loading}
>
  {loading ? (
    <>
      <span aria-hidden="true" className="animate-spin">⟳</span>
      <span>Loading...</span>
    </>
  ) : (
    "Submit"
  )}
</button>

// Modal with ARIA
<dialog
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
  aria-modal="true"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to proceed?</p>
</dialog>

// Status badge
<span
  role="status"
  aria-live="polite"
  className="text-hacker-neon-green"
>
  Operation completed successfully
</span>
```

### 8.4 Touch Targets

```tsx
// Minimum 44x44px touch targets
<button
  className="
    min-h-[44px]
    min-w-[44px]
    px-4
    py-3
    flex
    items-center
    justify-center
    gap-2
  "
>
  <Icon className="w-5 h-5" />
  <span>Action</span>
</button>

// Spacing between touch targets
<div className="flex gap-4">
  <button className="min-h-[44px] min-w-[44px]">Button 1</button>
  <button className="min-h-[44px] min-w-[44px]">Button 2</button>
</div>
```

### 8.5 Screen Reader Support

```tsx
// Visually hidden text for screen readers
<span className="sr-only">
  {isActive ? "Current step" : "Not current step"}
</span>

// Icon button with label
<button
  aria-label="Open menu"
  className="p-3 min-h-[44px] min-w-[44px]"
>
  <MenuIcon className="w-6 h-6" />
</button>

// Loading announcement
<div
  role="status"
  aria-live="polite"
  aria-atomic="false"
>
  {loading && <span>Loading missions...</span>}
</div>
```

---

## Summary

This design guide provides a comprehensive foundation for building the MissionImpossible hacker-style UI. Key takeaways:

1. **Color Palette**: Deep navy backgrounds with cyan, neon green, and magenta accents
2. **Typography**: Orbitron for display, Roboto Mono for code/data, Inter for body text
3. **Animations**: Smooth transitions with glow effects, pulse animations, and clippath transitions
4. **Components**: Terminal-style inputs, glowing cards, and cyberpunk-inspired UI elements
5. **Accessibility**: WCAG 2.1 AA compliant with proper focus states and screen reader support

All Tailwind classes are designed to be composable and responsive across all device sizes.

---

*Document Version: 1.0*
*Last Updated: 2024-01-03*
*Framework: Next.js 14+ with Tailwind CSS*
