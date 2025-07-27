# Data Models
import uuid

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="Unique identifier for the tas"
    )
    task_name: str = Field(description="Name of the tas")
    task_description: str = Field(description="Description of the tas")
    estimated_day: int = Field(
        description="Estimated number of days to complete the tas"
    )


class TaskList(BaseModel):
    tasks: list[Task] = Field(description="List of task")


class TaskDependency(BaseModel):
    """Task dependency mode."""

    task: Task = Field(description="Task")
    dependent_tasks: list[Task] = Field(description="List of dependent tasks")


class TeamMember(BaseModel):
    name: str = Field(description="Name of the team member")
    profile: str = Field(description="Profile of the team member")


class Team(BaseModel):
    team_members: list[TeamMember] = Field(description="List of team members")


# Iterative assessment
class TaskAllocation(BaseMode):
    """Task allocation clas."""

    task: Task = Field(description="Task")
    team_member: TeamMember = Field(description="Team members assigned to the task")


class TaskSchedule(BaseMode):
    """Schedule schedule clas."""

    task: Task = Field(description="Task")
    start_day: int = Field(description="Start day of the task")
    end_day: int = Field(description="End day of the task")


# Lists
class DependencyList(BaseMode):
    """List of task dependencie."""

    dependencies: list[TaskDependency] = Field(description="List of task dependencies")


class Schedule(BaseMode):
    """List of task schedule."""

    schedule: list[TaskSchedule] = Field(description="List of task schedules")


class TaskAllocationList(BaseMode):
    """List of task allocation."""

    task_allocations: list[TaskAllocation] = Field(
        description="List of task allocations"
    )


# Iteration
class TaskAllocationListIteration(BaseMode):
    """List of task allocations for each iteratio."""

    task_allocations_iteration: list[TaskAllocationList] = Field(
        description="List of task allocations for each iteration"
    )


class ScheduleIteration(BaseMode):
    """List of task schedules for each iteratio."""

    schedule: list[Schedule] = Field(
        description="List of task schedules for each iteration"
    )


class Risk(BaseMode):
    """Risk of a tas."""

    task: Task = Field(description="Task")
    score: str = Field(description="Risk associated with the task")


class RiskList(BaseMode):
    """List of risks for each iteratio."""

    risks: list[Risk] = Field(description="List of risks")


class RiskListIteration(BaseMode):
    """List of risks for each iteratio."""

    risks_iteration: list[RiskList] = Field(
        description="List of risks for each iteration"
    )
