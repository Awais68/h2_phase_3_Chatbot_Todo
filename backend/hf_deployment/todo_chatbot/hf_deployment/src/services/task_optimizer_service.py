"""
Task Optimizer Service implementing AI algorithms for task optimization.
"""
from typing import List, Dict, Any, Tuple
from datetime import datetime
import re
from difflib import SequenceMatcher

from backend.src.models.task import Task
from backend.src.models.task_optimization import (
    DuplicateDetection,
    PriorityAnalysis,
    TimeEstimate,
    TaskGrouping,
    AutomationOpportunity,
    OptimizationResponse
)


class TaskOptimizerService:
    """Service for analyzing tasks and providing optimization suggestions."""

    # Priority keywords from subagent configuration
    PRIORITY_KEYWORDS = {
        "high": ["urgent", "critical", "asap", "important", "emergency", "deadline"],
        "medium": ["soon", "needed", "required", "plan"],
        "low": ["later", "maybe", "consider", "someday"]
    }

    # Automation pattern keywords
    AUTOMATION_PATTERNS = {
        "recurring": ["daily", "weekly", "monthly", "every", "routine"],
        "integration": ["email", "calendar", "api", "sync", "import"],
        "scheduled": ["at", "schedule", "reminder", "notify"]
    }

    # Category keywords for grouping
    CATEGORY_KEYWORDS = {
        "shopping": ["buy", "purchase", "shop", "groceries", "store"],
        "work": ["meeting", "project", "deadline", "presentation", "report"],
        "personal": ["personal", "self", "hobby", "leisure"],
        "health": ["doctor", "exercise", "gym", "health", "medical"],
        "finance": ["pay", "bill", "bank", "money", "budget"],
        "home": ["clean", "repair", "fix", "home", "house"],
        "learning": ["learn", "study", "read", "course", "tutorial"]
    }

    @staticmethod
    def calculate_levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return TaskOptimizerService.calculate_levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @staticmethod
    def calculate_similarity(s1: str, s2: str) -> float:
        """Calculate similarity score between two strings (0-1)."""
        s1_lower = s1.lower().strip()
        s2_lower = s2.lower().strip()

        # Use SequenceMatcher for fuzzy matching
        ratio = SequenceMatcher(None, s1_lower, s2_lower).ratio()
        return ratio

    def detect_duplicates(self, tasks: List[Task], threshold: float = 0.8) -> List[DuplicateDetection]:
        """
        Detect duplicate or similar tasks using fuzzy string matching.

        Args:
            tasks: List of tasks to analyze
            threshold: Similarity threshold (0-1), default 0.8 means 80% similarity

        Returns:
            List of duplicate detection results
        """
        duplicates = []
        checked_pairs = set()

        for i, task1 in enumerate(tasks):
            for j, task2 in enumerate(tasks):
                if i >= j:  # Skip same task and already checked pairs
                    continue

                pair_key = (min(task1.id, task2.id), max(task1.id, task2.id))
                if pair_key in checked_pairs:
                    continue

                checked_pairs.add(pair_key)

                # Calculate similarity for title
                title_similarity = self.calculate_similarity(task1.title, task2.title)

                # Also consider description if available
                desc_similarity = 0.0
                if task1.description and task2.description:
                    desc_similarity = self.calculate_similarity(task1.description, task2.description)

                # Weighted average (title is more important)
                overall_similarity = 0.7 * title_similarity + 0.3 * desc_similarity

                if overall_similarity >= threshold:
                    # Calculate confidence based on how far above threshold
                    confidence = min(1.0, overall_similarity + 0.1)

                    duplicates.append(DuplicateDetection(
                        task_ids=[task1.id, task2.id],
                        similarity_score=round(overall_similarity, 2),
                        confidence=round(confidence, 2),
                        suggestion=f"Tasks '{task1.title}' and '{task2.title}' appear to be duplicates. Consider merging them.",
                        merge_recommendation=f"Keep: '{task1.title}' (created first), Delete: '{task2.title}'"
                    ))

        return duplicates

    def analyze_priority(self, tasks: List[Task]) -> List[PriorityAnalysis]:
        """
        Suggest priority levels based on keyword analysis.

        Args:
            tasks: List of tasks to analyze

        Returns:
            List of priority analysis results
        """
        priorities = []

        for task in tasks:
            text = f"{task.title} {task.description}".lower()
            detected_keywords = []
            priority_scores = {"high": 0, "medium": 0, "low": 0}

            # Check for priority keywords
            for priority_level, keywords in self.PRIORITY_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in text:
                        detected_keywords.append(keyword)
                        priority_scores[priority_level] += 1

            # Determine priority based on scores
            if priority_scores["high"] > 0:
                priority = "high"
                confidence = min(0.9, 0.6 + (priority_scores["high"] * 0.1))
            elif priority_scores["medium"] > 0:
                priority = "medium"
                confidence = min(0.85, 0.5 + (priority_scores["medium"] * 0.1))
            elif priority_scores["low"] > 0:
                priority = "low"
                confidence = min(0.8, 0.5 + (priority_scores["low"] * 0.1))
            else:
                priority = "medium"  # Default
                confidence = 0.4  # Low confidence for default

            reasoning = self._build_priority_reasoning(priority, detected_keywords, task)

            priorities.append(PriorityAnalysis(
                task_id=task.id,
                priority=priority,
                confidence=round(confidence, 2),
                reasoning=reasoning,
                keywords=detected_keywords
            ))

        return priorities

    def _build_priority_reasoning(self, priority: str, keywords: List[str], task: Task) -> str:
        """Build reasoning explanation for priority assignment."""
        if keywords:
            keyword_str = ", ".join(keywords)
            return f"Assigned '{priority}' priority based on keywords: {keyword_str}"
        else:
            return f"Assigned '{priority}' priority as default (no priority keywords detected)"

    def estimate_time(self, tasks: List[Task]) -> List[TimeEstimate]:
        """
        Estimate time requirements based on complexity analysis.

        Args:
            tasks: List of tasks to analyze

        Returns:
            List of time estimation results
        """
        estimates = []

        for task in tasks:
            text = f"{task.title} {task.description}"
            word_count = len(text.split())

            # Base estimate from word count
            base_hours = 1.0
            if word_count < 10:
                base_hours = 0.5
            elif word_count < 30:
                base_hours = 1.0
            elif word_count < 60:
                base_hours = 2.0
            else:
                base_hours = 4.0

            # Complexity factors
            complexity_factors = []
            text_lower = text.lower()

            # Technical terms increase complexity
            technical_terms = ["api", "database", "integration", "deploy", "test", "code", "system"]
            tech_count = sum(1 for term in technical_terms if term in text_lower)
            if tech_count > 0:
                base_hours *= (1 + tech_count * 0.3)
                complexity_factors.append(f"technical complexity ({tech_count} technical terms)")

            # Size keywords
            if any(word in text_lower for word in ["large", "complex", "comprehensive"]):
                base_hours *= 1.5
                complexity_factors.append("large scope indicated")
            elif any(word in text_lower for word in ["simple", "quick", "small", "minor"]):
                base_hours *= 0.7
                complexity_factors.append("simple scope indicated")

            # Multiple steps
            if "and" in text_lower or "," in text:
                step_count = text.count(",") + text.count(" and ")
                if step_count > 2:
                    base_hours *= (1 + step_count * 0.2)
                    complexity_factors.append(f"multiple steps ({step_count})")

            # Calculate confidence interval (±30%)
            min_hours = round(base_hours * 0.7, 1)
            max_hours = round(base_hours * 1.3, 1)
            estimated_hours = round(base_hours, 1)

            # Confidence based on factors detected
            confidence = 0.6 + min(0.3, len(complexity_factors) * 0.1)

            estimates.append(TimeEstimate(
                task_id=task.id,
                estimated_hours=estimated_hours,
                confidence_interval={"min": min_hours, "max": max_hours},
                confidence=round(confidence, 2),
                complexity_factors=complexity_factors if complexity_factors else ["standard complexity"]
            ))

        return estimates

    def recommend_grouping(self, tasks: List[Task]) -> List[TaskGrouping]:
        """
        Recommend task groupings based on semantic clustering.

        Args:
            tasks: List of tasks to analyze

        Returns:
            List of task grouping recommendations
        """
        # Group tasks by category
        category_groups: Dict[str, List[int]] = {}

        for task in tasks:
            text = f"{task.title} {task.description}".lower()
            detected_category = None
            max_matches = 0

            # Find best matching category
            for category, keywords in self.CATEGORY_KEYWORDS.items():
                matches = sum(1 for keyword in keywords if keyword in text)
                if matches > max_matches:
                    max_matches = matches
                    detected_category = category

            # Assign to category if detected
            if detected_category:
                if detected_category not in category_groups:
                    category_groups[detected_category] = []
                category_groups[detected_category].append(task.id)

        # Convert to TaskGrouping objects
        groupings = []
        for category, task_ids in category_groups.items():
            if len(task_ids) >= 2:  # Only suggest groups with 2+ tasks
                confidence = min(0.9, 0.5 + len(task_ids) * 0.1)

                groupings.append(TaskGrouping(
                    name=f"{category.capitalize()} Tasks",
                    task_ids=task_ids,
                    category=category,
                    confidence=round(confidence, 2),
                    reasoning=f"Found {len(task_ids)} tasks related to {category} activities"
                ))

        return groupings

    def detect_automation_opportunities(self, tasks: List[Task]) -> List[AutomationOpportunity]:
        """
        Identify tasks that could be automated.

        Args:
            tasks: List of tasks to analyze

        Returns:
            List of automation opportunity detections
        """
        opportunities = []

        # Track patterns
        pattern_tasks: Dict[str, List[int]] = {}

        for task in tasks:
            text = f"{task.title} {task.description}".lower()

            for automation_type, keywords in self.AUTOMATION_PATTERNS.items():
                for keyword in keywords:
                    if keyword in text:
                        if automation_type not in pattern_tasks:
                            pattern_tasks[automation_type] = []
                        if task.id not in pattern_tasks[automation_type]:
                            pattern_tasks[automation_type].append(task.id)

        # Generate automation suggestions
        for automation_type, task_ids in pattern_tasks.items():
            if len(task_ids) >= 1:  # Suggest automation for even single recurring tasks
                confidence = min(0.9, 0.6 + len(task_ids) * 0.1)

                suggestion, implementation = self._build_automation_suggestion(automation_type, len(task_ids))

                opportunities.append(AutomationOpportunity(
                    task_ids=task_ids,
                    automation_type=automation_type,
                    confidence=round(confidence, 2),
                    suggestion=suggestion,
                    implementation=implementation
                ))

        return opportunities

    def _build_automation_suggestion(self, automation_type: str, task_count: int) -> Tuple[str, str]:
        """Build automation suggestion and implementation details."""
        suggestions = {
            "recurring": (
                f"Detected {task_count} recurring task(s). Consider setting up automatic task creation on a schedule.",
                "Use cron jobs or task scheduler to create these tasks automatically at specified intervals."
            ),
            "integration": (
                f"Detected {task_count} task(s) that could benefit from API integration.",
                "Implement API integrations with email, calendar, or other services to sync data automatically."
            ),
            "scheduled": (
                f"Detected {task_count} task(s) that could be scheduled with reminders.",
                "Set up automated reminders or notifications for these tasks at specified times."
            )
        }

        return suggestions.get(automation_type, (
            f"Detected {task_count} task(s) with automation potential.",
            "Review these tasks for automation opportunities."
        ))

    def optimize_tasks(self, tasks: List[Task]) -> OptimizationResponse:
        """
        Run all optimization algorithms on tasks.

        Args:
            tasks: List of tasks to optimize

        Returns:
            Complete optimization response with all suggestions
        """
        duplicates = self.detect_duplicates(tasks)
        priorities = self.analyze_priority(tasks)
        time_estimates = self.estimate_time(tasks)
        groups = self.recommend_grouping(tasks)
        automations = self.detect_automation_opportunities(tasks)

        total_suggestions = (
            len(duplicates) +
            len(priorities) +
            len(time_estimates) +
            len(groups) +
            len(automations)
        )

        return OptimizationResponse(
            duplicates=duplicates,
            priorities=priorities,
            time_estimates=time_estimates,
            groups=groups,
            automations=automations,
            total_suggestions=total_suggestions,
            analysis_timestamp=datetime.utcnow()
        )
