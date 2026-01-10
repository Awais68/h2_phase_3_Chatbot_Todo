# Feature Specification: Multi-language Support (English + Urdu)

**Feature Branch**: `009-multi-language`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "Create Phase II multi-language support specification (BONUS +100 points)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Language Switching (Priority: P1)

As a user who speaks both English and Urdu, I want to switch between languages so that I can use the application in my preferred language.

**Why this priority**: Language switching is the core value proposition of this feature. Without it, users cannot access the application in their preferred language, defeating the entire purpose of the internationalization effort.

**Independent Test**: Can be fully tested by visiting the language switcher, selecting a language, and verifying all visible text changes to the selected language.

**Acceptance Scenarios**:

1. **Given** a user views the application in English, **When** they select Urdu from the language switcher, **Then** all UI text changes to Urdu and the layout direction changes to right-to-left.
2. **Given** a user views the application in Urdu, **When** they select English from the language switcher, **Then** all UI text changes to English and the layout direction changes to left-to-right.
3. **Given** a user selects a language, **When** they navigate to a different page, **Then** the selected language persists across all pages.
4. **Given** a user selects a language, **When** they refresh the browser, **Then** the selected language remains the same.

---

### User Story 2 - Complete UI Translation (Priority: P1)

As a non-English speaking user, I want all application text to be translated so that I can understand and use all features without needing to know English.

**Why this priority**: Partial translations create confusion and frustration. Users expect complete translation coverage to use the application effectively in their native language.

**Independent Test**: Can be fully tested by navigating through all pages and features while using each supported language, verifying that every visible text element displays in the selected language.

**Acceptance Scenarios**:

1. **Given** a user switches to Urdu, **When** they view the login page, **Then** all text including labels, buttons, headings, and messages appear in Urdu.
2. **Given** a user switches to Urdu, **When** they view the tasks page, **Then** all task-related text including titles, descriptions, filter labels, and button text appear in Urdu.
3. **Given** a user switches to Urdu, **When** they view the dashboard, **Then** all dashboard text including welcome messages, stats labels, and navigation items appear in Urdu.
4. **Given** a user switches to Urdu, **When** they encounter validation errors, **Then** all error messages and validation text appear in Urdu.

---

### User Story 3 - RTL Layout for Urdu (Priority: P1)

As an Urdu-speaking user, I want the interface to flow from right to left when using Urdu so that the reading direction matches my natural language orientation.

**Why this priority**: Right-to-left (RTL) support is essential for Urdu readability. An LTR layout with RTL text creates a poor user experience and appears unprofessional to Urdu-speaking users.

**Independent Test**: Can be fully tested by switching to Urdu and verifying that the layout direction, text alignment, and interactive elements adapt appropriately for RTL reading.

**Acceptance Scenarios**:

1. **Given** a user switches to Urdu, **When** they view any page, **Then** the overall layout direction changes to right-to-left.
2. **Given** a user views the application in Urdu, **When** they read text, **Then** text alignment is right-aligned as expected.
3. **Given** a user views the application in Urdu, **When** they interact with flex containers, **Then** the visual flow follows RTL patterns (e.g., navigation items appear in reverse order).
4. **Given** a user switches between languages, **When** the direction changes, **Then** the transition is smooth without jarring layout shifts.

---

### User Story 4 - Localized Date and Time (Priority: P2)

As a user in different locales, I want dates and times to be formatted according to my cultural conventions so that I can easily understand when tasks were created or updated.

**Why this priority**: Date formatting varies significantly across cultures. Users should see dates in a familiar format that matches their expectations for their language and region.

**Independent Test**: Can be fully tested by creating tasks at different times and viewing task timestamps while using different languages to verify appropriate date formatting.

**Acceptance Scenarios**:

