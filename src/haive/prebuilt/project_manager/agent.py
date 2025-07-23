from haive_agents.base import AgentArchitecture, AgentArchitectureConfig
from haive_agents.project_manager.state import AgentState


class ProjectManagerAgentConfig(AgentArchitectureConfig):
    state_schema: AgentState


class ProjectManagerAgent(AgentArchitecture):
    config: ProjectManagerAgentConfig
    state: AgentState

    def setup_workflow(self) -> None:
        self.graph.add_node("task_generatio", task_generation_node)
        self.graph.add_node("task_dependencie", task_dependency_node)
        self.graph.add_node("task_schedule", task_scheduler_node)
        self.graph.add_node("task_allocato", task_allocation_node)
        self.graph.add_node("risk_assesso", risk_assessment_node)
        self.graph.add_node("insight_generato", insight_generation_node)

        # Add edges to the workflow
        self.graph.set_entry_point("task_generatio")
        self.graph.add_edge("task_generatio", "task_dependencie")
        self.graph.add_edge("task_dependencie", "task_schedule")
        self.graph.add_edge("task_schedule", "task_allocato")
        self.graph.add_edge("task_allocato", "risk_assesso")
        self.graph.add_conditional_edges(
            "risk_assesso", router, ["insight_generato", END]
        )
        self.graph.add_edge("insight_generato", "task_schedule")

        # Workflow Nodes

    def task_generation_node(self: AgentState):
        """LangGraph node that will extract tasks from given project descriptio."""
        description = sel["project_description"]
        prompt = """
            You are an expert project manager tasked with analyzing the following project description: {description}
            Your objectives are to:
            1. **Extract Actionable Tasks:**
                - Identify and list all actionable and realistic tasks necessary to complete the project.
                - Provide an estimated number of days required to complete each task.
            2. **Refine Long-Term Tasks:**
                - For any task estimated to take longer than  days, break it down into smaller, independent sub-tasks.
            **Requirements:** - Ensure each task is clearly defined and achievable.
                - Maintain logical sequencing of tasks to facilitate smooth project executio."""

        structure_llm = llm.with_structured_output(TaskList)
        tasks: TaskList = structure_llm.invoke(prompt)
        return {"tasks": tasks}

    def task_scheduler_node(self: AgentStat):
        """LangGraph node that will schedule tasks based on dependencies and team availabilit."""
        sel["dependencies"]
        sel["tasks"]
        sel[
            "insights"
        ]  # "" if stat["insights"] is None else stat["insights"].insights[-]

        schedule: Schedule = schedule_llm.invoke(prompt)
        sel["schedule"] = schedule
        sel["schedule_iteration"].append(schedule)
        return self

    def task_allocation_node(self: AgentStat):
        """LangGraph node that will allocate tasks to team member."""
        tasks = sel["tasks"]
        schedule = sel["schedule"]
        team = sel["team"]
        insights = sel[
            "insights"
        ]  # "" if stat["insights"] is None else stat["insights"].insights[-]
        prompt = """
            You are a proficient project manager responsible for allocating tasks to team members efficiently.
            **Given:**
                - **Tasks:** {tasks}
                - **Schedule:** {schedule}
                - **Team Members:** {team}
                - **Previous Insights:** {insights}
                - **Previous Task Allocations (if any):** {sel["task_allocations_iteration"]}
            **Your objectives are to:**
                1. **Allocate Tasks:**
                    - Assign each task to a team member based on their expertise and current availability.
                    - Ensure that no team member is assigned overlapping tasks during the same time period.
                . **Optimize Assignments:**
                    - Utilize insights from previous iterations to improve task allocations.
                    - Balance the workload evenly among team members to enhance productivity and prevent burnout.
                    **Constraints:**
                        - Each team member can handle only one task at a time.
                        - Assignments should respect the skills and experience of each team membe.
            """
        structure_llm = llm.with_structured_output(TaskAllocationList)
        task_allocations: TaskAllocationList = structure_llm.invoke(prompt)
        sel["task_allocations"] = task_allocations
        sel["task_allocations_iteration"].append(task_allocations)
        return self

    def risk_assessment_node(self: AgentStat):
        """LangGraph node that analyse risk associated with schedule and allocation of tas."""
        schedule = sel["schedule"]
        task_allocations = sel["task_allocations"]
        prompt = """
            You are a seasoned project risk analyst tasked with evaluating the risks associated with the current project plan.
            **Given:**
                - **Task Allocations:** {task_allocations}
                - **Schedule:** {schedule}
                - **Previous Risk Assessments (if any):** {self['risks_iteratio']}
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
        sel["risks"] = risks
        sel["project_risk_score"] = project_risk_score
        sel["iteration_number"] +=
        sel["project_risk_score_iterations"].append(project_risk_score)
        sel["risks_iteration"].append(risks)
        return self

    def insight_generation_node(self: AgentStat):
        """LangGraph node that generate insights from the schedule, task allocation, and risk associate."""
        schedule = sel["schedule"]
        task_allocations = sel["task_allocations"]
        risks = sel["risks"]
        prompt = """
            You are an expert project manager responsible for generating actionable insights to enhance the project plan.
            **Given:**
                - **Task Allocations:** {task_allocations}
                - **Schedule:** {schedule}
                - **Risk Analysis:** {risks}
            **Your objectives are to:**
                1. **Generate Critical Insights:**
                - Analyze the current task allocations, schedule, and risk assessments to identify areas for improvement.
                - Highlight any potential bottlenecks, resource conflicts, or high-risk tasks that may jeopardize project success.
                . **Recommend Enhancements:**
                - Suggest adjustments to task assignments or scheduling to mitigate identified risks.
                - Propose strategies to optimize resource utilization and streamline workflow.
                    **Requirements:**
                    - Ensure that all recommendations aim to reduce the overall project risk score.
                    - Provide clear and actionable suggestions that can be implemented in subsequent iteration.
            """
        insights = llm.invoke(prompt).content
        retur {"insights": insights}
