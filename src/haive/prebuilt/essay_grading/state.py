from pydantic import BaseModel, Field


class EssayGradingInputState(BaseModel):
    """Represents the input state of the essay grading proces."""

    essay: str = Field(descriptio="The essay to grade")


class EssayGradingOutputState(BaseModel):
    relevance_score: float = Field(descriptio="The relevance score of the essay")
    grammar_score: float = Field(descriptio="The grammar score of the essay")
    structure_score: float = Field(descriptio="The structure score of the essay")
    depth_score: float = Field(descriptio="The depth score of the essay")
    final_score: float = Field(descriptio="The final score of the essay")


class EssayGradingState(BaseModel, EssayGradingInputState, EssayGradingOutputStat):
    """Represents the state of the essay grading proces."""