1. **Given** a user views tasks in English, **When** they see task timestamps, **Then** dates are formatted in the English convention (e.g., "Jan 1, 2024, 10:30 AM").
2. **Given** a user views tasks in Urdu, **When** they see task timestamps, **Then** dates are formatted in the Urdu/Arabic convention using Urdu month names.
3. **Given** a user views task statistics, **When** they see counts and numbers, **Then** numbers are displayed using appropriate numerals (Western for English, Eastern-Arabic for Urdu).

---

### User Story 5 - Language Persistence (Priority: P2)

As a returning user, I want my language preference to be remembered so that I don't have to select my preferred language every time I visit the application.

**Why this priority**: Forgetting language preferences creates friction for returning users. Storing preferences provides a seamless experience across sessions and visits.

**Independent Test**: Can be fully tested by selecting a language, closing the browser, reopening the application, and verifying the previously selected language is still active.

**Acceptance Scenarios**:

1. **Given** a user selects Urdu, **When** they close and reopen the browser, **Then** the application loads in Urdu automatically.
2. **Given** a user changes their language preference, **When** they return to the application, **Then** the new preference is respected.
3. **Given** a user is logged in, **When** they change their language preference, **Then** the preference should be saved to their user profile if database persistence is implemented.

---

### User Story 6 - Browser Language Detection (Priority: P3)

As a new visitor, I want the application to automatically detect my browser's language preference so that I can immediately use the application without needing to switch languages.

**Why this priority**: Browser language detection provides a frictionless first experience for new users. It reduces the barrier to entry and shows respect for the user's existing system preferences.

**Independent Test**: Can be fully tested by configuring browser language settings to prefer Urdu, visiting the application for the first time, and verifying Urdu is automatically selected.

**Acceptance Scenarios**:

1. **Given** a new visitor with browser set to Urdu, **When** they first visit the application, **Then** the application displays in Urdu.
2. **Given** a new visitor with browser set to English, **When** they first visit the application, **Then** the application displays in English.
3. **Given** a visitor with an unsupported browser language, **When** they visit the application, **Then** the application defaults to English.

---

### User Story 7 - Translation Fallback (Priority: P2)

As a user, I want the application to gracefully handle any missing translations so that I always see readable text even if some translations are incomplete.

**Why this priority**: During development and maintenance, some translation keys may be missing. The application should never show raw translation keys to users, which would appear broken and unprofessional.

**Independent Test**: Can be fully tested by intentionally adding translation keys that exist in English but not in Urdu, and verifying that fallback behavior shows the English text or a sensible default.

**Acceptance Scenarios**:

1. **Given** a translation key is missing in Urdu, **When** the component renders that text, **Then** the application displays the English fallback text.
2. **Given** a translation key is missing in all languages, **When** the component renders that text, **Then** the application displays the key name or a placeholder rather than crashing.
3. **Given** new translation keys are added, **When** they are rendered, **Then** the application handles them gracefully with appropriate logging for developers.

---

### User Story 8 - Accessible Language Support (Priority: P2)

As a user relying on assistive technologies, I want the language and direction attributes to be properly set so that screen readers interpret content correctly.

**Why this priority**: Screen readers need to know the language and reading direction to pronounce content correctly. Without proper attributes, assistive technology users may experience incorrect pronunciation or confusion.

**Independent Test**: Can be fully tested using browser developer tools and accessibility audit tools to verify proper lang and dir attributes on HTML elements.

**Acceptance Scenarios**:

1. **Given** a user views the application in Urdu, **When** inspected with developer tools, **Then** the html element has lang="ur" and dir="rtl" attributes.
2. **Given** a user views the application in English, **When** inspected with developer tools, **Then** the html element has lang="en" and dir="ltr" attributes.
3. **Given** a screen reader is used, **When** reading content in Urdu, **Then** the pronunciation follows Urdu language rules.

---

### Edge Cases

- **What happens when a user visits a direct URL with an unsupported locale?**
  - The application redirects to the default locale (English) or shows a 404 page with a language selection option.

- **What happens when translation files have syntax errors?**
  - The application logs errors during build/runtime and falls back to a minimal set of translations or default strings.

