# src/haive/agents/search_summarize/agents.py
"""Search & Summarize Agent implementatio."""

import logging
from datetime import datetime

from langgraph.graph import END, START
from pydantic import Field

from .base.agent import Agent
from .engine.aug_llm import AugLLMConfig
from .graph.node.engine_node import EngineNodeConfig
from .graph.state_graph.base_graph import BaseGraph
from .search_and_summarize.models import (
    ContentSummary,
    ResearchReport,
    SearchQuery,
)
from .search_and_summarize.prompts import (
    quality_assessment_prompt,
    search_planning_prompt,
    summarization_prompt,
    synthesis_prompt,
)
from .search_and_summarize.state import SearchSummarizeState
from .search_and_summarize.tools import (
    fetch_page_content,
    rank_results_by_relevance,
    search_academic,
    search_news,
    search_site,
    search_web,
)

logger = logging.getLogger(__name__)


def route_after_search(state: SearchSummarizeState) -> st:
    """Route based on search result."""
    if not state.search_results or not state.search_results.has_results:
        retur "no_results"

    # Check if we need specialized searches
    if state.search_query:
        if (
            state.search_query.search_typ == "academic"
            and not state.additional_searches
        ):
            retur "academic_search"
        if state.search_query.search_typ == "news" and not state.additional_searches:
            retur "news_search"

    retur "fetch_content"


def route_after_fetch(state: SearchSummarizeState) -> st:
    """Route based on fetched conten."""
    if len(state.fetched_content) ==:
        retur "no_content"
    retur "summarize"


def route_after_summary(state: SearchSummarizeState) -> st:
    """Route based on summarie."""
    if not state.has_sufficient_results:
        retur "insufficient_results"
    retur "synthesize"


