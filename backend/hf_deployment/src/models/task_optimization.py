"""
TaskOptimization model for storing optimization analysis results.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON


class TaskOptimization(SQLModel, table=True):
    """Task optimization entity for storing AI analysis results."""

    __tablename__ = "task_optimizations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Analysis metadata
    analysis_type: str = Field(max_length=50, index=True)  # duplicate, priority, time_estimate, grouping, automation
    task_ids: List[int] = Field(sa_column=Column(JSON))  # Tasks analyzed

    # Results
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)  # Confidence score 0-1
    suggestions: Dict[str, Any] = Field(sa_column=Column(JSON))  # Analysis results

    # Status
    applied: bool = Field(default=False)  # Whether user applied the suggestion
    rejected: bool = Field(default=False)  # Whether user rejected the suggestion

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DuplicateDetection(SQLModel):
    """Schema for duplicate task detection result."""

    task_ids: List[int]
    similarity_score: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    suggestion: str
    merge_recommendation: Optional[str] = None


class PriorityAnalysis(SQLModel):
    """Schema for priority recommendation result."""

    task_id: int
    priority: str  # high, medium, low
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    keywords: List[str]


class TimeEstimate(SQLModel):
    """Schema for time estimation result."""

    task_id: int
    estimated_hours: float = Field(gt=0)
    confidence_interval: Dict[str, float]  # {min: X, max: Y}
    confidence: float = Field(ge=0.0, le=1.0)
    complexity_factors: List[str]


class TaskGrouping(SQLModel):
    """Schema for task grouping recommendation."""

    name: str
    task_ids: List[int]
    category: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class AutomationOpportunity(SQLModel):
    """Schema for automation detection result."""

    task_ids: List[int]
    automation_type: str  # recurring, integration, api, scheduled
    confidence: float = Field(ge=0.0, le=1.0)
    suggestion: str
    implementation: str


class OptimizationRequest(SQLModel):
    """Schema for optimization request."""

    task_ids: Optional[List[int]] = None  # Specific tasks to analyze, None = all tasks
    analysis_types: Optional[List[str]] = None  # Specific analyses, None = all types


class OptimizationResponse(SQLModel):
    """Schema for optimization response."""

    duplicates: List[DuplicateDetection] = []
    priorities: List[PriorityAnalysis] = []
    time_estimates: List[TimeEstimate] = []
    groups: List[TaskGrouping] = []
    automations: List[AutomationOpportunity] = []
    total_suggestions: int
    analysis_timestamp: datetime


class OptimizationActionRequest(SQLModel):
    """Schema for applying/rejecting optimization suggestion."""

    optimization_id: int
    action: str  # apply, reject
    parameters: Optional[Dict[str, Any]] = None  # Additional parameters for applying
