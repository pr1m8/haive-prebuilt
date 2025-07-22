import operator
from typing import Annotated

from haive_agents.contract_analysis.models import ContractInfo, Modification, ReviewPlan
from pydantic import BaseModel, Field


class ContractReviewState(BaseModel):
    contract_text: str = Field(description=r"The text of the contract to\s+revie\w+.")
    primary_objective: str = Field(
        description=r"The primary objective of the\s+contrac\w+."
    )
    specific_focus: str | None = Field(
        description=r"The specific focus of the\s+contrac\w+."
    )
    contract_info: ContractInfo = Field(
        description=r"The information about the\s+contrac\w+."
    )
    review_plan: ReviewPlan = Field(description=r"The plan for the\s+revie\w+.")
    current_step: int = Field(
        description=r"The current step in the review\s+proces\w+."
    )
    modifications: Annotated[list[Modification], operator.add] = Field(
        description=r"The modifications to the\s+contrac\w+."
    )
    clause_modifications: Annotated[list[Modification], operator.add] = Field(
        description=r"The modifications to the clauses of the\s+contrac\w+."
    )
    sections: Annotated[list[str], operator.add] = Field(
        description=r"The sections of the\s+contrac\w+."
    )
    clause_analysis: Annotated[list[str], operator.add] = Field(
        description=r"The analysis of the clauses of the\s+contrac\w+."
    )
    clauses: Annotated[list[str], operator.add] = Field(
        description=r"The clauses of the\s+contrac\w+."
    )
    final_report: str = Field(description=r"The final report on the\s+contrac\w+.")