- **What happens when switching languages during a form submission?**
  - Form state is preserved during language switch; only translated text changes, not user input.

- **What happens when very long Urdu text exceeds container widths?**
  - Urdu text wraps appropriately; RTL-aware text wrapping handles long words and phrases correctly.

- **What happens when users have custom font settings that conflict with the Urdu font?**
  - The application attempts to use Noto Nastaliq Urdu with fallback to system Urdu-compatible fonts.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a language switcher component accessible from the navigation area.
- **FR-002**: The system MUST support English (en) as the default language with complete translations.
- **FR-003**: The system MUST support Urdu (ur) as a secondary language with complete translations.
- **FR-004**: The system MUST persist the user's language preference across browser sessions using localStorage.
- **FR-005**: The system MUST change the text direction to RTL when Urdu is selected.
- **FR-006**: The system MUST change the text direction to LTR when English is selected.
- **FR-007**: The system MUST format dates and times according to the selected language's conventions.
- **FR-008**: The system MUST format numbers using appropriate numeral systems for each language.
- **FR-009**: The system MUST provide translations for all common UI elements including loading, save, cancel, delete, edit, close, confirm, and search.
- **FR-010**: The system MUST provide translations for all authentication-related text including login, signup, logout, email, password, name, and related messages.
- **FR-011**: The system MUST provide translations for all task management text including task titles, descriptions, filters, sorting, and action labels.
- **FR-012**: The system MUST provide translations for all dashboard text including welcome messages, quick actions, and statistics.
- **FR-013**: The system MUST provide translations for all error and validation messages.
- **FR-014**: The system MUST load the appropriate font for Urdu text rendering when Urdu is selected.
- **FR-015**: The system MUST support URL-based language routing (e.g., /en/tasks, /ur/tasks).
- **FR-016**: The system MUST provide fallback translation when a key is missing in the current locale.
- **FR-017**: The system MUST set the html lang attribute to match the current locale.
- **FR-018**: The system MUST set the html dir attribute to match the current locale (ltr or rtl).
- **FR-019**: The system SHOULD detect browser language preferences on first visit.
- **FR-020**: The system SHOULD store user language preference in the user database when the user is authenticated.
- **FR-021**: The system MUST ensure smooth transitions between languages without layout shifts.
- **FR-022**: The system MUST support string interpolation for dynamic values like user names and counts.
- **FR-023**: The system MUST support nested translation keys using dot notation (e.g., tasks.filter.all).

### Key Entities

- **Locale**: A supported language and regional preference identifier (en for English, ur for Urdu). Each locale defines translation files, direction (LTR/RTL), and formatting conventions.
- **Translation Message**: A key-value pair mapping a translation key to its localized text for a specific locale. Messages support variable interpolation using curly brace syntax.
- **Translation Namespace**: A logical grouping of related translation messages, such as common, auth, tasks, dashboard, errors, and validation. Namespaces help organize translations and prevent key collisions.
- **Language Preference**: A user setting indicating their preferred locale. Stored in localStorage for anonymous users and optionally in the user database for authenticated users.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of UI text is available in both English and Urdu with complete translation coverage.
- **SC-002**: Language switching completes within 200ms without perceptible delay to the user.
- **SC-003**: Users can switch languages and navigate between pages with their preference persisting across 100% of sessions.
- **SC-004**: Urdu content displays with proper RTL layout and text alignment on all pages and components.
- **SC-005**: Date and time formatting follows language-appropriate conventions (English format for en, Urdu format for ur).
- **SC-006**: Users switching to Urdu see properly rendered Urdu font (Noto Nastaliq Urdu or fallback).
- **SC-007**: No raw translation keys are visible to users under any circumstances (100% fallback coverage).
- **SC-008**: The html element has correct lang and dir attributes matching the selected locale (verified via accessibility audit).
- **SC-009**: Layout shifts during language switching are imperceptible (less than 100ms cumulative layout shift).
- **SC-010**: Translation files are properly structured and organized by namespace for maintainability.

