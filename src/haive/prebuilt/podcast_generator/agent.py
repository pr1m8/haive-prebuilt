from langchain.llms.base import BaseLLM
from langgraph.graph import END, START

from .nodes import (
    Start_parallel,
    finalize_report,
    initiate_all_interviews,
    write_conclusion,
    write_introduction,
    write_report,
)
from .state import PodcastGeneratorState

# TODO: These need to be properly defined or imported
Agent = None  # This should be the base Agent class
plan_self = None  # This should be defined elsewhere
interview_self = None  # This should be defined elsewhere


class PodcastGeneratorAgent(Agent):
    def __init__(self, llm: BaseLLM, state: PodcastGeneratorState):
        super().__init__(llm, state)

    def setup_workflow(self):
        self.graph.add_node("Planing", plan_self.graph.compile())
        self.graph.add_node("Start research", Start_parallel)
        self.graph.add_node("Create podcast", interview_self.graph.compile())
        self.graph.add_node("Write report", write_report)
        self.graph.add_node("Write introduction", write_introduction)
        self.graph.add_node("Write conclusion", write_conclusion)
        self.graph.add_node("Finalize podcast", finalize_report)

        # Logic
        self.graph.add_edge(START, "Planing")
        self.graph.add_edge("Planing", "Start research")
        self.graph.add_conditional_edges(
            "Start research", initiate_all_interviews, ["Planing", "Create podcast"]
        )
        self.graph.add_edge("Create podcast", "Write report")
        self.graph.add_edge("Create podcast", "Write introduction")
        self.graph.add_edge("Create podcast", "Write conclusion")
        self.graph.add_edge(
            ["Write introduction", "Write report", "Write conclusion"],
            "Finalize podcast",
        )
        self.graph.add_edge("Finalize podcast", END)
