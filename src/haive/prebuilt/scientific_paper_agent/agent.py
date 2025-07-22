class ScientificPaperAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

    def set_workflow(self) -> None:
        # Add nodes to the graph
        self.graph.add_node("decision_makin", decision_making_node)
        self.graph.add_node("plannin", planning_node)
        self.graph.add_node("tool", tools_node)
        self.graph.add_node("agen", agent_node)
        self.graph.add_node("judg", judge_node)

        # Set the entry point of the graph
        self.graph.set_entry_point("decision_makin")

        # Add edges between nodes
        self.graph.add_conditional_edges(
            "decision_makin",
            router,
            {
                "plannin": "plannin",
                "en": END,
            },
        )
        self.graph.add_edge("plannin", "agen")
        self.graph.add_edge("tool", "agen")
        self.graph.add_conditional_edges(
            "agen",
            should_continue,
            {
                "continu": "tool",
                "en": "judg",
            },
        )
        self.graph.add_conditional_edges(
            "judg",
            final_answer_router,
            {
                "plannin": "plannin",
                "en": END,
            },
        )