### Dependencies

- The internationalization library (next-intl) must be installed and configured.
- Date formatting library (date-fns) with locale support must be available.
- Urdu font (Noto Nastaliq Urdu or equivalent) must be available via web font.
- Tailwind CSS RTL plugin should be available for RTL-aware utility classes.
- Translation files must be maintained as JSON files organized by locale.

### Assumptions

- English is the default language and requires no special font handling.
- Urdu uses Eastern-Arabic numerals (٠١٢٣٤٥٦٧٨٩) for number formatting.
- The translation namespaces (common, auth, tasks, dashboard, errors, validation) cover all required text.
- RTL support can be achieved through CSS dir attribute and minimal CSS adjustments.
- Translation keys follow a consistent dot-notation pattern for organization.
- Missing translations fall back to English text as the default fallback language.

### Out of Scope

- Additional languages beyond English and Urdu (may be added in future phases).
- Region-specific locale variants (e.g., en-GB, en-US treated as en).
- Currency formatting and localization.
- Time zone conversion (display in UTC or server time zone).
- Translated user-generated content (tasks remain in the language they were created).
- Translation management UI (translations managed via JSON files).
- Machine translation services (all translations provided manually).
- Pluralization rules beyond basic singular/plural handling.
- Gender-specific translations.
- Right-to-left support for complex JavaScript-heavy components that manipulate DOM directly.

---

## Complete Translation Files

### English Translations (en.json)

```json
{
  "common": {
    "appName": "Todo App",
    "loading": "Loading...",
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "close": "Close",
    "confirm": "Confirm",
    "search": "Search"
  },
  "auth": {
    "login": "Login",
    "signup": "Sign Up",
    "logout": "Logout",
    "email": "Email",
    "password": "Password",
    "name": "Full Name",
    "welcomeBack": "Welcome Back",
    "createAccount": "Create Account",
    "alreadyHaveAccount": "Already have an account?",
    "dontHaveAccount": "Don't have an account?",
    "loginSuccess": "Logged in successfully",
    "signupSuccess": "Account created successfully",
    "invalidCredentials": "Invalid email or password",
    "emailAlreadyExists": "Email already registered"
  },
  "tasks": {
    "title": "Your Tasks",
    "newTask": "New Task",
    "editTask": "Edit Task",
    "deleteTask": "Delete Task",
    "taskTitle": "Task Title",
    "taskDescription": "Task Description",
    "createTask": "Create Task",
    "updateTask": "Update Task",
    "markComplete": "Mark as Complete",
    "markIncomplete": "Mark as Incomplete",
    "confirmDelete": "Are you sure you want to delete this task?",
    "taskCreated": "Task created successfully",
    "taskUpdated": "Task updated successfully",
    "taskDeleted": "Task deleted successfully",
    "noTasks": "No tasks yet",
    "noTasksDescription": "Get started by creating your first task",
    "filter": {
      "all": "All",
      "pending": "Pending",
      "completed": "Completed"
    },
    "sort": {
      "created": "Created Date",
      "updated": "Updated Date",
      "title": "Title"
    },
    "stats": {
      "total": "Total Tasks",
      "pending": "Pending",
      "completed": "Completed"
    }
  },
  "dashboard": {
    "welcome": "Welcome, {name}",
    "quickActions": "Quick Actions",
    "recentTasks": "Recent Tasks",
    "viewAll": "View All"
  },
  "errors": {
    "generic": "Something went wrong",
    "networkError": "Network error. Please try again.",
    "unauthorized": "You are not authorized",
    "notFound": "Not found",
    "validationError": "Please check your input"
  },
  "validation": {
    "required": "This field is required",
    "emailInvalid": "Please enter a valid email",
    "passwordTooShort": "Password must be at least 8 characters",
    "titleTooLong": "Title must be less than 200 characters",
    "descriptionTooLong": "Description must be less than 1000 characters"
  }
}
```

