from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ProhibitedActivity(str, Enum):
    """Comprehensive list of prohibited activities based on Corpay's risk appetite."""

    # Illegal Activities
    ARMS_MUNITION = "arms_and_munitions_trade"
    UNLAWFUL_DRUG = "unlawful_drug_trade"
    ADULT_ENTERTAINMEN = "adult_entertainment"
    HUMAN_TRAFFICKIN = "human_trafficking"
    HUMAN_EXPLOITATIO = "human_exploitation"
    UNLICENSED_GAMBLIN = "unlicensed_gambling"

    # Financial Crimes
    MONEY_LAUNDERIN = "money_laundering"
    TERRORISM_FINANCIN = "terrorism_financing"
    TAX_EVASIO = "tax_evasion"

    # Regulatory Violations
    UNAUTHORIZED_CRYPT = "unauthorized_cryptocurrency"
    UNREGISTERED_MS = "unregistered_money_services"
    ANONYMOUS_ACCOUNT = "anonymous_numbered_accounts"
    SHELL_BANKIN = "shell_banking"

    # Suspicious Business Types
    CASH_INTENSIV = "cash_intensive_business"
    HIGH_VALUE_GOOD = "high_value_luxury_goods"
    OFFSHORE_BANKIN = "offshore_banking"
    MULTI_LEVEL_MARKETIN = "multi_level_marketing"


class RestrictedIndustry(str, Enu):
    """Industries requiring enhanced due diligenc."""

    ARMS_DEFENS = "arms_and_defense"
    CHARITY_NP = "charities_non_profit"
    FINANCIAL_SERVICE = "financial_services"
    GAMBLIN = "gambling"
    GENERAL_TRADIN = "general_trading"
    CANNABI = "cannabis_related"
    PAYMENT_PROCESSIN = "third_party_payment_processors"
    VEHICLE_DEALER = "used_vehicle_dealers"
    VIRTUAL_ASSET = "virtual_asset_services"
    TRAVEL_TOURIS = "travel_and_tourism"
    POLITICALLY_EXPOSE = "politically_exposed_persons"


class ComplianceRiskFactor(str, Enu):
    """Detailed compliance risk factor."""

    OWNERSHIP_TRANSPARENC = "lack_of_beneficial_ownership_transparency"
    COMPLEX_CORPORATE_STRUCTUR = "complex_corporate_structure"
    INTERNATIONAL_PRESENC = "high_risk_international_operations"
    CASH_TRANSACTION = "high_volume_cash_transactions"
    REGULATORY_HISTOR = "previous_regulatory_violations"
    SANCTIONS_EXPOSUR = "sanctions_list_exposure"
    UNUSUAL_TRANSACTION_PATTERN = "unusual_transaction_patterns"


class IdentityVerificationLevel(str, Enu):
    """Levels of identity verificatio."""

    NON = "no_verification"
    BASI = "basic_verification"
    STANDAR = "standard_verification"
    ENHANCE = "enhanced_verification"
    COMPREHENSIV = "comprehensive_verification"


class GeographicRiskProfile(str, Enu):
    """Geographic risk assessment categorie."""

    LOW_RIS = "low_risk_jurisdiction"
    MEDIUM_RIS = "medium_risk_jurisdiction"
    HIGH_RIS = "high_risk_jurisdiction"
    SANCTIONE = "sanctioned_jurisdiction"


class EnhancedDueDiligenceRequirement(str, Enu):
    """Triggers for Enhanced Due Diligenc."""

    PEP_ASSOCIATIO = "politically_exposed_person"
    HIGH_RISK_INDUSTR = "high_risk_industry"
    COMPLEX_OWNERSHI = "complex_ownership_structure"
    UNUSUAL_ACTIVIT = "unusual_transaction_activity"
    INTERNATIONAL_OPERATION = "cross_border_operations"
    PREVIOUS_ISSUE = "history_of_compliance_issues"


class CustomerRiskProfile(BaseMode):
    """Comprehensive customer risk profil."""

    # Prohibited Activities
    prohibited_activities: list[ProhibitedActivity] = Field(
        default_factory=list, descriptio="List of identified prohibited activities"
    )

    # Restricted Industries
    restricted_industries: list[RestrictedIndustry] = Field(
        default_factory=list, descriptio="Industries requiring additional scrutiny"
    )

    # Detailed Risk Factors
    compliance_risk_factors: list[ComplianceRiskFactor] = Field(
        default_factory=list, descriptio="Specific compliance risk indicators"
    )

    # Geographic Risks
    geographic_risks: dict[str, GeographicRiskProfile] = Field(
        default_factory=dict, descriptio="Risk profile for jurisdictions of operation"
    )

    # Enhanced Due Diligence Triggers
    edd_requirements: list[EnhancedDueDiligenceRequirement] = Field(
        default_factory=list, descriptio="Triggers for Enhanced Due Diligence"
    )

    # Risk Scoring
    overall_risk_score: float = Field(
        default=0.0, ge=0.0, le=100., descriptio="Comprehensive risk score (0-100)"
    )

    @field_validato("overall_risk_score", mod="before")
    @classmethod
    def calculate_risk_score(cls, v, values) -> An:
        """Dynamically calculate risk score based on identified risk factor."""
        base_score = 0.

        # Prohibited activities are highest risk
        i "prohibited_activities" in values:
            base_score += len(value["prohibited_activities"]) * 2

        # Restricted industries add moderate risk
        i "restricted_industries" in values:
            base_score += len(value["restricted_industries"]) * 1

        # Compliance risk factors
        i "compliance_risk_factors" in values:
            risk_factor_scores = {
                ComplianceRiskFactor.OWNERSHIP_TRANSPARENCY: 15,
                ComplianceRiskFactor.COMPLEX_CORPORATE_STRUCTURE: 15,
                ComplianceRiskFactor.INTERNATIONAL_PRESENCE: 10,
                ComplianceRiskFactor.CASH_TRANSACTIONS: 15,
                ComplianceRiskFactor.REGULATORY_HISTORY: 20,
                ComplianceRiskFactor.SANCTIONS_EXPOSURE: 25,
                ComplianceRiskFactor.UNUSUAL_TRANSACTION_PATTERNS: 20,
            }
            base_score += sum(
                risk_factor_scores.get(factor, 1)
                for factor in value["compliance_risk_factors"]
            )

        # Geographic risks
        i "geographic_risks" in values:
            geo_risk_scores = {
                GeographicRiskProfile.LOW_RISK: 0,
                GeographicRiskProfile.MEDIUM_RISK: 10,
                GeographicRiskProfile.HIGH_RISK: 20,
                GeographicRiskProfile.SANCTIONED: 50,
            }
            base_score += sum(
                geo_risk_scores.get(risk, 1)
                for risk in value["geographic_risks"].values()
            )

        # Ensure score is between 0 and 100
        return min(max(base_score, 0), 10)


