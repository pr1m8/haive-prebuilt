# src/haive/agents/news_reporter/models.py
"""
Models for General News Reporter System.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl, computed_field


class NewsSearchConfig(BaseModel):
    """Configuration for news search."""

    topic: str = Field(
        description="Topic to search for (e.g., 'artificial intelligence', 'climate change', 'economics')"
    )
    search_type: Literal["news", "general", "academic", "business"] = Field(
        default="news", description="Type of search to perform"
    )
    time_period: Literal["1d", "3d", "1w", "1m", "3m"] = Field(
        default="1w", description="Time period for news recency"
    )
    search_depth: Literal["basic", "advanced"] = Field(
        default="advanced", description="Search depth level"
    )
    max_results: int = Field(
        default=20, ge=5, le=100, description="Maximum number of results to fetch"
    )
    language: str = Field(default="en", description="Language code for search")


class Article(BaseModel):
    """Represents a news article."""

    title: str = Field(description="Article headline")
    url: HttpUrl = Field(description="Source URL")
    content: str = Field(description="Article content/snippet")
    source: str = Field(description="Source publication")
    published_date: Optional[datetime] = Field(
        default=None, description="Publication date"
    )
    author: Optional[str] = Field(default=None, description="Article author")
    relevance_score: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Relevance to search topic"
    )

    @computed_field
    @property
    def days_old(self) -> Optional[int]:
        """Days since publication."""
        if not self.published_date:
            return None
        return (datetime.now() - self.published_date).days


class SummaryStyle(BaseModel):
    """Configuration for summary generation."""

    target_audience: Literal[
        "general", "technical", "executive", "academic", "youth"
    ] = Field(default="general", description="Target audience for summaries")
    length: Literal["brief", "standard", "detailed"] = Field(
        default="standard", description="Summary length preference"
    )
    focus_areas: Optional[List[str]] = Field(
        default=None, description="Specific aspects to focus on"
    )
    simplify_technical: bool = Field(
        default=True, description="Whether to simplify technical terms"
    )
    include_implications: bool = Field(
        default=True, description="Include why this matters"
    )


class ArticleSummary(BaseModel):
    """Summary of an article."""

    title: str = Field(description="Original article title")
    summary: str = Field(description="Generated summary")
    key_points: List[str] = Field(default_factory=list, description="Key takeaways")
    implications: Optional[str] = Field(default=None, description="Why this matters")
    url: HttpUrl = Field(description="Source URL")
    source: str = Field(description="Source publication")
    category: Optional[str] = Field(default=None, description="Assigned category")


class NewsCategory(BaseModel):
    """Category for organizing news."""

    name: str = Field(description="Category name")
    description: str = Field(description="What this category covers")
    articles: List[ArticleSummary] = Field(
        default_factory=list, description="Articles in this category"
    )

    @computed_field
    @property
    def article_count(self) -> int:
        """Number of articles in category."""
        return len(self.articles)


class ReportMetadata(BaseModel):
    """Metadata for the news report."""

    topic: str = Field(description="Main topic of the report")
    time_period: str = Field(description="Period covered")
    total_sources: int = Field(description="Number of sources analyzed")
    generation_time: datetime = Field(
        default_factory=datetime.now, description="When report was generated"
    )
    search_config: NewsSearchConfig = Field(description="Search configuration used")


class NewsReport(BaseModel):
    """Complete news report."""

    title: str = Field(description="Report title")
    subtitle: Optional[str] = Field(default=None, description="Report subtitle")
    executive_summary: str = Field(description="High-level overview")
    introduction: str = Field(description="Engaging introduction")
    categories: List[NewsCategory] = Field(
        default_factory=list, description="News organized by category"
    )
    key_trends: List[str] = Field(
        default_factory=list, description="Major trends identified"
    )
    spotlight_article: Optional[ArticleSummary] = Field(
        default=None, description="Featured article"
    )
    conclusion: Optional[str] = Field(default=None, description="Concluding thoughts")
    metadata: ReportMetadata = Field(description="Report metadata")

    @computed_field
    @property
    def total_articles(self) -> int:
        """Total number of articles in report."""
        return sum(cat.article_count for cat in self.categories)

    @computed_field
    @property
    def report_date(self) -> str:
        """Formatted report date."""
        return self.metadata.generation_time.strftime("%B %d, %Y")


class ReportConfig(BaseModel):
    """Configuration for report generation."""

    report_style: Literal["newsletter", "brief", "comprehensive", "executive"] = Field(
        default="newsletter", description="Overall report style"
    )
    max_categories: int = Field(
        default=6, ge=3, le=10, description="Maximum number of categories"
    )
    articles_per_category: int = Field(
        default=3, ge=1, le=10, description="Articles per category"
    )
    include_trends: bool = Field(default=True, description="Include trend analysis")
    include_spotlight: bool = Field(
        default=True, description="Include spotlight article"
    )
    output_format: Literal["markdown", "html", "json"] = Field(
        default="markdown", description="Output format"
    )
    save_to_file: bool = Field(default=True, description="Save report to file")
    filename_pattern: str = Field(
        default="{topic}_{date}",
        description="Filename pattern (supports {topic}, {date})",
    )