### Urdu Translations (ur.json)

```json
{
  "common": {
    "appName": "ٹوڈو ایپ",
    "loading": "لوڈ ہو رہا ہے...",
    "save": "محفوظ کریں",
    "cancel": "منسوخ کریں",
    "delete": "حذف کریں",
    "edit": "ترمیم کریں",
    "close": "بند کریں",
    "confirm": "تصدیق کریں",
    "search": "تلاش کریں"
  },
  "auth": {
    "login": "لاگ ان",
    "signup": "سائن اپ",
    "logout": "لاگ آؤٹ",
    "email": "ای میل",
    "password": "پاس ورڈ",
    "name": "پورا نام",
    "welcomeBack": "خوش آمدید",
    "createAccount": "اکاؤنٹ بنائیں",
    "alreadyHaveAccount": "پہلے سے اکاؤنٹ ہے؟",
    "dontHaveAccount": "اکاؤنٹ نہیں ہے؟",
    "loginSuccess": "کامیابی سے لاگ ان ہو گئے",
    "signupSuccess": "اکاؤنٹ کامیابی سے بنا دیا گیا",
    "invalidCredentials": "غلط ای میل یا پاس ورڈ",
    "emailAlreadyExists": "یہ ای میل پہلے سے رجسٹرڈ ہے"
  },
  "tasks": {
    "title": "آپ کے کام",
    "newTask": "نیا کام",
    "editTask": "کام میں ترمیم",
    "deleteTask": "کام حذف کریں",
    "taskTitle": "کام کا عنوان",
    "taskDescription": "کام کی تفصیل",
    "createTask": "کام بنائیں",
    "updateTask": "کام اپ ڈیٹ کریں",
    "markComplete": "مکمل کے طور پر نشان زد کریں",
    "markIncomplete": "نامکمل کے طور پر نشان زد کریں",
    "confirmDelete": "کیا آپ واقعی یہ کام حذف کرنا چاہتے ہیں؟",
    "taskCreated": "کام کامیابی سے بنا دیا گیا",
    "taskUpdated": "کام کامیابی سے اپ ڈیٹ کر دیا گیا",
    "taskDeleted": "کام کامیابی سے حذف کر دیا گیا",
    "noTasks": "ابھی کوئی کام نہیں",
    "noTasksDescription": "اپنا پہلا کام بنا کر شروع کریں",
    "filter": {
      "all": "تمام",
      "pending": "زیر التواء",
      "completed": "مکمل"
    },
    "sort": {
      "created": "بنانے کی تاریخ",
      "updated": "اپ ڈیٹ کی تاریخ",
      "title": "عنوان"
    },
    "stats": {
      "total": "کل کام",
      "pending": "زیر التواء",
      "completed": "مکمل"
    }
  },
  "dashboard": {
    "welcome": "خوش آمدید، {name}",
    "quickActions": "فوری کارروائیاں",
    "recentTasks": "حالیہ کام",
    "viewAll": "سب دیکھیں"
  },
  "errors": {
    "generic": "کچھ غلط ہو گیا",
    "networkError": "نیٹ ورک کی خرابی۔ دوبارہ کوشش کریں۔",
    "unauthorized": "آپ کو اجازت نہیں ہے",
    "notFound": "نہیں ملا",
    "validationError": "براہ کرم اپنی ان پٹ چیک کریں"
  },
  "validation": {
    "required": "یہ فیلڈ ضروری ہے",
    "emailInvalid": "براہ کرم درست ای میل درج کریں",
    "passwordTooShort": "پاس ورڈ کم از کم 8 حروف کا ہونا چاہیے",
    "titleTooLong": "عنوان 200 حروف سے کم ہونا چاہیے",
    "descriptionTooLong": "تفصیل 1000 حروف سے کم ہونی چاہیے"
  }
}
```
