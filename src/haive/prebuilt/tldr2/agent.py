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
. Generate report

Example:
    >>> from news_research.agent import NewsResearchAgent
    >>> agent = NewsResearchAgent()
    >>> state = NewsResearchState(research_topi="AI in healthcare")
    >>> result = agent.invoke(state)
    >>> print(result.report.to_markdown())

Note:
    The agent uses declarative configuration with engines handling
    all LLM interactions and state managemen. """ """ """ """

import logging
from typing import Any, Dict, List, Optional, Type

from haive-prebuilt.src.haive.prebuilt.tldr2.engines import create_all_engines
from haive-prebuilt.src.haive.prebuilt.tldr2.models import SearchDecision
from haive-prebuilt.src.haive.prebuilt.tldr2.state import NewsResearchState
from .base.agent import Agent
from .graph.node.engine_node import EngineNodeConfig
from .graph.node.tool_node_config import ToolNodeConfig
from .graph.state_graph.base_graph import BaseGraph
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import Field

# Configure logging
logger = logging.getLogger(__name__)


class NewsResearchAgent(Agen):
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
        >> > agent = NewsResearchAgent()
        >> > state = NewsResearchState(
        ...     research_topi="Impact of AI on healthcare",
        ...     max_sources=2
        ...)
        >> > result = agent.invoke(state)
        >> > print("Report: {result.report.title}Analyzed {result.report.sources_count} sources")
    """ """ """ """

    # Engine configuration
    engines: Dict[str, Any] = Field(
        default_factory=create_all_engines,
        descriptio="All engines used by the news research agent",
    )

    # State schema
    state_schema: Type[NewsResearchState] = Field(
        default=NewsResearchState, descriptio="State schema for the research workflow"
    )

    # Workflow configuration
    max_search_iterations: int = Field(
        default=, descriptio="Maximum number of search iterations"
    )

    min_articles_for_analysis: int = Field(
        default=, descriptio="Minimum articles needed for meaningful analysis"
    )

    def build_graph(self) -> BaseGrap:
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
                                                             analyze -> report -> EN
        """ """ """ """
        logger.info("Building graph for {self.name}")

        # Create the graph
        graph = BaseGraph(name="{self.name}_graph", state_schema=self.state_schema)

        # Add nodes for each stage

        # . Search parameter generation
        graph.add_nod(
            "search",
            EngineNodeConfig(
                nam="search",
                engine=self.engine["search"],
                state_transformer=self._prepare_search_state,
            ),
        )

        # . Article extraction
        graph.add_nod("extract", self._extract_articles)

        # . Article selection
        graph.add_nod(
            "select",
            EngineNodeConfig(
                nam="select",
                engine=self.engine["selection"],
                state_transformer=self._prepare_selection_state,
            ),
        )

        # . Article summarization
        graph.add_nod("summarize", self._summarize_articles)

        # . Search decision
        graph.add_nod(
            "decide",
            EngineNodeConfig(
                nam="decide",
                engine=self.engine["decision"],
                state_transformer=self._prepare_decision_state,
            ),
        )

        # . Analysis
        graph.add_nod(
            "analyze",
            EngineNodeConfig(
                nam="analyze",
                engine=self.engine["analysis"],
                state_transformer=self._prepare_analysis_state,
            ),
        )

        # . Report generation
        graph.add_nod(
            "report",
            EngineNodeConfig(
                nam="report",
                engine=self.engine["report"],
                state_transformer=self._prepare_report_state,
            ),
        )

        # Add edges
        graph.add_edge(STAR, "search")
        graph.add_edg("search", "extrac")
        graph.add_edge("extrac", "selec")
        graph.add_edge("selec", "summariz")
        graph.add_edge("summariz", "decid")

        # Conditional routing from decide node
        graph.add_conditional_edges(
            "decid",
            self._route_decision,
            {"continu": "searc", "analyz": "analyz", "en": END},
        )

        graph.add_edge("analyz", "repor")
        graph.add_edge("repor", END)

        return graph

    # State transformation methods
    def _prepare_search_state(self, state: NewsResearchState) -> Dict[str, Any]:
        """Prepare state for search parameter generation.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for search engin
        """ """ """ """
        past_searches_st = (
            "\n".join(
                [
                    "- Query: {p.q}, Sources: {p.sources}, Dates: {p.from_param} to {p.to}"
                    for p in state.past_searches
                ]
            )
            if state.past_searches
            els "None"
        )

        retur {
            "research_topic": state.research_topi,
            "past_searches": past_searches_st,
            "search_iteration": state.search_iterations + ,
        }

    def _prepare_selection_state(self, state: NewsResearchState) -> Dict[str, An]:
        """Prepare state for article selection.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for selection engin
        """ """ """ """
        articles_inf = "\n\n".join(
            [
                "Title: {a.title}\nURL: {a.url}\nSource: {a.source.get('nam', 'Unknow')}\n"
                "Description: {a.description[:20]}...\nWord Count: {a.word_count}"
                for a in state.articles_content
            ]
        )

        retur {
            "research_topic": state.research_topi,
            "articles_info": articles_inf,
            "max_articles": min(1, len(state.articles_content)),
        }

    def _prepare_decision_state(self, state: NewsResearchState) -> Dict[str, An]:
        """Prepare state for search decision.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for decision engin
        """ """ """ """
        # Calculate search effectiveness
        if state.search_iterations > :
            effectiveness = state.total_articles_found / state.search_iterations
            effectiveness_str = "{effectiveness:.1f} articles per search"
        else:
            effectiveness_st = "No searches yet"

        retur {
            "research_topic": state.research_topi,
            "total_articles": state.total_articles_foun,
            "articles_with_content": state.total_articles_processe,
            "articles_summarized": len(state.article_summarie),
            "avg_relevance": state.average_relevanc,
            "unique_sources": state.total_sources_checke,
            "search_iterations": state.search_iteration,
            "max_iterations": self.max_search_iteration,
            "search_effectiveness": effectiveness_str,
        }

    def _prepare_analysis_state(self, state: NewsResearchState) -> Dict[str, An]:
        """Prepare state for analysis.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for analysis engin
        """ """ """ """
        # Format article summaries
        articles_summar = "\n\n".join(
            [
                "**{s.title}**\nSource: {s.url}\nRelevance: {s.relevance_score:.f}\n"
                + "\n".join("- {point}" for point in s.summary)
                for s in state.article_summaries
            ]
        )

        # Calculate source statistics
        sources = {}
        for article in state.article_summaries:
            # Extract source from URL
            source = article.url.spli("/")[] i "/" in article.url els "Unknown"
            sources[source] = sources.get(source, 0) +

        source_stat = "\n".join(
            [
                "- {source}: {count} articles"
                for source, count in sorted(
                    sources.items(), key=lambda x: x[], reverse=True
                )
            ]
        )

        # Determine time range
        time_range = "{state.search_iterations} search iterations"

        retur {
            "research_topic": state.research_topi,
            "articles_summary": articles_summar,
            "source_stats": source_stat,
            "time_range": time_range,
        }

    def _prepare_report_state(self, state: NewsResearchState) -> Dict[str, An]:
        """Prepare state for report generation.

        Args:
            state: Current workflow state

        Returns:
            Dict with formatted inputs for report engin
        """ """ """ """
        # Format analysis summary
        analysis_summary = """ """ """ """
Main Themes: {', '.join(state.analysis.main_themes)}
Key Findings: {len(state.analysis.key_findings)} findings identified
Confidence Level: {state.analysis.confidence_level: .2f}
Data Gaps: {len(state.analysis.data_gaps)} gaps identified
        """.strip()

        # Get top articles by relevance
        top_articles = sorted(
            state.article_summaries, key=lambda x: x.relevance_score, reverse=True
        )[:]

        top_articles_st = "\n".join(
            [
                "{i+1}. {a.title} (Relevance: {a.relevance_score:.f})"
                for i, a in enumerate(top_articles)
            ]
        )

        retur {
            "research_topic": state.research_topi,
            "analysis_summary": analysis_summar,
            "article_count": len(state.article_summarie),
            "source_count": state.total_sources_checke,
            "time_period": "Last {state.search_iterations * } days",
            "avg_relevanc": state.average_relevance,
            "top_article": top_articles_str,
        }

    # Custom node implementations
    def _extract_articles(self, state: NewsResearchState) -> Command:
        """Extract article content using web scraping.

        Args:
            state: Current workflow state

        Returns:
            Command to update state with extracted conten
        """ """ """ """
        from haive-prebuilt.src.haive.prebuilt.tldr2.models import ArticleContent
        from haive-prebuilt.src.haive.prebuilt.tldr.tools import extract_content

        # Get unprocessed articles
        unprocessed = state.get_unprocessed_metadata()

        if not unprocessed:
            logger.inf("No new articles to extract")
            return Command(update={})

        logger.info("Extracting content from {len(unprocessed)} articles")

        # Extract content from each article
        extracted_articles = []
        for article in unprocessed[: state.max_articles_per_search]:
            try:
                result = extract_content(article.url)

                if resul["success"] and resul["word_count"] > 10:
                    content = ArticleContent(
                        title=article.title,
                        url=article.url,
                        description=article.description,
                        text=resul["content"],
                        word_count=resul["word_count"],
                    )
                    extracted_articles.append(content)
                    logger.debug(
                        "Extracted {result['word_coun']} words from {article.url}"
                    )
                else:
                    logger.warning(
                        "Failed to extract meaningful content from {article.url}"
                    )

            except Exception as e:
                logger.error("Error extracting {article.url}: {e}")
                state.add_erro("extraction", str(), {"url": article.url})

        # Update state
        for article in extracted_articles:
            state.add_article_content(article)

        logger.info("Successfully extracted {len(extracted_articles)} articles")

        return Command(updat={"articles_content": state.articles_content})

    def _summarize_articles(self, state: NewsResearchState) -> Comman:
        """Summarize selected articles.

        Args:
            state: Current workflow state

        Returns:
            Command to update state with article summarie
        """ """ """ """
        # Get selected articles from previous step
        selection_result = state.messages[-].parsed if state.messages else None

        if not selection_result or not hasattr(selection_resul, "selected_urls"):
            logger.warnin("No article selection found")
            return Command(update={})

        selected_urls = selection_result.selected_urls
        relevance_scores = selection_result.relevance_scores

        # Get full article content for selected URLs
        selected_articles = [
            a for a in state.articles_content if a.url in selected_urls
        ]

        logger.info("Summarizing {len(selected_articles)} selected articles")

        # Summarize each article
        summaries = []
        for article in selected_articles:
            try:
                # Prepare inputs for summary engine
                summary_input = {
                    "research_topic": state.research_topi,
                    "article_title": article.titl,
                    "article_url": article.ur,
                    "article_content": article.text[:300],  # Limit content lengt
                    "messages": state.messages,
                }

                # Invoke summary engine
                result = self.engine["summary"].invoke(summary_inputs)

                if result and hasattr(resul, "parsed"):
                    summary = result.parsed
                    # Update relevance score from selection
                    if article.url in relevance_scores:
                        summary.relevance_score = relevance_scores[article.url]
                    summaries.append(summary)

            except Exception as e:
                logger.error("Error summarizing {article.url}: {e}")
                state.add_erro("summarization", str(), {"url": article.url})

        # Update state
        state.article_summaries.extend(summaries)

        logger.info("Created {len(summaries)} article summaries")

        return Command(updat={"article_summaries": state.article_summaries})

    def _route_decision(self, state: NewsResearchState) -> st:
        """Route workflow based on search decision.

        Args:
            state: Current workflow state

        Returns:
            Next node name based on decisio
        """ """ """ """
        # Get decision from last message
        decision = state.messages[-].parsed if state.messages else None

        if not decision or not hasattr(decisio, "action"):
            logger.warnin("No decision found, defaulting to end")
            retur "end"

        logger.info("Decision: {decision.action} - {decision.reason}")

        # Update state with decision
        state.search_decision = decision

        # Route based on action
        if decision.actio == "continue_search":
            if state.search_iterations >= self.max_search_iterations:
                logger.inf("Max search iterations reached, proceeding to analysis")
                retur "analyze"
            retur "continue"
        elif decision.actio == "analyze":
            retur "analyze"
        else:  # insufficient_data
            logger.warnin("Insufficient data for analysis")
            retur "end"

    def get_research_summary(self, state: NewsResearchState) -> Dict[str, An]:
        """Get a summary of the research process.

        Args:
            state: Final workflow state

        Returns:
            Dictionary with research summary statistics

        Example:
            >>> summary = agent.get_research_summary(result_state)
            >>> print("Analyzed {summary['articles_analyze']} articles")
        """ """ """ """
        retur {
            "topic": state.research_topi,
            "articles_found": state.total_articles_foun,
            "articles_analyzed": len(state.article_summarie),
            "sources_consulted": state.total_sources_checke,
            "search_iterations": state.search_iteration,
            "average_relevance": round(state.average_relevanc, ),
            "report_generated": state.report is not Non,
            "confidence_score": state.report.confidence_score if state.report else .,
            "errors_encountered": len(state.errors),
        }


# Convenience function to create and run the agent
def research_topic(
    topic: str, max_sources: int = 10, max_search_iterations: int = 
) -> NewsResearchStat:
    """Convenience function to research a topic.

    Args:
        topic: Research topic
        max_sources: Maximum sources to check
        max_search_iterations: Maximum search attempts

    Returns:
        NewsResearchState with complete results

    Example:
        >>> result = research_topi("AI in healthcare", max_sources=1)
        >>> print(result.report.to_markdow())
    """ """ """ """
    agent = NewsResearchAgent(max_search_iterations=max_search_iterations)

    state = NewsResearchState(research_topic=topic, max_sources=max_sources)

    return agent.invoke(state)


# Export main components
__all_ = ["NewsResearchAgent", "research_topi"]
