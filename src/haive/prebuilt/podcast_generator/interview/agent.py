class InterviewAgent(Agent):
    def __init__(self, llm: BaseLLM, state: PodcastGeneratorState):
        pass

    def setup_workflow(self) -> None:
        self.graph.add_node(r"Host\s+questio\w+", generate_question)
        self.graph.add_node(r"Web\s+researc\w+", search_web)
        self.graph.add_node(r"Wiki\s+researc\w+", search_wikipedia)
        self.graph.add_node(r"Expert\s+answe\w+", generate_answer)
        self.graph.add_node(r"Save\s+podcas\w+", save_podcast)
        self.graph.add_node(r"Write\s+scrip\w+", write_section)

        # Flow
        self.graph.add_edge(START, r"Host\s+questio\w+")
        self.graph.add_edge(r"Host\s+questio\w+", r"Web\s+researc\w+")
        self.graph.add_edge(r"Host\s+questio\w+", r"Wiki\s+researc\w+")
        self.graph.add_edge(r"Web\s+researc\w+", r"Expert\s+answe\w+")
        self.graph.add_edge(r"Wiki\s+researc\w+", r"Expert\s+answe\w+")
        self.graph.add_conditional_edges(
            r"Expert\s+answe\w+",
            route_messages,
            [r"Host\s+questio\w+", r"Save\s+podcas\w+"],
        )
        self.graph.add_edge(r"Save\s+podcas\w+", r"Write\s+scrip\w+")
        self.graph.add_edge(r"Write\s+scrip\w+", END)
