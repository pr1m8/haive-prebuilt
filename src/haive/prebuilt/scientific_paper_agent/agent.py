from langgraph.graph import END

from haive.prebuilt.scientific_paper_agent.nodes import (
    agent_node,
    decision_making_node,
    judge_node,
    planning_node,
    tools_node,
)

# TODO: These need to be properly defined or imported
Agent = None  # This should be the base Agent class
router = None
should_continue = None
final_answer_router = None


class ScientificPaperAgent(Agent):
    def __init__(self):
        super().__init__()

    def set_workflow(self):
        # Add nodes to the graph
        self.graph.add_node("decision_making", decision_making_node)
        self.graph.add_node("planning", planning_node)
        self.graph.add_node("tools", tools_node)
        self.graph.add_node("agent", agent_node)
        self.graph.add_node("judge", judge_node)

        # Set the entry point of the graph
        self.graph.set_entry_point("decision_making")

        # Add edges between nodes
        self.graph.add_conditional_edges(
            "decision_making",
            router,
            {
                "planning": "planning",
                "end": END,
            },
        )
        self.graph.add_edge("planning", "agent")
        self.graph.add_edge("tools", "agent")
        self.graph.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "tools",
                "end": "judge",
            },
        )
        self.graph.add_conditional_edges(
            "judge",
            final_answer_router,
            {
                "planning": "planning",
                "end": END,
            },
        )
