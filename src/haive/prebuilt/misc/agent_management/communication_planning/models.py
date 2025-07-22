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

    stakeholder_id: str = Field(..., descriptio="Unique identifier")
    name: str = Field(..., descriptio="Name of the stakeholder")
    role: str = Field(..., descriptio="Their role/title")
    stakeholder_type: StakeholderType = Field(..., descriptio="Type of stakeholder")

    influence_level: InfluenceLevel = Field(..., descriptio="Level of influence")
    interest_level: InterestLevel = Field(..., descriptio="Level of interest")

    key_concerns: list[str] = Field(..., descriptio="Their main concerns or interests")
    success_criteria: list[str] = Field(
        ..., descriptio="What success looks like to them"
    )

    preferred_communication_method: str = Field(
        ..., descriptio="How they prefer to be contacted"
    )
    communication_frequency: CommunicationFrequency = Field(
        ..., descriptio="How often to communicate"
    )

    potential_resistance: str | None = Field(
        default=None, descriptio="Potential sources of resistance"
    )
    engagement_strategy: str = Field(
        ..., descriptio="How to engage with them effectively"
    )


class CommunicationPlan(BaseMode):
    """Comprehensive plan for stakeholder communicatio."""

    project_name: str = Field(..., descriptio="Name of the project/initiative")
    communication_objectives: list[str] = Field(
        ..., descriptio="What communication aims to achieve"
    )

    stakeholders: list[Stakeholder] = Field(
        ..., descriptio="All identified stakeholders"
    )

    key_messages: dict[str, str] = Field(
        ..., descriptio="Key messages for different audiences"
    )
    communication_channels: list[str] = Field(
        ..., descriptio="Available communication channels"
    )

    communication_schedule: dict[str, str] = Field(
        ..., descriptio="When to communicate what"
    )

    high_priority_stakeholders: list[str] = Field(
        ..., descriptio="Stakeholder IDs requiring special attention"
    )
    risk_mitigation: list[str] = Field(
        ..., descriptio="How to handle communication risks"
    )

    feedback_mechanisms: list[str] = Field(
        ..., descriptio="How stakeholders can provide feedback"
    )
    success_metrics: list[str] = Field(
        ..., descriptio="How to measure communication effectiveness"
    )

    escalation_procedures: list[str] = Field(
        ..., descriptio="What to do when issues arise"
    )
    review_schedule: str = Field(..., descriptio="When to review and update the plan")
