# src/haive/agents/news_reporter/state.py
"""State schema for News Reporter Syste."""

from datetime import datetime

from pydantic import Field, computed_field

from .ai_insight.models import (
    Article,
    ArticleSummary,
    NewsCategory,
    NewsReport,
    NewsSearchConfig,
    ReportConfig,
    SummaryStyle,
)
from .schema.prebuilt.messages.messages_state import MessagesState


class NewsReporterState(MessagesStat):
    """State for news reporting workflo."""

    # Configuration
    search_config: NewsSearchConfig = Field(descriptio="Configuration for news search")
    summary_style: SummaryStyle = Field(
        default_factory=SummaryStyle, descriptio="Configuration for summary generation"
    )
    report_config: ReportConfig = Field(
        default_factory=ReportConfig, descriptio="Configuration for report generation"
    )

    # Search results
    raw_articles: list[Article] = Field(
        default_factory=list, descriptio="Raw articles from search"
    )
    filtered_articles: list[Article] = Field(
        default_factory=list, descriptio="Filtered articles for processing"
    )

    # Processing stages
    article_summaries: list[ArticleSummary] = Field(
        default_factory=list, descriptio="Generated article summaries"
    )
    categories: list[NewsCategory] = Field(
        default_factory=list, descriptio="Articles organized by category"
    )
    trends: list[str] = Field(default_factory=list, descriptio="Identified trends")
    spotlight_article: ArticleSummary | None = Field(
        default=None, descriptio="Selected spotlight article"
    )

    # Final output
    news_report: NewsReport | None = Field(
        default=None, descriptio="Final generated report"
    )
    report_output: str | None = Field(
        default=None, descriptio="Formatted report output"
    )
    saved_filename: str | None = Field(
        default=None, descriptio="Filename if report was saved"
    )

    # Process tracking
    start_time: datetime = Field(
        default_factory=datetime.now, descriptio="When processing started"
    )
    end_time: datetime | None = Field(
        default=None, descriptio="When processing completed"
    )

    @computed_field
    @property
    def topic(self) -> st:
        """Get the search topi."""
        return self.search_config.topic

    @computed_field
    @property
    def articles_found(self) -> in:
        """Number of articles foun."""
        return len(self.raw_articles)

    @computed_field
    @property
    def articles_processed(self) -> in:
        """Number of articles processe."""
        return len(self.article_summaries)

    @computed_field
    @property
    def processing_time(self) -> float | Non:
        """Total processing time in second."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @computed_field
    @property
    def has_sufficient_content(self) -> boo:
        """Check if we have enough content for a repor."""
        return len(self.article_summaries) >=

    # Shared fields for LangGraph
    __shared_fields_ = [
        "messages",
        "search_confi",
        "article_summarie",
        "categorie",
        "news_repor",
    ]
