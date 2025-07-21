"""
Master startup agent that orchestrates all subgraphs for complete startup development.

This agent manages the entire flow from ideation through pitch deck creation,
coordinating between different specialized subgraphs.
"""

from typing import Any, Dict, List, Literal, Optional, Union

from haive.agents.base.agent import Agent
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from pydantic import BaseModel, Field

from haive.prebuilt.startup.business_model_subgraph import (
    BusinessModelState,
    build_business_model_subgraph,
)

# Import subgraphs
from haive.prebuilt.startup.ideation_subgraph import (
    IdeationState,
    build_ideation_subgraph,
)
from haive.prebuilt.startup.market_research_subgraph import (
    MarketResearchState,
    build_market_research_subgraph,
)

# Import models
from haive.prebuilt.startup.models import IdeaPortfolio, StartupIdea
from haive.prebuilt.startup.pitch_deck_models import PitchDeck, PitchDeckMetadata
from haive.prebuilt.startup.pitch_deck_subgraph import (
    PitchDeckState,
    build_pitch_deck_subgraph,
)


class MasterStartupState(StateSchema):
    """Master state that coordinates all subgraphs."""

    messages: List[BaseMessage] = Field(default_factory=list)

    # Master control
    workflow_stage: Literal[
        "ideation", "research", "business_model", "pitch_deck", "complete"
    ] = "ideation"
    user_goal: str = Field(default="Create a fundable startup with pitch deck")

    # Shared data between subgraphs
    selected_idea: Optional[StartupIdea] = None
    idea_portfolio: Optional[IdeaPortfolio] = None

    # Results from subgraphs
    ideation_results: Optional[Dict[str, Any]] = None
    market_research_results: Optional[Dict[str, Any]] = None
    business_model_results: Optional[Dict[str, Any]] = None
    pitch_deck_results: Optional[PitchDeck] = None

    # Quality gates
    idea_validated: bool = False
    market_validated: bool = False
    model_validated: bool = False
    deck_approved: bool = False

    # User preferences
    target_industry: Optional[str] = None
    funding_goal: Optional[float] = None
    time_to_market: Optional[str] = None

    # Shared fields with subgraphs
    __shared_fields__ = ["messages", "selected_idea"]


class StartupDevelopmentRequest(BaseModel):
    """Request model for startup development."""

    focus_area: Optional[str] = Field(
        None, description="Industry or problem space to focus on"
    )
    constraints: List[str] = Field(
        default_factory=list, description="Any constraints or requirements"
    )
    funding_goal: Optional[float] = Field(None, description="Target funding amount")
    target_stage: Literal["idea", "validated", "pitch_ready"] = Field(
        default="pitch_ready", description="How far to develop the startup"
    )


class StartupDevelopmentResponse(BaseModel):
    """Response model for startup development."""

    startup_idea: StartupIdea
    pitch_deck: Optional[PitchDeck] = None
    market_validation: Dict[str, Any]
    business_model: Dict[str, Any]
    next_steps: List[str]
    estimated_fundability: float = Field(..., ge=0.0, le=1.0)


