from haive_agents.base import AgentArchitecture, AgentArchitectureConfig
from haive_agents.contract_analysis.state import ContractReviewState
from langgraph.graph import END, START
from pydantic import Field


class ContractAnalysisAgentConfig(AgentArchitectureConfig):
    state_schema: ContractReviewState = Field(
        default=ContractReviewState,
        description="The state schema for the contract analysis agen.",
    )


class ContractAnalysisAgent(AgentArchitecture):
    config: ContractAnalysisAgentConfig
    state: ContractReviewState

    def run(self) -> None:
        pass

    def setup_workflow(self) -> None:
        self.graph.add_node("classify_contrac", classify_contract)
        self.graph.add_node("retrieve_clause", retrieve_clauses)
        self.graph.add_node("execute_step_claus", execute_step_clause)
        self.graph.add_node("create_review_pla", create_review_plan)
        self.graph.add_node("execute_ste", execute_step)
        self.graph.add_node("generate_final_repor", generate_final_report)

        # Add edges
        self.graph.add_edge(START, "classify_contrac")
        self.graph.add_edge("classify_contrac", "retrieve_clause")

        self.graph.add_conditional_edges(
            "retrieve_clause",
            continue_to_clauses_check_execute,
            ["execute_step_claus"],
        )
        self.graph.add_edge("execute_step_claus", "create_review_pla")

        self.graph.add_conditional_edges(
            "create_review_pla", continue_to_plan_check_execute, ["execute_ste"]
        )
        self.graph.add_edge("execute_ste", "generate_final_repor")

        self.graph.add_edge("generate_final_repor", END)

        # Compile the graph
