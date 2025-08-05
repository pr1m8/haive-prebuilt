from haive.agents.project_manager.state import AgentState
from langgraph.graph import END

from haive.prebuilt.project_manager.aug_llms import llm, schedule_llm
from haive.prebuilt.project_manager.models import (
    RiskList,
    Schedule,
    TaskAllocationList,
    TaskList,
)


# Node Functions
def task_dependency_node(state: AgentState):
    """Node to analyze task dependencies"""
    state["tasks"]
    # Simple implementation - in real scenario, this would analyze dependencies
    state["dependencies"] = []
    return state


def router(state: AgentState):
    """Router to determine next step based on risk score"""
    risk_score = state.get("project_risk_score", 0)
    if risk_score > 0.7:  # High risk threshold
        return "insight_generator"
    return END


def task_generation_node(state: AgentState):
    """LangGraph node that will extract tasks from given project description"""
    description = state["project_description"]
    prompt = f"""
        You are an expert project manager tasked with analyzing the following project description: {description}
        Your objectives are to:
        1. **Extract Actionable Tasks:**
            - Identify and list all actionable and realistic tasks necessary to complete the project.
            - Provide an estimated number of days required to complete each task.
        2. **Refine Long-Term Tasks:**
            - For any task estimated to take longer than 5 days, break it down into smaller, independent sub-tasks.
        **Requirements:** - Ensure each task is clearly defined and achievable.
            - Maintain logical sequencing of tasks to facilitate smooth project execution."""

    structure_llm = llm.with_structured_output(TaskList)
    tasks: TaskList = structure_llm.invoke(prompt)
    return {"tasks": tasks}

    def task_scheduler_node(state: AgentState):
        """LangGraph node that will schedule tasks based on dependencies and team availability"""
        state["dependencies"]
        state["tasks"]
        state[
            "insights"
        ]  # "" if state["insights"] is None else state["insights"].insights[-1]

        schedule: Schedule = schedule_llm.invoke(prompt)
        state["schedule"] = schedule
        state["schedule_iteration"].append(schedule)
        return state

    def task_allocation_node(state: AgentState):
        """LangGraph node that will allocate tasks to team members"""
        tasks = state["tasks"]
        schedule = state["schedule"]
        team = state["team"]
        insights = state[
            "insights"
        ]  # "" if state["insights"] is None else state["insights"].insights[-1]
        prompt = f"""
            You are a proficient project manager responsible for allocating tasks to team members efficiently.
            **Given:**
                - **Tasks:** {tasks}
                - **Schedule:** {schedule}
                - **Team Members:** {team}
                - **Previous Insights:** {insights}
                - **Previous Task Allocations (if any):** {state["task_allocations_iteration"]}
            **Your objectives are to:**
                1. **Allocate Tasks:**
                    - Assign each task to a team member based on their expertise and current availability.
                    - Ensure that no team member is assigned overlapping tasks during the same time period.
                2. **Optimize Assignments:**
                    - Utilize insights from previous iterations to improve task allocations.
                    - Balance the workload evenly among team members to enhance productivity and prevent burnout.
                    **Constraints:**
                        - Each team member can handle only one task at a time.
                        - Assignments should respect the skills and experience of each team member.
            """
        structure_llm = llm.with_structured_output(TaskAllocationList)
        task_allocations: TaskAllocationList = structure_llm.invoke(prompt)
        state["task_allocations"] = task_allocations
        state["task_allocations_iteration"].append(task_allocations)
        return state

    def risk_assessment_node(state: AgentState):
        """LangGraph node that analyse risk associated with schedule and allocation of task"""
        schedule = state["schedule"]
        task_allocations = state["task_allocations"]
        prompt = f"""
            You are a seasoned project risk analyst tasked with evaluating the risks associated with the current project plan.
            **Given:**
                - **Task Allocations:** {task_allocations}
                - **Schedule:** {schedule}
                - **Previous Risk Assessments (if any):** {state["risks_iteration"]}
            **Your objectives are to:**
                1. **Assess Risks:**
                    - Analyze each allocated task and its scheduled timeline to identify potential risks.
                    - Consider factors such as task complexity, resource availability, and dependency constraints.
                2. **Assign Risk Scores:**
                - Assign a risk score to each task on a scale from 0 (no risk) to 10 (high risk).
                - If a task assignment remains unchanged from a previous iteration (same team member and task), retain the existing risk score to ensure consistency.
                - If the team member has more time between tasks - assign lower risk score for the tasks
                - If the task is assigned to a more senior person - assign lower risk score for the tasks
                3. **Calculate Overall Project Risk:**
                - Sum the individual task risk scores to determine the overall project risk score.
            """
        structure_llm = llm.with_structured_output(RiskList)
        risks: RiskList = structure_llm.invoke(prompt)
        project_task_risk_scores = [int(risk.score) for risk in risks.risks]
        project_risk_score = sum(project_task_risk_scores)
        state["risks"] = risks
        state["project_risk_score"] = project_risk_score
        state["iteration_number"] += 1
        state["project_risk_score_iterations"].append(project_risk_score)
        state["risks_iteration"].append(risks)
        return state

    def insight_generation_node(state: AgentState):
        """LangGraph node that generate insights from the schedule, task allocation, and risk associated"""
        schedule = state["schedule"]
        task_allocations = state["task_allocations"]
        risks = state["risks"]
        prompt = f"""
            You are an expert project manager responsible for generating actionable insights to enhance the project plan.
            **Given:**
                - **Task Allocations:** {task_allocations}
                - **Schedule:** {schedule}
                - **Risk Analysis:** {risks}
            **Your objectives are to:**
                1. **Generate Critical Insights:**
                - Analyze the current task allocations, schedule, and risk assessments to identify areas for improvement.
                - Highlight any potential bottlenecks, resource conflicts, or high-risk tasks that may jeopardize project success.
                2. **Recommend Enhancements:**
                - Suggest adjustments to task assignments or scheduling to mitigate identified risks.
                - Propose strategies to optimize resource utilization and streamline workflow.
                    **Requirements:**
                    - Ensure that all recommendations aim to reduce the overall project risk score.
                    - Provide clear and actionable suggestions that can be implemented in subsequent iterations.
            """
        insights = llm.invoke(prompt).content
        return {"insights": insights}