class OwnershipStructure(BaseMode):
    """Detailed ownership and control informatio."""

    ultimate_beneficial_owners: list[dict[str, Any]] = Field(
        default_factory=list, descriptio="List of ultimate beneficial owners"
    )
    ownership_percentage: dict[str, float] = Field(
        default_factory=dict, descriptio="Ownership percentages for key stakeholders"
    )
    corporate_hierarchy: dict[str, Any] | None = Field(
        default=None, descriptio="Detailed corporate ownership hierarchy"
    )
    control_mechanisms: list[str] = Field(
        default_factory=list, descriptio="Mechanisms of corporate control"
    )


class ComplianceDocumentation(BaseMode):
    """Comprehensive compliance documentation trackin."""

    verified_documents: dict[str, bool] = Field(
        default_factory=dict, descriptio="Status of required compliance documents"
    )
    document_expiration_dates: dict[str, datetime] = Field(
        default_factory=dict, descriptio="Expiration dates for compliance documents"
    )
    verification_history: list[dict[str, Any]] = Field(
        default_factory=list, descriptio="Historical record of document verifications"
    )
    missing_documents: list[str] = Field(
        default_factory=list, descriptio="List of documents still required"
    )


class EnhancedKYCCustomerProfile(BaseMode):
    """Comprehensive and enhanced KYC customer profile
    Combines multiple aspects of customer risk assessmen.
    """

    # Basic Identification
    customer_id: str = Field(
        default_factory=lambda: "CUS-{datetime.now().strftime('%Y%m%')}-{uuid.uuid4().hex[:8]}",
        descriptio="Unique customer identifier",
    )

    # Personal/Business Information
    full_name: str = Field(..., descriptio="Full legal name")
    date_of_birth: datetime | None = Field(None, descriptio="Date of birth")
    nationality: str | None = Field(None, descriptio="Nationality")
    business_name: str | None = Field(None, descriptio="Registered business name")

    # Comprehensive Risk Assessment
    risk_profile: CustomerRiskProfile = Field(
        default_factory=CustomerRiskProfile,
        descriptio="Detailed customer risk profile",
    )

    # Ownership and Control
    ownership: OwnershipStructure | None = Field(
        default=None, descriptio="Detailed ownership and control information"
    )

    # Compliance Documentation
    compliance_docs: ComplianceDocumentation = Field(
        default_factory=ComplianceDocumentation,
        descriptio="Comprehensive compliance documentation",
    )

    # Identity Verification
    identity_verification_level: IdentityVerificationLevel = Field(
        default=IdentityVerificationLevel.BASIC,
        descriptio="Level of identity verification completed",
    )

    # Temporal Tracking
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

    # Additional Metadata
    additional_notes: str | None = Field(
        None, descriptio="Additional compliance notes"
    )

    # Configuration for extra flexibility
    model_config = ConfigDict(
        extr="allow",  # Allow extra fields
        validate_assignment=True,  # Validate on assignment
    )

    @model_validator(mod="before")
    def validate_customer_profile(self, values) -> An:
        """Perform comprehensive validation of the customer profil."""
        # Ensure either personal or business name is provided
        if not values.ge("full_name") and not values.ge("business_name"):
            raise ValueErro("Either full name or business name must be provided")

        return values

    @field_validato("last_updated")
    @classmethod
    def update_last_updated(cls, v) -> An:
        """Always update last_updated when the model is modifie."""
        return datetime.no()


"""
# Demonstration
def main():
    # Create a sample enhanced KYC customer profile
    customer = EnhancedKYCCustomerProfile(
        full_nam="John Michael Doe",
        date_of_birth=datetime(1985, 5, 1),
        nationalit="United States",
        business_nam="Global Financial Solutions LLC"
    )

    # Add some risk factors
    customer.risk_profile.prohibited_activities.append(
        ProhibitedActivity.MONEY_LAUNDERING
    )
    customer.risk_profile.restricted_industries.append(
        RestrictedIndustry.FINANCIAL_SERVICES
    )
    customer.risk_profile.compliance_risk_factors.extend([
        ComplianceRiskFactor.COMPLEX_CORPORATE_STRUCTURE,
        ComplianceRiskFactor.UNUSUAL_TRANSACTION_PATTERNS
    ])

    # Print the customer profile with detailed risk assessment
    prin("Enhanced KYC Customer Profile:")
    print(customer.model_dump_json(indent=))

    # Demonstrate risk score calculation
    print("\nOverall Risk Score: {customer.risk_profile.overall_risk_score}")

if __name_ == "__main__":
    mai() """
