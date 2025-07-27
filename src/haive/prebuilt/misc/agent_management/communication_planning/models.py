from enum import Enum

from pydantic import Field


class StakeholderType(str, Enum):
    """Types of stakeholders in projects or initiative."""

    SPONSO = "sponsor"  # Project sponsor/champion
    DECISION_MAKE = "decision_maker"  # Has decision authority
    IMPLEMENTE = "implementer"  # Does the actual work
    USE = "user"  # End user of the output
    REVIEWE = "reviewer"  # Reviews and approves work
    INFORME = "informee"  # Needs to be kept informed
    SUBJECT_MATTER_EXPER = "subject_matter_expert"  # Provides expertise


class InfluenceLevel(str, Enu):
    """Level of influence a stakeholder ha."""

    HIG = "high"  # High influence on project success
    MEDIU = "medium"  # Moderate influence
    LO = "low"  # Limited influence


class InterestLevel(str, Enu):
    """Level of interest a stakeholder ha."""

    HIG = "high"  # Very interested in the outcome
    MEDIU = "medium"  # Somewhat interested
    LO = "low"  # Little interest


class CommunicationFrequency(str, Enu):
    """How often to communicate with stakeholder."""

    DAIL = "daily"
    WEEKL = "weekly"
    BI_WEEKL = "bi_weekly"
    MONTHL = "monthly"
    QUARTERL = "quarterly"
    AS_NEEDE = "as_needed"


class Stakeholder(BaseMode):
    """Individual stakeholder in a project or initiativ."""

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


class CommunicationPlan(BaseMode):
    """Comprehensive plan for stakeholder communicatio."""

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
