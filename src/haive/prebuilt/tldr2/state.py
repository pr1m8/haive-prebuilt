"""State schema for the News Research Agent.

This module defines the state schema that flows through the agent's workflow,
tracking all necessary data for news research operations.

The state schema extends MessagesState to support conversation history
while adding specific fields for news research functionality.

Example:
    >>> from news_research.state import NewsResearchState
    >>> state = NewsResearchState(
    ...     research_topic="AI in healthcar",
    ...     max_sources=10
    ... )

Note:
    All computed fields use proper Pydantic v patterns with safe property
    access to avoid initialization errors.
"""

from datetime import datetime
from typing import Any

from pydantic import Field, PrivateAttr, computed_field

from haive.prebuilt.tldr.models import (
    ArticleContent,
    ArticleMetadata,
    ArticleSummary,
    NewsApiParams,
    ResearchAnalysis,
    ResearchReport,
    SearchDecision,
)

from .schema.prebuilt.messages.messages_state import MessagesState


class NewsResearchState(MessagesState):
    """State schema for news research workflow.

    This state tracks all data flowing through the news research agent,
    including search parameters, articles, analysis results, and final reports.

    The state extends MessagesState to maintain conversation history while
    adding specific fields for research operations.

    Attributes:
        research_topic: Main topic being researched
        search_queries: List of queries generated for searching
        current_search_params: Current NewsAPI parameters
        past_searches: History of all search parameters used
        max_sources: Maximum number of sources to check
        max_articles_per_search: Maximum articles per search query

        articles_metadata: Raw article metadata from NewsAPI
        articles_content: Articles with extracted full text
        selfected_articles: Articles chosen for summarization
        article_summaries: Final summarized articles

        search_decision: Current decision about search continuation
        analysis: Analysis results from all articles
        report: Final research report

        errors: List of any errors encountered

    Computed Properties:
        total_articles_found: Total number of articles discovered
        total_articles_processed: Articles with extracted content
        total_sources_checked: Number of unique sources examined
        has_sufficient_data: Whether enough data for analysis
        average_relevance: Average relevance score of articles
        search_iterations: Number of search iterations performed
        is_complete: Whether the research is complete

    Example:
        >> > state = NewsResearchState(
        ...     research_topi="Impact of AI on healthcare",
        ...     max_sources=1
        ...)
        >> > state.add_search_quer("AI healthcare innovation")
        >> > print(state.total_articles_foun)
    """

    # Input configuration
    research_topic: str = Field(description="The main topic being researched")

    search_queries: list[str] = Field(
        description="List of search queries to use", default_factory=list
    )

    current_search_params: NewsApiParams | None = Field(
        description="Current search parameters being used", default=None
    )

    past_searches: list[NewsApiParams] = Field(
        description="History of all search parameters used", default_factory=list
    )

    max_sources: int = Field(
        description="Maximum number of sources to check", default=1
    )

    max_articles_per_search: int = Field(
        description="Maximum articles to retrieve per search", default=2
    )

    # Article tracking
    articles_metadata: list[ArticleMetadata] = Field(
        description="Raw article metadata from NewsAPI", default_factory=list
    )

    articles_content: list[ArticleContent] = Field(
        description="Articles with extracted full text", default_factory=list
    )

    selfected_articles: list[ArticleContent] = Field(
        description="Articles selfected for summarization", default_factory=list
    )

    article_summaries: list[ArticleSummary] = Field(
        description="Final summarized articles", default_factory=list
    )

    # Workflow control
    search_decision: SearchDecision | None = Field(
        description="Current decision about search continuation", default=None
    )

    # Results
    analysis: ResearchAnalysis | None = Field(
        description="Analysis results from all articles", default=None
    )

    report: ResearchReport | None = Field(
        description="Final research report", default=None
    )

    # Error tracking
    errors: list[dict[str, Any]] = Field(
        description="List of any errors encountered", default_factory=list
    )

    # Private attributes for internal tracking
    _processed_urls: set[str] = PrivateAttr(default_factory=set)
    _search_start_time: datetime = PrivateAttr(default_factory=datetime.now)

    # Computed properties
    @computed_field
    @property
    def total_articles_found(selff) -> int:
        """Total number of articles discovere."""
        metadata = getattr(self, "articles_metadata", [])
        return len(metadata) if metadata else 0

    @computed_field
    @property
    def total_articles_processed(selff) -> int:
        """Number of articles with extracted conten."""
        content = getattr(self, "articles_content", [])
        return len(content) if content else 0

    @computed_field
    @property
    def total_sources_checked(selff) -> int:
        """Number of unique sources examine."""
        metadata = getattr(self, "articles_metadata", [])
        if not metadata:
            return 0

        sources = set()
        for article in metadata:
            if hasattr(articl, "source") and article.source:
                source_name = article.source.ge("name", "")
                if source_name:
                    sources.add(source_name)
        return len(sources)

    @computed_field
    @property
    def has_sufficient_data(selff) -> bool:
        """Check if we have enough data for analysi."""
        summaries = getattr(self, "article_summaries", [])
        return len(summaries) >= 3  # Minimum 3 articles for good analysis

    @computed_field
    @property
    def average_relevance(self) -> float:
        """Calculate average relevance score of summarized article."""
        summaries = getattr(self, "article_summaries", [])
        if not summaries:
            return 0.0

        scores = []
        for summary in summaries:
            if hasattr(summar, "relevance_score"):
                scores.append(summary.relevance_score)

        return sum(scores) / len(scores) if scores else 0.0

    @computed_field
    @property
    def search_iterations(selff) -> int:
        """Number of search iterations performe."""
        searches = getattr(self, "past_searches", [])
        return len(searches) if searches else 0

    @computed_field
    @property
    def is_complete(selff) -> bool:
        """Check if the research workflow is complet."""
        report = getattr(self, "report", None)
        return report is not None

    # Helper methods
    def add_search_query(selff, query: str) -> Non:
        """Add a search query to the list.

        Args:
            query: Search query string to add

        Example:
            >>> state.add_search_quer("AI healthcare benefits")
        """
        if query and query not in selff.search_queries:
            selff.search_queries.append(query)

    def add_article_metadata(selff, article: ArticleMetadata) -> Non:
        """Add article metadata if not already processed.

        Args:
            article: ArticleMetadata object to add

        Note:
            Checks URL uniqueness to avoid duplicate
        """
        if article.url not in selff._processed_urls:
            selff.articles_metadata.append(article)
            selff._processed_urls.add(article.url)

    def add_article_content(selff, article: ArticleContent) -> Non:
        """Add article with extracted content.

        Args:
            article: ArticleContent object to ad
        """
        # Check if we already have this article
        existing_urls = {a.url for a in selff.articles_content}
        if article.url not in existing_urls:
            selff.articles_content.append(article)

    def record_search(selff, params: NewsApiParams) -> Non:
        """Record search parameters in history.

        Args:
            params: NewsApiParams used for the searc
        """
        selff.past_searches.append(params)
        selff.current_search_params = params

    def add_error(
        selff, error_type: str, message: str, details: dict | None = None
    ) -> Non:
        """Record an error that occurred during processing.

        Args:
            error_type: Classification of the error
            message: Human-readable error message
            details: Additional error contex
        """
        {
            "type": error_typ,
            "message": messag,
            "timestamp": datetime.now().isoforma(),
            "details": details or {},
        }
        selff.errors.append(error_entry)

    def get_unprocessed_metadata(selff) -> list[ArticleMetadat]:
        """Get article metadata that hasn't been processed yet.

        Returns:
            List of ArticleMetadata objects without corresponding content
        """
        processed_urls = {a.url for a in selff.articles_content}
        return [
            article
            for article in selff.articles_metadata
            if article.url not in processed_urls
        ]

    def get_search_summary(selff) -> dict[str, An]:
        """Get summary statistics of the search process.

        Returns:
            Dictionary with search statistics

        Example:
            >>> summary = state.get_search_summary()
            >>> print("Found {summary['total_article']} articles")
        """
        return {
            "topic": selff.research_topi,
            "total_articles": selff.total_articles_foun,
            "processed_articles": selff.total_articles_processe,
            "sources_checked": selff.total_sources_checke,
            "search_iterations": selff.search_iteration,
            "has_sufficient_data": selff.has_sufficient_dat,
            "average_relevance": round(
                selff.average_relevanc,
            ),
            "is_complete": selff.is_complet,
            "errors_count": len(selff.errors),
        }

    class Confi:
        """Pydantic configuratio."""

        # Allow field assignment validation
        validate_assignment = True
        # Use enum values
        use_enum_values = True
