# src/haive/agents/news_reporter/state.py
"""
State schema for News Reporter System.
"""

from datetime import datetime
from typing import List, Optional

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from pydantic import Field, computed_field

from haive.prebuilt.ai_insight.models import (
    Article,
    ArticleSummary,
    NewsCategory,
    NewsReport,
    NewsSearchConfig,
    ReportConfig,
    SummaryStyle,
)


class NewsReporterState(MessagesState):
    """State for news reporting workflow."""

    # Configuration
    search_config: NewsSearchConfig = Field(description="Configuration for news search")
    summary_style: SummaryStyle = Field(
        default_factory=SummaryStyle, description="Configuration for summary generation"
    )
    report_config: ReportConfig = Field(
        default_factory=ReportConfig, description="Configuration for report generation"
    )

    # Search results
    raw_articles: List[Article] = Field(
        default_factory=list, description="Raw articles from search"
    )
    filtered_articles: List[Article] = Field(
        default_factory=list, description="Filtered articles for processing"
    )

    # Processing stages
    article_summaries: List[ArticleSummary] = Field(
        default_factory=list, description="Generated article summaries"
    )
    categories: List[NewsCategory] = Field(
        default_factory=list, description="Articles organized by category"
    )
    trends: List[str] = Field(default_factory=list, description="Identified trends")
    spotlight_article: Optional[ArticleSummary] = Field(
        default=None, description="Selected spotlight article"
    )

    # Final output
    news_report: Optional[NewsReport] = Field(
        default=None, description="Final generated report"
    )
    report_output: Optional[str] = Field(
        default=None, description="Formatted report output"
    )
    saved_filename: Optional[str] = Field(
        default=None, description="Filename if report was saved"
    )

    # Process tracking
    start_time: datetime = Field(
        default_factory=datetime.now, description="When processing started"
    )
    end_time: Optional[datetime] = Field(
        default=None, description="When processing completed"
    )

    @computed_field
    @property
    def topic(self) -> str:
        """Get the search topic."""
        return self.search_config.topic

    @computed_field
    @property
    def articles_found(self) -> int:
        """Number of articles found."""
        return len(self.raw_articles)

    @computed_field
    @property
    def articles_processed(self) -> int:
        """Number of articles processed."""
        return len(self.article_summaries)

    @computed_field
    @property
    def processing_time(self) -> Optional[float]:
        """Total processing time in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @computed_field
    @property
    def has_sufficient_content(self) -> bool:
        """Check if we have enough content for a report."""
        return len(self.article_summaries) >= 3

    # Shared fields for LangGraph
    __shared_fields__ = [
        "messages",
        "search_config",
        "article_summaries",
        "categories",
        "news_report",
    ]
