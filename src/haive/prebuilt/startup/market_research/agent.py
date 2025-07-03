"""Market research subgraph for comprehensive market analysis.

This subgraph handles market sizing, competitive analysis, and trend research.
"""

from typing import Any

from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from pydantic import Field

from haive.prebuilt.startup.market_research.models import (
    CompetitorAnalysis,
    MarketResearch,
    StartupIdea,
)
from haive.prebuilt.startup.market_research.prompts import (
    competitor_analysis_aug_llm,
    industry_research_aug_llm,
    market_research_aug_llm,
)


class MarketResearchState(StateSchema):
    """State for market research subgraph."""

    messages: list[BaseMessage] = Field(default_factory=list)

    # Input
    startup_idea: StartupIdea | None = None
    research_depth: str = Field(
        default="comprehensive"
    )  # quick, standard, comprehensive

    # Research results
    market_research: MarketResearch | None = None
    competitor_analyses: list[CompetitorAnalysis] = Field(default_factory=list)
    industry_analysis: dict[str, Any] | None = None

    # Market insights
    market_size_validated: bool = False
    competition_mapped: bool = False
    trends_identified: bool = False

    # Summary
    go_no_go_recommendation: str | None = None
    key_insights: list[str] = Field(default_factory=list)


def analyze_market_size_node(state: MarketResearchState) -> dict[str, Any]:
    """Analyze market size and dynamics."""
    if not state.startup_idea:
        return {
            "messages": [
                HumanMessage(content="No startup idea provided for market research")
            ]
        }

    engine = market_research_aug_llm.create_runnable()

    result = engine.invoke(
        {
            "idea_name": state.startup_idea.name,
            "problem_description": state.startup_idea.problem.description,
            "solution_description": state.startup_idea.solution.description,
            "category": state.startup_idea.category,
            "research_priorities": [
                "market_size",
                "growth_rate",
                "customer_segments",
                "trends",
            ],
        }
    )

    # Validate market size
    market_size_validated = False
    if (
        result.total_addressable_market
        and result.total_addressable_market > 1_000_000_000
    ):
        market_size_validated = True

    return {
        "market_research": result,
        "market_size_validated": market_size_validated,
        "messages": [
            HumanMessage(
                content=f"Market analysis complete. TAM: ${result.total_addressable_market:,.0f}"
            )
        ],
    }


def analyze_competitors_node(state: MarketResearchState) -> dict[str, Any]:
    """Deep competitive analysis."""
    if not state.startup_idea:
        return {
            "messages": [
                HumanMessage(content="No startup idea for competitive analysis")
            ]
        }

    engine = competitor_analysis_aug_llm.create_runnable()

    result = engine.invoke(
        {
            "startup_name": state.startup_idea.name,
            "solution_description": state.startup_idea.solution.description,
            "target_market": (
                state.market_research.primary_customers[0]
                if state.market_research
                else "General market"
            ),
            "key_features": state.startup_idea.solution.key_features,
        }
    )

    return {
        "competitor_analyses": result.competitors,
        "competition_mapped": True,
        "messages": [
            HumanMessage(content=f"Analyzed {len(result.competitors)} competitors")
        ],
    }


def analyze_industry_trends_node(state: MarketResearchState) -> dict[str, Any]:
    """Analyze industry trends and dynamics."""
    if not state.startup_idea:
        return {
            "messages": [HumanMessage(content="No startup idea for industry analysis")]
        }

    engine = industry_research_aug_llm.create_runnable()

    result = engine.invoke(
        {
            "industry": state.startup_idea.category.value,
            "focus_areas": [
                "trends",
                "regulations",
                "technology_shifts",
                "investment_activity",
            ],
            "geography": "Global",
            "time_horizon": "5 years",
        }
    )

    # Extract key insights
    key_insights = []
    for trend in result.key_trends[:3]:
        key_insights.append(f"Trend: {trend['name']} - {trend['impact']}")

    return {
        "industry_analysis": result.model_dump(),
        "trends_identified": True,
        "key_insights": key_insights,
        "messages": [HumanMessage(content="Industry analysis complete")],
    }


def synthesize_market_insights_node(state: MarketResearchState) -> dict[str, Any]:
    """Synthesize all market research into actionable insights."""
    insights = state.key_insights.copy()

    # Add market size insight
    if state.market_research:
        if state.market_size_validated:
            insights.append(
                f"Large market opportunity: ${state.market_research.total_addressable_market:,.0f} TAM"
            )
        else:
            insights.append("Market size may be limited - consider niche strategy")

    # Add competitive insights
    if state.competitor_analyses:
        if len(state.competitor_analyses) > 5:
            insights.append("Highly competitive market - differentiation critical")
        else:
            insights.append("Moderate competition - opportunity for new entrant")

    # Make go/no-go recommendation
    positive_signals = sum(
        [
            state.market_size_validated,
            len(state.competitor_analyses) < 10,
            state.trends_identified,
        ]
    )

    if positive_signals >= 2:
        recommendation = "GO - Favorable market conditions"
    else:
        recommendation = "CAUTION - Market challenges identified"

    return {
        "go_no_go_recommendation": recommendation,
        "key_insights": insights,
        "messages": [
            HumanMessage(content=f"Market research complete: {recommendation}")
        ],
    }


def determine_research_depth(state: MarketResearchState) -> str:
    """Determine how deep to go with research."""
    if state.research_depth == "quick":
        if state.market_research:
            return "synthesize"
        return "market_size"

    if not state.market_research:
        return "market_size"
    if not state.competition_mapped:
        return "competitors"
    if not state.trends_identified and state.research_depth == "comprehensive":
        return "industry"
    return "synthesize"


def build_market_research_subgraph() -> StateGraph:
    """Build the market research subgraph."""
    graph = StateGraph(MarketResearchState)

    # Add nodes
    graph.add_node("analyze_market_size", analyze_market_size_node)
    graph.add_node("analyze_competitors", analyze_competitors_node)
    graph.add_node("analyze_industry_trends", analyze_industry_trends_node)
    graph.add_node("synthesize_insights", synthesize_market_insights_node)

    # Entry routing based on what's needed
    graph.add_conditional_edges(
        START,
        determine_research_depth,
        {
            "market_size": "analyze_market_size",
            "competitors": "analyze_competitors",
            "industry": "analyze_industry_trends",
            "synthesize": "synthesize_insights",
        },
    )

    # Market size can lead to competitors or synthesis
    graph.add_conditional_edges(
        "analyze_market_size",
        determine_research_depth,
        {"competitors": "analyze_competitors", "synthesize": "synthesize_insights"},
    )

    # Competitors can lead to industry or synthesis
    graph.add_conditional_edges(
        "analyze_competitors",
        determine_research_depth,
        {"industry": "analyze_industry_trends", "synthesize": "synthesize_insights"},
    )

    # Industry trends lead to synthesis
    graph.add_edge("analyze_industry_trends", "synthesize_insights")

    # Synthesis is the end
    graph.add_edge("synthesize_insights", END)

    return graph.compile()
