"""Agent Utilities Models.

This module provides consolidated models for various agent utility functions
including goal decomposition, decision analysis, resource planning, quality
assessment, workflow optimization, and communication planning.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

# Communication Planning Models


class StakeholderType(str, Enum):
    """Types of stakeholders in projects or initiatives."""

    SPONSOR = "sponsor"
    DECISION_MAKER = "decision_maker"
    IMPLEMENTER = "implementer"
    USER = "user"
    REVIEWER = "reviewer"
    INFORMEE = "informee"
    SUBJECT_MATTER_EXPERT = "subject_matter_expert"


class InfluenceLevel(str, Enum):
    """Level of influence a stakeholder has."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class InterestLevel(str, Enum):
    """Level of interest a stakeholder has."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CommunicationFrequency(str, Enum):
    """How often to communicate with stakeholders."""

    DAILY = "daily"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    AS_NEEDED = "as_needed"


class Stakeholder(BaseModel):
    """Individual stakeholder in a project or initiative."""

    stakeholder_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the stakeholder")
    role: str = Field(..., description="Their role/title")
    type: StakeholderType = Field(..., description="Type of stakeholder")
    influence_level: InfluenceLevel = Field(..., description="Level of influence")
    interest_level: InterestLevel = Field(..., description="Level of interest")
    contact_info: Optional[str] = Field(None, description="Contact information")


class CommunicationPlan(BaseModel):
    """Communication plan for a stakeholder."""

    stakeholder_id: str = Field(..., description="Reference to stakeholder")
    frequency: CommunicationFrequency = Field(
        ..., description="Communication frequency"
    )
    method: str = Field(..., description="Communication method (email, meeting, etc.)")
    content_type: str = Field(..., description="Type of content to communicate")
    responsible_party: str = Field(
        ..., description="Who is responsible for communication"
    )


# Decision Analysis Models


class DecisionType(str, Enum):
    """Types of decisions that need to be made."""

    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"
    RESOURCE_ALLOCATION = "resource_allocation"
    PRIORITIZATION = "prioritization"


class DecisionCriteria(BaseModel):
    """Criteria for evaluating decision options."""

    criteria_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the criteria")
    description: str = Field(..., description="Description of the criteria")
    weight: float = Field(..., ge=0.0, le=1.0, description="Weight/importance (0-1)")
    is_constraint: bool = Field(
        default=False, description="Whether this is a hard constraint"
    )


class DecisionOption(BaseModel):
    """Option to be evaluated for a decision."""

    option_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the option")
    description: str = Field(..., description="Description of the option")
    pros: List[str] = Field(default_factory=list, description="Advantages")
    cons: List[str] = Field(default_factory=list, description="Disadvantages")
    estimated_cost: Optional[float] = Field(None, description="Estimated cost")
    estimated_effort: Optional[str] = Field(None, description="Estimated effort")


class DecisionAnalysis(BaseModel):
    """Complete decision analysis framework."""

    analysis_id: str = Field(..., description="Unique identifier")
    decision_title: str = Field(..., description="Title of the decision")
    decision_type: DecisionType = Field(..., description="Type of decision")
    criteria: List[DecisionCriteria] = Field(..., description="Evaluation criteria")
    options: List[DecisionOption] = Field(..., description="Available options")
    deadline: Optional[datetime] = Field(None, description="Decision deadline")
    stakeholders: List[str] = Field(
        default_factory=list, description="Involved stakeholders"
    )


# Goal Decomposition Models


class GoalType(str, Enum):
    """Types of goals."""

    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    PERSONAL = "personal"
    TEAM = "team"
    PROJECT = "project"


class GoalStatus(str, Enum):
    """Status of goal completion."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class PriorityLevel(str, Enum):
    """Priority levels for goals and tasks."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SubGoal(BaseModel):
    """Individual sub-goal within a larger goal decomposition."""

    subgoal_id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Title of the sub-goal")
    description: str = Field(..., description="Detailed description")
    priority: PriorityLevel = Field(..., description="Priority level")
    status: GoalStatus = Field(
        default=GoalStatus.NOT_STARTED, description="Current status"
    )
    estimated_effort: Optional[str] = Field(None, description="Estimated effort")
    dependencies: List[str] = Field(
        default_factory=list, description="Dependent sub-goal IDs"
    )
    assignee: Optional[str] = Field(None, description="Assigned person/team")
    due_date: Optional[datetime] = Field(None, description="Due date")


class GoalDecomposition(BaseModel):
    """Complete goal decomposition structure."""

    goal_id: str = Field(..., description="Unique identifier")
    main_goal: str = Field(..., description="Main goal statement")
    goal_type: GoalType = Field(..., description="Type of goal")
    target_completion: Optional[datetime] = Field(
        None, description="Target completion date"
    )
    success_criteria: List[str] = Field(..., description="Criteria for success")
    sub_goals: List[SubGoal] = Field(..., description="Decomposed sub-goals")
    owner: Optional[str] = Field(None, description="Goal owner")


# Resource Planning Models


class ResourceType(str, Enum):
    """Types of resources needed for projects."""

    HUMAN = "human"
    FINANCIAL = "financial"
    EQUIPMENT = "equipment"
    SOFTWARE = "software"
    INFRASTRUCTURE = "infrastructure"
    TIME = "time"
    EXPERTISE = "expertise"


class ResourceAvailability(str, Enum):
    """Availability status of resources."""

    AVAILABLE = "available"
    PARTIALLY_AVAILABLE = "partially_available"
    UNAVAILABLE = "unavailable"
    RESERVED = "reserved"
    ALLOCATED = "allocated"


class Resource(BaseModel):
    """Individual resource definition."""

    resource_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the resource")
    type: ResourceType = Field(..., description="Type of resource")
    description: str = Field(..., description="Description of the resource")
    availability: ResourceAvailability = Field(..., description="Current availability")
    cost_per_unit: Optional[float] = Field(None, description="Cost per unit")
    capacity: Optional[float] = Field(None, description="Maximum capacity")
    current_allocation: Optional[float] = Field(None, description="Current allocation")


class ResourceRequirement(BaseModel):
    """Requirement for a specific resource."""

    requirement_id: str = Field(..., description="Unique identifier")
    resource_type: ResourceType = Field(..., description="Type of resource needed")
    quantity_needed: float = Field(..., description="Quantity required")
    duration: Optional[str] = Field(None, description="Duration needed")
    priority: PriorityLevel = Field(..., description="Priority of this requirement")
    justification: str = Field(..., description="Why this resource is needed")
    alternatives: List[str] = Field(
        default_factory=list, description="Alternative resources"
    )


class ResourcePlan(BaseModel):
    """Complete resource planning document."""

    plan_id: str = Field(..., description="Unique identifier")
    project_name: str = Field(..., description="Name of the project")
    requirements: List[ResourceRequirement] = Field(
        ..., description="Resource requirements"
    )
    available_resources: List[Resource] = Field(..., description="Available resources")
    allocation_strategy: str = Field(..., description="Strategy for allocation")
    total_budget: Optional[float] = Field(None, description="Total budget available")
    timeline: Optional[str] = Field(None, description="Project timeline")


# Quality Assessment Models


class QualityDimension(str, Enum):
    """Dimensions of quality to assess."""

    FUNCTIONALITY = "functionality"
    RELIABILITY = "reliability"
    USABILITY = "usability"
    EFFICIENCY = "efficiency"
    MAINTAINABILITY = "maintainability"
    PORTABILITY = "portability"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"


class QualityMetric(BaseModel):
    """Individual quality metric definition."""

    metric_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the metric")
    dimension: QualityDimension = Field(..., description="Quality dimension")
    description: str = Field(..., description="Description of what this measures")
    measurement_method: str = Field(..., description="How to measure this metric")
    target_value: Optional[float] = Field(None, description="Target value")
    current_value: Optional[float] = Field(None, description="Current measured value")
    unit: Optional[str] = Field(None, description="Unit of measurement")


class QualityIssue(BaseModel):
    """Quality issue or defect."""

    issue_id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Title of the issue")
    description: str = Field(..., description="Detailed description")
    dimension: QualityDimension = Field(..., description="Quality dimension affected")
    severity: PriorityLevel = Field(..., description="Severity level")
    status: str = Field(default="open", description="Current status")
    assigned_to: Optional[str] = Field(None, description="Assigned person")
    created_date: datetime = Field(
        default_factory=datetime.now, description="Creation date"
    )


class QualityAssessment(BaseModel):
    """Complete quality assessment report."""

    assessment_id: str = Field(..., description="Unique identifier")
    subject: str = Field(..., description="What is being assessed")
    assessment_date: datetime = Field(
        default_factory=datetime.now, description="Assessment date"
    )
    metrics: List[QualityMetric] = Field(..., description="Quality metrics")
    issues: List[QualityIssue] = Field(
        default_factory=list, description="Identified issues"
    )
    overall_score: Optional[float] = Field(None, description="Overall quality score")
    recommendations: List[str] = Field(
        default_factory=list, description="Recommendations"
    )
    assessor: str = Field(..., description="Who performed the assessment")


# Workflow Optimization Models


class ProcessType(str, Enum):
    """Types of processes that can be optimized."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    ITERATIVE = "iterative"
    EVENT_DRIVEN = "event_driven"


