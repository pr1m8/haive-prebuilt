# src/haive/agents/search_summarize/state.py
"""
State schema for Search & Summarize Agent System.
"""

from datetime import datetime
from typing import Dict, List, Optional

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from pydantic import Field, computed_field

from haive.prebuilt.search_and_summarize.models import (
    ContentSummary,
    ResearchReport,
    SearchQuery,
    SearchResults,
    SummaryConfig,
)


class SearchSummarizeState(MessagesState):
    """State for search and summarize workflow."""

    # Input configuration
    search_query: Optional[SearchQuery] = Field(
        default=None, description="Structured search query"
    )
    summary_config: SummaryConfig = Field(
        default_factory=SummaryConfig, description="Configuration for summarization"
    )

    # Search results
    search_results: Optional[SearchResults] = Field(
        default=None, description="Results from web search"
    )
    additional_searches: List[SearchResults] = Field(
        default_factory=list, description="Results from additional specialized searches"
    )

    # Content and summaries
    fetched_content: Dict[str, str] = Field(
        default_factory=dict, description="Fetched content by URL"
    )
    content_summaries: List[ContentSummary] = Field(
        default_factory=list, description="Individual content summaries"
    )

    # Final output
    research_report: Optional[ResearchReport] = Field(
        default=None, description="Final synthesized research report"
    )

    # Quality metrics
    quality_scores: Dict[str, float] = Field(
        default_factory=dict, description="Quality scores for each source"
    )

    # Process metadata
    start_time: datetime = Field(
        default_factory=datetime.now, description="When the research started"
    )
    end_time: Optional[datetime] = Field(
        default=None, description="When the research completed"
    )

    @computed_field
    @property
    def query_text(self) -> str:
        """Extract query text from messages or search_query."""
        if self.search_query:
            return self.search_query.query
        elif self.messages:
            for msg in self.messages:
                if msg.type == "human":
                    return msg.content
        return ""

    @computed_field
    @property
    def total_sources(self) -> int:
        """Total number of sources found."""
        count = 0
        if self.search_results:
            count += len(self.search_results.results)
        for search in self.additional_searches:
            count += len(search.results)
        return count

    @computed_field
    @property
    def sources_summarized(self) -> int:
        """Number of sources actually summarized."""
        return len(self.content_summaries)

    @computed_field
    @property
    def processing_time(self) -> Optional[float]:
        """Total processing time in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @computed_field
    @property
    def has_sufficient_results(self) -> bool:
        """Check if we have enough results to create a report."""
        return self.sources_summarized >= 2

    # Shared fields for LangGraph
    __shared_fields__ = [
        "messages",
        "search_query",
        "search_results",
        "content_summaries",
        "research_report",
    ]
