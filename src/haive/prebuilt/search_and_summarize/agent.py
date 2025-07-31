# src/haive/agents/search_summarize/agents.py
"""
Search & Summarize Agent implementation.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from haive.agents.base.agent import Agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field

from haive.prebuilt.search_and_summarize.models import (
    ContentSummary,
    ResearchReport,
    SearchQuery,
)
from haive.prebuilt.search_and_summarize.prompts import (
    quality_assessment_prompt,
    search_planning_prompt,
    summarization_prompt,
    synthesis_prompt,
)
from haive.prebuilt.search_and_summarize.state import SearchSummarizeState
from haive.prebuilt.search_and_summarize.tools import (
    fetch_page_content,
    rank_results_by_relevance,
    search_academic,
    search_news,
    search_site,
    search_web,
)

logger = logging.getLogger(__name__)


def route_after_search(state: SearchSummarizeState) -> str:
    """Route based on search results."""
    if not state.search_results or not state.search_results.has_results:
        return "no_results"

    # Check if we need specialized searches
    if state.search_query:
        if (
            state.search_query.search_type == "academic"
            and not state.additional_searches
        ):
            return "academic_search"
        elif state.search_query.search_type == "news" and not state.additional_searches:
            return "news_search"

    return "fetch_content"


def route_after_fetch(state: SearchSummarizeState) -> str:
    """Route based on fetched content."""
    if len(state.fetched_content) == 0:
        return "no_content"
    return "summarize"


def route_after_summary(state: SearchSummarizeState) -> str:
    """Route based on summaries."""
    if not state.has_sufficient_results:
        return "insufficient_results"
    return "synthesize"


class SearchSummarizeAgent(Agent):
    """
    Agent that searches the web and creates comprehensive research summaries.
    """

    # Define engines
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=lambda: {
            "search_planner": AugLLMConfig(
                name="search_planner",
                structured_output_model=SearchQuery,
                structured_output_version="v2",
                prompt_template=search_planning_prompt,
                temperature=0.3,
            ),
            "searcher": AugLLMConfig(
                name="searcher",
                tools=[
                    search_web,
                    search_academic,
                    search_news,
                    search_site,
                    rank_results_by_relevance,
                ],
                temperature=0.1,
            ),
            "content_fetcher": AugLLMConfig(
                name="content_fetcher", tools=[fetch_page_content], temperature=0.0
            ),
            "summarizer": AugLLMConfig(
                name="summarizer",
                structured_output_model=ContentSummary,
                structured_output_version="v2",
                prompt_template=summarization_prompt,
                temperature=0.3,
            ),
            "synthesizer": AugLLMConfig(
                name="synthesizer",
                structured_output_model=ResearchReport,
                structured_output_version="v2",
                prompt_template=synthesis_prompt,
                temperature=0.5,
            ),
            "quality_assessor": AugLLMConfig(
                name="quality_assessor",
                prompt_template=quality_assessment_prompt,
                temperature=0.2,
            ),
        }
    )

    state_schema: type = Field(default=SearchSummarizeState)

    def build_graph(self) -> BaseGraph:
        """Build the search and summarize workflow graph."""
        graph = BaseGraph(name=self.name)

        # Search planning node
        plan_node = EngineNodeConfig(
            name="plan_search", engine=self.engines["search_planner"]
        )
        graph.add_node("plan_search", plan_node)
        graph.add_edge(START, "plan_search")

        # Main search node
        search_node = EngineNodeConfig(name="search", engine=self.engines["searcher"])
        graph.add_node("search", search_node)
        graph.add_edge("plan_search", "search")

        # Conditional routing after search
        graph.add_conditional_edges(
            "search",
            route_after_search,
            {
                "academic_search": "search_academic",
                "news_search": "search_news",
                "fetch_content": "fetch_content",
                "no_results": "handle_no_results",
            },
        )

        # Specialized search nodes
        academic_node = EngineNodeConfig(
            name="search_academic", engine=self.engines["searcher"]
        )
        graph.add_node("search_academic", academic_node)
        graph.add_edge("search_academic", "fetch_content")

        news_node = EngineNodeConfig(
            name="search_news", engine=self.engines["searcher"]
        )
        graph.add_node("search_news", news_node)
        graph.add_edge("search_news", "fetch_content")

        # Content fetching node
        fetch_node = EngineNodeConfig(
            name="fetch_content", engine=self.engines["content_fetcher"]
        )
        graph.add_node("fetch_content", fetch_node)

        # Route after fetching
        graph.add_conditional_edges(
            "fetch_content",
            route_after_fetch,
            {"summarize": "summarize", "no_content": "handle_no_content"},
        )

        # Summarization node
        summary_node = EngineNodeConfig(
            name="summarize", engine=self.engines["summarizer"]
        )
        graph.add_node("summarize", summary_node)

        # Route after summarization
        graph.add_conditional_edges(
            "summarize",
            route_after_summary,
            {"synthesize": "synthesize", "insufficient_results": "handle_insufficient"},
        )

        # Synthesis node
        synthesis_node = EngineNodeConfig(
            name="synthesize", engine=self.engines["synthesizer"]
        )
        graph.add_node("synthesize", synthesis_node)

        # Quality assessment (optional)
        quality_node = EngineNodeConfig(
            name="assess_quality", engine=self.engines["quality_assessor"]
        )
        graph.add_node("assess_quality", quality_node)
        graph.add_edge("synthesize", "assess_quality")
        graph.add_edge("assess_quality", END)

        # Error handling nodes
        graph.add_node("handle_no_results", self.handle_no_results)
        graph.add_edge("handle_no_results", END)

        graph.add_node("handle_no_content", self.handle_no_content)
        graph.add_edge("handle_no_content", END)

        graph.add_node("handle_insufficient", self.handle_insufficient_results)
        graph.add_edge("handle_insufficient", END)

        return graph

    def handle_no_results(self, state: SearchSummarizeState) -> SearchSummarizeState:
        """Handle case when no search results are found."""
        state.research_report = ResearchReport(
            query=state.query_text,
            executive_summary="No search results found for the given query.",
            summaries=[],
            key_insights=["No results found. Try refining your search query."],
            metadata={"error": "no_results"},
        )
        state.end_time = datetime.now()
        return state

    def handle_no_content(self, state: SearchSummarizeState) -> SearchSummarizeState:
        """Handle case when content cannot be fetched."""
        state.research_report = ResearchReport(
            query=state.query_text,
            executive_summary="Unable to fetch content from search results.",
            summaries=[],
            key_insights=[
                "Content could not be retrieved. The sources may be inaccessible."
            ],
            metadata={"error": "no_content"},
        )
        state.end_time = datetime.now()
        return state

    def handle_insufficient_results(
        self, state: SearchSummarizeState
    ) -> SearchSummarizeState:
        """Handle case when there are insufficient results for synthesis."""
        # Create basic report with what we have
        state.research_report = ResearchReport(
            query=state.query_text,
            executive_summary=f"Limited results found. Only {state.sources_summarized} source(s) could be analyzed.",
            summaries=state.content_summaries,
            key_insights=[f"Found {state.sources_summarized} relevant source(s)"],
            metadata={"warning": "insufficient_results"},
        )
        state.end_time = datetime.now()
        return state


# Convenience function to create a simple search-summarize agent
def create_research_agent(
    search_types: Optional[List[str]] = None,
    preferred_domains: Optional[List[str]] = None,
    summary_style: str = "bullet_points",
    max_results: int = 5,
) -> SearchSummarizeAgent:
    """
    Create a configured search and summarize agent.

    Args:
        search_types: Types of searches to perform (general, academic, news)
        preferred_domains: Domains to prioritize in results
        summary_style: Style of summaries (bullet_points, paragraph, etc.)
        max_results: Maximum results per search

    Returns:
        Configured SearchSummarizeAgent
    """
    # Configure the agent based on parameters
    agent = SearchSummarizeAgent()

    # Add configuration to agent metadata
    agent.metadata = {
        "search_types": search_types or ["general"],
        "preferred_domains": preferred_domains or [],
        "summary_style": summary_style,
        "max_results": max_results,
    }

    return agent
