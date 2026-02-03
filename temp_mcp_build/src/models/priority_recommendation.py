"""
PriorityRecommendation model for storing AI-suggested task priorities.
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from enum import Enum


class PriorityLevel(str, Enum):
    """Priority levels for tasks."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PriorityRecommendation(SQLModel, table=True):
    """Priority recommendation entity for AI-suggested task priorities."""

    __tablename__ = "priority_recommendations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    task_id: int = Field(foreign_key="tasks.id", index=True)

    # Recommendation details
    recommended_priority: str = Field(max_length=20)  # high, medium, low
    current_priority: Optional[str] = Field(default=None, max_length=20)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)  # Confidence score 0-1

    # Analysis details
    reasoning: str = Field(max_length=500)  # Explanation for the recommendation
    keywords: List[str] = Field(sa_column=Column(JSON))  # Keywords that influenced priority
    factors: dict = Field(sa_column=Column(JSON))  # Additional factors considered

    # User action
    applied: bool = Field(default=False)  # Whether user applied the recommendation
    rejected: bool = Field(default=False)  # Whether user rejected the recommendation
    user_feedback: Optional[str] = Field(default=None, max_length=500)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    applied_at: Optional[datetime] = None


class PriorityRecommendationCreate(SQLModel):
    """Schema for creating a priority recommendation."""

    task_id: int
    recommended_priority: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(max_length=500)
    keywords: List[str] = []
    factors: dict = {}


class PriorityRecommendationUpdate(SQLModel):
    """Schema for updating a priority recommendation."""

    applied: Optional[bool] = None
    rejected: Optional[bool] = None
    user_feedback: Optional[str] = Field(default=None, max_length=500)


class PriorityRecommendationResponse(SQLModel):
    """Schema for priority recommendation response."""

    id: int
    user_id: int
    task_id: int
    recommended_priority: str
    current_priority: Optional[str]
    confidence: float
    reasoning: str
    keywords: List[str]
    factors: dict
    applied: bool
    rejected: bool
    user_feedback: Optional[str]
    created_at: datetime
    updated_at: datetime
    applied_at: Optional[datetime]


class PriorityAnalysisRequest(SQLModel):
    """Schema for requesting priority analysis."""

    task_ids: Optional[List[int]] = None  # Specific tasks to analyze, None = all tasks
    include_completed: bool = False  # Whether to include completed tasks
    min_confidence: float = Field(default=0.5, ge=0.0, le=1.0)  # Minimum confidence threshold


class PriorityAnalysisResult(SQLModel):
    """Schema for priority analysis results."""

    task_id: int
    task_title: str
    recommended_priority: str
    confidence: float
    reasoning: str
    keywords: List[str]
    change_required: bool  # True if current priority differs from recommended


class PriorityDistribution(SQLModel):
    """Schema for priority distribution statistics."""

    high_count: int
    medium_count: int
    low_count: int
    unassigned_count: int
    total_count: int
    recommendations_pending: int
    recommendations_applied: int
    recommendations_rejected: int


class PriorityKeywordAnalysis(SQLModel):
    """Schema for keyword-based priority analysis."""

    keyword: str
    frequency: int
    average_priority: str
    tasks_with_keyword: List[int]