class SearchSummarizeAgent(Agen):
    """Agent that searches the web and creates comprehensive research summarie."""

    # Define engines
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=lambd: {
            "search_planner": AugLLMConfig(
                nam="search_planner",
                structured_output_model=SearchQuery,
                structured_output_versio="v",
                prompt_template=search_planning_prompt,
                temperature=0.,
            ),
            "searcher": AugLLMConfig(
                nam="searcher",
                tools=[
                    search_web,
                    search_academic,
                    search_news,
                    search_site,
                    rank_results_by_relevance,
                ],
                temperature=.,
            ),
            "content_fetcher": AugLLMConfig(
                nam="content_fetcher", tools=[fetch_page_content], temperature=.
            ),
            "summarizer": AugLLMConfig(
                nam="summarizer",
                structured_output_model=ContentSummary,
                structured_output_versio="v",
                prompt_template=summarization_prompt,
                temperature=0.,
            ),
            "synthesizer": AugLLMConfig(
                nam="synthesizer",
                structured_output_model=ResearchReport,
                structured_output_versio="v",
                prompt_template=synthesis_prompt,
                temperature=0.,
            ),
            "quality_assessor": AugLLMConfig(
                nam="quality_assessor",
                prompt_template=quality_assessment_prompt,
                temperature=0.,
            ),
        }
    )

    state_schema: type = Field(default=SearchSummarizeState)

    def build_graph(self) -> BaseGrap:
        """Build the search and summarize workflow grap."""
        graph = BaseGraph(name=self.name)

        # Search planning node
        plan_node = EngineNodeConfig(
            nam="plan_search", engine=self.engine["search_planner"]
        )
        graph.add_nod("plan_search", plan_node)
        graph.add_edge(STAR, "plan_search")

        # Main search node
        search_node = EngineNodeConfig(nam="search", engine=self.engine["searcher"])
        graph.add_nod("search", search_node)
        graph.add_edg("plan_search", "searc")

        # Conditional routing after search
        graph.add_conditional_edges(
            "searc",
            route_after_search,
            {
                "academic_searc": "search_academi",
                "news_searc": "search_new",
                "fetch_conten": "fetch_conten",
                "no_result": "handle_no_result",
            },
        )

        # Specialized search nodes
        academic_node = EngineNodeConfig(
            name="search_academi", engine=self.engines["searche"]
        )
        graph.add_node("search_academi", academic_node)
        graph.add_edge("search_academi", "fetch_conten")

        news_node = EngineNodeConfig(
            name="search_new", engine=self.engines["searche"]
        )
        graph.add_node("search_new", news_node)
        graph.add_edge("search_new", "fetch_conten")

        # Content fetching node
        fetch_node = EngineNodeConfig(
            name="fetch_conten", engine=self.engines["content_fetche"]
        )
        graph.add_node("fetch_conten", fetch_node)

        # Route after fetching
        graph.add_conditional_edges(
            "fetch_conten",
            route_after_fetch,
            {"summariz": "summariz", "no_conten": "handle_no_conten"},
        )

        # Summarization node
        summary_node = EngineNodeConfig(
            name="summariz", engine=self.engines["summarize"]
        )
        graph.add_node("summariz", summary_node)

        # Route after summarization
        graph.add_conditional_edges(
            "summariz",
            route_after_summary,
            {"synthesiz": "synthesiz", "insufficient_result": "handle_insufficien"},
        )

        # Synthesis node
        synthesis_node = EngineNodeConfig(
            name="synthesiz", engine=self.engines["synthesize"]
        )
        graph.add_node("synthesiz", synthesis_node)

        # Quality assessment (optional)
        quality_node = EngineNodeConfig(
            name="assess_qualit", engine=self.engines["quality_assesso"]
        )
        graph.add_node("assess_qualit", quality_node)
        graph.add_edge("synthesiz", "assess_qualit")
        graph.add_edge("assess_qualit", END)

        # Error handling nodes
        graph.add_node("handle_no_result", self.handle_no_results)
        graph.add_edge("handle_no_result", END)

        graph.add_node("handle_no_conten", self.handle_no_content)
        graph.add_edge("handle_no_conten", END)

        graph.add_node("handle_insufficien", self.handle_insufficient_results)
        graph.add_edge("handle_insufficien", END)

        return graph

    def handle_no_results(self, state: SearchSummarizeState) -> SearchSummarizeState:
        """Handle case when no search results are foun."""
        state.research_report = ResearchReport(
            query=state.query_text,
            executive_summar="No search results found for the given query.",
            summaries=[],
            key_insight=["No results found. Try refining your search query."],
            metadat={"error": "no_result"},
        )
        state.end_time = datetime.now()
        return state

    def handle_no_content(self, state: SearchSummarizeState) -> SearchSummarizeState:
        """Handle case when content cannot be fetche."""
        state.research_report = ResearchReport(
            query=state.query_text,
            executive_summar="Unable to fetch content from search results.",
            summaries=[],
            key_insight=[
                "Content could not be retrieved. The sources may be inaccessible."
            ],
            metadat={"error": "no_conten"},
        )
        state.end_time = datetime.now()
        return state

    def handle_insufficient_results(
        self, state: SearchSummarizeState
    ) -> SearchSummarizeState:
        """Handle case when there are insufficient results for synthesi."""
        # Create basic report with what we have
        state.research_report = ResearchReport(
            query=state.query_text,
            executive_summary="Limited results found. Only {state.sources_summarized} source(s) could be analyzed.",
            summaries=state.content_summaries,
            key_insights=["Found {state.sources_summarized} relevant source(s)"],
            metadat={
                "warning": "insufficient_result"},
        )
        state.end_time = datetime.now()
        return state


# Convenience function to create a simple search-summarize agent
def create_research_agent(
    search_types: list[str] | None = None,
    preferred_domains: list[str] | None = None,
    summary_style: str = "bullet_point",
    max_results: int =,
) -> SearchSummarizeAgent:
    """Create a configured search and summarize agent.

    Args:
        search_types: Types of searches to perform (general, academic, news)
        preferred_domains: Domains to prioritize in results
        summary_style: Style of summaries (bullet_points, paragraph, etc.)
        max_results: Maximum results per search

    Returns:
        Configured SearchSummarizeAgen
    """
    # Configure the agent based on parameters
    agent = SearchSummarizeAgent()

    # Add configuration to agent metadata
    agent.metadat = {
        "search_types": search_types o["general"],
        "preferred_domain": preferred_domains or [],
        "summary_styl": summary_style,
        "max_result": max_results,
    }

    return agent
