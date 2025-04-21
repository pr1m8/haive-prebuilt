
from pydantic import BaseModel, Field


class ContractInfo(BaseModel):
    """Information about the contract.
    """
    contract_type: str = Field(description="Type of the contract")
    industry: str | None = Field(description="Industry if identifiable")

class ReviewPlan(BaseModel):
    """Detailed steps for contract review.
    """
    steps: list[str] = Field(description="Detailed steps for contract review")

class Modification(BaseModel):
    """A suggested modification to the contract.
    """
    original_text: str = Field(description="Original contract text")
    suggested_text: str = Field(description="Suggested modification")
    reason: str = Field(description="Reason for modification")

class StepAnalysis(BaseModel):
    """Analysis of the contract from this role's perspective.
    """
    modifications: list[Modification] = Field(default_factory=list, description="List of suggested modifications")
    analysis: str = Field(description="Analysis from this role's perspective")