class MasterStartupAgent(Agent):
    """
    Master agent that orchestrates the complete startup development process.

    This agent coordinates between ideation, research, business model development,
    and pitch deck creation subgraphs.
    """

    name: str = Field(default="Master Startup Development Agent")
    description: str = Field(
        default="Orchestrates the complete startup journey from idea to pitch deck"
    )

    # Subgraph configurations
    enable_ideation: bool = Field(default=True)
    enable_deep_research: bool = Field(default=True)
    enable_business_modeling: bool = Field(default=True)
    enable_pitch_deck: bool = Field(default=True)

    # Quality thresholds
    min_idea_score: float = Field(default=6.0, ge=0.0, le=10.0)
    min_market_size: float = Field(default=100_000_000)  # $100M minimum TAM

    def build_graph(self) -> StateGraph:
        """Build the master coordination graph."""
        graph = StateGraph(MasterStartupState)

        # Add subgraphs as nodes
        if self.enable_ideation:
            graph.add_node("ideation_subgraph", build_ideation_subgraph())

        if self.enable_deep_research:
            graph.add_node("market_research_subgraph", build_market_research_subgraph())

        if self.enable_business_modeling:
            graph.add_node("business_model_subgraph", build_business_model_subgraph())

        if self.enable_pitch_deck:
            graph.add_node("pitch_deck_subgraph", build_pitch_deck_subgraph())

        # Add coordination nodes
        graph.add_node("coordinate_workflow", self.coordinate_workflow_node)
        graph.add_node("extract_results", self.extract_results_node)
        graph.add_node("quality_gate", self.quality_gate_node)
        graph.add_node("prepare_final_output", self.prepare_final_output_node)

        # Entry point
        graph.add_edge(START, "coordinate_workflow")

        # Workflow coordination routes to appropriate subgraph
        graph.add_conditional_edges(
            "coordinate_workflow",
            self.determine_next_subgraph,
            {
                "ideation": "ideation_subgraph",
                "research": "market_research_subgraph",
                "business_model": "business_model_subgraph",
                "pitch_deck": "pitch_deck_subgraph",
                "complete": "prepare_final_output",
            },
        )

        # All subgraphs return to extract results
        for subgraph in [
            "ideation_subgraph",
            "market_research_subgraph",
            "business_model_subgraph",
            "pitch_deck_subgraph",
        ]:
            if subgraph in graph.nodes:
                graph.add_edge(subgraph, "extract_results")

        # Extract results goes to quality gate
        graph.add_edge("extract_results", "quality_gate")

        # Quality gate decides next action
        graph.add_conditional_edges(
            "quality_gate",
            self.quality_gate_decision,
            {
                "continue": "coordinate_workflow",
                "retry": "coordinate_workflow",
                "complete": "prepare_final_output",
            },
        )

        # Final output
        graph.add_edge("prepare_final_output", END)

        return graph

    def coordinate_workflow_node(self, state: MasterStartupState) -> Dict[str, Any]:
        """Coordinate the workflow and prepare for next subgraph."""
        updates = {}

        # Set user preferences if this is the first run
        if not state.messages:
            updates["messages"] = [
                HumanMessage(content="Starting startup development process"),
                AIMessage(
                    content="I'll help you develop a complete startup from idea to pitch deck. Let me start by generating some innovative ideas."
                ),
            ]

        # Prepare data for next subgraph based on stage
        if state.workflow_stage == "research" and state.selected_idea:
            updates["messages"].append(
                AIMessage(
                    content=f"Now researching the market for: {state.selected_idea.name}"
                )
            )
        elif state.workflow_stage == "business_model" and state.selected_idea:
            updates["messages"].append(
                AIMessage(content="Developing the business model based on our research")
            )
        elif state.workflow_stage == "pitch_deck":
            updates["messages"].append(
                AIMessage(content="Creating your pitch deck - this is the final step!")
            )

        return updates

    def extract_results_node(self, state: MasterStartupState) -> Dict[str, Any]:
        """Extract results from completed subgraph."""
        updates = {}

        # Extract based on current stage
        if state.workflow_stage == "ideation":
            # Extract the best idea from ideation results
            if hasattr(state, "raw_ideas") and state.raw_ideas:
                # Create a basic StartupIdea from the best raw idea
                # In practice, this would be more sophisticated
                import uuid

                from haive.prebuilt.startup.models import (
                    IdeaCategory,
                    create_basic_idea,
                )

                best_idea_str = state.raw_ideas[0]
                parts = best_idea_str.split(":")
                name = parts[0].strip()
                problem_solution = (
                    parts[1].split("-")
                    if len(parts) > 1
                    else ["Unknown problem", "Unknown solution"]
                )

                selected_idea = create_basic_idea(
                    name=name,
                    problem=problem_solution[0].strip(),
                    solution=(
                        problem_solution[1].strip()
                        if len(problem_solution) > 1
                        else "Innovative solution"
                    ),
                    category=IdeaCategory.AI_ML,  # Default
                )

                updates["selected_idea"] = selected_idea
                updates["ideation_results"] = {
                    "ideas_generated": len(state.raw_ideas),
                    "best_idea": name,
                }
                updates["idea_validated"] = True

        elif state.workflow_stage == "research":
            # Extract market research results
            if hasattr(state, "market_research") and state.market_research:
                updates["market_research_results"] = {
                    "tam": state.market_research.total_addressable_market,
                    "growth_rate": state.market_research.growth_rate,
                    "competition_level": len(state.market_research.direct_competitors),
                    "go_no_go": state.go_no_go_recommendation,
                }
                updates["market_validated"] = state.market_size_validated

                # Update the selected idea with research
                if state.selected_idea:
                    state.selected_idea.market_research = state.market_research

        elif state.workflow_stage == "business_model":
            # Extract business model results
            if hasattr(state, "business_model_canvas") and state.business_model_canvas:
                updates["business_model_results"] = {
                    "revenue_streams": state.business_model_canvas.revenue_streams,
                    "key_metrics": state.business_model_canvas.metrics,
                    "score": (
                        state.idea_metrics.overall_score if state.idea_metrics else 0
                    ),
                }
                updates["model_validated"] = state.model_validated

                # Update the selected idea
                if state.selected_idea:
                    state.selected_idea.business_model = state.business_model_canvas
                    state.selected_idea.metrics = state.idea_metrics

        elif state.workflow_stage == "pitch_deck":
            # Extract pitch deck
            if hasattr(state, "pitch_deck") and state.pitch_deck:
                updates["pitch_deck_results"] = state.pitch_deck
                updates["deck_approved"] = state.deck_approved

        return updates

    def quality_gate_node(self, state: MasterStartupState) -> Dict[str, Any]:
        """Check quality gates and decide if we can proceed."""
        updates = {}

        # Check stage-specific quality gates
        if state.workflow_stage == "ideation":
            if not state.idea_validated:
                updates["messages"] = [
                    AIMessage(content="Need to generate better ideas")
                ]
                # Would trigger retry logic
            else:
                updates["workflow_stage"] = "research"

        elif state.workflow_stage == "research":
            if not state.market_validated:
                updates["messages"] = [
                    AIMessage(content="Market size too small, pivoting idea")
                ]
                updates["workflow_stage"] = "ideation"  # Go back to ideation
            else:
                updates["workflow_stage"] = "business_model"

        elif state.workflow_stage == "business_model":
            if not state.model_validated:
                updates["messages"] = [
                    AIMessage(content="Business model needs refinement")
                ]
                # Stay in business model stage for refinement
            else:
                updates["workflow_stage"] = "pitch_deck"

        elif state.workflow_stage == "pitch_deck":
            if state.deck_approved:
                updates["workflow_stage"] = "complete"
            else:
                updates["messages"] = [
                    AIMessage(content="Refining pitch deck based on feedback")
                ]

        return updates

    def prepare_final_output_node(self, state: MasterStartupState) -> Dict[str, Any]:
        """Prepare the final output with all results."""

        # Calculate fundability score
        fundability_score = 0.0
        factors = []

        if state.market_validated:
            fundability_score += 0.3
            factors.append("Strong market opportunity")

        if state.model_validated:
            fundability_score += 0.3
            factors.append("Solid business model")

        if state.deck_approved:
            fundability_score += 0.3
            factors.append("Compelling pitch deck")

        if state.selected_idea and state.selected_idea.metrics:
            if state.selected_idea.metrics.overall_score > 7:
                fundability_score += 0.1
                factors.append("High-scoring idea")

        # Generate next steps
        next_steps = []
        if fundability_score >= 0.8:
            next_steps = [
                "Schedule meetings with target investors",
                "Prepare detailed financial model",
                "Build MVP prototype",
                "Recruit advisors",
            ]
        else:
            next_steps = [
                "Conduct customer interviews",
                "Refine value proposition",
                "Build proof of concept",
                "Gather more market data",
            ]

        # Create final response
        response = StartupDevelopmentResponse(
            startup_idea=state.selected_idea,
            pitch_deck=state.pitch_deck_results,
            market_validation=state.market_research_results or {},
            business_model=state.business_model_results or {},
            next_steps=next_steps,
            estimated_fundability=fundability_score,
        )

        final_message = f"""
🎉 **Startup Development Complete!**

**Startup:** {state.selected_idea.name if state.selected_idea else 'Your Startup'}
**Fundability Score:** {fundability_score:.0%}

**Key Success Factors:**
{chr(10).join(f'✅ {factor}' for factor in factors)}

**Recommended Next Steps:**
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(next_steps))}

Your pitch deck is ready and you're prepared to approach investors!
"""

        return {
            "messages": [AIMessage(content=final_message)],
            "final_response": response,
        }

    def determine_next_subgraph(self, state: MasterStartupState) -> str:
        """Determine which subgraph to run next."""
        return state.workflow_stage

    def quality_gate_decision(self, state: MasterStartupState) -> str:
        """Make quality gate decision."""
        if state.workflow_stage == "complete":
            return "complete"
        elif any(
            [
                state.workflow_stage == "ideation" and not state.idea_validated,
                state.workflow_stage == "research" and not state.market_validated,
            ]
        ):
            return "retry"
        else:
            return "continue"

    def invoke_with_goal(self, user_goal: str, **kwargs) -> StartupDevelopmentResponse:
        """
        Invoke the master agent with a specific goal.

        Args:
            user_goal: Natural language description of what the user wants
            **kwargs: Additional parameters

        Returns:
            Complete startup development response
        """
        initial_state = {
            "messages": [HumanMessage(content=user_goal)],
            "user_goal": user_goal,
            "target_industry": kwargs.get("industry"),
            "funding_goal": kwargs.get("funding_goal"),
            "time_to_market": kwargs.get("time_to_market", "6-12 months"),
        }

        # Compile and run the graph
        compiled_graph = self.compile()
        result = compiled_graph.invoke(initial_state)

        return result.get(
            "final_response",
            StartupDevelopmentResponse(
                startup_idea=result.get("selected_idea"),
                pitch_deck=result.get("pitch_deck_results"),
                market_validation={},
                business_model={},
                next_steps=["Continue development"],
                estimated_fundability=0.5,
            ),
        )


# Convenience function to create and run the master agent
def develop_startup(
    goal: str = "Create a fundable B2B SaaS startup with pitch deck",
    industry: Optional[str] = None,
    funding_goal: Optional[float] = None,
    **kwargs,
) -> StartupDevelopmentResponse:
    """
    Develop a complete startup from idea to pitch deck.

    Args:
        goal: Natural language description of the startup goal
        industry: Target industry/vertical
        funding_goal: Target funding amount
        **kwargs: Additional parameters

    Returns:
        Complete startup package with idea, research, and pitch deck
    """
    agent = MasterStartupAgent()
    return agent.invoke_with_goal(
        user_goal=goal, industry=industry, funding_goal=funding_goal, **kwargs
    )


# Example usage
if __name__ == "__main__":
    # Create a complete fintech startup
    result = develop_startup(
        goal="Create an innovative fintech startup that helps millennials save money",
        industry="fintech",
        funding_goal=2_000_000,
    )

    print(f"Developed: {result.startup_idea.name}")
    print(f"Fundability: {result.estimated_fundability:.0%}")
    print(f"Next steps: {', '.join(result.next_steps)}")
