# Data Models
import uuid

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="Unique identifier for the task"
    )
    task_name: str = Field(description="Name of the task")
    task_description: str = Field(description="Description of the task")
    estimated_day: int = Field(
        description="Estimated number of days to complete the task"
    )


class TaskList(BaseModel):
    tasks: list[Task] = Field(description="List of tasks")


class TaskDependency(BaseModel):
    """Task dependency model"""

    task: Task = Field(description="Task")
    dependent_tasks: list[Task] = Field(description="List of dependent tasks")


class TeamMember(BaseModel):
    name: str = Field(description="Name of the team member")
    profile: str = Field(description="Profile of the team member")


class Team(BaseModel):
    team_members: list[TeamMember] = Field(description="List of team members")


# Iterative assessment
class TaskAllocation(BaseModel):
    """Task allocation class"""

    task: Task = Field(description="Task")
    team_member: TeamMember = Field(description="Team members assigned to the task")


class TaskSchedule(BaseModel):
    """Schedule schedule class"""

    task: Task = Field(description="Task")
    start_day: int = Field(description="Start day of the task")
    end_day: int = Field(description="End day of the task")


# Lists
class DependencyList(BaseModel):
    """List of task dependencies"""

    dependencies: list[TaskDependency] = Field(description="List of task dependencies")


class Schedule(BaseModel):
    """List of task schedules"""

    schedule: list[TaskSchedule] = Field(description="List of task schedules")


class TaskAllocationList(BaseModel):
    """List of task allocations"""

    task_allocations: list[TaskAllocation] = Field(
        description="List of task allocations"
    )


# Iteration
class TaskAllocationListIteration(BaseModel):
    """List of task allocations for each iteration"""

    task_allocations_iteration: list[TaskAllocationList] = Field(
        description="List of task allocations for each iteration"
    )


class ScheduleIteration(BaseModel):
    """List of task schedules for each iteration"""

    schedule: list[Schedule] = Field(
        description="List of task schedules for each iteration"
    )


class Risk(BaseModel):
    """Risk of a task"""

    task: Task = Field(description="Task")
    score: str = Field(description="Risk associated with the task")


class RiskList(BaseModel):
    """List of risks for each iteration"""

    risks: list[Risk] = Field(description="List of risks")


class RiskListIteration(BaseModel):
    """List of risks for each iteration"""

    risks_iteration: list[RiskList] = Field(
        description="List of risks for each iteration"
    )
