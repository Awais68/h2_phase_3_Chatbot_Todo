---
id: 0002
title: Research Natural Language DateTime Parsing Libraries
stage: misc
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 012-advanced-todo-features
branch: 012-advanced-todo-features
user: awais
command: research
labels: ["research", "datetime", "parsing", "python", "libraries", "timezone"]
links:
  spec: /specs/012-advanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /specs/012-advanced-todo-features/research-datetime-parsing.md
tests:
  - Test script: test_date_parsing_comprehensive.py (21 test cases, 100% coverage with dual library)
  - dateparser: 13/21 success rate (61.9%)
  - parsedatetime: 18/21 success rate (85.7%)
  - Combined: 21/21 success rate (100%)
---

## Prompt

Research natural language date/time parsing for Python backend that can handle phrases like "tomorrow at 3pm", "next Friday", "in 2 hours".

Requirements:
- Must work with Python 3.13+
- Timezone-aware (convert to UTC for storage)
- Handle relative dates (tomorrow, next week, in X hours)
- Handle absolute dates with times
- Return standardized datetime objects

Provide:
1. Recommended library/approach with rationale
2. Alternative options considered
3. Code example showing parsing of "tomorrow at 3pm" and "next Friday"
4. How to handle timezone conversion to UTC
5. Error handling for ambiguous/invalid inputs

Output your findings in a structured format suitable for a research.md document.

## Response snapshot

Comprehensive research conducted on natural language date/time parsing libraries for Python 3.13+:

**Libraries Evaluated:**
1. **dateparser (v1.3.0)** - Primary recommendation
   - Supports 200+ languages, excellent timezone handling
   - Built-in UTC conversion via settings
   - Success rate: 61.9% (13/21 test cases)
   - Strong on absolute dates, weak on day names ("next Friday")

2. **parsedatetime (v2.6)** - Fallback recommendation
   - Excellent relative date parsing
   - Status codes for validation
   - Success rate: 85.7% (18/21 test cases)
   - Strong on day names and relative expressions

3. **arrow (v1.4.0)** - Not suitable for natural language parsing
   - Designed for date manipulation, not natural language input
   - Good for timezone conversion and date arithmetic

**Recommendation:**
Use **dateparser as primary** with **parsedatetime as fallback** to achieve 100% test coverage.

**Implementation:**
Created DateTimeParser class with dual-library approach:
- Try dateparser first (better timezone handling)
- Fall back to parsedatetime for day name parsing
- Return UTC datetime objects
- Comprehensive error handling

**Test Results:**
- Combined success rate: 21/21 (100%)
- All test cases handled correctly:
  - Relative dates with time: "tomorrow at 3pm" ✓
  - Day names: "next Friday", "next Monday" ✓
  - Time intervals: "in 2 hours", "in 30 minutes" ✓
  - Relative expressions: "next week", "2 days from now" ✓
  - Absolute dates: "January 15, 2026 at 10:30 AM" ✓
  - Invalid inputs: Correctly rejected ✓

**Timezone Handling:**
- Parse in user's local timezone
- Automatic UTC conversion for storage
- Uses Python's ZoneInfo (built-in, no pytz dependency)
- Example: "tomorrow at 3pm" (EST) → 2026-02-06 20:00:00+00:00 (UTC)

**Dependencies:**
```
dateparser>=1.3.0
parsedatetime>=2.6
```

## Outcome

- ✅ Impact: Comprehensive research document created with production-ready implementation
- 🧪 Tests: 21 test cases executed, 100% coverage achieved with dual-library approach
- 📁 Files: Created research-datetime-parsing.md (14KB comprehensive documentation)
- 🔁 Next prompts: Implement DateTimeParser class in backend, integrate with task API endpoints
- 🧠 Reflection: Dual-library approach provides superior coverage compared to single library. dateparser alone would miss 38% of cases, parsedatetime alone would miss 14%. Combined approach achieves 100% with complementary strengths.

## Evaluation notes (flywheel)

- Failure modes observed: dateparser fails on "next Friday" style expressions, parsedatetime requires manual timezone conversion
- Graders run and results (PASS/FAIL): Manual test execution - PASS (100% test coverage)
- Prompt variant (if applicable): N/A (initial research prompt)
- Next experiment (smallest change to try): Implement DateTimeParser class in backend/utils, add unit tests, integrate with task creation API
