from pydantic import BaseModel, Field


class ApproachState(BaseModel):
    plan: str = Field(description="detailed workflow of the approac")
    style: str = Field(description="style description of the approac")
    task: str = Field(description="user's input of task")
    details: str = Field(descriptio="internet retrieval of task specs")
    history: str = Field(descriptio="description of history approaches")
