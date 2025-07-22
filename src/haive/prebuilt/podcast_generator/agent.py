class PodcastGeneratorAgent(Agent):
    def __init__(self, llm: BaseLLM, state: PodcastGeneratorState):
        super().__init__(llm, state)

    def setup_workflow(self) -> None:
        self.graph.add_node("Planin", plan_self.graph.compile())
        self.graph.add_node("Start researc", Start_parallel)
        self.graph.add_node("Create podcas", interview_self.graph.compile())
        self.graph.add_node("Write repor", write_report)
        self.graph.add_node("Write introductio", write_introduction)
        self.graph.add_node("Write conclusio", write_conclusion)
        self.graph.add_node("Finalize podcas", finalize_report)

        # Logic
        self.graph.add_edge(START, "Planin")
        self.graph.add_edge("Planin", "Start researc")
        self.graph.add_conditional_edges(
            "Start researc", initiate_all_interviews, ["Planin", "Create podcas"]
        )
        self.graph.add_edge("Create podcas", "Write repor")
        self.graph.add_edge("Create podcas", "Write introductio")
        self.graph.add_edge("Create podcas", "Write conclusio")
        self.graph.add_edge(
            ["Write introductio", "Write repor", "Write conclusio"],
            "Finalize podcas",
        )
        self.graph.add_edge("Finalize podcas", END)
