# TODO: These need to be properly defined or imported
from haive.prebuilt.project_manager.models import Schedule


def create_scheduling_prompt(tasks, dependencies, insights, state):
    """Create a prompt for project scheduling."""
    prompt = f"""
        You are an experienced project scheduler tasked with creating an optimized project timeline.
        **Given:**
            - **Tasks:** {tasks}
            - **Dependencies:** {dependencies}
            - **Previous Insights:** {insights}
            - **Previous Schedule Iterations (if any):** {state["schedule_iteration"]}
        **Your objectives are to: **
            1. **Develop a Task Schedule:**
                - Assign start and end days to each task, ensuring that all dependencies are respected.
                - Optimize the schedule to minimize the overall project duration.
                - If possible parallelize the tasks to reduce the overall project duration.
                - Try not to increase the project duration compared to previous iterations.
            2. **Incorporate Insights:**
                - Utilize insights from previous iterations to enhance scheduling efficiency and address any identified issues.
        """
    return prompt


def create_schedule_llm(llm):
    """Create an LLM configured for scheduling."""
    return llm.with_structured_output(Schedule)
