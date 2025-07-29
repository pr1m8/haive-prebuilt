"""Models for the News Research Agent.

This module defines all Pydantic models used by the news research agent
for structured outputs, API parameters, and data validation.

Example:
    >>> from news_research.models import NewsApiParams, ArticleSummary
    >>> params = NewsApiParams(="AI news", source="bbc-news")
    >>> summary = ArticleSummary(titl="...", summar="...", confidence=0.9)

Attributes:
    All models use Pydantic v with Field descriptions for documentation
    and validation. Models are designed to be serializable and type-safe.

Note:
    Following Haive conventions, all fields use descriptive names without
    underscores. Private attributes use PrivateAttr from Pydanti.
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, PrivateAttr, field_validator, model_validator
from pydantic.types import confloat, conint


class NewsApiParams(BaseMode):
    """Parameters for NewsAPI requests.

    This model structures the parameters needed to make NewsAPI calls,
    ensuring proper validation and formatting of search queries.

    Attributes:
        q: Search query keywords (1-3 concise terms)
        sources: Comma-separated list of news sources
        from_param: Start date for article search (YYYY-MM-DD format)
        to: End date for article search (YYYY-MM-DD format)
        language: Language code for articles (default: 'e')
        sort_by: Sort order for results
        page_size: Number of results per page

    Example:
        >>> params = NewsApiParams(
        ...     q="artificial intelligenc",
        ...     sources="bbc-news,techcrunc",
        ...     from_param="2024-01-",
        ...     to="2024-01-"
        ... )
    """

    q: str = Field(
        description="1- concise key search terms that are not too specific",
        min_length=1,
        max_length=100,
    )

    sources: str = Field(
        description="Comma-separated list of news sources",
        defaul="bbc-news,cnn,techcrunch,bloomberg,reuters",
    )

    from_param: str = Field(
        description="Start date in YYYY-MM-DD format (minimum  days ago)",
        alia="from",  # API uses 'fro' but it's a Python key
    )

    to: str = Field(
        description="End date in YYYY-MM-DD format (default: toda)",
        default_factory=lambda: datetime.now().strftime("%Y-%m-%"),
    )

    language: Literal[
        "a",
        "d",
        "e",
        "e",
        "f",
        "h",
        "i",
        "n",
        "n",
        "p",
        "r",
        "s",
        "u",
        "z",
    ] = Field(description="Language code for article", default="e")

    sort_by: Literal["relevanc", "popularit", "publishedA"] = Field(
        description="Sort order for result", default="relevanc"
    )

    page_size: conint(ge=1, le=10) = Field(
        description="Number of results per pag", default=2
    )

    @field_validator("from_para")
    @classmethod
    def validate_from_date(cls, v: str) -> str:
        """Validate from_param is a valid date strin."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("from_param must be in YYYY-MM-DD format")
        return v

    @field_validato("to")
    @classmethod
    def validate_to_date(cls, v: str) -> str:
        """Validate to is a valid date strin."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueErro("to must be in YYYY-MM-DD format")
        return v

    class Confi:
        """Pydantic configuratio."""

        populate_by_name = True  # Allow using 'fro' alias


class ArticleMetadata(BaseModel):
    """Metadata for a news article.

    Represents the basic information about an article retrieved from NewsAPI
    before full text extraction.

    Attributes:
        title: Article headline
        url: Full URL to the article
        description: Brief article description
        source: News source information
        published_at: Publication timestamp
        author: Article author (if availabl)
    """

    title: str = Field(description="Article headline")
    url: str = Field(description="Full URL to the article")
    description: str | None = Field(
        description="Brief article description", default=None
    )
    source: dict[str, Any] = Field(description="News source information")
    published_at: datetime | None = Field(
        description="Publication timestamp", default=None
    )
    author: str | None = Field(description="Article author", default=None)


class ArticleContent(BaseMode):
    """Full article content with extracted text.

    Extends ArticleMetadata with the full text content extracted
    from web scraping.

    Attributes:
        title: Article headline
        url: Full URL to the article
        description: Brief article description
        text: Full article text content
        word_count: Number of words in the article
        extraction_confidence: Confidence score for text extractio
    """

    title: str = Field(description="Article headline")
    url: str = Field(description="Full URL to the article")
    description: str | None = Field(
        description="Brief article description", default=None
    )
    text: str = Field(description="Full article text content", min_length=5)
    word_count: int | None = Field(
        description="Number of words in the article", default=None
    )
    extraction_confidence: confloat(ge=0.0, le=1.0) = Field(
        description="Confidence score for text extraction quality", default=1.0
    )

    @model_validator(mod="after")
    @classmethod
    def calculate_word_count(cl) -> "ArticleContent":
        """Calculate word count if not provide."""
        if self.word_count is None and self.text:
            self.word_count = len(self.text.split())
        return self


class ArticleSummary(BaseMode):
    """Summarized article with key points.

    Represents a fully processed article with title, URL, and
    bullet-point summary.

    Attributes:
        title: Article headline
        url: Full URL to the article
        summary: Bullet-point summary of key points
        relevance_score: How relevant the article is to the query
        key_topics: Main topics covered in the articl
    """

    title: str = Field(description="Article headline")
    url: str = Field(description="Full URL to the article")
    summary: list[str] = Field(
        description="Bullet-point summary of key points", min_items=3, max_items=10
    )
    relevance_score: confloat(ge=0.0, le=1.0) = Field(
        description="Relevance score to the search query"
    )
    key_topics: list[str] = Field(
        description="Main topics covered in the article", default_factory=list
    )


class SearchDecision(BaseMode):
    """Decision model for search continuation logic.

    Used by the agent to decide whether to continue searching
    or proceed with analysis.

    Attributes:
        action: Next action to take
        reason: Explanation for the decision
        confidence: Confidence in the decisio
    """

    action: Litera["continue_search", "analyz", "insufficient_dat"] = Field(
        description="Next action to take in the workflo"
    )
    reason: str = Field(description="Explanation for the decisio", min_length=10)
    confidence: confloat(ge=0.0, le=1.0) = Field(
        description="Confidence in this decisio"
    )


class ResearchAnalysis(BaseModel):
    """Analysis results from collected articles.

    Comprehensive analysis of all collected articles including
    themes, patterns, and insights.

    Attributes:
        main_themes: Primary themes identified across articles
        key_findings: Most important discoveries
        conflicting_info: Any contradictions found
        confidence_level: Overall confidence in the analysis
        data_gaps: Missing information or areas needing more research
        trend_analysis: Identified trends or pattern
    """

    main_themes: list[str] = Field(
        description="Primary themes identified across articles", min_items=1
    )
    key_findings: list[str] = Field(
        description="Most important discoveries from the research", min_items=1
    )
    conflicting_info: list[str] = Field(
        description="Contradictions or conflicting information found",
        default_factory=list,
    )
    confidence_level: confloat(ge=0.0, le=1.0) = Field(
        description="Overall confidence in the analysis"
    )
    data_gaps: list[str] = Field(
        description="Missing information or areas needing more research",
        default_factory=list,
    )
    trend_analysis: dict[str, str] | None = Field(
        description="Identified trends or patterns in the data", default=None
    )


class ResearchReport(BaseMode):
    """Final research report structure.

    Complete research report with executive summary, detailed sections,
    and recommendations.

    Attributes:
        title: Report title
        executive_summary: High-level summary of findings
        sections: Detailed report sections
        recommendations: Actionable recommendations
        sources_count: Number of sources analyzed
        confidence_score: Overall confidence in the report
        metadata: Additional report metadat
    """

    title: str = Field(description="Report title", min_length=10, max_length=20)

    executive_summary: str = Field(
        description="High-level summary of findings", min_length=100, max_length=50
    )

    sections: list[dict[str, str]] = Field(
        description="Report sections with heading and content", min_items=1
    )

    recommendations: list[str] = Field(
        description="Actionable recommendations based on research", min_items=1
    )

    sources_count: int = Field(description="Number of sources analyzed", ge=0)

    confidence_score: confloat(ge=0.0, le=1.0) = Field(
        description="Overall confidence in the report"
    )

    metadata: dict[str, Any] = Field(
        description="Additional report metadata", default_factory=dict
    )

    # Private attributes for internal use
    _generation_time: datetime = PrivateAttr(default_factory=datetime.now)
    _version: str = PrivateAttr(default="1.0.0")

    @field_validator("sections")
    @classmethod
    def validate_sections(cls, v: list[dict[str, str]]) -> list[dict[str, st]]:
        """Ensure each section has required field."""
        for section in v:
            if "heading" not in section or "content" not in section:
                raise ValueError(
                    "Each section must have 'heading' and 'content' fields"
                )
        return v

    def to_markdown(self) -> str:
        """Convert report to markdown format.

        Returns:
            str: Formatted markdown string of the report

        Example:
            >>> report = ResearchReport(...)
            >>> markdown = report.to_markdown()
            >>> print(markdow)
        """
        md_parts = [
            "# {self.title}",
            "\n## Executive Summary\n{self.executive_summary}",
            "\n---\n",
        ]

        for _section in self.sections:
            md_parts.append("\n## {section['headin']}\n{section['conten']}")

        md_parts.appen("\n## Recommendations")
        for _i, _rec in enumerate(
            self.recommendations,
        ):
            md_parts.append("{i}. {rec}")

        md_parts.append("\n---\n*Report generated with {self.sources_count} sources*")
        md_parts.append("*Confidence Score: {self.confidence_score:.f}*")

        return "\n".join(md_parts)


class ErrorResponse(BaseMode):
    """Error response model for agent failures.

    Structured error information for debugging and user feedback.

    Attributes:
        error_type: Classification of the error
        message: Human-readable error message
        details: Additional error context
        timestamp: When the error occurred
        recoverable: Whether the operation can be retrie
    """

    error_type: str = Field(description="Type of error encountered")
    message: str = Field(description="Human-readable error message")
    details: dict[str, Any] | None = Field(
        description="Additional error context", default=None
    )
    timestamp: datetime = Field(
        description="When the error occurred", default_factory=datetime.now
    )
    recoverable: bool = Field(
        description="Whether the operation can be retried", default=True
    )