class BottleneckType(str, Enum):
    """Types of bottlenecks in processes."""

    RESOURCE = "resource"
    DEPENDENCY = "dependency"
    APPROVAL = "approval"
    COMMUNICATION = "communication"
    TECHNICAL = "technical"
    CAPACITY = "capacity"


class ProcessStep(BaseModel):
    """Individual step in a process."""

    step_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Name of the step")
    description: str = Field(..., description="Description of what happens")
    estimated_duration: Optional[str] = Field(None, description="Estimated duration")
    required_resources: List[str] = Field(
        default_factory=list, description="Required resources"
    )
    prerequisites: List[str] = Field(
        default_factory=list, description="Prerequisite steps"
    )
    owner: Optional[str] = Field(None, description="Step owner")


class ProcessBottleneck(BaseModel):
    """Identified bottleneck in a process."""

    bottleneck_id: str = Field(..., description="Unique identifier")
    step_id: str = Field(..., description="Affected process step")
    type: BottleneckType = Field(..., description="Type of bottleneck")
    description: str = Field(..., description="Description of the bottleneck")
    impact: str = Field(..., description="Impact on the process")
    proposed_solution: Optional[str] = Field(None, description="Proposed solution")
    priority: PriorityLevel = Field(..., description="Priority for resolution")


class WorkflowOptimization(BaseModel):
    """Complete workflow optimization analysis."""

    optimization_id: str = Field(..., description="Unique identifier")
    workflow_name: str = Field(..., description="Name of the workflow")
    process_type: ProcessType = Field(..., description="Type of process")
    current_steps: List[ProcessStep] = Field(..., description="Current process steps")
    identified_bottlenecks: List[ProcessBottleneck] = Field(
        ..., description="Identified bottlenecks"
    )
    optimization_goals: List[str] = Field(..., description="Goals for optimization")
    proposed_changes: List[str] = Field(
        default_factory=list, description="Proposed changes"
    )
    expected_improvements: List[str] = Field(
        default_factory=list, description="Expected improvements"
    )
    implementation_plan: Optional[str] = Field(None, description="Implementation plan")
