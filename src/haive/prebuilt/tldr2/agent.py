"""News Research Agent implementation.

This module implements the main NewsResearchAgent class that orchestrates
the entire news research workflow using the Haive framework.

The agent follows a multi-stage workflow:
1. Generate search parameters
2. Search for articles
3. Extract article content
4. Select relevant articles
5. Summarize articles
6. Analyze findings
7. Generate report

Example:
    >>> from news_research.agent import NewsResearchAgent
    >>> agent = NewsResearchAgent()
    >>> state = NewsResearchState(research_topic="AI in healthcare")
    >>> result = agent.invoke(state)
    >>> print(result.report.to_markdown())

Note:
    The agent uses declarative configuration with engines handling
    all LLM interactions and state management.
"""

import logging
from typing import Any, Dict, List, Optional, Type

from haive.agents.base.agent import Agent
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import Field

from haive.prebuilt.tldr2.engines import create_all_engines
from haive.prebuilt.tldr2.models import SearchDecision
from haive.prebuilt.tldr2.state import NewsResearchState

# Configure logging
logger = logging.getLogger(__name__)


class NewsResearchAgent(Agent):
    """News Research Agent for comprehensive article research and analysis.

    This agent implements a complete news research workflow that finds,
    analyzes, and reports on news articles for any given topic.

    The agent uses multiple specialized engines for different tasks:
    - Search engine: Generates NewsAPI search parameters
    - Extraction engine: Coordinates content extraction
    - Selection engine: Chooses most relevant articles
    - Summary engine: Creates article summaries
    - Decision engine: Controls workflow logic
    - Analysis engine: Synthesizes findings
    - Report engine: Generates final report

    Attributes:
        engines: Dictionary of specialized engines
        state_schema: NewsResearchState for workflow data
        max_search_iterations: Maximum search attempts
        min_articles_for_analysis: Minimum articles needed

    Example:
        >>> agent = NewsResearchAgent()
        >>> state = NewsResearchState(
        ...     research_topic="Impact of AI on healthcare",
        ...     max_sources=20
        ... )
        >>> result = agent.invoke(state)
        >>> print(f"Report: {result.report.title}")
        >>> print(f"Analyzed {result.report.sources_count} sources")
    """

    # Engine configuration
    engines: Dict[str, Any] = Field(
        default_factory=create_all_engines,
        description="All engines used by the news research agent",
    )

    # State schema
    state_schema: Type[NewsResearchState] = Field(
        default=NewsResearchState, description="State schema for the research workflow"
    )

    # Workflow configuration
    max_search_iterations: int = Field(
        default=5, description="Maximum number of search iterations"
    )

    min_articles_for_analysis: int = Field(
        default=3, description="Minimum articles needed for meaningful analysis"
    )

    def build_graph(self) -> BaseGraph:
        """Build the news research workflow graph.

        Creates a graph that orchestrates the research workflow through
        multiple stages with conditional routing based on results.

        Returns:
            BaseGraph: Configured workflow graph

        Workflow:
            START -> search -> extract -> select -> summarize -> decide
                                                                   |
                     <--------------------------------------------|
                                                                   |
                                                                   v
                                                             analyze -> report -> END
        """
        logger.info(f"Building graph for {self.name}")

        # Create the graph
        graph = BaseGraph(name=f"{self.name}_graph", state_schema=self.state_schema)

        # Add nodes for each stage

        # 1. Search parameter generation
        graph.add_node(
            "search",
            EngineNodeConfig(
                name="search",
                engine=self.engines["search"],
                state_transformer=self._prepare_search_state,
            ),
        )

        # 2. Article extraction
        graph.add_node("extract", self._extract_articles)

        # 3. Article selection
        graph.add_node(
            "select",
            EngineNodeConfig(
                name="select",
                engine=self.engines["selection"],
                state_transformer=self._prepare_selection_state,
            ),
        )

        # 4. Article summarization
        graph.add_node("summarize", self._summarize_articles)

        # 5. Search decision
        graph.add_node(
            "decide",
            EngineNodeConfig(
                name="decide",
                engine=self.engines["decision"],
                state_transformer=self._prepare_decision_state,
            ),
        )

        # 6. Analysis
        graph.add_node(
            "analyze",
            EngineNodeConfig(
                name="analyze",
                engine=self.engines["analysis"],
                state_transformer=self._prepare_analysis_state,
            ),
        )

        # 7. Report generation
        graph.add_node(
            "report",
            EngineNodeConfig(
                name="report",
                engine=self.engines["report"],
                state_transformer=self._prepare_report_state,
            ),
        )

        # Add edges
        graph.add_edge(START, "search")
        graph.add_edge("search", "extract")
        graph.add_edge("extract", "select")
        graph.add_edge("select", "summarize")
        graph.add_edge("summarize", "decide")

        # Conditional routing from decide node
        graph.add_conditional_edges(
            "decide",
            self._route_decision,
            {"continue": "search", "analyze": "analyze", "end": END},
        )

        graph.add_edge("analyze", "report")
        graph.add_edge("report", END)

        return graph

    # State transformation methods
    def _prepare_search_state(self, state: NewsResearchState) -> Dict[str, Any]:
        """Prepare state for search parameter generation.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for search engine
        """
        past_searches_str = (
            "\n".join(
                [
                    f"- Query: {p.q}, Sources: {p.sources}, Dates: {p.from_param} to {p.to}"
                    for p in state.past_searches
                ]
            )
            if state.past_searches
            else "None"
        )

        return {
            "research_topic": state.research_topic,
            "past_searches": past_searches_str,
            "search_iteration": state.search_iterations + 1,
        }

    def _prepare_selection_state(self, state: NewsResearchState) -> Dict[str, Any]:
        """Prepare state for article selection.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for selection engine
        """
        articles_info = "\n\n".join(
            [
                f"Title: {a.title}\nURL: {a.url}\nSource: {a.source.get('name', 'Unknown')}\n"
                f"Description: {a.description[:200]}...\nWord Count: {a.word_count}"
                for a in state.articles_content
            ]
        )

        return {
            "research_topic": state.research_topic,
            "articles_info": articles_info,
            "max_articles": min(10, len(state.articles_content)),
        }

    def _prepare_decision_state(self, state: NewsResearchState) -> Dict[str, Any]:
        """Prepare state for search decision.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for decision engine
        """
        # Calculate search effectiveness
        if state.search_iterations > 0:
            effectiveness = state.total_articles_found / state.search_iterations
            effectiveness_str = f"{effectiveness:.1f} articles per search"
        else:
            effectiveness_str = "No searches yet"

        return {
            "research_topic": state.research_topic,
            "total_articles": state.total_articles_found,
            "articles_with_content": state.total_articles_processed,
            "articles_summarized": len(state.article_summaries),
            "avg_relevance": state.average_relevance,
            "unique_sources": state.total_sources_checked,
            "search_iterations": state.search_iterations,
            "max_iterations": self.max_search_iterations,
            "search_effectiveness": effectiveness_str,
        }

    def _prepare_analysis_state(self, state: NewsResearchState) -> Dict[str, Any]:
        """Prepare state for analysis.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for analysis engine
        """
        # Format article summaries
        articles_summary = "\n\n".join(
            [
                f"**{s.title}**\nSource: {s.url}\nRelevance: {s.relevance_score:.2f}\n"
                + "\n".join(f"- {point}" for point in s.summary)
                for s in state.article_summaries
            ]
        )

        # Calculate source statistics
        sources = {}
        for article in state.article_summaries:
            # Extract source from URL
            source = article.url.split("/")[2] if "/" in article.url else "Unknown"
            sources[source] = sources.get(source, 0) + 1

        source_stats = "\n".join(
            [
                f"- {source}: {count} articles"
                for source, count in sorted(
                    sources.items(), key=lambda x: x[1], reverse=True
                )
            ]
        )

        # Determine time range
        time_range = f"{state.search_iterations} search iterations"

        return {
            "research_topic": state.research_topic,
            "articles_summary": articles_summary,
            "source_stats": source_stats,
            "time_range": time_range,
        }

    def _prepare_report_state(self, state: NewsResearchState) -> Dict[str, Any]:
        """Prepare state for report generation.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for report engine
        """
        # Format analysis summary
        analysis_summary = f"""
Main Themes: {', '.join(state.analysis.main_themes)}
Key Findings: {len(state.analysis.key_findings)} findings identified
Confidence Level: {state.analysis.confidence_level:.2f}
Data Gaps: {len(state.analysis.data_gaps)} gaps identified
        """.strip()

        # Get top articles by relevance
        top_articles = sorted(
            state.article_summaries, key=lambda x: x.relevance_score, reverse=True
        )[:5]

        top_articles_str = "\n".join(
            [
                f"{i+1}. {a.title} (Relevance: {a.relevance_score:.2f})"
                for i, a in enumerate(top_articles)
            ]
        )

        return {
            "research_topic": state.research_topic,
            "analysis_summary": analysis_summary,
            "article_count": len(state.article_summaries),
            "source_count": state.total_sources_checked,
            "time_period": f"Last {state.search_iterations * 7} days",
            "avg_relevance": state.average_relevance,
            "top_articles": top_articles_str,
        }

    # Custom node implementations
    def _extract_articles(self, state: NewsResearchState) -> Command:
        """Extract article content using web scraping.

        Args:
            state: Current workflow state

        Returns:
            Command to update state with extracted content
        """
        from haive.prebuilt.tldr2.models import ArticleContent
        from haive.prebuilt.tldr2.tools import extract_content

        # Get unprocessed articles
        unprocessed = state.get_unprocessed_metadata()

        if not unprocessed:
            logger.info("No new articles to extract")
            return Command(update={})

        logger.info(f"Extracting content from {len(unprocessed)} articles")

        # Extract content from each article
        extracted_articles = []
        for article in unprocessed[: state.max_articles_per_search]:
            try:
                result = extract_content(article.url)

                if result["success"] and result["word_count"] > 100:
                    content = ArticleContent(
                        title=article.title,
                        url=article.url,
                        description=article.description,
                        text=result["content"],
                        word_count=result["word_count"],
                    )
                    extracted_articles.append(content)
                    logger.debug(
                        f"Extracted {result['word_count']} words from {article.url}"
                    )
                else:
                    logger.warning(
                        f"Failed to extract meaningful content from {article.url}"
                    )

            except Exception as e:
                logger.error(f"Error extracting {article.url}: {e}")
                state.add_error("extraction", str(e), {"url": article.url})

        # Update state
        for article in extracted_articles:
            state.add_article_content(article)

        logger.info(f"Successfully extracted {len(extracted_articles)} articles")

        return Command(update={"articles_content": state.articles_content})

    def _summarize_articles(self, state: NewsResearchState) -> Command:
        """Summarize selected articles.

        Args:
            state: Current workflow state

        Returns:
            Command to update state with article summaries
        """
        # Get selected articles from previous step
        selection_result = state.messages[-1].parsed if state.messages else None

        if not selection_result or not hasattr(selection_result, "selected_urls"):
            logger.warning("No article selection found")
            return Command(update={})

        selected_urls = selection_result.selected_urls
        relevance_scores = selection_result.relevance_scores

        # Get full article content for selected URLs
        selected_articles = [
            a for a in state.articles_content if a.url in selected_urls
        ]

        logger.info(f"Summarizing {len(selected_articles)} selected articles")

        # Summarize each article
        summaries = []
        for article in selected_articles:
            try:
                # Prepare inputs for summary engine
                summary_inputs = {
                    "research_topic": state.research_topic,
                    "article_title": article.title,
                    "article_url": article.url,
                    "article_content": article.text[:3000],  # Limit content length
                    "messages": state.messages,
                }

                # Invoke summary engine
                result = self.engines["summary"].invoke(summary_inputs)

                if result and hasattr(result, "parsed"):
                    summary = result.parsed
                    # Update relevance score from selection
                    if article.url in relevance_scores:
                        summary.relevance_score = relevance_scores[article.url]
                    summaries.append(summary)

            except Exception as e:
                logger.error(f"Error summarizing {article.url}: {e}")
                state.add_error("summarization", str(e), {"url": article.url})

        # Update state
        state.article_summaries.extend(summaries)

        logger.info(f"Created {len(summaries)} article summaries")

        return Command(update={"article_summaries": state.article_summaries})

    def _route_decision(self, state: NewsResearchState) -> str:
        """Route workflow based on search decision.

        Args:
            state: Current workflow state

        Returns:
            Next node name based on decision
        """
        # Get decision from last message
        decision = state.messages[-1].parsed if state.messages else None

        if not decision or not hasattr(decision, "action"):
            logger.warning("No decision found, defaulting to end")
            return "end"

        logger.info(f"Decision: {decision.action} - {decision.reason}")

        # Update state with decision
        state.search_decision = decision

        # Route based on action
        if decision.action == "continue_search":
            if state.search_iterations >= self.max_search_iterations:
                logger.info("Max search iterations reached, proceeding to analysis")
                return "analyze"
            return "continue"
        elif decision.action == "analyze":
            return "analyze"
        else:  # insufficient_data
            logger.warning("Insufficient data for analysis")
            return "end"

    def get_research_summary(self, state: NewsResearchState) -> Dict[str, Any]:
        """Get a summary of the research process.

        Args:
            state: Final workflow state

        Returns:
            Dictionary with research summary statistics

        Example:
            >>> summary = agent.get_research_summary(result_state)
            >>> print(f"Analyzed {summary['articles_analyzed']} articles")
        """
        return {
            "topic": state.research_topic,
            "articles_found": state.total_articles_found,
            "articles_analyzed": len(state.article_summaries),
            "sources_consulted": state.total_sources_checked,
            "search_iterations": state.search_iterations,
            "average_relevance": round(state.average_relevance, 2),
            "report_generated": state.report is not None,
            "confidence_score": state.report.confidence_score if state.report else 0.0,
            "errors_encountered": len(state.errors),
        }


# Convenience function to create and run the agent
def research_topic(
    topic: str, max_sources: int = 10, max_search_iterations: int = 3
) -> NewsResearchState:
    """Convenience function to research a topic.

    Args:
        topic: Research topic
        max_sources: Maximum sources to check
        max_search_iterations: Maximum search attempts

    Returns:
        NewsResearchState with complete results

    Example:
        >>> result = research_topic("AI in healthcare", max_sources=15)
        >>> print(result.report.to_markdown())
    """
    agent = NewsResearchAgent(max_search_iterations=max_search_iterations)

    state = NewsResearchState(research_topic=topic, max_sources=max_sources)

    return agent.invoke(state)


# Export main components
__all__ = ["NewsResearchAgent", "research_topic"]
