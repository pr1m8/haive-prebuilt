# src/haive/agents/news_reporter/agents.py
"""
General News Reporter Agent implementation.
"""

import logging
from datetime import datetime
from typing import Dict, List

from haive.agents.base.agent import Agent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field

from haive.prebuilt.ai_insight.models import (
    ArticleSummary,
    NewsCategory,
    NewsReport,
    ReportMetadata,
)
from haive.prebuilt.ai_insight.prompts import (
    categorization_prompt,
    report_generation_prompt,
    spotlight_selection_prompt,
    summarization_prompt,
    trend_analysis_prompt,
)
from haive.prebuilt.ai_insight.state import NewsReporterState
from haive.prebuilt.ai_insight.tools import (
    filter_articles_by_relevance,
    save_report_to_file,
    search_news,
)

logger = logging.getLogger(__name__)


def route_after_search(state: NewsReporterState) -> str:
    """Route based on search results."""
    if not state.raw_articles:
        return "no_results"
    return "filter"


def route_after_filter(state: NewsReporterState) -> str:
    """Route based on filtered articles."""
    if not state.filtered_articles:
        return "insufficient_content"
    return "summarize"


def route_after_summary(state: NewsReporterState) -> str:
    """Route based on summaries."""
    if not state.has_sufficient_content:
        return "insufficient_content"
    return "categorize"


class NewsReporterAgent(Agent):
    """
    General news reporter agent that can cover any topic.

    The agent intelligently:
    - Searches for news on the given topic
    - Categorizes articles based on their content
    - Generates appropriate summaries for the target audience
    - Identifies trends from the actual content
    - Creates a well-structured report
    """

    # Define engines
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=lambda: {
            "searcher": AugLLMConfig(
                name="searcher",
                tools=[search_news, filter_articles_by_relevance],
                temperature=0.1,
            ),
            "summarizer": AugLLMConfig(
                name="summarizer",
                structured_output_model=ArticleSummary,
                structured_output_version="v2",
                prompt_template=summarization_prompt,
                temperature=0.3,
            ),
            "categorizer": AugLLMConfig(
                name="categorizer",
                structured_output_model=List[NewsCategory],
                structured_output_version="v2",
                prompt_template=categorization_prompt,
                temperature=0.5,
            ),
            "trend_analyzer": AugLLMConfig(
                name="trend_analyzer",
                structured_output_model=List[str],
                structured_output_version="v2",
                prompt_template=trend_analysis_prompt,
                temperature=0.5,
            ),
            "spotlight_selector": AugLLMConfig(
                name="spotlight_selector",
                structured_output_model=ArticleSummary,
                structured_output_version="v2",
                prompt_template=spotlight_selection_prompt,
                temperature=0.3,
            ),
            "report_generator": AugLLMConfig(
                name="report_generator",
                structured_output_model=NewsReport,
                structured_output_version="v2",
                prompt_template=report_generation_prompt,
                temperature=0.7,
            ),
            "publisher": AugLLMConfig(
                name="publisher", tools=[save_report_to_file], temperature=0.1
            ),
        }
    )

    state_schema: type = Field(default=NewsReporterState)

    def build_graph(self) -> BaseGraph:
        """Build the news reporting workflow graph."""
        graph = BaseGraph(name=self.name)

        # Search node
        search_node = EngineNodeConfig(name="search", engine=self.engines["searcher"])
        graph.add_node("search", search_node)
        graph.add_edge(START, "search")

        # Routing after search
        graph.add_conditional_edges(
            "search",
            route_after_search,
            {"filter": "filter", "no_results": "handle_no_results"},
        )

        # Filter node
        filter_node = EngineNodeConfig(
            name="filter",
            engine=self.engines["searcher"],  # Reuse searcher for filtering
        )
        graph.add_node("filter", filter_node)

        # Routing after filter
        graph.add_conditional_edges(
            "filter",
            route_after_filter,
            {"summarize": "summarize", "insufficient_content": "handle_insufficient"},
        )

        # Summarize node
        summary_node = EngineNodeConfig(
            name="summarize", engine=self.engines["summarizer"]
        )
        graph.add_node("summarize", summary_node)

        # Routing after summary
        graph.add_conditional_edges(
            "summarize",
            route_after_summary,
            {"categorize": "categorize", "insufficient_content": "handle_insufficient"},
        )

        # Categorize node
        categorize_node = EngineNodeConfig(
            name="categorize", engine=self.engines["categorizer"]
        )
        graph.add_node("categorize", categorize_node)
        graph.add_edge("categorize", "analyze_trends")

        # Trend analysis node
        trend_node = EngineNodeConfig(
            name="analyze_trends", engine=self.engines["trend_analyzer"]
        )
        graph.add_node("analyze_trends", trend_node)

        # Conditional spotlight selection
        graph.add_conditional_edges(
            "analyze_trends",
            lambda s: (
                "select_spotlight"
                if s.report_config.include_spotlight
                else "generate_report"
            ),
            {
                "select_spotlight": "select_spotlight",
                "generate_report": "generate_report",
            },
        )

        # Spotlight selection node
        spotlight_node = EngineNodeConfig(
            name="select_spotlight", engine=self.engines["spotlight_selector"]
        )
        graph.add_node("select_spotlight", spotlight_node)
        graph.add_edge("select_spotlight", "generate_report")

        # Report generation node
        report_node = EngineNodeConfig(
            name="generate_report", engine=self.engines["report_generator"]
        )
        graph.add_node("generate_report", report_node)

        # Conditional save
        graph.add_conditional_edges(
            "generate_report",
            lambda s: "publish" if s.report_config.save_to_file else END,
            {"publish": "publish", END: END},
        )

        # Publish node
        publish_node = EngineNodeConfig(
            name="publish", engine=self.engines["publisher"]
        )
        graph.add_node("publish", publish_node)
        graph.add_edge("publish", END)

        # Error handling nodes
        graph.add_node("handle_no_results", self.handle_no_results)
        graph.add_edge("handle_no_results", END)

        graph.add_node("handle_insufficient", self.handle_insufficient_content)
        graph.add_edge("handle_insufficient", END)

        return graph

    def handle_no_results(self, state: NewsReporterState) -> NewsReporterState:
        """Handle case when no results are found."""
        state.news_report = NewsReport(
            title=f"No news found for: {state.topic}",
            executive_summary="No articles were found for the specified search criteria.",
            introduction="Try adjusting your search parameters or checking back later.",
            categories=[],
            metadata=ReportMetadata(
                topic=state.topic,
                time_period=state.search_config.time_period,
                total_sources=0,
                search_config=state.search_config,
            ),
        )
        state.end_time = datetime.now()
        return state

    def handle_insufficient_content(
        self, state: NewsReporterState
    ) -> NewsReporterState:
        """Handle case when there's insufficient content."""
        # Create minimal report with what we have
        state.news_report = NewsReport(
            title=f"Limited news coverage for: {state.topic}",
            executive_summary=f"Only {state.articles_processed} articles found and processed.",
            introduction="Limited news coverage was available for this topic.",
            categories=[
                NewsCategory(
                    name="Available Articles",
                    description="All articles found",
                    articles=state.article_summaries,
                )
            ],
            metadata=ReportMetadata(
                topic=state.topic,
                time_period=state.search_config.time_period,
                total_sources=state.articles_found,
                search_config=state.search_config,
            ),
        )
        state.end_time = datetime.now()
        return state
