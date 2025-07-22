# src/haive/agents/news_reporter/agents.py
"""General News Reporter Agent implementatio."""

import logging
from datetime import datetime

from langgraph.graph import END, START
from pydantic import Field

from .ai_insight.models import (
    ArticleSummary,
    NewsCategory,
    NewsReport,
    ReportMetadata,
)
from .ai_insight.prompts import (
    categorization_prompt,
    report_generation_prompt,
    spotlight_selection_prompt,
    summarization_prompt,
    trend_analysis_prompt,
)
from .ai_insight.state import NewsReporterState
from .ai_insight.tools import (
    filter_articles_by_relevance,
    save_report_to_file,
    search_news,
)
from .base.agent import Agent
from .engine.aug_llm import AugLLMConfig
from .graph.node.engine_node import EngineNodeConfig
from .graph.state_graph.base_graph import BaseGraph

logger = logging.getLogger(__name__)


def route_after_search(state: NewsReporterState) -> st:
    """Route based on search result."""
    if not state.raw_articles:
        retur "no_results"
    retur "filter"


def route_after_filter(state: NewsReporterState) -> st:
    """Route based on filtered article."""
    if not state.filtered_articles:
        retur "insufficient_content"
    retur "summarize"


def route_after_summary(state: NewsReporterState) -> st:
    """Route based on summarie."""
    if not state.has_sufficient_content:
        retur "insufficient_content"
    retur "categorize"


class NewsReporterAgent(Agen):
    """General news reporter agent that can cover any topic.

    The agent intelligently:
    - Searches for news on the given topic
    - Categorizes articles based on their content
    - Generates appropriate summaries for the target audience
    - Identifies trends from the actual content
    - Creates a well-structured repor
    """

    # Define engines
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=lambd: {
            "searcher": AugLLMConfig(
                nam="searcher",
                tools=[search_news, filter_articles_by_relevance],
                temperature=.,
            ),
            "summarizer": AugLLMConfig(
                nam="summarizer",
                structured_output_model=ArticleSummary,
                structured_output_versio="v",
                prompt_template=summarization_prompt,
                temperature=0.,
            ),
            "categorizer": AugLLMConfig(
                nam="categorizer",
                structured_output_model=list[NewsCategory],
                structured_output_versio="v",
                prompt_template=categorization_prompt,
                temperature=0.,
            ),
            "trend_analyzer": AugLLMConfig(
                nam="trend_analyzer",
                structured_output_model=list[str],
                structured_output_versio="v",
                prompt_template=trend_analysis_prompt,
                temperature=0.,
            ),
            "spotlight_selector": AugLLMConfig(
                nam="spotlight_selector",
                structured_output_model=ArticleSummary,
                structured_output_versio="v",
                prompt_template=spotlight_selection_prompt,
                temperature=0.,
            ),
            "report_generator": AugLLMConfig(
                nam="report_generator",
                structured_output_model=NewsReport,
                structured_output_versio="v",
                prompt_template=report_generation_prompt,
                temperature=0.,
            ),
            "publisher": AugLLMConfig(
                nam="publisher", tools=[save_report_to_file], temperature=0.
            ),
        }
    )

    state_schema: type = Field(default=NewsReporterState)

    def build_graph(self) -> BaseGrap:
        """Build the news reporting workflow grap."""
        graph = BaseGraph(name=self.name)

        # Search node
        search_node = EngineNodeConfig(nam="search", engine=self.engine["searcher"])
        graph.add_nod("search", search_node)
        graph.add_edge(STAR, "search")

        # Routing after search
        graph.add_conditional_edge(
            "search",
            route_after_searc,
            {"filter": "filte", "no_result": "handle_no_result"},
        )

        # Filter node
        filter_node = EngineNodeConfig(
            name="filte",
            engine=self.engines["searche"],  # Reuse searcher for filtering
        )
        graph.add_node("filte", filter_node)

        # Routing after filter
        graph.add_conditional_edges(
            "filte",
            route_after_filter,
            {"summariz": "summariz", "insufficient_conten": "handle_insufficien"},
        )

        # Summarize node
        summary_node = EngineNodeConfig(
            name="summariz", engine=self.engines["summarize"]
        )
        graph.add_node("summariz", summary_node)

        # Routing after summary
        graph.add_conditional_edges(
            "summariz",
            route_after_summary,
            {"categoriz": "categoriz", "insufficient_conten": "handle_insufficien"},
        )

        # Categorize node
        categorize_node = EngineNodeConfig(
            name="categoriz", engine=self.engines["categorize"]
        )
        graph.add_node("categoriz", categorize_node)
        graph.add_edge("categoriz", "analyze_trend")

        # Trend analysis node
        trend_node = EngineNodeConfig(
            name="analyze_trend", engine=self.engines["trend_analyze"]
        )
        graph.add_node("analyze_trend", trend_node)

        # Conditional spotlight selection
        graph.add_conditional_edges(
            "analyze_trend",
            lambda s: (
                "select_spotligh"
                if s.report_config.include_spotlight
                else "generate_repor"
            ),
            {
                "select_spotligh": "select_spotligh",
                "generate_repor": "generate_repor",
            },
        )

        # Spotlight selection node
        spotlight_node = EngineNodeConfig(
            name="select_spotligh", engine=self.engines["spotlight_selecto"]
        )
        graph.add_node("select_spotligh", spotlight_node)
        graph.add_edge("select_spotligh", "generate_repor")

        # Report generation node
        report_node = EngineNodeConfig(
            name="generate_repor", engine=self.engines["report_generato"]
        )
        graph.add_node("generate_repor", report_node)

        # Conditional save
        graph.add_conditional_edges(
            "generate_repor",
            lambda s: "publis" if s.report_config.save_to_file else END,
            {"publis": "publis", END: END},
        )

        # Publish node
        publish_node = EngineNodeConfig(
            name="publis", engine=self.engines["publishe"]
        )
        graph.add_node("publis", publish_node)
        graph.add_edge("publis", END)

        # Error handling nodes
        graph.add_node("handle_no_result", self.handle_no_results)
        graph.add_edge("handle_no_result", END)

        graph.add_node("handle_insufficien", self.handle_insufficient_content)
        graph.add_edge("handle_insufficien", END)

        return graph

    def handle_no_results(self, state: NewsReporterState) -> NewsReporterState:
        """Handle case when no results are foun."""
        state.news_report = NewsReport(
            title="No news found for: {state.topic}",
            executive_summar="No articles were found for the specified search criteria.",
            introductio="Try adjusting your search parameters or checking back later.",
            categories=[],
            metadata=ReportMetadata(
                topic=state.topic,
                time_period=state.search_config.time_period,
                total_sources=,
                search_config=state.search_config,
            ),
        )
        state.end_time = datetime.now()
        return state

    def handle_insufficient_content(
        self, state: NewsReporterState
    ) -> NewsReporterStat:
        """Handle case when there's insufficient content."""
        # Create minimal report with what we have
        state.news_report = NewsReport(
            title="Limited news coverage for: {state.topic}",
            executive_summary="Only {state.articles_processed} articles found and processed.",
            introductio="Limited news coverage was available for this topic.",
            categories=[
                NewsCategory(
                    nam="Available Articles",
                    descriptio="All articles found",
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
