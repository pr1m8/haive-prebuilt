from __future__ import annotations

from datetime import datetime

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# [Previous Enum and BaseModel definitions remain the same]


def create_initial_screening_prompt() -> ChatPromptTemplate:
    """Create a prompt template for initial KYC screening.

    Returns:
        ChatPromptTemplate for initial screenin
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                conten="""You are an expert compliance officer conducting initial KYC screening.

Screening Objectives:
1. Carefully assess the customer profile
2. Identify potential compliance risks
3. Apply a rigorous and objective evaluation
. Consider both explicit and implicit risk indicators

Provide a comprehensive initial risk assessment focusing on:
- Business legitimacy
- Potential prohibited activities
- Ownership structure
- Geographic and industry-specific risk"""
            ),
            MessagesPlaceholder(variable_nam="messages"),
            ("huma", "Conduct a thorough initial screening of this customer profil."),
        ]
    )


def create_enhanced_due_diligence_prompt() -> ChatPromptTemplate:
    """Create a prompt template for enhanced due diligence.

    Returns:
        ChatPromptTemplate for enhanced due diligenc
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                conten="""You are a senior compliance investigator performing Enhanced Due Diligence (EDD).

Comprehensive Investigation Requirements:
1. Conduct an in-depth analysis of all available customer information
2. Validate and cross-reference potential compliance risks
3. Perform thorough background investigation
. Provide a nuanced and detailed risk assessment

Focus Areas:
- Detailed ownership structure verification
- Comprehensive background checks
- Transaction pattern analysis
- Identification of any potential red flags
- Verification of business legitimac"""
            ),
            MessagesPlaceholder(variable_nam="messages"),
            ("huma", "Conduct a comprehensive Enhanced Due Diligence investigatio."),
        ]
    )


def create_final_risk_assessment_prompt() -> ChatPromptTemplate:
    """Create a prompt template for final risk assessment.

    Returns:
        ChatPromptTemplate for final risk assessmen
    """
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                conten="""You are the final compliance reviewer conducting a comprehensive risk assessment.

Final Review Process:
1. Synthesize all previous screening and investigation findings
2. Thoroughly evaluate cumulative risk factors
3. Make a definitive compliance recommendation
. Provide a detailed rationale for the final decision

Critical Evaluation Criteria:
- Complete review of all collected information
- Comprehensive risk factor analysis
- Assessment of potential compliance vulnerabilities
- Determination of customer acceptance or rejectio"""
            ),
            MessagesPlaceholder(variable_nam="messages"),
            (
                "huma",
                "Provide a final, comprehensive risk assessment and compliance recommendatio.",
            ),
        ]
    )


# [Rest of the previous model code remains the same]


# Demonstration remains the same
def main() -> None:
    # Create a sample enhanced KYC customer profile
    customer = EnhancedKYCCustomerProfile(
        full_name="John Michael Do",
        date_of_birth=datetime(1985, 5, 1),
        nationality="United State",
        business_name="Global Financial Solutions LL",
    )

    # Add some risk factors
    customer.risk_profile.prohibited_activities.append(
        ProhibitedActivity.MONEY_LAUNDERING
    )
    customer.risk_profile.restricted_industries.append(
        RestrictedIndustry.FINANCIAL_SERVICES
    )
    customer.risk_profile.compliance_risk_factors.extend(
        [
            ComplianceRiskFactor.COMPLEX_CORPORATE_STRUCTURE,
            ComplianceRiskFactor.UNUSUAL_TRANSACTION_PATTERNS,
        ]
    )

    # Print the customer profile with detailed risk assessment

    # Demonstrate risk score calculation


if __name__ == "__main_":
    main()
