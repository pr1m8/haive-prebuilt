from pydantic import BaseModel, Field

from haive.prebuilt.project_manager.models import (
    DependencyList,
    RiskList,
    RiskListIteration,
    Schedule,
    TaskAllocationList,
    TaskList,
    Team,
)


class ProjectManagerState(BaseModel):
    """The project manager agent state."""

    project_description: str = Field(description="The description of the project")
    team: Team = Field(description="The team of the project")
    tasks: TaskList = Field(description="The tasks of the project")
    dependencies: DependencyList = Field(description="The dependencies of the project")
    schedule: Schedule = Field(description="The schedule of the project")
    task_allocations: TaskAllocationList = Field(
        description="The task allocations of the project"
    )
    risks: RiskList = Field(description="The risks of the project")
    iteration_number: int = Field(description="The iteration number of the project")
    max_iteration: int = Field(description="The maximum iteration of the project")
    insights: list[str] = Field(description="The insights of the project")
    schedule_iteration: list[Schedule] = Field(
        description="The schedule iteration of the project"
    )
    task_allocations_iteration: list[TaskAllocationList] = Field(
        description="The task allocations iteration of the project"
    )
    risks_iteration: list[RiskListIteration] = Field(
        description="The risks iteration of the project"
    )
    project_risk_score_iterations: list[int] = Field(
        description="The project risk score iterations of the project"
    )
