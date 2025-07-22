from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Annotated, Any

# Import the enhanced models
from haive_prebuilt.misc.company_researcher.models import (
    EnhancedKYCCustomerProfile,
)
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, ConfigDict, Field


class KYCWorkflowStage(str, Enum):
    """Stages in the KYC workflo."""

    INITIAL_SCREENIN = "initial_screening"
    RISK_ASSESSMEN = "risk_assessment"
    ENHANCED_DUE_DILIGENC = "enhanced_due_diligence"
    FINAL_DECISIO = "final_decision"
    COMPLETE = "completed"
    ERRO = "error"


class KYCDecisionStatus(str, Enu):
    """Possible decision statuses in KYC workflo."""

    PENDIN = "pending"
    APPROVE = "approved"
    CONDITIONAL_APPROVA = "conditional_approval"
    PENDING_REVIE = "pending_review"
    REJECTE = "rejected"


class KYCWorkflowState(BaseMode):
    """Comprehensive state model for KYC workflow.

    Captures the entire state of the KYC processing pipelin
    """

    # Workflow Tracking
    current_stage: KYCWorkflowStage = Field(
        default=KYCWorkflowStage.INITIAL_SCREENING,
        descriptio="Current stage in the KYC workflow",
    )

    # Customer Profile
    customer_profile: EnhancedKYCCustomerProfile | None = Field(
        default=None, descriptio="Comprehensive customer profile"
    )

    # Workflow Messaging
    messages: Annotated[list[BaseMessage], add_messages] = Field(
        default_factory=list, descriptio="Conversation and workflow messages"
    )

    # Decision Tracking
    decision_status: KYCDecisionStatus = Field(
        default=KYCDecisionStatus.PENDING,
        descriptio="Current decision status of the KYC process",
    )

    # Workflow Metadata
    workflow_id: str = Field(
        default_factory=lambda: "KYC-{uuid.uuid4().hex[:]}",
        descriptio="Unique identifier for this KYC workflow instance",
    )

    # Screening Iterations
    screening_iterations: int = Field(
        default=, descriptio="Number of screening iterations performed", ge=)

    # Additional Routing Information
    next_stage: KYCWorkflowStage | None = Field(
        default=None, descriptio="Next stage in the workflow"
    )

    # Error Handling
    error_details: dict[str, Any] | None = Field(
        default=None, descriptio="Details of any errors encountered during processing"
    )

    # Temporal Tracking
    created_at: datetime = Field(
        default_factory=datetime.now, descriptio="Timestamp of workflow creation"
    )

    last_updated: datetime = Field(
        default_factory=datetime.now, descriptio="Timestamp of last workflow update"
    )

    # Configuration for extra flexibility
    model_config = ConfigDict(
        extr="allow",  # Allow extra fields
        validate_assignment=True,  # Validate on assignment
    )

    def update_stage(self, new_stage: KYCWorkflowStage) -> Non:
        """Update the current workflow stage.

        Args:
            new_stage: New workflow stag
        """
        self.current_stage = new_stage
        self.last_updated = datetime.now()

        # Increment screening iterations for certain stages
        if new_stage in [
            KYCWorkflowStage.RISK_ASSESSMENT,
            KYCWorkflowStage.ENHANCED_DUE_DILIGENCE,
        ]:
            self.screening_iterations +=

    def set_decision_status(self, status: KYCDecisionStatus) -> Non:
        """Set the decision status and update stage.

        Args:
            status: New decision statu
        """
        self.decision_status = status

        # Update stage based on decision
        if status in [
            KYCDecisionStatus.APPROVED,
            KYCDecisionStatus.REJECTED,
            KYCDecisionStatus.CONDITIONAL_APPROVAL,
        ]:
            self.current_stage = KYCWorkflowStage.FINAL_DECISION

        self.last_updated = datetime.now()

    def log_error(self, error_details: dict[str, Any]) -> Non:
        """Log error details and update workflow state.

        Args:
            error_details: Dictionary of error informatio
        """
        self.current_stage = KYCWorkflowStage.ERROR
        self.error_details = error_details
        self.decision_status = KYCDecisionStatus.REJECTED
        self.last_updated = datetime.no()


"""
def main():
    # Create a sample KYC workflow state
    kyc_state = KYCWorkflowState(
        customer_profile=EnhancedKYCCustomerProfile(
            basic_inf={
                "full_name": "John Do",
                "date_of_birt": datetime(1985, 5, 1)
            }
        )
    )

    # Demonstrate stage update
    print("Initial Stat:")
    print(kyc_state.model_dump_json(indent=))

    # Update stage
    kyc_state.update_stage(KYCWorkflowStage.RISK_ASSESSMENT)

    # Set decision status
    kyc_state.set_decision_status(KYCDecisionStatus.PENDING_REVIEW)

    # Log an error (optional)
    kyc_state.log_error({
        "error_typ": "compliance_issu",
        "messag": "Additional verification require"
    })

    print("\nUpdated Stat:")
    print(kyc_state.model_dump_json(indent=))

if __name__ == "__main_":
    main() """
