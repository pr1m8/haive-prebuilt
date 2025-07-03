from enum import Enum

from pydantic import BaseModel, Field


class StakeholderType(str, Enum):
    """Types of stakeholders in projects or initiatives."""

    SPONSOR = "sponsor"  # Project sponsor/champion
    DECISION_MAKER = "decision_maker"  # Has decision authority
    IMPLEMENTER = "implementer"  # Does the actual work
    USER = "user"  # End user of the output
    REVIEWER = "reviewer"  # Reviews and approves work
    INFORMEE = "informee"  # Needs to be kept informed
    SUBJECT_MATTER_EXPERT = "subject_matter_expert"  # Provides expertise


class InfluenceLevel(str, Enum):
    """Level of influence a stakeholder has."""

    HIGH = "high"  # High influence on project success
    MEDIUM = "medium"  # Moderate influence
    LOW = "low"  # Limited influence


class InterestLevel(str, Enum):
    """Level of interest a stakeholder has."""

    HIGH = "high"  # Very interested in the outcome
    MEDIUM = "medium"  # Somewhat interested
    LOW = "low"  # Little interest


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
    stakeholder_type: StakeholderType = Field(..., description="Type of stakeholder")

    influence_level: InfluenceLevel = Field(..., description="Level of influence")
    interest_level: InterestLevel = Field(..., description="Level of interest")

    key_concerns: list[str] = Field(..., description="Their main concerns or interests")
    success_criteria: list[str] = Field(
        ..., description="What success looks like to them"
    )

    preferred_communication_method: str = Field(
        ..., description="How they prefer to be contacted"
    )
    communication_frequency: CommunicationFrequency = Field(
        ..., description="How often to communicate"
    )

    potential_resistance: str | None = Field(
        default=None, description="Potential sources of resistance"
    )
    engagement_strategy: str = Field(
        ..., description="How to engage with them effectively"
    )


class CommunicationPlan(BaseModel):
    """Comprehensive plan for stakeholder communication."""

    project_name: str = Field(..., description="Name of the project/initiative")
    communication_objectives: list[str] = Field(
        ..., description="What communication aims to achieve"
    )

    stakeholders: list[Stakeholder] = Field(
        ..., description="All identified stakeholders"
    )

    key_messages: dict[str, str] = Field(
        ..., description="Key messages for different audiences"
    )
    communication_channels: list[str] = Field(
        ..., description="Available communication channels"
    )

    communication_schedule: dict[str, str] = Field(
        ..., description="When to communicate what"
    )

    high_priority_stakeholders: list[str] = Field(
        ..., description="Stakeholder IDs requiring special attention"
    )
    risk_mitigation: list[str] = Field(
        ..., description="How to handle communication risks"
    )

    feedback_mechanisms: list[str] = Field(
        ..., description="How stakeholders can provide feedback"
    )
    success_metrics: list[str] = Field(
        ..., description="How to measure communication effectiveness"
    )

    escalation_procedures: list[str] = Field(
        ..., description="What to do when issues arise"
    )
    review_schedule: str = Field(..., description="When to review and update the plan")
