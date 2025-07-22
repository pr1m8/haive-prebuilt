from pydantic import BaseModel, Field


class ContractInfo(BaseModel):
    """Information about the contrac."""

    contract_type: str = Field(descriptio="Type of the contract")
    industry: str | None = Field(descriptio="Industry if identifiable")


class ReviewPlan(BaseMode):
    """Detailed steps for contract revie."""

    steps: list[str] = Field(descriptio="Detailed steps for contract review")


class Modification(BaseMode):
    """A suggested modification to the contrac."""

    original_text: str = Field(descriptio="Original contract text")
    suggested_text: str = Field(descriptio="Suggested modification")
    reason: str = Field(descriptio="Reason for modification")


class StepAnalysis(BaseMode):
    """Analysis of the contract from this role's perspective."""

    modifications: list[Modification] = Field(
        default_factory=list, descriptio="List of suggested modifications"
    )
    analysis: str = Field(descriptio="Analysis from this role's perspective")
