"""State schema for the News Research Agent.

This module defines the state schema that flows through the agent's workflow,
tracking all necessary data for news research operations.

The state schema extends MessagesState to support conversation history
while adding specific fields for news research functionality.

Example:
    >>> from news_research.state import NewsResearchState
    >>> state = NewsResearchState(
    ...     research_topic="AI in healthcare",
    ...     max_sources=10
    ... )

Note:
    All computed fields use proper Pydantic v2 patterns with safe property
    access to avoid initialization errors.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from pydantic import Field, PrivateAttr, computed_field

from .models import (
    ArticleContent,
    ArticleMetadata,
    ArticleSummary,
    NewsApiParams,
    ResearchAnalysis,
    ResearchReport,
    SearchDecision,
)


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
        selected_articles: Articles chosen for summarization
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
        >>> state = NewsResearchState(
        ...     research_topic="Impact of AI on healthcare",
        ...     max_sources=15
        ... )
        >>> state.add_search_query("AI healthcare innovation")
        >>> print(state.total_articles_found)
    """

    # Input configuration
    research_topic: str = Field(description="The main topic being researched")

    search_queries: List[str] = Field(
        description="List of search queries to use", default_factory=list
    )

    current_search_params: Optional[NewsApiParams] = Field(
        description="Current search parameters being used", default=None
    )

    past_searches: List[NewsApiParams] = Field(
        description="History of all search parameters used", default_factory=list
    )

    max_sources: int = Field(
        description="Maximum number of sources to check", default=10
    )

    max_articles_per_search: int = Field(
        description="Maximum articles to retrieve per search", default=20
    )

    # Article tracking
    articles_metadata: List[ArticleMetadata] = Field(
        description="Raw article metadata from NewsAPI", default_factory=list
    )

    articles_content: List[ArticleContent] = Field(
        description="Articles with extracted full text", default_factory=list
    )

    selected_articles: List[ArticleContent] = Field(
        description="Articles selected for summarization", default_factory=list
    )

    article_summaries: List[ArticleSummary] = Field(
        description="Final summarized articles", default_factory=list
    )

    # Workflow control
    search_decision: Optional[SearchDecision] = Field(
        description="Current decision about search continuation", default=None
    )

    # Results
    analysis: Optional[ResearchAnalysis] = Field(
        description="Analysis results from all articles", default=None
    )

    report: Optional[ResearchReport] = Field(
        description="Final research report", default=None
    )

    # Error tracking
    errors: List[Dict[str, Any]] = Field(
        description="List of any errors encountered", default_factory=list
    )

    # Private attributes for internal tracking
    _processed_urls: Set[str] = PrivateAttr(default_factory=set)
    _search_start_time: datetime = PrivateAttr(default_factory=datetime.now)

    # Computed properties
    @computed_field
    @property
    def total_articles_found(self) -> int:
        """Total number of articles discovered."""
        metadata = getattr(self, "articles_metadata", [])
        return len(metadata) if metadata else 0

    @computed_field
    @property
    def total_articles_processed(self) -> int:
        """Number of articles with extracted content."""
        content = getattr(self, "articles_content", [])
        return len(content) if content else 0

    @computed_field
    @property
    def total_sources_checked(self) -> int:
        """Number of unique sources examined."""
        metadata = getattr(self, "articles_metadata", [])
        if not metadata:
            return 0

        sources = set()
        for article in metadata:
            if hasattr(article, "source") and article.source:
                source_name = article.source.get("name", "")
                if source_name:
                    sources.add(source_name)
        return len(sources)

    @computed_field
    @property
    def has_sufficient_data(self) -> bool:
        """Check if we have enough data for analysis."""
        summaries = getattr(self, "article_summaries", [])
        return len(summaries) >= 3  # Minimum 3 articles for good analysis

    @computed_field
    @property
    def average_relevance(self) -> float:
        """Calculate average relevance score of summarized articles."""
        summaries = getattr(self, "article_summaries", [])
        if not summaries:
            return 0.0

        scores = []
        for summary in summaries:
            if hasattr(summary, "relevance_score"):
                scores.append(summary.relevance_score)

        return sum(scores) / len(scores) if scores else 0.0

    @computed_field
    @property
    def search_iterations(self) -> int:
        """Number of search iterations performed."""
        searches = getattr(self, "past_searches", [])
        return len(searches) if searches else 0

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if the research workflow is complete."""
        report = getattr(self, "report", None)
        return report is not None

    # Helper methods
    def add_search_query(self, query: str) -> None:
        """Add a search query to the list.

        Args:
            query: Search query string to add

        Example:
            >>> state.add_search_query("AI healthcare benefits")
        """
        if query and query not in self.search_queries:
            self.search_queries.append(query)

    def add_article_metadata(self, article: ArticleMetadata) -> None:
        """Add article metadata if not already processed.

        Args:
            article: ArticleMetadata object to add

        Note:
            Checks URL uniqueness to avoid duplicates
        """
        if article.url not in self._processed_urls:
            self.articles_metadata.append(article)
            self._processed_urls.add(article.url)

    def add_article_content(self, article: ArticleContent) -> None:
        """Add article with extracted content.

        Args:
            article: ArticleContent object to add
        """
        # Check if we already have this article
        existing_urls = {a.url for a in self.articles_content}
        if article.url not in existing_urls:
            self.articles_content.append(article)

    def record_search(self, params: NewsApiParams) -> None:
        """Record search parameters in history.

        Args:
            params: NewsApiParams used for the search
        """
        self.past_searches.append(params)
        self.current_search_params = params

    def add_error(
        self, error_type: str, message: str, details: Optional[Dict] = None
    ) -> None:
        """Record an error that occurred during processing.

        Args:
            error_type: Classification of the error
            message: Human-readable error message
            details: Additional error context
        """
        error_entry = {
            "type": error_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
        }
        self.errors.append(error_entry)

    def get_unprocessed_metadata(self) -> List[ArticleMetadata]:
        """Get article metadata that hasn't been processed yet.

        Returns:
            List of ArticleMetadata objects without corresponding content
        """
        processed_urls = {a.url for a in self.articles_content}
        return [
            article
            for article in self.articles_metadata
            if article.url not in processed_urls
        ]

    def get_search_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the search process.

        Returns:
            Dictionary with search statistics

        Example:
            >>> summary = state.get_search_summary()
            >>> print(f"Found {summary['total_articles']} articles")
        """
        return {
            "topic": self.research_topic,
            "total_articles": self.total_articles_found,
            "processed_articles": self.total_articles_processed,
            "sources_checked": self.total_sources_checked,
            "search_iterations": self.search_iterations,
            "has_sufficient_data": self.has_sufficient_data,
            "average_relevance": round(self.average_relevance, 2),
            "is_complete": self.is_complete,
            "errors_count": len(self.errors),
        }

    class Config:
        """Pydantic configuration."""

        # Allow field assignment validation
        validate_assignment = True
        # Use enum values
        use_enum_values = True
