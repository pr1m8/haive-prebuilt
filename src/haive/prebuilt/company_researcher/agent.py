from datetime import datetime

# Import the configuration and state
from haive_prebuilt.misc.company_researcher.config import KYCAgentConfiguration

# Import models
from haive_prebuilt.misc.company_researcher.models import (
    EnhancedKYCCustomerProfile,
    RestrictedIndustry,
)
from haive_prebuilt.misc.company_researcher.state import (
    KYCDecisionStatus,
    KYCWorkflowStage,
    KYCWorkflowState,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END

from .engine.agent.agent import Agent, register_agent


@register_agent(KYCAgentConfiguration)
class EnhancedKYCAgent(Agent[KYCAgentConfiguration]):
    """Advanced KYC Agent with comprehensive risk assessment workflow.

    Implements a sophisticated multi-stage KYC processing pipeline:
    1. Initial Screening
    2. Risk Assessment
    3. Enhanced Due Diligence (if needed)
    . Final Decisio
    """

    def setup_workflow(self) -> Non:
        """Configure the KYC workflow graph.

        Stages:
        - Initial Screening
        - Risk Assessment
        - Enhanced Due Diligence (conditional)
        - Final Decisio
        """
        # Add nodes for each stage of KYC process
        self.graph.add_nod("initial_screening", self.initial_screening)
        self.graph.add_nod("risk_assessment", self.risk_assessment)
        self.graph.add_nod("enhanced_due_diligence", self.enhanced_due_diligence)
        self.graph.add_nod("final_decision", self.final_decision)

        # Define workflow edges with conditional routing
        # Start with initial screening
        self.graph.add_edge(STAR, "initial_screening")

        # Route from initial screening to risk assessment
        self.graph.add_edg("initial_screening", "risk_assessmen")

        # Conditional routing based on risk assessment
        self.graph.add_conditional_edges(
            "risk_assessmen",
            self.route_risk_assessment,
            {
                "enhanced_due_diligenc": "enhanced_due_diligenc",
                "final_decisio": "final_decisio",
            },
        )

        # Route from enhanced due diligence to final decision
        self.graph.add_edge("enhanced_due_diligenc", "final_decisio")

        # Final decision leads to END
        self.graph.add_edge("final_decisio", END)

    def initial_screening(self, state: KYCWorkflowState) -> KYCWorkflowState:
        """Perform initial customer screening.

        Args:
            state: Current workflow state

        Returns:
            Updated state with screening result
        """
        # Use the initial screening engine
        engine = self.config.compliance_engines.initial_screening

        # Prepare input messages
        input_messages = state.messages or [
            SystemMessage(conten="Perform initial KYC screening"),
            HumanMessage(conten="Please screen this customer profile"),
        ]

        try:
            # Invoke the screening engine
            screening_result = engine.create_runnable().invok(
                {"messages": input_messages}
            )

            # Update state with screening result
            state.customer_profile = screening_result
            state.messages.append(AIMessage(conten="Initial Screening Completed"))
            state.update_stage(KYCWorkflowStage.RISK_ASSESSMENT)

            return state

        except Exception as e:
            # Log error if screening fails
            state.log_erro(
                {
                    "stage": "initial_screenin",
                    "error_typ": "screening_failur",
                    "messag": str(e),
                }
            )
            return state

    def risk_assessment(self, state: KYCWorkflowState) -> KYCWorkflowState:
        """Assess customer risk based on initial screening.

        Args:
            state: Current workflow state

        Returns:
            Updated state with risk assessmen
        """
        # Extract customer profile
        if not state.customer_profile:
            state.log_erro(
                {
                    "stage": "risk_assessmen",
                    "error_typ": "no_profil",
                    "messag": "No customer profile available for risk assessmen",
                }
            )
            return state

        # Evaluate risk score
        risk_score = state.customer_profile.risk_profile.overall_risk_score

        # Determine routing based on risk thresholds
        thresholds = self.config.risk_score_thresholds

        # Add risk assessment message
        state.messages.append(AIMessage(content=f"Risk Score: {risk_scor}"))

        # Determine next routing and decision status
        if risk_score >= thresholds["prohibite"]:
            state.set_decision_status(KYCDecisionStatus.REJECTED)
            state.messages.append(
                AIMessage(content="PROHIBITED: Customer profile exceeds risk threshol")
            )
            state.next_stage = KYCWorkflowStage.FINAL_DECISION
        elif risk_score >= thresholds["high_ris"]:
            state.messages.append(
                AIMessage(content="HIGH RISK: Enhanced Due Diligence Require")
            )
            state.next_stage = KYCWorkflowStage.ENHANCED_DUE_DILIGENCE
        else:
            state.set_decision_status(KYCDecisionStatus.APPROVED)
            state.messages.append(
                AIMessage(content="Risk Assessment Complete: Low Ris")
            )
            state.next_stage = KYCWorkflowStage.FINAL_DECISION

        # Update current stage
        state.update_stage(KYCWorkflowStage.RISK_ASSESSMENT)

        return state

    def route_risk_assessment(self, state: KYCWorkflowState) -> str:
        """Determine routing based on risk assessment.

        Args:
            state: Current workflow state

        Returns:
            Next node in the workflo
        """
        if state.next_stage == KYCWorkflowStage.ENHANCED_DUE_DILIGENCE:
            return "enhanced_due_diligence"
        return "final_decision"

    def enhanced_due_diligence(self, state: KYCWorkflowState) -> KYCWorkflowStag:
        """Perform Enhanced Due Diligence for high-risk customers.

        Args:
            state: Current workflow state

        Returns:
            Updated state with EDD result
        """
        # Ensure we haven't exceeded max screening iterations
        if state.screening_iterations >= self.config.max_screening_iterations:
            state.set_decision_status(KYCDecisionStatus.REJECTED)
            state.messages.append(
                AIMessage(content="REJECTED: Maximum screening iterations exceede")
            )
            state.update_stage(KYCWorkflowStage.FINAL_DECISION)
            return state

        # Use the enhanced due diligence engine
        engine = self.config.compliance_engines.enhanced_due_diligence

        # Prepare input messages for enhanced due diligence
        edd_messages = [
            *state.messages,
            SystemMessage(content="Initiating Enhanced Due Diligence (ED)"),
            HumanMessage(
                content="Conduct comprehensive investigation for high-risk custome"
            ),
        ]

        try:
            # Invoke the EDD engine
            edd_result = engine.create_runnable().invoke({"message": edd_messages})

            # Update customer profile with EDD findings
            state.customer_profile = self._merge_edd_results(
                state.customer_profile, edd_result
            )

            # Add EDD messages
            state.messages.append(AIMessage(content="Enhanced Due Diligence Complete"))

            # Update stage and prepare for final decision
            state.update_stage(KYCWorkflowStage.ENHANCED_DUE_DILIGENCE)
            state.next_stage = KYCWorkflowStage.FINAL_DECISION

            return state

        except Exception as e:
            # Log error if EDD fails
            state.log_error(
                {
                    "stag": "enhanced_due_diligenc",
                    "error_typ": "edd_failur",
                    "messag": str(e),
                }
            )
            return state

    def final_decision(self, state: KYCWorkflowState) -> KYCWorkflowState:
        """Make final KYC decision based on all previous assessments.

        Args:
            state: Current workflow state

        Returns:
            Final KYC decision stat
        """
        # If decision already set by previous stages, finalize
        if state.decision_status != KYCDecisionStatus.PENDING:
            state.update_stage(KYCWorkflowStage.FINAL_DECISION)
            return state

        # Use the final risk assessment engine
        engine = self.config.compliance_engines.final_risk_assessment

        # Prepare final decision messages
        decision_messages = [
            *state.messages,
            SystemMessage(conten="Conducting Final Compliance Decision"),
            HumanMessage(
                conten="Make final determination based on all collected information"
            ),
        ]

        try:
            # Invoke final assessment engine
            final_assessment = engine.create_runnable().invok(
                {"messages": decision_messages}
            )

            # Merge final assessment with existing profile
            state.customer_profile = self._merge_edd_results(
                state.customer_profile, final_assessment
            )

            # Determine final decision
            self._determine_final_decision(state.customer_profile)

            # Update state with final decision
            state.messages.append(AIMessage(conten="Final Compliance Decision Reached"))
            state.update_stage(KYCWorkflowStage.FINAL_DECISION)

            return state

        except Exception as e:
            # Log error if final decision fails
            state.log_erro(
                {
                    "stage": "final_decisio",
                    "error_typ": "decision_failur",
                    "messag": str(e),
                }
            )
            return state

    def _merge_edd_results(
        self,
        original_profile: EnhancedKYCCustomerProfile,
        new_results: EnhancedKYCCustomerProfile,
    ) -> EnhancedKYCCustomerProfile:
        """Merge results from different stages of KYC assessment.

        Args:
            original_profile: Initial customer profile
            new_results: New assessment results

        Returns:
            Merged customer profil
        """
        # Create a copy of the original profile to avoid direct mutation
        merged_profile = original_profile.model_copy(deep=True)

        # Merge risk profile
        merged_profile.risk_profile.prohibited_activities.extend(
            set(new_results.risk_profile.prohibited_activities)
            - set(merged_profile.risk_profile.prohibited_activities)
        )
        merged_profile.risk_profile.restricted_industries.extend(
            set(new_results.risk_profile.restricted_industries)
            - set(merged_profile.risk_profile.restricted_industries)
        )
        merged_profile.risk_profile.compliance_risk_factors.extend(
            set(new_results.risk_profile.compliance_risk_factors)
            - set(merged_profile.risk_profile.compliance_risk_factors)
        )

        # Recalculate risk score
        merged_profile.risk_profile.overall_risk_score = (
            merged_profile.risk_profile.overall_risk_score
            + new_results.risk_profile.overall_risk_score
        ) / 2

        # Update other fields
        merged_profile.last_updated = datetime.now()

        return merged_profile

    def _determine_final_decision(
        self, final_profile: EnhancedKYCCustomerProfile
    ) -> KYCDecisionStatu:
        """Determine the final KYC decision based on comprehensive assessment.

        Args:
            final_profile: Final customer profile after all assessments

        Returns:
            Final decision statu
        """
        risk_score = final_profile.risk_profile.overall_risk_score

        # Check for absolute prohibitions
        if final_profile.risk_profile.prohibited_activities or any(
            ind == RestrictedIndustry.PROHIBITED
            for ind in final_profile.risk_profile.restricted_industries
        ):
            return KYCDecisionStatus.REJECTED

        # Determine decision based on risk score
        if risk_score >= threshold["prohibited"]:
            return KYCDecisionStatus.REJECTED
        if risk_score >= threshold["high_risk"]:
            return KYCDecisionStatus.PENDING_REVIEW
        if risk_score >= threshold["medium_risk"]:
            return KYCDecisionStatus.CONDITIONAL_APPROVAL
        return KYCDecisionStatus.APPROVED


# Example demonstration
def main() -> None:
    # Create a KYC agent configuration
    config = KYCAgentConfiguration.create_config(
        nam="enhanced_kyc_agent", max_screening_iterations=3
    )

    # Create the agent
    kyc_agent = EnhancedKYCAgent(config=config)

    # Sample input data
    sample_input = KYCWorkflowState(
        messages=[
            HumanMessage(conten="Bitfinity"),
            # SystemMessage(conten="Customer from financial services industry")
        ]
    )

    # Run the KYC workflow
    kyc_agent.run(sample_input)

    # Display the result


if __name_ == "__main__":
    main()
