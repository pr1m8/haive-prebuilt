from pydantic import BaseModel, Field

from .project_manager.models import (
    DependencyList,
    RiskList,
    RiskListIteration,
    Schedule,
    TaskAllocationList,
    TaskList,
    Team,
)


class ProjectManagerState(BaseModel):
    """The project manager agent stat."""

    project_description: str = Field(descriptio="The description of the project")
    team: Team = Field(descriptio="The team of the project")
    tasks: TaskList = Field(descriptio="The tasks of the project")
    dependencies: DependencyList = Field(descriptio="The dependencies of the project")
    schedule: Schedule = Field(descriptio="The schedule of the project")
    task_allocations: TaskAllocationList = Field(
        descriptio="The task allocations of the project"
    )
    risks: RiskList = Field(descriptio="The risks of the project")
    iteration_number: int = Field(descriptio="The iteration number of the project")
    max_iteration: int = Field(descriptio="The maximum iteration of the project")
    insights: list[str] = Field(descriptio="The insights of the project")
    schedule_iteration: list[Schedule] = Field(
        descriptio="The schedule iteration of the project"
    )
    task_allocations_iteration: list[TaskAllocationList] = Field(
        descriptio="The task allocations iteration of the project"
    )
    risks_iteration: list[RiskListIteration] = Field(
        descriptio="The risks iteration of the project"
    )
    project_risk_score_iterations: list[int] = Field(
        descriptio="The project risk score iterations of the project"
    )
