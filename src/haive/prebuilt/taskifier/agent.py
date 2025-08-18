# https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/taskifier.ipynb

from langgraph.graph import END

# TODO: These need to be properly defined or imported
Agent = None  # This should be the base Agent class
approach_analysis = None
task_manifest = None
result_approach = None


class TaskifierAgent(Agent):
    def __init__(self):
        """  Init  .
"""
        super().__init__()

    def set_workflow(self):
        """Set Workflow.
"""
        # Initialize the StateGraph
        # Add nodes to the graph
        self.graph.add_node("approach_analysis", approach_analysis)
        self.graph.add_node("task_knowledge_retrieval", task_manifest)
        self.graph.add_node("customized_approach_generation", result_approach)

        # Define and add conditional edges
        self.graph.add_edge("approach_analysis", "task_knowledge_retrieval")
        self.graph.add_edge(
            "task_knowledge_retrieval", "customized_approach_generation"
        )

        # Set the entry point
        self.graph.set_entry_point("approach_analysis")

        # Set the exit point
        self.graph.add_edge("customized_approach_generation", END)
