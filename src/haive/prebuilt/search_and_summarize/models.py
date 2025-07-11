# src/haive/agents/search_summarize/models.py
"""
Models for Search & Summarize Agent System.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl


class SearchQuery(BaseModel):
    """Search query with optional site filtering."""

    query: str = Field(description="The search query")
    specific_site: Optional[str] = Field(
        default=None,
        description="Optional domain to search within (e.g., 'nature.com')",
    )
    max_results: int = Field(
        default=5, ge=1, le=20, description="Maximum number of search results"
    )
    search_type: Literal["general", "academic", "news", "technical"] = Field(
        default="general", description="Type of search to perform"
    )


class SearchResult(BaseModel):
    """Individual search result."""

    title: str = Field(description="Title of the result")
    snippet: str = Field(description="Text snippet from the result")
    url: HttpUrl = Field(description="URL of the result")
    source_domain: str = Field(description="Domain of the source")
    relevance_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Relevance score if available"
    )
    timestamp: Optional[datetime] = Field(
        default=None, description="Publication date if available"
    )


class SearchResults(BaseModel):
    """Collection of search results."""

    query: str = Field(description="Original search query")
    results: List[SearchResult] = Field(description="List of search results")
    total_results: int = Field(description="Total number of results found")
    search_time: float = Field(description="Time taken to search in seconds")

    @property
    def has_results(self) -> bool:
        """Check if search returned any results."""
        return len(self.results) > 0


class SummaryConfig(BaseModel):
    """Configuration for summarization."""

    style: Literal["bullet_points", "paragraph", "key_facts", "executive"] = Field(
        default="bullet_points", description="Summary style"
    )
    max_length: int = Field(default=150, description="Maximum length in words")
    focus_areas: Optional[List[str]] = Field(
        default=None, description="Specific areas to focus on in summary"
    )
    include_quotes: bool = Field(
        default=False, description="Whether to include relevant quotes"
    )


class ContentSummary(BaseModel):
    """Summary of a piece of content."""

    source_title: str = Field(description="Title of the source")
    source_url: HttpUrl = Field(description="URL of the source")
    summary: str = Field(description="The summary text")
    key_points: List[str] = Field(
        default_factory=list, description="Key points extracted"
    )
    relevance_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How relevant this content is to the query",
    )
    quotes: Optional[List[str]] = Field(
        default=None, description="Notable quotes if requested"
    )


class ResearchReport(BaseModel):
    """Complete research report combining all summaries."""

    query: str = Field(description="Original research query")
    executive_summary: str = Field(description="High-level summary of all findings")
    summaries: List[ContentSummary] = Field(description="Individual content summaries")
    key_insights: List[str] = Field(description="Key insights across all sources")
    common_themes: List[str] = Field(
        default_factory=list, description="Common themes identified"
    )
    contradictions: Optional[List[str]] = Field(
        default=None, description="Contradicting information found"
    )
    recommendations: Optional[List[str]] = Field(
        default=None, description="Recommendations based on findings"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @property
    def source_count(self) -> int:
        """Number of sources summarized."""
        return len(self.summaries)

    @property
    def average_relevance(self) -> float:
        """Average relevance score across all summaries."""
        if not self.summaries:
            return 0.0
        scores = [s.relevance_score for s in self.summaries]
        return sum(scores) / len(scores)
