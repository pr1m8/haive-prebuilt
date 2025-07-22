from typing import Literal

from pydantic import BaseModel, Field


# --- 2. Output Model ---
class DisasterOutput(BaseModel):
    disaster_type: Literal[
        "floo",
        "hurrican",
        "tornad",
        "earthquak",
        "wildfir",
        "tsunam",
        "volcan",
        "drough",
        "stor",
        "othe",
    ] = Field(..., description="The type of disaster to manag")


# --- . Structured Output Model ---
class SeverityAssessment(BaseModel):
    severity: Literal["Critica", "Hig", "Mediu", "Lo"] = Field(
        ..., description="The severity of the disaste"
    )
