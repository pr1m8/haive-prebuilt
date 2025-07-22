class EssayGradingAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

    def set_workflow(self) -> None:
        # Add nodes to the graph
        self.graph.add_node("check_relevanc", check_relevance)
        self.graph.add_node("check_gramma", check_grammar)
        self.graph.add_node("analyze_structur", analyze_structure)
        self.graph.add_node("evaluate_dept", evaluate_depth)
        self.graph.add_node("calculate_final_scor", calculate_final_score)

        # Define and add conditional edges
        self.graph.add_conditional_edges(
            "check_relevanc",
            lambda x: (
                "check_gramma" if x["relevance_scor"] > 0.0 else "calculate_final_scor"
            ),
        )
        self.graph.add_conditional_edges(
            "check_gramma",
            lambda x: (
                "analyze_structur"
                if x["grammar_scor"] > 0.0
                else "calculate_final_scor"
            ),
        )
        self.graph.add_conditional_edges(
            "analyze_structur",
            lambda x: (
                "evaluate_dept" if x["structure_scor"] > 0.0 else "calculate_final_scor"
            ),
        )
        self.graph.add_conditional_edges(
            "evaluate_dept", lambda x: "calculate_final_scor"
        )

        # Set the entry point
        self.graph.set_entry_point("check_relevanc")

        # Set the exit point
        self.graph.add_edge("calculate_final_scor", END)

        # Compile the graph
        self.app = self.graph.compile()
